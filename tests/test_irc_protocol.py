"""IRC plugin (RFC 1459 / RFC 2812) — offline helpers + local stub probes."""

from __future__ import annotations

import socket
import threading

from uhbs_core.models import TargetSpec
from uhbs_core.protocols import get_plugin
from uhbs_core.protocols.irc import (
    IRCPlugin,
    build_irc_registration,
    extract_irc_numerics,
)
from uhbs_core.protocols.registry import register


def test_irc_plugin_resolves_when_registered() -> None:
    register(IRCPlugin())
    p = get_plugin("irc")
    assert isinstance(p, IRCPlugin)
    assert p.name == "irc"


def test_extract_numerics_and_registration_bytes() -> None:
    assert extract_irc_numerics(":irc.example 001 uhbs :Welcome\r\n") == [1]
    assert extract_irc_numerics(":irc.example 421 uhbs INVALID :Unknown command\r\n") == [421]
    reg = build_irc_registration("n1", "u1", "real name")
    assert reg.startswith(b"NICK n1\r\nUSER u1")


def test_irc_probes_do_not_raise_on_unreachable() -> None:
    plugin = IRCPlugin()
    target = TargetSpec(name="x", host="127.0.0.1", port=1, protocol="irc", protocols=["irc"])
    for method in (plugin.probe_fsm, plugin.probe_negotiation, plugin.probe_state):
        checks = method("127.0.0.1", 1, target, None)
        assert isinstance(checks, list)
        assert checks


def _serve_irc_stub() -> tuple[str, int, threading.Event, socket.socket]:
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
                    conn.sendall(b":stub NOTICE * :UHBS IRC stub ready\r\n")
                    buf = b""
                    registered = False
                    nick = "uhbs"
                    while True:
                        chunk = conn.recv(4096)
                        if not chunk:
                            break
                        buf += chunk
                        while b"\n" in buf:
                            line, buf = buf.split(b"\n", 1)
                            text = line.decode("utf-8", "replace").strip()
                            if not text:
                                continue
                            upper = text.upper()
                            if "PING" in upper and text.startswith(":"):
                                token = text.split()[-1].lstrip(":")
                                conn.sendall(f":stub PING {token}\r\n".encode())
                                continue
                            if upper.startswith("PONG "):
                                continue
                            if upper.startswith("NICK "):
                                nick = text.split()[1].lstrip(":")[:16]
                                continue
                            if upper.startswith("USER "):
                                conn.sendall(
                                    f":stub 001 {nick} :Welcome to the UHBS stub\r\n".encode()
                                )
                                registered = True
                                continue
                            if "@@@" in text or upper.startswith("@@@"):
                                conn.sendall(
                                    b":stub 421 uhbs @@@UHBS_NOT_A_COMMAND :Unknown command\r\n"
                                )
                                continue
                            if not registered and upper.split()[0] not in {
                                "NICK",
                                "USER",
                                "CAP",
                                "QUIT",
                            }:
                                conn.sendall(b":stub 451 uhbs :You have not registered\r\n")
                                continue
                            conn.sendall(b":stub 421 uhbs X :Unknown command\r\n")
                except (TimeoutError, OSError):
                    pass

    threading.Thread(target=_loop, daemon=True).start()
    return host, port, stop, srv


def test_irc_plugin_against_stub() -> None:
    host, port, stop, srv = _serve_irc_stub()
    try:
        plugin = IRCPlugin()
        target = TargetSpec(name="stub", host=host, port=port, user="uhbsprobe")
        fsm = plugin.probe_fsm(host, port, target, None)
        nego = plugin.probe_negotiation(host, port, target, None)
        state = plugin.probe_state(host, port, target, None)
        assert fsm[0].id == "irc.fsm.invalid_command"
        assert fsm[0].passed
        assert any(c.id == "irc.nego.banner_or_ping" and c.passed for c in nego)
        assert any(c.id == "irc.nego.registration_numerics" and c.passed for c in nego)
        assert state[0].id == "irc.state.nick_user_handshake"
        assert state[0].passed
    finally:
        stop.set()
        srv.close()
