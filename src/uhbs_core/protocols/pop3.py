from __future__ import annotations

from uhbs_core.protocols.base import ProtocolPlugin

from ..models import CheckResult, TargetSpec
from ..rfc_probes import probe_pop3_rfc1939
from ..tps import TPS


class POP3Plugin(ProtocolPlugin):
    """RFC 1939 POP3 — mail retrieval decoys (Authorization → Transaction)."""

    name = "pop3"
    families = ("it", "mail")

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        suite = probe_pop3_rfc1939(host, port)
        if suite.skipped:
            return [
                CheckResult(
                    id="pop3.fsm.skipped",
                    team="blue",
                    passed=False,
                    detail=suite.skip_reason,
                    score=0.0,
                )
            ]
        return [
            c
            for c in suite.checks
            if "preauth" in c.id or "unknown" in c.id or "bare_lf" in c.id
        ]

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        suite = probe_pop3_rfc1939(host, port)
        return [c for c in suite.checks if "greeting" in c.id or "capa" in c.id]

    def probe_state(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        # USER → PASS → STAT → QUIT — auth gate then transaction verb
        from ..rfc_probes import _pop3_status, _transact

        user = (target.user or "uhbs").encode("ascii", "replace")
        password = (target.password or "uhbs").encode("ascii", "replace")
        script = (
            b"USER " + user + b"\r\n"
            b"PASS " + password + b"\r\n"
            b"STAT\r\n"
            b"QUIT\r\n"
        )
        raw, _, err = _transact(host, port, script, recv_first=True)
        statuses = _pop3_status(raw)
        # Greeting + USER + PASS should yield multiple +OK; STAT after auth too
        ok_count = sum(1 for s in statuses if s == "+OK")
        ok = ok_count >= 3
        return [
            CheckResult(
                id="pop3.state.user_pass_stat",
                team="blue",
                passed=ok,
                detail=f"statuses={statuses}" if statuses else (err or "no statuses"),
                score=100.0 if ok else 30.0,
                evidence=[raw[:400].decode("utf-8", "replace")],
            )
        ]
