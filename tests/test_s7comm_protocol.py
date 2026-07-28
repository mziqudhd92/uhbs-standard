"""S7comm framing helpers + offline stub probes."""

from __future__ import annotations

import socket
import struct
import threading

from uhbs_core.models import TargetSpec
from uhbs_core.protocols import get_plugin
from uhbs_core.protocols.s7comm import (
    S7commPlugin,
    build_cotp_cr,
    build_s7_setup_communication,
    build_tpkt,
    is_cotp_cc,
    is_s7_setup_ack,
    is_tpkt,
)
from uhbs_core.tps import TPS


def test_s7comm_plugin_resolves_and_aliases() -> None:
    p = get_plugin("s7comm")
    assert isinstance(p, S7commPlugin)
    assert p.name == "s7comm"
    for alias in ("s7", "iso-tsap", "isotp", "iso_on_tcp"):
        assert get_plugin(alias).name == "s7comm"


def test_tpkt_and_cotp_framing() -> None:
    payload = b"\x11\xe0" + b"\x00" * 10
    framed = build_tpkt(payload)
    assert framed[:2] == b"\x03\x00"
    assert struct.unpack("!H", framed[2:4])[0] == len(framed)
    assert is_tpkt(framed)

    cr = build_cotp_cr()
    assert is_tpkt(cr)
    assert cr[5] == 0xE0  # CR
    assert b"\xc1\x02\x01\x00" in cr
    assert b"\xc2\x02\x01\x02" in cr

    setup = build_s7_setup_communication()
    assert is_tpkt(setup)
    assert b"\x32\x01" in setup
    assert b"\xf0" in setup


def test_s7comm_against_stub() -> None:
    # CC: TPKT + LI=2 + D0 (minimal Connection Confirm)
    cc = build_tpkt(b"\x02\xd0\x00\x01\x00\x01\x00")
    # Setup Ack: TPKT + COTP DT + S7 Ack with 0xF0
    s7_ack = (
        b"\x32\x03\x00\x00\x04\x00\x00\x08\x00\x00"
        b"\xf0\x00\x00\x01\x00\x01\x00\xf0"
    )
    setup_ack = build_tpkt(b"\x02\xf0\x80" + s7_ack)
    assert is_cotp_cc(cc)
    assert is_s7_setup_ack(setup_ack)

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 0))
    srv.listen(8)
    host, port = srv.getsockname()
    stop = threading.Event()

    def _loop() -> None:
        srv.settimeout(0.5)
        while not stop.is_set():
            try:
                conn, _ = srv.accept()
            except TimeoutError:
                continue
            with conn:
                conn.settimeout(2.0)
                try:
                    first = conn.recv(4096)
                    if not first:
                        continue
                    # Truncated / CR / anything: if looks like CR → CC then maybe Setup
                    if len(first) >= 6 and first[5] == 0xE0:
                        conn.sendall(cc)
                        second = conn.recv(4096)
                        if second and b"\xf0" in second:
                            conn.sendall(setup_ack)
                    else:
                        # FSM truncated — close cleanly
                        pass
                except OSError:
                    pass
        srv.close()

    th = threading.Thread(target=_loop, daemon=True)
    th.start()
    try:
        target = TargetSpec(
            name="s7-stub",
            host=host,
            port=port,
            protocol="s7comm",
            protocols=["s7comm"],
        )
        tps = TPS(
            name="s7-stub",
            profile_class="ICS-SCADA",
            protocol="s7comm",
            protocols=["s7comm"],
            strict_rfc_enforcement=True,
        )
        plugin = S7commPlugin()
        fsm = plugin.probe_fsm(host, port, target, tps)
        assert fsm[0].passed is True

        nego = plugin.probe_negotiation(host, port, target, tps)
        assert nego[0].id == "s7comm.nego.cotp_cc"
        assert nego[0].passed is True

        state = plugin.probe_state(host, port, target, tps)
        assert state[0].id == "s7comm.state.setup_communication"
        assert state[0].passed is True
        assert state[0].critical is True
    finally:
        stop.set()
        th.join(timeout=2.0)
