"""Oracle TNS plugin framing helpers + offline stub probes."""

from __future__ import annotations

import socket
import threading

from uhbs_core.models import TargetSpec
from uhbs_core.protocols import get_plugin
from uhbs_core.protocols.oracle import (
    OraclePlugin,
    build_accept_packet,
    build_connect_packet,
    build_refuse_packet,
    build_truncated_length_packet,
    is_connect_response,
    tns_packet_type,
)
from uhbs_core.protocols.registry import _REGISTRY, register
from uhbs_core.tps import TPS


def test_oracle_plugin_resolves_and_aliases() -> None:
    plugin = OraclePlugin()
    register(plugin)
    _REGISTRY["tns"] = plugin
    _REGISTRY["oracle-tns"] = plugin
    p = get_plugin("oracle")
    assert isinstance(p, OraclePlugin)
    assert p.name == "oracle"
    assert get_plugin("tns").name == "oracle"
    assert get_plugin("oracle-tns").name == "oracle"


def test_connect_and_truncated_framing() -> None:
    connect = build_connect_packet(service_name="XE")
    assert len(connect) >= 8
    assert connect[4] == 1  # Connect
    assert b"SERVICE_NAME=XE" in connect

    trunc = build_truncated_length_packet()
    assert trunc[:2] == b"\x01\x00"  # claims 256 bytes
    assert len(trunc) < 256


def test_oracle_unreachable_does_not_raise() -> None:
    plugin = OraclePlugin()
    target = TargetSpec(name="x", host="127.0.0.1", port=1, protocol="oracle")
    for method in (plugin.probe_fsm, plugin.probe_negotiation):
        checks = method("127.0.0.1", 1, target, None)
        assert isinstance(checks, list)
        assert checks


def test_oracle_nego_and_fsm_against_stub() -> None:
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 0))
    srv.listen(8)
    host, port = srv.getsockname()
    stop = threading.Event()

    refuse = build_refuse_packet("TNS-12541: TNS:no listener")
    accept = build_accept_packet()

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
                    data = conn.recv(4096)
                    if not data:
                        continue
                    if data[:2] == b"\x01\x00" and len(data) < 16:
                        conn.close()
                        continue
                    if len(data) >= 8 and data[4] == 1:
                        conn.sendall(accept if b"XE" in data else refuse)
                except OSError:
                    pass
        srv.close()

    th = threading.Thread(target=_loop, daemon=True)
    th.start()
    try:
        target = TargetSpec(
            name="tns-stub",
            host=host,
            port=port,
            protocol="oracle",
            protocols=["oracle"],
            annotations={"service_name": "XE"},
        )
        tps = TPS(
            name="tns-stub",
            profile_class="Low-Interaction",
            protocol="oracle",
            protocols=["oracle"],
            strict_rfc_enforcement=True,
        )
        plugin = OraclePlugin()
        fsm = plugin.probe_fsm(host, port, target, tps)
        assert fsm[0].id == "oracle.fsm.truncated_length"
        assert fsm[0].passed is True

        nego = plugin.probe_negotiation(host, port, target, tps)
        assert nego[0].id == "oracle.nego.connect"
        assert nego[0].passed is True
        assert "accept" in nego[0].detail.lower()

        target_orcl = TargetSpec(
            name="tns-stub",
            host=host,
            port=port,
            protocol="oracle",
            protocols=["oracle"],
        )
        nego_ref = plugin.probe_negotiation(host, port, target_orcl, tps)
        assert nego_ref[0].passed is True
        assert is_connect_response(refuse)
        assert tns_packet_type(refuse) == 4
    finally:
        stop.set()
        th.join(timeout=2.0)
