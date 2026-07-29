"""SOCKS5 proxy protocol — RFC 1928 (+ RFC 1929 username/password auth).

Primary wire checks: invalid version/method greeting handling (A1),
method selection / no-auth negotiation (A2), and CONNECT to a closed local
port (127.0.0.1:1) expecting a RFC ``REP`` (connection refused) without
requiring Internet egress.
"""

from __future__ import annotations

import ipaddress
import socket
import struct

from uhbs_core.models import CheckResult, TargetSpec
from uhbs_core.protocols.base import ProtocolPlugin
from uhbs_core.rfc_probes import _transact
from uhbs_core.tps import TPS

SOCKS5_VERSION = 0x05
CMD_CONNECT = 0x01
ATYP_IPV4 = 0x01
METHOD_NO_AUTH = 0x00
METHOD_NO_ACCEPTABLE = 0xFF
REP_SUCCEEDED = 0x00
REP_GENERAL_FAILURE = 0x01
REP_HOST_UNREACHABLE = 0x04
REP_CONNECTION_REFUSED = 0x05

# SOCKS4 (optional soft recognition — not the primary probe path)
SOCKS4_VERSION = 0x04
SOCKS4_REPLY_REJECT = 0x5B


def build_client_greeting(*methods: int, version: int = SOCKS5_VERSION) -> bytes:
    """RFC 1928 client greeting: VER, NMETHODS, METHODS."""
    m = list(methods) if methods else [METHOD_NO_AUTH]
    return bytes([version & 0xFF, len(m) & 0xFF, *[x & 0xFF for x in m]])


def parse_method_select(raw: bytes) -> tuple[int, int] | None:
    """Return (ver, method) from server method-selection message."""
    if len(raw) < 2:
        return None
    return raw[0], raw[1]


def is_method_select(raw: bytes) -> bool:
    parsed = parse_method_select(raw)
    return parsed is not None and parsed[0] == SOCKS5_VERSION


def build_connect_ipv4(host: str, port: int) -> bytes:
    """RFC 1928 CONNECT request for an IPv4 destination."""
    addr = ipaddress.IPv4Address(host)
    return (
        bytes([SOCKS5_VERSION, CMD_CONNECT, 0x00, ATYP_IPV4])
        + addr.packed
        + struct.pack("!H", int(port) & 0xFFFF)
    )


def parse_connect_reply(raw: bytes) -> int | None:
    """Return SOCKS5 ``REP`` byte from a server reply, if framed."""
    if len(raw) < 2 or raw[0] != SOCKS5_VERSION:
        return None
    return raw[1]


def build_socks4_connect(host: str, port: int, userid: bytes = b"") -> bytes:
    """Minimal SOCKS4 CONNECT (VN=4) for soft compatibility checks."""
    addr = ipaddress.IPv4Address(host)
    uid = userid if userid.endswith(b"\x00") else userid + b"\x00"
    return bytes([SOCKS4_VERSION, 0x01]) + struct.pack("!H", int(port) & 0xFFFF) + addr.packed + uid


def parse_socks4_reply(raw: bytes) -> tuple[int, int] | None:
    if len(raw) < 2:
        return None
    return raw[0], raw[1]


def _socks5_session(
    host: str,
    port: int,
    body,
    *,
    timeout: float = 4.0,
) -> tuple[bytes, str]:
    """Run ``body(sock)`` on one TCP connection; return (accumulated_recv, err)."""
    chunks: list[bytes] = []
    try:
        with socket.create_connection((host, port), timeout=timeout) as s:
            s.settimeout(timeout)
            body(s, chunks)
    except OSError as exc:
        return b"".join(chunks), str(exc)
    return b"".join(chunks), ""


class SOCKS5Plugin(ProtocolPlugin):
    name = "socks5"
    families = ("it",)

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        checks: list[CheckResult] = []

        # Invalid SOCKS version — server MUST reject (close or METHOD 0xFF).
        bad_ver, _, err_bad = _transact(
            host,
            port,
            build_client_greeting(METHOD_NO_AUTH, version=0x03),
            recv_first=False,
            timeout=3.0,
        )
        parsed_bad = parse_method_select(bad_ver)
        if parsed_bad == (SOCKS5_VERSION, METHOD_NO_ACCEPTABLE):
            score_bad = 100.0
            detail_bad = "method refusal for non-SOCKS5 version"
        elif bad_ver == b"" and err_bad:
            score_bad = 85.0
            detail_bad = err_bad[:120]
        elif bad_ver == b"":
            score_bad = 75.0
            detail_bad = "connection closed on bad version (no SOCKS reply)"
        else:
            score_bad = 40.0
            detail_bad = bad_ver[:8].hex() if bad_ver else (err_bad or "unexpected reply")
        checks.append(
            CheckResult(
                id="socks5.fsm.bad_version",
                team="blue",
                passed=score_bad >= 70.0,
                detail=detail_bad,
                score=score_bad,
            )
        )

        # No acceptable methods — server MUST reply VER=5 METHOD=0xFF.
        no_method, _, err_nm = _transact(
            host,
            port,
            build_client_greeting(0x7F),
            recv_first=False,
            timeout=3.0,
        )
        parsed_nm = parse_method_select(no_method)
        if parsed_nm == (SOCKS5_VERSION, METHOD_NO_ACCEPTABLE):
            score_nm = 100.0
            detail_nm = "METHOD 0xFF (no acceptable methods)"
        elif no_method == b"" and (err_nm or not no_method):
            score_nm = 55.0
            detail_nm = err_nm[:120] if err_nm else "closed without method refusal"
        else:
            score_nm = 25.0
            detail_nm = no_method[:8].hex() if no_method else (err_nm or "no reply")
        checks.append(
            CheckResult(
                id="socks5.fsm.unsupported_method",
                team="blue",
                passed=score_nm >= 70.0,
                detail=detail_nm,
                score=score_nm,
            )
        )

        # Soft SOCKS4: reject/grant reply shape (CD=0x5B/0x5A) when speaking SOCKS4.
        s4_raw, _, s4_err = _transact(
            host,
            port,
            build_socks4_connect("127.0.0.1", 1),
            recv_first=False,
            timeout=3.0,
        )
        s4 = parse_socks4_reply(s4_raw)
        if s4 and s4[0] == 0x00 and s4[1] in (0x5A, 0x5B):
            checks.append(
                CheckResult(
                    id="socks5.fsm.socks4_reply_shape",
                    team="blue",
                    passed=True,
                    detail=f"SOCKS4 CD=0x{s4[1]:02x}",
                    score=100.0,
                )
            )
        elif s4_raw == b"" and s4_err:
            checks.append(
                CheckResult(
                    id="socks5.fsm.socks4_reply_shape",
                    team="blue",
                    passed=True,
                    detail="SOCKS4 probe closed (SOCKS5-only server)",
                    score=50.0,
                )
            )
        else:
            checks.append(
                CheckResult(
                    id="socks5.fsm.socks4_reply_shape",
                    team="blue",
                    passed=True,
                    detail=(
                        s4_raw[:4].hex()
                        if s4_raw
                        else (s4_err or "no SOCKS4-shaped reply — skipped")
                    ),
                    score=50.0,
                )
            )

        return checks

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        raw, _, err = _transact(
            host,
            port,
            build_client_greeting(METHOD_NO_AUTH),
            recv_first=False,
            timeout=3.0,
        )
        parsed = parse_method_select(raw)
        if parsed == (SOCKS5_VERSION, METHOD_NO_AUTH):
            score = 100.0
            detail = "NO AUTH (0x00) selected"
            ok = True
        elif parsed == (SOCKS5_VERSION, METHOD_NO_ACCEPTABLE):
            score = 30.0
            detail = "METHOD 0xFF — no auth not offered"
            ok = False
        elif raw == b"":
            score = 0.0
            detail = err or "no method-selection reply"
            ok = False
        else:
            score = 20.0
            detail = raw[:8].hex() if raw else (err or "invalid greeting reply")
            ok = False
        return [
            CheckResult(
                id="socks5.nego.method_select",
                team="blue",
                passed=ok,
                detail=detail,
                score=score,
            )
        ]

    def probe_state(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        """CONNECT via proxy to 127.0.0.1:1 — expect local connection refused."""

        def _run(sock: socket.socket, chunks: list[bytes]) -> None:
            sock.sendall(build_client_greeting(METHOD_NO_AUTH))
            sel = sock.recv(32)
            chunks.append(sel)
            parsed = parse_method_select(sel)
            if parsed != (SOCKS5_VERSION, METHOD_NO_AUTH):
                return
            sock.sendall(build_connect_ipv4("127.0.0.1", 1))
            chunks.append(sock.recv(256))

        raw, err = _socks5_session(host, port, _run, timeout=4.0)
        rep = None
        if len(raw) >= 4 and raw[0] == SOCKS5_VERSION and raw[1] == METHOD_NO_AUTH:
            rep = parse_connect_reply(raw[2:])
        elif raw:
            rep = parse_connect_reply(raw)
        if rep == REP_CONNECTION_REFUSED:
            score = 100.0
            detail = "REP=0x05 connection refused (local closed port)"
            ok = True
        elif rep in (REP_HOST_UNREACHABLE, REP_GENERAL_FAILURE):
            score = 85.0
            detail = f"REP=0x{rep:02x} (proxy reported failure without hang)"
            ok = True
        elif rep == REP_SUCCEEDED:
            score = 40.0
            detail = "REP=0x00 unexpected success to closed port"
            ok = False
        elif raw and is_method_select(raw) and len(raw) <= 2:
            score = 20.0
            detail = "stopped after method select (no CONNECT reply)"
            ok = False
        elif err and not raw:
            score = 0.0
            detail = err[:120]
            ok = False
        else:
            score = 15.0
            detail = raw[:12].hex() if raw else (err or "no CONNECT reply")
            ok = False

        return [
            CheckResult(
                id="socks5.state.connect_local_refused",
                team="blue",
                passed=ok,
                detail=detail,
                score=score,
            )
        ]
