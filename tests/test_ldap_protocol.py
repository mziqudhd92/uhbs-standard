"""LDAP plugin — BER builders and local stub probes."""

from __future__ import annotations

import socket
import threading

from uhbs_core.models import CheckResult, TargetSpec
from uhbs_core.protocols import get_plugin, list_protocols
from uhbs_core.protocols.ldap import (
    LDAPPlugin,
    build_bind_request_anonymous,
    build_search_root_dse,
    build_unbind_request,
    has_search_result_entry,
    ldap_session,
    parse_bind_result_code,
    parse_search_done_result_code,
)
from uhbs_core.protocols.registry import register


def _ensure_ldap_registered() -> None:
    if "ldap" not in list_protocols():
        register(LDAPPlugin())


def test_ldap_plugin_resolves_and_aliases() -> None:
    _ensure_ldap_registered()
    p = get_plugin("ldap")
    assert isinstance(p, LDAPPlugin)
    assert p.name == "ldap"


def test_ber_bind_and_search_framing() -> None:
    bind = build_bind_request_anonymous()
    assert bind == bytes.fromhex("300c020101600702010304008000")
    search = build_search_root_dse()
    assert search.startswith(b"\x30")
    assert b"objectClass" in search
    assert b"+" in search
    unbind = build_unbind_request()
    assert b"\x42\x00" in unbind


def test_unreachable_does_not_raise() -> None:
    plugin = LDAPPlugin()
    target = TargetSpec(name="down", host="127.0.0.1", port=1)
    for fn in (plugin.probe_fsm, plugin.probe_negotiation, plugin.probe_state):
        out = fn("127.0.0.1", 1, target, None)
        assert isinstance(out, list)
        assert all(isinstance(c, CheckResult) for c in out)


def _bind_success(message_id: int) -> bytes:
    body = b"\x0a\x01\x00\x04\x00\x04\x00"
    op = b"\x61" + bytes([len(body)]) + body
    mid = b"\x02\x01" + bytes([message_id])
    inner = mid + op
    return b"\x30" + bytes([len(inner)]) + inner


def _search_done_success(message_id: int) -> bytes:
    body = b"\x0a\x01\x00\x04\x00\x04\x00"
    op = b"\x65" + bytes([len(body)]) + body
    mid = b"\x02\x01" + bytes([message_id])
    inner = mid + op
    return b"\x30" + bytes([len(inner)]) + inner


def _serve_ldap_stub(
    *,
    bind_rc: int = 0,
    search_ok: bool = True,
    reject_invalid: bool = True,
) -> tuple[str, int, threading.Event, socket.socket]:
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
                    while True:
                        data = conn.recv(65535)
                        if not data:
                            break
                        if reject_invalid and (
                            data.startswith(b"\xff")
                            or data.startswith(b"\x30\x08\x02\x01\x01\x60\x05\x02")
                        ):
                            break
                        if b"\x60" in data:
                            if bind_rc == 0:
                                conn.sendall(_bind_success(1))
                            else:
                                body = (
                                    bytes([0x0A, 0x01, bind_rc])
                                    + b"\x04\x00\x04\x00"
                                )
                                op = b"\x61" + bytes([len(body)]) + body
                                inner = b"\x02\x01\x01" + op
                                conn.sendall(b"\x30" + bytes([len(inner)]) + inner)
                            continue
                        if b"\x63" in data and search_ok and bind_rc == 0:
                            conn.sendall(_search_done_success(2))
                            continue
                        if b"\x42" in data:
                            break
                except (TimeoutError, OSError):
                    pass

    threading.Thread(target=_loop, daemon=True).start()
    return host, port, stop, srv


def test_ldap_against_stub() -> None:
    _ensure_ldap_registered()
    host, port, stop, srv = _serve_ldap_stub()
    try:
        plugin = LDAPPlugin()
        target = TargetSpec(name="stub", host=host, port=port)
        fsm = plugin.probe_fsm(host, port, target, None)
        nego = plugin.probe_negotiation(host, port, target, None)
        state = plugin.probe_state(host, port, target, None)
        assert fsm[0].id == "ldap.fsm.invalid_ber"
        assert fsm[0].passed
        assert nego[0].id == "ldap.nego.anonymous_bind"
        assert nego[0].passed
        assert state[0].id == "ldap.state.root_dse_search"
        assert state[0].passed

        raw, err = ldap_session(
            host,
            port,
            [
                build_bind_request_anonymous(),
                build_search_root_dse(),
                build_unbind_request(),
            ],
        )
        assert not err
        assert parse_bind_result_code(raw) == 0
        assert parse_search_done_result_code(raw) == 0 or has_search_result_entry(raw)
    finally:
        stop.set()
        srv.close()


def test_parse_bind_protocol_error() -> None:
    body = b"\x0a\x01\x02\x04\x00\x04\x0fprotocolError"
    op = b"\x61" + bytes([len(body)]) + body
    inner = b"\x02\x01\x01" + op
    raw = b"\x30" + bytes([len(inner)]) + inner
    assert parse_bind_result_code(raw) == 2


def test_ldap_rejects_oversize_ber_length() -> None:
    """A peer advertising a huge definite length must not allocate multi-GB."""
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 0))
    srv.listen(1)
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
                conn.recv(64)
                # SEQUENCE with definite length 0x01000000 (16 MiB) — over cap.
                conn.sendall(b"\x30\x84\x01\x00\x00\x00")
            break

    threading.Thread(target=_loop, daemon=True).start()
    try:
        raw, err = ldap_session(host, port, [build_bind_request_anonymous()], timeout=2.0)
        assert "exceeds" in err.lower() or "cap" in err.lower()
        assert len(raw) < 1024
    finally:
        stop.set()
        srv.close()
