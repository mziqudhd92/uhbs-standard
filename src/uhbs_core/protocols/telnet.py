from __future__ import annotations

import socket

from uhbs_core.protocols.base import ProtocolPlugin

from ..models import CheckResult, TargetSpec
from ..tps import TPS

IAC = 0xFF
WILL, WONT, DO, DONT = 0xFB, 0xFC, 0xFD, 0xFE

_LOGIN_KEYWORDS = (b"login", b"username", b"user:", b"user name")


def _negate_options(data: bytes) -> bytes:
    """Build minimal IAC replies (DO->WONT, WILL->DONT) so a server that
    waits for option negotiation to settle before printing its login
    banner will actually proceed."""
    out = bytearray()
    i = 0
    while i < len(data) - 2:
        if data[i] == IAC and data[i + 1] in (DO, WILL) and i + 2 < len(data):
            opt = data[i + 2]
            reply = WONT if data[i + 1] == DO else DONT
            out += bytes([IAC, reply, opt])
            i += 3
        else:
            i += 1
    return bytes(out)


class TelnetPlugin(ProtocolPlugin):
    """Telnet (RFC 854) IAC negotiation + login-prompt probe.

    Architecture note (2026-07-27 review): the original ``probe_fsm`` used
    ``has_iac = b"\\xff" in data or len(data) > 0`` — the ``or`` clause meant
    *any* non-empty TCP response (e.g. an HTTP banner on the wrong port, or
    a plain echo server) counted as a passing Telnet negotiation. That is a
    bypassable check for a benchmark harness. It has been replaced with a
    strict requirement for a literal IAC (``0xFF``) byte.

    Dual-engine evaluation mode (architecture review round 2, item 1): in
    Strict RFC mode (``tps.strict_rfc_enforcement`` True — the default, and
    what every shipped TPS file sets today) a missing IAC byte is a
    ``critical=True`` hard gate: it trips the Module A/B circuit breaker in
    ``check_scoring.score_checks``. In Canary/Alert mode
    (``strict_rfc_enforcement=False``) the same missing signal is scored as
    an explicit, non-critical partial-credit outcome instead — mirroring
    the alert-only handling already used for silent UDP protocols in
    ``udp_base.py`` — because a log-only decoy that never implements full
    RFC 854 option negotiation is not "broken," it is simply out of scope
    for strict protocol fidelity.
    """

    name = "telnet"
    families = ("it", "posix")

    @staticmethod
    def _strict(tps: TPS | None) -> bool:
        return tps is None or tps.strict_rfc_enforcement

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        strict = self._strict(tps)
        try:
            with socket.create_connection((host, port), timeout=3.0) as s:
                s.settimeout(2.0)
                try:
                    data = s.recv(1024)
                except TimeoutError:
                    data = b""
            has_iac = IAC in data
            if has_iac:
                score = 100.0
            elif strict:
                score = 0.0
            else:
                score = 35.0  # Canary/Alert mode: alert-only, not penalized as broken
            return [
                CheckResult(
                    id="telnet.fsm.iac_negotiation",
                    team="blue",
                    critical=strict,
                    passed=has_iac,
                    detail=(
                        f"recv={data[:40]!r}"
                        if has_iac
                        else (
                            f"no IAC (0xFF) byte in response — not real Telnet: recv={data[:40]!r}"
                            + ("" if strict else " (Canary/Alert mode: not hard-failed)")
                        )
                    ),
                    score=score,
                )
            ]
        except OSError as exc:
            return [
                CheckResult(
                    id="telnet.fsm.connect",
                    team="blue",
                    critical=strict,
                    passed=False,
                    detail=str(exc),
                    score=0.0,
                )
            ]

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        return self.probe_fsm(host, port, target, tps)

    def probe_state(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        # B1 — after real IAC negotiation, a login-style honeypot should
        # present a login/username prompt. This is a realism signal, not a
        # security gate (a valid Telnet stack could legitimately skip a
        # login banner), so it is NOT marked critical.
        try:
            with socket.create_connection((host, port), timeout=3.0) as s:
                s.settimeout(2.0)
                try:
                    first = s.recv(1024)
                except TimeoutError:
                    first = b""
                reply = _negate_options(first)
                if reply:
                    s.sendall(reply)
                try:
                    second = s.recv(1024)
                except TimeoutError:
                    second = b""
        except OSError as exc:
            return [
                CheckResult(
                    id="telnet.state.login_prompt",
                    team="blue",
                    passed=False,
                    detail=str(exc),
                    score=0.0,
                )
            ]

        combined = (first + second).lower()
        has_iac = IAC in (first + second)
        has_prompt = any(kw in combined for kw in _LOGIN_KEYWORDS)
        if has_prompt:
            score = 100.0
        elif has_iac:
            score = 50.0  # real Telnet negotiation, but no visible login banner yet
        else:
            score = 0.0
        return [
            CheckResult(
                id="telnet.state.login_prompt",
                team="blue",
                passed=has_prompt or has_iac,
                detail=(
                    f"login-style prompt observed: {combined[:80]!r}"
                    if has_prompt
                    else f"IAC negotiated but no login prompt seen: {combined[:80]!r}"
                    if has_iac
                    else f"no IAC / no prompt: {combined[:80]!r}"
                ),
                score=score,
            )
        ]
