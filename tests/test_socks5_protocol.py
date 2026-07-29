"""SOCKS5 plugin (RFC 1928) — framing helpers + local stub probes."""

from __future__ import annotations

import socket
import struct
import threading

from uhbs_core.models import TargetSpec
from uhbs_core.protocols import get_plugin
from uhbs_core.protocols.registry import register
from uhbs_core.protocols.socks5 import (
    SOCKS5Plugin,
    build_client_greeting,
    build_connect_ipv4,
    build_socks4_connect,
    parse_connect_reply,
    parse_method_select,
    parse_socks4_reply,
    REP_CONNECTION_REFUSED,
    METHOD_NO_ACCEPTABLE,
    METHOD_NO_AUTH,
    SOCKS5_VERSION,
)
from uhbs_core.tps import TPS


def test_socks5_plugin_resolves() -> None:
    register(SOCKS5Plugin())
    p = get_plugin("socks5")
    assert isinstance(p, SOCKS5Plugin)
    assert p.name == "socks5"


def test_framing_helpers() -> None:
    greet = build_client_greeting(METHOD_NO_AUTH)
    assert greet == b"\x05\x01\x00"
    assert parse_method_select(b"\x05\x00") == (SOCKS5_VERSION, METHOD_NO_AUTH)
    assert parse_method_select(b"\x05\xff") == (SOCKS5_VERSION, METHOD_NO_ACCEPTABLE)

    req = build_connect_ipv4("127.0.0.1", 1)
    assert req[:4] == b"\x05\x01\x00\x01"
    assert req[4:8] == b"\x7f\x00\x00\x01"
    assert struct.unpack("!H", req[8:10])[0] == 1

    rep = b"\x05\x05\x00\x01\x7f\x00\x00\x01\x00\x00"
    assert parse_connect_reply(rep) == REP_CONNECTION_REFUSED

    s4 = build_socks4_connect("127.0.0.1", 80, b"u")
    assert s4[0] == 0x04
    assert parse_socks4_reply(b"\x00\x5b") == (0, 0x5B)


def test_socks5_unreachable_does_not_raise() -> None:
    target = TargetSpec(
        name="closed",
        host="127.0.0.1",
        port=1,
        protocol="socks5",
        protocols=["socks5"],
    )
    plugin = SOCKS5Plugin()
    for probe in (
        plugin.probe_fsm,
        plugin.probe_negotiation,
        plugin.probe_state,
    ):
        checks = probe("127.0.0.1", 1, target, None)
        assert isinstance(checks, list)
        assert checks


def _serve_socks5(*, refuse_methods: set[int] | None = None) -> tuple[str, int, threading.Event, socket.socket]:
    """Minimal RFC 1928 stub: greeting → method → CONNECT → synthetic REP."""
    refuse = refuse_methods or set()
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
                    buf = conn.recv(4096)
                    if not buf:
                        continue
                    if buf[0] == 0x04:
                        conn.sendall(b"\x00\x5b\x00\x00\x00\x00\x00\x00")
                        continue
                    if buf[0] != SOCKS5_VERSION:
                        conn.sendall(bytes([SOCKS5_VERSION, METHOD_NO_ACCEPTABLE]))
                        continue
                    if len(buf) >= 2 and buf[1] == 0:
                        conn.sendall(bytes([SOCKS5_VERSION, METHOD_NO_ACCEPTABLE]))
                        continue
                    nmethods = buf[1] if len(buf) >= 2 else 0
                    methods = list(buf[2 : 2 + nmethods]) if len(buf) >= 2 + nmethods else []
                    pick = METHOD_NO_AUTH if METHOD_NO_AUTH in methods else None
                    if pick is None or any(m in refuse for m in methods):
                        conn.sendall(bytes([SOCKS5_VERSION, METHOD_NO_ACCEPTABLE]))
                        continue
                    conn.sendall(bytes([SOCKS5_VERSION, pick]))
                    req = conn.recv(4096)
                    if not req or req[0] != SOCKS5_VERSION or req[1] != 0x01:
                        continue
                    conn.sendall(
                        bytes([SOCKS5_VERSION, REP_CONNECTION_REFUSED, 0x00, 0x01])
                        + b"\x00\x00\x00\x00"
                        + b"\x00\x00"
                    )
                except (TimeoutError, OSError):
                    pass

    threading.Thread(target=_loop, daemon=True).start()
    return host, port, stop, srv


def test_socks5_plugin_against_stub() -> None:
    host, port, stop, srv = _serve_socks5()
    try:
        target = TargetSpec(
            name="socks-stub",
            host=host,
            port=port,
            protocol="socks5",
            protocols=["socks5"],
        )
        tps = TPS(
            name="socks-stub",
            profile_class="Low-Interaction",
            protocol="socks5",
            protocols=["socks5"],
            strict_rfc_enforcement=True,
        )
        plugin = SOCKS5Plugin()
        fsm = plugin.probe_fsm(host, port, target, tps)
        by_fsm = {c.id: c for c in fsm}
        assert by_fsm["socks5.fsm.bad_version"].passed
        assert by_fsm["socks5.fsm.unsupported_method"].passed

        nego = plugin.probe_negotiation(host, port, target, tps)
        assert nego[0].id == "socks5.nego.method_select"
        assert nego[0].passed

        state = plugin.probe_state(host, port, target, tps)
        assert state[0].id == "socks5.state.connect_local_refused"
        assert state[0].passed
    finally:
        stop.set()
        srv.close()
