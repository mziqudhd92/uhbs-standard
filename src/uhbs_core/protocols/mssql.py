"""Tabular Data Stream (TDS) wire checks — Pre-Login (type 0x12).

Transport is TCP (well-known port 1433). Module A focuses on framing tolerance
and Pre-Login option exchange; Login7 / SQL authentication is out of scope.
"""

from __future__ import annotations

import struct

from uhbs_core.models import CheckResult, TargetSpec
from uhbs_core.netutil import tcp_transact
from uhbs_core.protocols.base import ProtocolPlugin
from uhbs_core.tps import TPS

# TDS packet types (MS-TDS)
_TDS_PRELOGIN = 0x12
_TDS_TABULAR = 0x04

# Pre-Login option tokens
_PRELOGIN_VERSION = 0x00
_PRELOGIN_ENCRYPTION = 0x01
_PRELOGIN_TERMINATOR = 0xFF

# ENCRYPTION option values
_ENCRYPT_OFF = 0x00
_ENCRYPT_ON = 0x01
_ENCRYPT_NOT_SUP = 0x02
_ENCRYPT_REQ = 0x03

_ENCRYPTION_LABELS = {
    _ENCRYPT_OFF: "ENCRYPT_OFF",
    _ENCRYPT_ON: "ENCRYPT_ON",
    _ENCRYPT_NOT_SUP: "ENCRYPT_NOT_SUP",
    _ENCRYPT_REQ: "ENCRYPT_REQ",
}

# TDS token stream — ERROR token (post-handshake; some stacks emit early)
_TDS_TOKEN_ERROR = 0xAA


def build_prelogin_packet(
    *,
    version_data: bytes | None = None,
    encryption: int = _ENCRYPT_OFF,
    include_encryption: bool = True,
) -> bytes:
    """Build a client Pre-Login TDS message (type 0x12, status EOM)."""
    version_data = version_data or bytes([0x0F, 0x00, 0x07, 0x00, 0x00, 0x00])
    data = bytearray(version_data)
    tokens: list[tuple[int, int, int]] = [(_PRELOGIN_VERSION, 0, len(version_data))]
    if include_encryption:
        enc_off = len(data)
        data.append(encryption & 0xFF)
        tokens.append((_PRELOGIN_ENCRYPTION, enc_off, 1))

    stream = bytearray()
    for tok, off, ln in tokens:
        stream.append(tok)
        stream.extend(struct.pack(">HH", off, ln))
    stream.append(_PRELOGIN_TERMINATOR)
    body = bytes(stream) + bytes(data)
    length = 8 + len(body)
    header = (
        bytes([_TDS_PRELOGIN, 0x01])
        + struct.pack(">H", length)
        + struct.pack(">H", 0)
        + bytes([0, 0])
    )
    return header + body


def is_tds_packet(raw: bytes) -> bool:
    return len(raw) >= 8


def tds_packet_type(raw: bytes) -> int | None:
    if len(raw) < 1:
        return None
    return raw[0]


def tds_packet_length(raw: bytes) -> int | None:
    if len(raw) < 4:
        return None
    return struct.unpack(">H", raw[2:4])[0]


def parse_prelogin_options(raw: bytes) -> dict[int, bytes]:
    """Parse Pre-Login option values from a full TDS packet (header + body)."""
    if len(raw) < 9 or raw[0] != _TDS_PRELOGIN:
        return {}
    body = raw[8:]
    idx = 0
    spec: list[tuple[int, int, int]] = []
    while idx < len(body):
        token = body[idx]
        if token == _PRELOGIN_TERMINATOR:
            data = body[idx + 1 :]
            break
        if idx + 5 > len(body):
            return {}
        offset = struct.unpack(">H", body[idx + 1 : idx + 3])[0]
        length = struct.unpack(">H", body[idx + 3 : idx + 5])[0]
        spec.append((token, offset, length))
        idx += 5
    else:
        return {}

    out: dict[int, bytes] = {}
    for token, offset, length in spec:
        end = offset + length
        if end <= len(data):
            out[token] = data[offset:end]
    return out


def format_prelogin_detail(options: dict[int, bytes]) -> str:
    parts: list[str] = []
    if _PRELOGIN_VERSION in options:
        parts.append(f"VERSION={options[_PRELOGIN_VERSION].hex()}")
    if _PRELOGIN_ENCRYPTION in options and options[_PRELOGIN_ENCRYPTION]:
        enc = options[_PRELOGIN_ENCRYPTION][0]
        label = _ENCRYPTION_LABELS.get(enc, f"0x{enc:02x}")
        parts.append(f"ENCRYPTION={label}")
    return ", ".join(parts) if parts else "no recognized Pre-Login options"


def _fsm_survived(raw: bytes, err: str | None) -> bool:
    if err and not raw and "timed out" in err.lower():
        return False
    if not raw and not err:
        return True
    if _TDS_TOKEN_ERROR in raw[8:]:
        return True
    if tds_packet_type(raw) == _TDS_TABULAR:
        return True
    return bool(raw) or bool(err)


class MssqlPlugin(ProtocolPlugin):
    """TDS (Pre-Login / Login7 family) over TCP."""

    name = "mssql"
    families = ("it", "database")

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        # Truncated TDS length — must not hang the harness.
        junk = bytes([0x12, 0x01, 0x01, 0x00]) + b"\x00" * 4 + b"\xff"
        raw, _, err = tcp_transact(host, port, junk, timeout=3.0, recv_first=False)
        ok = _fsm_survived(raw, err)

        # Unrecognized verb / garbage RESP-style payload on TDS port.
        raw2, _, err2 = tcp_transact(
            host, port, b"NOT-TDS-GARBAGE\r\n", timeout=3.0, recv_first=False
        )
        ok2 = _fsm_survived(raw2, err2)
        ok = ok and ok2

        detail = ""
        if raw2:
            detail = f"garbage_reply len={len(raw2)} type=0x{raw2[0]:02x}"
        elif raw:
            detail = f"trunc_reply len={len(raw)}"
        else:
            detail = err2 or err or "closed"

        return [
            CheckResult(
                id="mssql.fsm.invalid_framing",
                team="blue",
                passed=ok,
                detail=detail[:160],
                score=80.0 if ok else 0.0,
            )
        ]

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        prelogin = build_prelogin_packet()
        raw, _, err = tcp_transact(
            host, port, prelogin, timeout=3.0, recv_first=False
        )
        options = parse_prelogin_options(raw)
        nego_ok = (
            len(raw) >= 8
            and tds_packet_type(raw) == _TDS_PRELOGIN
            and (
                _PRELOGIN_VERSION in options
                or _PRELOGIN_ENCRYPTION in options
            )
        )
        if nego_ok:
            detail = format_prelogin_detail(options)
        elif raw:
            detail = (
                f"type=0x{raw[0]:02x} len={len(raw)} "
                f"tds_len={tds_packet_length(raw)}"
            )
        else:
            detail = err or "no Pre-Login response"

        return [
            CheckResult(
                id="mssql.nego.prelogin",
                team="blue",
                passed=nego_ok,
                detail=detail,
                score=100.0 if nego_ok else 0.0,
            )
        ]
