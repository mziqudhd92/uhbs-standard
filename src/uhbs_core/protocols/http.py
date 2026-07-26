from __future__ import annotations

from typing import List, Optional

from ..models import CheckResult, TargetSpec
from ..rfc_probes import _transact, probe_http_rfc9110
from ..tps import TPS
from uhbs_core.protocols.base import ProtocolPlugin


class HTTPPlugin(ProtocolPlugin):
    name = "http"
    families = ("it", "web", "api")

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: Optional[TPS]
    ) -> List[CheckResult]:
        suite = probe_http_rfc9110(host, port)
        if suite.skipped:
            return [
                CheckResult(
                    id="http.fsm.skipped",
                    team="blue",
                    passed=False,
                    detail=suite.skip_reason,
                    score=0.0,
                )
            ]
        return [
            c
            for c in suite.checks
            if "reject" in c.id or "invalid" in c.id or "unknown" in c.id or "bare_lf" in c.id
        ]

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: Optional[TPS]
    ) -> List[CheckResult]:
        suite = probe_http_rfc9110(host, port)
        return [c for c in suite.checks if "valid_get" in c.id]

    def probe_state(
        self, host: str, port: int, target: TargetSpec, tps: Optional[TPS]
    ) -> List[CheckResult]:
        # Cookie / path echo style: PUT-ish then GET (many decoys only GET)
        raw1, _, _ = _transact(
            host,
            port,
            b"GET /uhbs-marker HTTP/1.1\r\nHost: bench\r\nConnection: close\r\n\r\n",
        )
        raw2, _, _ = _transact(
            host,
            port,
            b"GET /uhbs-marker HTTP/1.1\r\nHost: bench\r\nConnection: close\r\n\r\n",
        )
        ok = raw1.startswith(b"HTTP/") and raw2.startswith(b"HTTP/")
        return [
            CheckResult(
                id="http.state.consistent_get",
                team="blue",
                passed=ok,
                detail="consistent HTTP responses" if ok else "inconsistent/no HTTP",
                score=100.0 if ok else 20.0,
            )
        ]
