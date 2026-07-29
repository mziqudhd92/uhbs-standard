"""LDAP plugin — RFC 4511 BER messages over TCP (minimal hand-rolled ASN.1).

RFC 4513 covers bind authentication choices; probes use anonymous simple bind.
"""

from __future__ import annotations

import socket

from uhbs_core.models import CheckResult, TargetSpec
from uhbs_core.netutil import tcp_transact
from uhbs_core.protocols.base import ProtocolPlugin
from uhbs_core.tps import TPS

# LDAP result codes (RFC 4511 §4.1.9)
_LDAP_SUCCESS = 0
_LDAP_PROTOCOL_ERROR = 2

# Invalid / truncated BER for FSM probes
_INVALID_BER = b"\x30\x08\x02\x01\x01\x60\x05\x02"  # length mismatch / truncated
_GARBAGE_BER = b"\xff\x30\x00"


def _ber_length(n: int) -> bytes:
    if n < 0x80:
        return bytes([n])
    body = n.to_bytes((n.bit_length() + 7) // 8, "big")
    return bytes([0x80 | len(body)]) + body


def _ber_tlv(tag: int, content: bytes, *, constructed: bool = False) -> bytes:
    flags = tag
    if constructed:
        flags |= 0x20
    return bytes([flags]) + _ber_length(len(content)) + content


def _ber_integer(value: int) -> bytes:
    if value == 0:
        payload = b"\x00"
    else:
        payload = value.to_bytes((value.bit_length() + 8) // 8, "big", signed=True)
        if payload[0] & 0x80:
            payload = b"\x00" + payload
    return _ber_tlv(0x02, payload)


def _ber_octet_string(data: bytes) -> bytes:
    return _ber_tlv(0x04, data)


def _ber_enumerated(value: int) -> bytes:
    payload = (
        b"\x00"
        if value == 0
        else bytes([value])
        if value < 128
        else value.to_bytes(2, "big")
    )
    return _ber_tlv(0x0A, payload)


def _ber_boolean(value: bool) -> bytes:
    return _ber_tlv(0x01, b"\xff" if value else b"\x00")


def _ber_sequence(parts: bytes) -> bytes:
    return _ber_tlv(0x30, parts, constructed=True)


def _ber_app(tag: int, content: bytes) -> bytes:
    return _ber_tlv(0x40 | tag, content, constructed=True)


def _ber_context(tag: int, content: bytes) -> bytes:
    return _ber_tlv(0x80 | tag, content)


def build_ldap_message(message_id: int, protocol_op: bytes) -> bytes:
    inner = _ber_integer(message_id) + protocol_op
    return _ber_sequence(inner)


def build_bind_request_anonymous(*, version: int = 3, message_id: int = 1) -> bytes:
    """Anonymous simple bind (RFC 4513 §5.1.2)."""
    auth = _ber_context(0, b"")
    bind_body = _ber_integer(version) + _ber_octet_string(b"") + auth
    op = _ber_app(0, bind_body)
    return build_ldap_message(message_id, op)


def build_search_root_dse(*, message_id: int = 2) -> bytes:
    """Base-object search on empty DN with ``+`` attributes (rootDSE)."""
    base = _ber_octet_string(b"")
    scope = _ber_enumerated(0)  # baseObject
    deref = _ber_enumerated(0)  # never
    size_limit = _ber_integer(0)
    time_limit = _ber_integer(0)
    types_only = _ber_boolean(False)
    # present filter: (objectClass=*)
    present = _ber_context(7, b"objectClass")
    attrs = _ber_sequence(_ber_octet_string(b"+"))
    search_body = (
        base
        + scope
        + deref
        + size_limit
        + time_limit
        + types_only
        + present
        + attrs
    )
    op = _ber_app(3, search_body)
    return build_ldap_message(message_id, op)


def build_unbind_request(*, message_id: int = 3) -> bytes:
    op = _ber_tlv(0x42, b"")  # [APPLICATION 2] IMPLICIT NULL
    return build_ldap_message(message_id, op)


def parse_bind_result_code(raw: bytes) -> int | None:
    """Return bindResponse resultCode if present."""
    idx = 0
    while idx < len(raw):
        pos = raw.find(b"\x61", idx)  # bindResponse [APPLICATION 1]
        if pos == -1:
            return None
        window = raw[pos : pos + 96]
        enum_pos = window.find(b"\x0a")
        if enum_pos != -1 and enum_pos + 2 < len(window):
            length = window[enum_pos + 1]
            if length == 1:
                return window[enum_pos + 2]
        idx = pos + 1
    return None


def parse_search_done_result_code(raw: bytes) -> int | None:
    """Return searchResultDone resultCode if present."""
    idx = 0
    while idx < len(raw):
        pos = raw.find(b"\x65", idx)  # searchResultDone [APPLICATION 5]
        if pos == -1:
            return None
        window = raw[pos : pos + 96]
        enum_pos = window.find(b"\x0a")
        if enum_pos != -1 and enum_pos + 2 < len(window):
            length = window[enum_pos + 1]
            if length == 1:
                return window[enum_pos + 2]
        idx = pos + 1
    return None


def has_search_result_entry(raw: bytes) -> bool:
    return b"\x64" in raw  # searchResEntry [APPLICATION 4]


def _recv_exact(sock: socket.socket, n: int) -> bytes:
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            break
        buf += chunk
    return buf


def _read_ber_message(sock: socket.socket) -> bytes:
    tag = _recv_exact(sock, 1)
    if not tag:
        return b""
    lb = _recv_exact(sock, 1)
    if not lb:
        return tag
    if lb[0] & 0x80:
        nlen = lb[0] & 0x7F
        lbytes = _recv_exact(sock, nlen)
        if len(lbytes) != nlen:
            return tag + lb + lbytes
        length = int.from_bytes(lbytes, "big")
        len_field = lb + lbytes
    else:
        length = lb[0]
        len_field = lb
    body = _recv_exact(sock, length)
    return tag + len_field + body


def ldap_session(
    host: str,
    port: int,
    outbound: list[bytes],
    *,
    timeout: float = 4.0,
) -> tuple[bytes, str]:
    """Send LDAP messages on one TCP connection; collect one BER reply per send."""
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            sock.settimeout(timeout)
            collected = b""
            for i, msg in enumerate(outbound):
                sock.sendall(msg)
                is_unbind = b"\x42\x00" in msg or msg.endswith(b"\x42\x00")
                if is_unbind and i == len(outbound) - 1:
                    break
                reply = _read_ber_message(sock)
                collected += reply
            return collected, ""
    except OSError as exc:
        return b"", str(exc)


class LDAPPlugin(ProtocolPlugin):
    """RFC 4511 LDAP — BER bind/search/unbind over TCP (389)."""

    name = "ldap"
    families = ("it",)

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        raw_trunc, _, err_trunc = tcp_transact(
            host, port, _INVALID_BER, timeout=3.0, recv_first=False
        )
        raw_garbage, _, err_garbage = tcp_transact(
            host, port, _GARBAGE_BER, timeout=3.0, recv_first=False
        )
        raw = raw_trunc + raw_garbage
        err = err_trunc or err_garbage

        rc = parse_bind_result_code(raw)
        protocol_err = rc == _LDAP_PROTOCOL_ERROR
        closed = (not raw and bool(err)) or (not raw and not err)
        if protocol_err:
            score = 100.0
            detail = f"bindResponse resultCode={_LDAP_PROTOCOL_ERROR} (protocolError)"
        elif closed:
            score = 75.0
            detail = err or "connection closed on invalid BER (no spurious success)"
        elif rc is not None and rc == _LDAP_SUCCESS:
            score = 15.0
            detail = "invalid BER accepted with bind success — weak fidelity"
        elif raw:
            score = 55.0
            detail = f"reply len={len(raw)} resultCode={rc}"
        else:
            score = 40.0
            detail = err or "no response"
        return [
            CheckResult(
                id="ldap.fsm.invalid_ber",
                team="blue",
                passed=score >= 70.0,
                detail=detail,
                score=score,
            )
        ]

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        bind = build_bind_request_anonymous()
        raw, _, err = tcp_transact(host, port, bind, timeout=3.0, recv_first=False)
        rc = parse_bind_result_code(raw)
        ok = rc == _LDAP_SUCCESS
        detail = (
            f"resultCode={rc}"
            if rc is not None
            else (raw[:80].hex() if raw else (err or "no bindResponse"))
        )
        return [
            CheckResult(
                id="ldap.nego.anonymous_bind",
                team="blue",
                passed=ok,
                detail=detail,
                score=100.0 if ok else (30.0 if rc is not None else 0.0),
            )
        ]

    def probe_state(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        bind = build_bind_request_anonymous(message_id=1)
        search = build_search_root_dse(message_id=2)
        unbind = build_unbind_request(message_id=3)
        raw, err = ldap_session(host, port, [bind, search, unbind], timeout=4.0)
        bind_rc = parse_bind_result_code(raw)
        if bind_rc != _LDAP_SUCCESS:
            ok = False
            detail = f"bind resultCode={bind_rc}" if bind_rc is not None else (err or "bind failed")
            score = 25.0 if bind_rc is not None else 0.0
        else:
            done_rc = parse_search_done_result_code(raw)
            ok = done_rc == _LDAP_SUCCESS or has_search_result_entry(raw)
            detail = (
                f"searchDone={done_rc} entry={has_search_result_entry(raw)}"
                if ok
                else f"searchDone={done_rc} len={len(raw)}"
            )
            score = 100.0 if ok else 35.0
        return [
            CheckResult(
                id="ldap.state.root_dse_search",
                team="blue",
                passed=ok,
                detail=detail,
                score=score,
            )
        ]
