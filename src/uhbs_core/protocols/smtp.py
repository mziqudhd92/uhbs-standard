from __future__ import annotations

from uhbs_core.protocols.base import ProtocolPlugin

from ..models import CheckResult, TargetSpec
from ..rfc_probes import probe_smtp_rfc5321
from ..tps import TPS


class SMTPPlugin(ProtocolPlugin):
    name = "smtp"
    families = ("it", "mail")

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        suite = probe_smtp_rfc5321(host, port)
        if suite.skipped:
            return [
                CheckResult(
                    id="smtp.fsm.skipped",
                    team="blue",
                    passed=False,
                    detail=suite.skip_reason,
                    score=0.0,
                )
            ]
        return [
            c
            for c in suite.checks
            if "bad_sequence" in c.id or "unknown" in c.id or "bare_lf" in c.id
        ]

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        suite = probe_smtp_rfc5321(host, port)
        return [c for c in suite.checks if "greeting" in c.id or "ehlo" in c.id]

    def probe_state(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        # MAIL transaction then RSET — state reset is realism signal
        from ..rfc_probes import _smtp_codes, _transact

        raw, _, err = _transact(
            host,
            port,
            b"EHLO uhbs.invalid\r\nMAIL FROM:<a@b.c>\r\nRSET\r\nMAIL FROM:<a@b.c>\r\nQUIT\r\n",
            recv_first=True,
        )
        codes = _smtp_codes(raw)
        ok = codes.count(250) >= 2 or (250 in codes and 220 in codes)
        return [
            CheckResult(
                id="smtp.state.mail_rset",
                team="blue",
                passed=ok,
                detail=f"codes={codes}" if codes else (err or "no codes"),
                score=100.0 if ok else 30.0,
            )
        ]
