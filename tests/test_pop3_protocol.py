"""POP3 plugin + RFC 1939 probes against a local stub."""

from __future__ import annotations

import socket
import threading

from uhbs_core.models import TargetSpec
from uhbs_core.protocols import get_plugin, list_protocols
from uhbs_core.protocols.pop3 import POP3Plugin
from uhbs_core.rfc_probes import probe_pop3_rfc1939


def test_pop3_plugin_resolves_and_aliases() -> None:
    assert "pop3" in list_protocols()
    p = get_plugin("pop3")
    assert isinstance(p, POP3Plugin)
    assert p.name == "pop3"
    assert get_plugin("pop-3").name == "pop3"
    assert get_plugin("pop").name == "pop3"


def _serve_pop3(
    responses: dict[str, bytes], *, auth_gate: bool = True
) -> tuple[str, int, threading.Event, socket.socket]:
    """Minimal RFC-shaped POP3 stub.

    ``responses`` maps uppercase command verb → reply line(s) including CRLF.
    Greeting is sent on connect. If ``auth_gate``, STAT/LIST/RETR before USER/PASS
    get ``-ERR``.
    """
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
                    conn.sendall(b"+OK UHBS POP3 stub ready\r\n")
                    authed = False
                    buf = b""
                    while True:
                        chunk = conn.recv(4096)
                        if not chunk:
                            break
                        buf += chunk
                        while b"\n" in buf:
                            line, buf = buf.split(b"\n", 1)
                            cmd = line.decode("utf-8", "replace").strip()
                            if not cmd:
                                continue
                            verb = cmd.split()[0].upper()
                            if verb == "QUIT":
                                conn.sendall(b"+OK Bye\r\n")
                                break
                            preauth = {"STAT", "LIST", "RETR", "DELE"}
                            if verb in preauth and auth_gate and not authed:
                                conn.sendall(b"-ERR not authenticated\r\n")
                                continue
                            if verb == "USER":
                                conn.sendall(responses.get("USER", b"+OK User accepted\r\n"))
                                continue
                            if verb == "PASS":
                                conn.sendall(responses.get("PASS", b"+OK Password accepted\r\n"))
                                authed = True
                                continue
                            if verb == "CAPA":
                                conn.sendall(
                                    responses.get(
                                        "CAPA",
                                        b"+OK Capability list follows\r\nUIDL\r\n.\r\n",
                                    )
                                )
                                continue
                            if verb == "STAT":
                                conn.sendall(responses.get("STAT", b"+OK 0 0\r\n"))
                                continue
                            if verb == "NOOP":
                                conn.sendall(b"+OK\r\n")
                                continue
                            conn.sendall(b"-ERR unrecognized\r\n")
                except (TimeoutError, OSError):
                    pass

    threading.Thread(target=_loop, daemon=True).start()
    return host, port, stop, srv


def test_pop3_rfc_and_plugin_against_stub() -> None:
    host, port, stop, srv = _serve_pop3({})
    try:
        suite = probe_pop3_rfc1939(host, port)
        assert not suite.skipped
        by_id = {c.id: c for c in suite.checks}
        assert by_id["rfc1939.greeting_ok"].passed
        assert by_id["rfc1939.preauth_stat"].passed
        assert by_id["rfc1939.preauth_list"].passed
        assert by_id["rfc1939.unknown_command"].passed
        assert by_id["rfc1939.capa"].passed

        plugin = POP3Plugin()
        target = TargetSpec(name="stub", host=host, port=port, user="u", password="p")
        tps = None
        fsm = plugin.probe_fsm(host, port, target, tps)
        nego = plugin.probe_negotiation(host, port, target, tps)
        state = plugin.probe_state(host, port, target, tps)
        assert any(c.passed for c in fsm)
        assert any("greeting" in c.id for c in nego)
        assert state[0].id == "pop3.state.user_pass_stat"
        assert state[0].passed
    finally:
        stop.set()
        srv.close()


def test_pop3_preauth_fail_when_open_maildrop() -> None:
    # Stub that answers STAT before auth with +OK — should fail preauth check
    host, port, stop, srv = _serve_pop3({}, auth_gate=False)
    try:
        # Override: without auth_gate, STAT returns +OK immediately
        suite = probe_pop3_rfc1939(host, port)
        by_id = {c.id: c for c in suite.checks}
        # Without auth gate the stub still returns +OK for STAT via responses path
        # when auth_gate=False — our stub falls through to STAT handler → +OK
        assert by_id["rfc1939.preauth_stat"].passed is False
    finally:
        stop.set()
        srv.close()
