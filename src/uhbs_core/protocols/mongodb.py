"""MongoDB wire protocol plugin (OP_MSG / legacy OP_QUERY hello/isMaster).

Framing follows the MongoDB Wire Protocol: 16-byte little-endian MsgHeader
(messageLength, requestID, responseTo, opCode) plus opcode-specific body.
BSON documents use standard type tags (int32 0x10, boolean 0x08, string 0x02).
"""

from __future__ import annotations

import socket
import struct
import time

from uhbs_core.models import CheckResult, TargetSpec
from uhbs_core.netutil import tcp_transact
from uhbs_core.protocols.base import ProtocolPlugin
from uhbs_core.tps import TPS

# Standard opcodes (wire protocol)
_OP_REPLY = 1
_OP_QUERY = 2004
_OP_MSG = 2013

# Reserved / invalid opcode for FSM probes
_OP_INVALID = 0x00DEAD00


def _header(message_length: int, request_id: int, response_to: int, opcode: int) -> bytes:
    return struct.pack("<iiii", message_length, request_id, response_to, opcode)


def _bson_int32_field(name: str, value: int) -> bytes:
    return b"\x10" + name.encode() + b"\x00" + struct.pack("<i", value)


def _bson_str_field(name: str, value: str) -> bytes:
    enc = value.encode() + b"\x00"
    return b"\x02" + name.encode() + b"\x00" + struct.pack("<i", len(enc)) + enc


def build_bson_document(fields: list[tuple[str, int | str]]) -> bytes:
    """Minimal BSON builder for int32 and string fields only."""
    elems: list[bytes] = []
    for key, val in fields:
        if isinstance(val, int):
            elems.append(_bson_int32_field(key, val))
        else:
            elems.append(_bson_str_field(key, val))
    body = b"".join(elems) + b"\x00"
    return struct.pack("<i", 4 + len(body)) + body


def build_op_query_is_master(*, request_id: int = 1) -> bytes:
    """Legacy OP_QUERY isMaster on ``admin.$cmd``."""
    query = build_bson_document([("isMaster", 1)])
    flags = 0
    coll = b"admin.$cmd\x00"
    body = struct.pack("<i", flags) + coll + struct.pack("<ii", 0, 1) + query
    length = 16 + len(body)
    return _header(length, request_id, 0, _OP_QUERY) + body


def build_op_msg_command(
    fields: list[tuple[str, int | str]], *, request_id: int = 1
) -> bytes:
    """OP_MSG with a single kind-0 (body) BSON command document."""
    doc = build_bson_document(fields)
    section = b"\x00" + doc
    body = struct.pack("<I", 0) + section
    length = 16 + len(body)
    return _header(length, request_id, 0, _OP_MSG) + body


def build_hello_op_msg(*, request_id: int = 1) -> bytes:
    return build_op_msg_command([("hello", 1), ("$db", "admin")], request_id=request_id)


def build_ping_op_msg(*, request_id: int = 2) -> bytes:
    return build_op_msg_command([("ping", 1), ("$db", "admin")], request_id=request_id)


def parse_msg_header(raw: bytes) -> dict[str, int] | None:
    if len(raw) < 16:
        return None
    length, req_id, resp_to, opcode = struct.unpack("<iiii", raw[:16])
    return {
        "length": length,
        "request_id": req_id,
        "response_to": resp_to,
        "opcode": opcode,
    }


def is_valid_reply_opcode(opcode: int) -> bool:
    return opcode in (_OP_REPLY, _OP_MSG)


def looks_like_hello_reply(raw: bytes) -> bool:
    """Heuristic parse for hello/isMaster command replies (OP_REPLY or OP_MSG)."""
    hdr = parse_msg_header(raw)
    if hdr is None:
        return False
    if not is_valid_reply_opcode(hdr["opcode"]):
        return False
    if len(raw) >= 16 and hdr["length"] > len(raw) + 4096:
        return False
    lower = raw.lower()
    has_ok = b"ok\x00" in raw
    has_hello_meta = any(
        needle in raw or needle in lower
        for needle in (
            b"maxWireVersion",
            b"maxwireversion",
            b"isMaster",
            b"ismaster",
            b"isWritablePrimary",
            b"iswritableprimary",
            b"helloOk",
            b"hellook",
        )
    )
    return bool(has_ok and has_hello_meta)


def looks_like_ping_reply(raw: bytes) -> bool:
    hdr = parse_msg_header(raw)
    if hdr is None or not is_valid_reply_opcode(hdr["opcode"]):
        return False
    return b"ok\x00" in raw and (b"ping\x00" in raw or b"\x10ok\x00" in raw)


def build_invalid_opcode_frame(*, request_id: int = 99) -> bytes:
    """Header-only message with an unknown opcode (must not hang peers)."""
    return _header(16, request_id, 0, _OP_INVALID)


def build_truncated_header() -> bytes:
    """Only eight bytes of the sixteen-byte MsgHeader."""
    return struct.pack("<ii", 32, 1)


def _recv_some(sock: socket.socket, *, timeout: float = 2.0, limit: int = 65535) -> bytes:
    sock.settimeout(timeout)
    chunks: list[bytes] = []
    total = 0
    try:
        while total < limit:
            try:
                chunk = sock.recv(min(4096, limit - total))
            except TimeoutError:
                break
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
            if total >= 16:
                declared = struct.unpack("<i", chunks[0][:4])[0]
                if 16 <= declared <= limit and total >= declared:
                    break
    except OSError:
        pass
    return b"".join(chunks)


def _session_hello_then_ping(
    host: str, port: int, *, timeout: float = 4.0
) -> tuple[bytes, bytes, str]:
    """Two OP_MSG commands on one TCP session (hello then ping)."""
    t0 = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout) as s:
            s.sendall(build_hello_op_msg(request_id=1))
            hello_raw = _recv_some(s, timeout=timeout)
            s.sendall(build_ping_op_msg(request_id=2))
            ping_raw = _recv_some(s, timeout=timeout)
            _ = (time.perf_counter() - t0) * 1000.0
            return hello_raw, ping_raw, ""
    except OSError as exc:
        return b"", b"", str(exc)


class MongoDBPlugin(ProtocolPlugin):
    """MongoDB wire protocol (hello/isMaster negotiation, OP_MSG commands)."""

    name = "mongodb"
    families = ("it", "database")

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        checks: list[CheckResult] = []

        bad_raw, _, bad_err = tcp_transact(
            host, port, build_invalid_opcode_frame(), timeout=3.0, recv_first=False
        )
        bad_closed = bad_raw == b"" or bool(bad_err)
        bad_replied = bool(bad_raw) and parse_msg_header(bad_raw) is not None
        if bad_closed:
            bad_score = 100.0
            bad_detail = bad_err or "connection closed on invalid opcode"
        elif bad_replied:
            bad_score = 70.0
            bad_detail = f"reply opcode={parse_msg_header(bad_raw)!r}"[:120]
        else:
            bad_score = 40.0
            bad_detail = (bad_raw[:80].hex() if bad_raw else "ambiguous response")[:120]
        checks.append(
            CheckResult(
                id="mongodb.fsm.invalid_opcode",
                team="blue",
                passed=bad_score >= 70.0,
                detail=bad_detail,
                score=bad_score,
            )
        )

        trunc_raw, _, trunc_err = tcp_transact(
            host, port, build_truncated_header(), timeout=3.0, recv_first=False
        )
        trunc_ok = bool(trunc_raw) or bool(trunc_err) or trunc_raw == b""
        if trunc_err and "timed out" in trunc_err.lower() and not trunc_raw:
            trunc_ok = False
        trunc_score = 100.0 if trunc_ok else 0.0
        checks.append(
            CheckResult(
                id="mongodb.fsm.truncated_header",
                team="blue",
                passed=trunc_score >= 70.0,
                detail=(
                    trunc_err
                    or (f"len={len(trunc_raw)}" if trunc_raw else "closed without hang")
                )[:120],
                score=trunc_score if trunc_ok else 0.0,
            )
        )
        return checks

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        checks: list[CheckResult] = []

        msg_raw, _, msg_err = tcp_transact(
            host, port, build_hello_op_msg(), timeout=3.0, recv_first=False
        )
        msg_ok = looks_like_hello_reply(msg_raw)
        checks.append(
            CheckResult(
                id="mongodb.nego.op_msg_hello",
                team="blue",
                passed=msg_ok,
                detail=(
                    f"opcode={parse_msg_header(msg_raw)!r}"[:80]
                    if msg_raw
                    else (msg_err or "no OP_MSG hello reply")
                ),
                score=100.0 if msg_ok else 0.0,
            )
        )

        query_raw, _, query_err = tcp_transact(
            host, port, build_op_query_is_master(), timeout=3.0, recv_first=False
        )
        query_ok = looks_like_hello_reply(query_raw)
        checks.append(
            CheckResult(
                id="mongodb.nego.op_query_ismaster",
                team="blue",
                passed=query_ok,
                detail=(
                    f"opcode={parse_msg_header(query_raw)!r}"[:80]
                    if query_raw
                    else (query_err or "no OP_QUERY isMaster reply")
                ),
                score=100.0 if query_ok else 0.0,
            )
        )
        return checks

    def probe_state(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        hello_raw, ping_raw, err = _session_hello_then_ping(host, port, timeout=4.0)
        if err and not hello_raw and not ping_raw:
            return [
                CheckResult(
                    id="mongodb.state.hello_ping",
                    team="blue",
                    passed=False,
                    detail=err,
                    score=0.0,
                )
            ]
        hello_ok = looks_like_hello_reply(hello_raw)
        ping_hdr = parse_msg_header(ping_raw)
        ping_ok = looks_like_ping_reply(ping_raw) or (
            bool(ping_raw)
            and ping_hdr is not None
            and is_valid_reply_opcode(ping_hdr["opcode"])
            and b"ok\x00" in ping_raw
        )
        ok = hello_ok and ping_ok
        detail_parts = []
        if hello_raw:
            detail_parts.append(f"hello={parse_msg_header(hello_raw)!r}")
        if ping_raw:
            detail_parts.append(f"ping={parse_msg_header(ping_raw)!r}")
        if not detail_parts:
            detail_parts.append(err or "no session replies")
        return [
            CheckResult(
                id="mongodb.state.hello_ping",
                team="blue",
                passed=ok,
                detail=" ".join(detail_parts)[:120],
                score=100.0 if ok else (50.0 if hello_ok else 20.0),
            )
        ]
