"""IMAP plugin + RFC 3501 probes against a local stub."""

from __future__ import annotations

import socket
import threading

from uhbs_core.models import TargetSpec
from uhbs_core.protocols import get_plugin
from uhbs_core.protocols.imap import IMAPPlugin, probe_imap_rfc3501
from uhbs_core.protocols.registry import register


def _ensure_imap_registered() -> None:
    register(IMAPPlugin())


def test_imap_plugin_resolves_and_aliases() -> None:
    _ensure_imap_registered()
    p = get_plugin("imap")
    assert isinstance(p, IMAPPlugin)
    assert p.name == "imap"


def test_imap_unreachable_does_not_raise() -> None:
    _ensure_imap_registered()
    target = TargetSpec(name="x", host="127.0.0.1", port=1, protocol="imap")
    plugin = get_plugin("imap")
    for probe in (plugin.probe_fsm, plugin.probe_negotiation, plugin.probe_state):
        checks = probe("127.0.0.1", 1, target, None)
        assert isinstance(checks, list)
        assert checks


def _serve_imap(*, auth_gate: bool = True) -> tuple[str, int, threading.Event, socket.socket]:
    """Minimal RFC-shaped IMAP4 stub on 127.0.0.1."""
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 0))
    srv.listen(8)
    host, port = srv.getsockname()
    stop = threading.Event()

    def _tagged(tag: str, code: str, msg: str) -> bytes:
        return f"{tag} {code} {msg}\r\n".encode("ascii")

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
                    conn.sendall(b"* OK IMAP4rev1 UHBS stub ready\r\n")
                    authed = False
                    buf = b""
                    while True:
                        chunk = conn.recv(4096)
                        if not chunk:
                            break
                        buf += chunk
                        while b"\r\n" in buf:
                            _line, buf = buf.split(b"\r\n", 1)
                            line = _line.decode("utf-8", "replace").strip()
                            if not line:
                                continue
                            parts = line.split(None, 2)
                            if len(parts) < 2:
                                conn.sendall(_tagged("A000", "BAD", "missing command"))
                                continue
                            tag, verb = parts[0], parts[1].upper()
                            rest = parts[2] if len(parts) > 2 else ""

                            if verb == "LOGOUT":
                                conn.sendall(_tagged(tag, "OK", "LOGOUT completed"))
                                break
                            if verb == "CAPABILITY":
                                conn.sendall(
                                    b"* CAPABILITY IMAP4rev1 LOGIN AUTH=PLAIN\r\n"
                                    + _tagged(tag, "OK", "CAPABILITY completed")
                                )
                                continue
                            if verb == "LOGIN":
                                if auth_gate and rest.endswith('"uhbs"'):
                                    conn.sendall(_tagged(tag, "NO", "LOGIN failed"))
                                else:
                                    conn.sendall(_tagged(tag, "OK", "LOGIN completed"))
                                    authed = True
                                continue
                            if verb == "AUTHENTICATE" and rest.upper().startswith("PLAIN"):
                                conn.sendall(_tagged(tag, "NO", "AUTHENTICATE failed"))
                                continue
                            if verb in {"SELECT", "EXAMINE", "FETCH", "STORE", "COPY"}:
                                if auth_gate and not authed:
                                    conn.sendall(_tagged(tag, "NO", "not authenticated"))
                                    continue
                                conn.sendall(_tagged(tag, "OK", f"{verb} completed"))
                                continue
                            if verb == "FOOBAR" or verb not in {
                                "CAPABILITY",
                                "NOOP",
                                "LOGOUT",
                                "LOGIN",
                                "AUTHENTICATE",
                            }:
                                conn.sendall(_tagged(tag, "BAD", "unknown command"))
                                continue
                            conn.sendall(_tagged(tag, "OK", "completed"))
                except (TimeoutError, OSError):
                    pass

    threading.Thread(target=_loop, daemon=True).start()
    return host, port, stop, srv


def test_imap_rfc_and_plugin_against_stub() -> None:
    host, port, stop, srv = _serve_imap()
    try:
        suite = probe_imap_rfc3501(host, port)
        assert not suite.skipped
        by_id = {c.id: c for c in suite.checks}
        assert by_id["rfc3501.greeting_ok"].passed
        assert by_id["rfc3501.capability"].passed
        assert by_id["rfc3501.preauth_select"].passed
        assert by_id["rfc3501.preauth_fetch"].passed
        assert by_id["rfc3501.unknown_command"].passed

        plugin = IMAPPlugin()
        target = TargetSpec(name="stub", host=host, port=port, user="u", password="uhbs")
        fsm = plugin.probe_fsm(host, port, target, None)
        nego = plugin.probe_negotiation(host, port, target, None)
        state = plugin.probe_state(host, port, target, None)
        assert any(c.passed for c in fsm)
        assert any("greeting" in c.id for c in nego)
        assert state[0].id == "imap.state.login_gate"
        assert state[0].passed
        assert "NO" in state[0].detail or "auth gate" in state[0].detail.lower()
    finally:
        stop.set()
        srv.close()


def test_imap_preauth_select_fail_when_open_mailbox() -> None:
    host, port, stop, srv = _serve_imap(auth_gate=False)
    try:
        suite = probe_imap_rfc3501(host, port)
        by_id = {c.id: c for c in suite.checks}
        assert by_id["rfc3501.preauth_select"].passed is False
    finally:
        stop.set()
        srv.close()


def test_imap_login_ok_when_stub_accepts_any() -> None:
    host, port, stop, srv = _serve_imap(auth_gate=False)
    try:
        plugin = IMAPPlugin()
        target = TargetSpec(name="stub", host=host, port=port, user="alice", password="secret")
        state = plugin.probe_state(host, port, target, None)
        assert state[0].passed
        assert "OK" in state[0].detail
    finally:
        stop.set()
        srv.close()
