"""PostgreSQL wire protocol plugin (Startup / Authentication / ErrorResponse).

Client-speaks-first (unlike MySQL). Framing follows the PostgreSQL frontend/backend
protocol (v3): StartupMessage and SSLRequest have no type byte; typed messages are
``type (1) + int32 length (includes self) + payload``.
"""

from __future__ import annotations

import socket
import struct

from uhbs_core.models import CheckResult, TargetSpec
from uhbs_core.netutil import tcp_transact
from uhbs_core.protocols.base import ProtocolPlugin
from uhbs_core.tps import TPS

# Protocol 3.0
_PG_PROTOCOL_3 = 196608
# SSLRequest code
_SSL_REQUEST_CODE = 80877103


def build_startup_message(
    user: str = "uhbs",
    database: str = "postgres",
    *,
    protocol: int = _PG_PROTOCOL_3,
) -> bytes:
    """Build an untyped StartupMessage (length-prefixed)."""
    params = (
        f"user\x00{user}\x00"
        f"database\x00{database}\x00"
        "\x00"
    ).encode()
    body = struct.pack("!I", protocol) + params
    return struct.pack("!I", 4 + len(body)) + body


def build_ssl_request() -> bytes:
    """Build SSLRequest (length=8, code=80877103)."""
    return struct.pack("!II", 8, _SSL_REQUEST_CODE)


def build_password_message(password: str = "uhbs-bad") -> bytes:
    """Build PasswordMessage ('p')."""
    payload = password.encode() + b"\x00"
    return b"p" + struct.pack("!I", 4 + len(payload)) + payload


def _msg_type(raw: bytes) -> bytes:
    return raw[:1] if raw else b""


def _is_auth_message(raw: bytes) -> bool:
    """Authentication* backend message starts with 'R'."""
    return len(raw) >= 9 and raw[0:1] == b"R"


def _is_error_response(raw: bytes) -> bool:
    return len(raw) >= 5 and raw[0:1] == b"E"


class PostgresPlugin(ProtocolPlugin):
    """PostgreSQL frontend/backend protocol (RFC-style wire checks)."""

    name = "postgres"
    families = ("it", "database")

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        # Truncated Startup length claim — must not hang the harness.
        junk = b"\x00\x00\x00\x10\x00\x03"  # claims 16 bytes, only 2 follow
        raw, _, err = tcp_transact(host, port, junk, timeout=3.0, recv_first=False)
        ok = bool(raw) or not err or (err and "timed out" not in err.lower())
        # Prefer: ErrorResponse, clean close, or any reply. Soft-pass on clean close.
        if err and not raw and "timed out" in err.lower():
            ok = False
        if not raw and not err:
            ok = True  # peer closed after bad frame
        return [
            CheckResult(
                id="postgres.fsm.truncated_startup",
                team="blue",
                passed=ok,
                detail=(
                    f"type={_msg_type(raw)!r} len={len(raw)}"
                    if raw
                    else (err or "closed")
                ),
                score=80.0 if ok else 0.0,
            )
        ]

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        checks: list[CheckResult] = []

        # A2a — SSLRequest → 'N' (refuse) or 'S' (accept); both are protocol-valid.
        ssl_raw, _, ssl_err = tcp_transact(
            host, port, build_ssl_request(), timeout=3.0, recv_first=False
        )
        ssl_ok = bool(ssl_raw) and ssl_raw[:1] in (b"N", b"S")
        checks.append(
            CheckResult(
                id="postgres.nego.ssl_request",
                team="blue",
                passed=ssl_ok,
                detail=(
                    f"reply={ssl_raw[:8]!r}"
                    if ssl_raw
                    else (ssl_err or "no SSLRequest reply")
                ),
                score=100.0 if ssl_ok else 0.0,
            )
        )

        # A2b — StartupMessage → Authentication* ('R') or ErrorResponse ('E').
        raw, _, err = tcp_transact(
            host, port, build_startup_message(), timeout=3.0, recv_first=False
        )
        nego_ok = _is_auth_message(raw) or _is_error_response(raw)
        detail = ""
        if _is_auth_message(raw) and len(raw) >= 9:
            auth_type = struct.unpack("!I", raw[5:9])[0]
            detail = f"Authentication type={auth_type}"
        elif _is_error_response(raw):
            detail = raw[5:80].decode("utf-8", "replace")
        else:
            detail = err or f"unexpected type={_msg_type(raw)!r} len={len(raw)}"
        checks.append(
            CheckResult(
                id="postgres.nego.startup",
                team="blue",
                passed=nego_ok,
                detail=detail,
                score=100.0 if nego_ok else 0.0,
            )
        )
        return checks

    def probe_state(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        """B1 — rejected authentication (ErrorResponse / 28P01).

        Dual-engine: Strict RFC marks auth rejection ``critical``; Canary mode
        soft-scores honeypots that accept any password (common for decoys).
        """
        strict = tps is None or tps.strict_rfc_enforcement
        # One connection: Startup → Authentication* → Password → expect ErrorResponse.
        # Some low-interaction decoys slow down after Module A timing storms
        # (thousands of accept/close cycles); allow a longer socket timeout and
        # one retry so B1 is not a false "timed out" under load.
        last_err = "no reply after StartupMessage"
        for _attempt in range(2):
            try:
                with socket.create_connection((host, int(port)), timeout=15.0) as s:
                    s.settimeout(15.0)
                    s.sendall(build_startup_message(user="uhbs_no_such_user"))
                    first = s.recv(65535)
                    if not first:
                        last_err = "no reply after StartupMessage"
                        continue
                    # If server already ErrorResponse'd, count as deny.
                    if _is_error_response(first):
                        return [
                            CheckResult(
                                id="postgres.state.auth_deny",
                                team="blue",
                                critical=strict,
                                passed=True,
                                detail=first[5:120].decode("utf-8", "replace"),
                                score=100.0,
                            )
                        ]
                    if _is_auth_message(first):
                        s.sendall(build_password_message("definitely-wrong-password"))
                        second = s.recv(65535)
                        denied = False
                        if _is_error_response(second):
                            denied = True
                            text = second[5:120].decode("utf-8", "replace")
                        elif second[:1] == b"R" and len(second) >= 9:
                            auth_type = struct.unpack("!I", second[5:9])[0]
                            denied = auth_type != 0
                            text = (
                                "AuthenticationOk (accepted bad password)"
                                if auth_type == 0
                                else f"Authentication type={auth_type} after PasswordMessage"
                            )
                        else:
                            text = (
                                second[:80].hex()
                                if second
                                else f"post-auth len={len(second)}"
                            )
                        return [
                            CheckResult(
                                id="postgres.state.auth_deny",
                                team="blue",
                                critical=strict,
                                passed=denied,
                                detail=(
                                    text
                                    + (
                                        ""
                                        if (denied or strict)
                                        else " (Canary/Alert mode: not hard-failed)"
                                    )
                                ),
                                score=100.0 if denied else (0.0 if strict else 35.0),
                            )
                        ]
                    last_err = f"unexpected after Startup: type={_msg_type(first)!r}"
            except OSError as exc:
                last_err = str(exc)[:160]
                continue
        return [
            CheckResult(
                id="postgres.state.auth_deny",
                team="blue",
                critical=strict,
                passed=False,
                detail=last_err,
                score=0.0 if strict else 35.0,
            )
        ]
