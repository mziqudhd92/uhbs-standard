"""Oracle Net TNS (Transparent Network Substrate) wire checks.

Client-speaks-first on TCP (typical port 1521): Connect (type 1) → Accept (2),
Refuse (4), Redirect (5), or Resend (9). Packet framing is a 8-byte header
(length, checksum, type, flags, header checksum) plus type-specific payload.

Probe shape follows publicly documented NSE-style TNS Connect descriptors; no
real database credentials are required for Module A checks.
"""

from __future__ import annotations

import struct

from uhbs_core.models import CheckResult, TargetSpec
from uhbs_core.netutil import tcp_transact
from uhbs_core.protocols.base import ProtocolPlugin
from uhbs_core.tps import TPS

# TNS packet types (Oracle Net foundation)
_TNS_CONNECT = 1
_TNS_ACCEPT = 2
_TNS_REFUSE = 4
_TNS_REDIRECT = 5
_TNS_RESEND = 9

_CONNECT_RESPONSE_TYPES = frozenset(
    {_TNS_ACCEPT, _TNS_REFUSE, _TNS_REDIRECT, _TNS_RESEND}
)


def _tns_header(pkt_type: int, payload_len: int, *, flags: int = 0) -> bytes:
    total = 8 + payload_len
    return struct.pack("!HHBBH", total, 0, pkt_type, flags, 0)


def build_connect_packet(*, service_name: str = "ORCL") -> bytes:
    """Build a minimal TNS Connect with a public-probe-style DESCRIPTION."""
    connect_data = (
        f"(DESCRIPTION=(CONNECT_DATA=(SERVICE_NAME={service_name})"
        f"(CID=(PROGRAM=)(HOST=)(USER=))(COMMAND=)(SERVICE=)(VERSION=)(UNKNOWN=))))"
    ).encode("ascii")
    # Fixed connect header (version … connect flags 0) per Net foundation layout.
    connect_fixed = struct.pack(
        "!11H2B",
        315,  # version
        300,  # compatible version
        0,  # service options
        0x0800,  # SDU
        0xFFFF,  # TDU
        0x4F08,  # NT protocol characteristics (common probe value)
        0,  # line turnaround
        0x0100,  # value of one in hardware
        len(connect_data),
        32,  # offset from packet start to connect data (8-byte TNS + 24-byte connect hdr)
        0x0800,  # max connect data receivable
        0x41,  # connect flags
        0x41,  # connect flags 0
    )
    payload = connect_fixed + connect_data
    return _tns_header(_TNS_CONNECT, len(payload)) + payload


def build_truncated_length_packet() -> bytes:
    """TNS header claiming 256 bytes but only 10 bytes on the wire."""
    return b"\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00"


def tns_packet_type(raw: bytes) -> int | None:
    if len(raw) < 5:
        return None
    return raw[4]


def tns_type_label(pkt_type: int | None) -> str:
    if pkt_type == _TNS_ACCEPT:
        return "accept"
    if pkt_type == _TNS_REFUSE:
        return "refuse"
    if pkt_type == _TNS_REDIRECT:
        return "redirect"
    if pkt_type == _TNS_RESEND:
        return "resend"
    if pkt_type == _TNS_CONNECT:
        return "connect"
    if pkt_type is None:
        return "none"
    return f"type={pkt_type}"


def is_connect_response(raw: bytes) -> bool:
    pt = tns_packet_type(raw)
    return pt in _CONNECT_RESPONSE_TYPES


def parse_refuse_detail(raw: bytes) -> str:
    if len(raw) < 10:
        return raw.hex() if raw else "empty"
    # Refuse user data often carries a 2-byte reason code then ASCII text.
    text = raw[10:120].decode("ascii", "replace").strip("\x00")
    if text:
        return text[:100]
    code = struct.unpack("!H", raw[8:10])[0] if len(raw) >= 10 else 0
    return f"refuse_code={code}"


def parse_accept_detail(raw: bytes) -> str:
    if len(raw) < 12:
        return f"accept len={len(raw)}"
    ver = struct.unpack("!H", raw[8:10])[0]
    compat = struct.unpack("!H", raw[10:12])[0]
    return f"accept version={ver} compatible={compat}"


def parse_redirect_detail(raw: bytes) -> str:
    if len(raw) < 12:
        return f"redirect len={len(raw)}"
    data_len = struct.unpack("!H", raw[10:12])[0] if len(raw) >= 12 else 0
    host = raw[12 : 12 + min(data_len, 80)].decode("ascii", "replace").strip("\x00")
    return host[:100] if host else f"redirect data_len={data_len}"


def describe_connect_response(raw: bytes) -> str:
    pt = tns_packet_type(raw)
    if pt == _TNS_ACCEPT:
        return parse_accept_detail(raw)
    if pt == _TNS_REFUSE:
        return parse_refuse_detail(raw)
    if pt == _TNS_REDIRECT:
        return parse_redirect_detail(raw)
    if pt == _TNS_RESEND:
        return "resend (repeat connect)"
    if raw:
        return f"unexpected {tns_type_label(pt)} len={len(raw)}"
    return "closed"


def build_refuse_packet(reason: str = "ORA-12541") -> bytes:
    """Minimal TNS Refuse for offline stubs."""
    msg = reason.encode("ascii", "replace") + b"\x00"
    body = struct.pack("!H", 0) + msg
    return _tns_header(_TNS_REFUSE, len(body)) + body


def build_accept_packet(*, version: int = 315, compatible: int = 300) -> bytes:
    body = struct.pack("!HHHH", version, compatible, 0x800, 0xFFFF)
    return _tns_header(_TNS_ACCEPT, len(body)) + body


class OraclePlugin(ProtocolPlugin):
    """Oracle Net TNS listener checks (Connect / Accept / Refuse / Redirect)."""

    name = "oracle"
    families = ("it", "database")

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        junk = build_truncated_length_packet()
        raw, _, err = tcp_transact(host, port, junk, timeout=3.0, recv_first=False)
        ok = bool(raw) or not err or (err and "timed out" not in err.lower())
        if err and not raw and "timed out" in err.lower():
            ok = False
        if not raw and not err:
            ok = True
        if raw and tns_packet_type(raw) in (_TNS_REFUSE, _TNS_RESEND):
            ok = True
        detail = describe_connect_response(raw) if raw else (err or "closed")
        return [
            CheckResult(
                id="oracle.fsm.truncated_length",
                team="blue",
                passed=ok,
                detail=detail,
                score=80.0 if ok else 0.0,
            )
        ]

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        svc = target.annotations.get("service_name", "ORCL")
        connect = build_connect_packet(service_name=str(svc))
        raw, _, err = tcp_transact(host, port, connect, timeout=3.0, recv_first=False)
        nego_ok = is_connect_response(raw)
        detail = describe_connect_response(raw) if raw else (err or "no TNS reply")
        return [
            CheckResult(
                id="oracle.nego.connect",
                team="blue",
                passed=nego_ok,
                detail=detail,
                score=100.0 if nego_ok else 0.0,
            )
        ]
