from __future__ import annotations

import socket
from typing import List, Optional

from ..models import CheckResult, TargetSpec
from ..tps import TPS
from uhbs_core.protocols.base import ProtocolPlugin


class TelnetPlugin(ProtocolPlugin):
    name = "telnet"
    families = ("it", "posix")

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: Optional[TPS]
    ) -> List[CheckResult]:
        try:
            with socket.create_connection((host, port), timeout=3.0) as s:
                s.settimeout(2.0)
                data = s.recv(1024)
                # IAC negotation bytes (0xff) expected in RFC 854
                has_iac = b"\xff" in data or len(data) > 0
                return [
                    CheckResult(
                        id="telnet.fsm.banner_or_iac",
                        team="blue",
                        passed=has_iac,
                        detail=f"recv={data[:40]!r}",
                        score=100.0 if has_iac else 0.0,
                    )
                ]
        except OSError as exc:
            return [
                CheckResult(
                    id="telnet.fsm.connect",
                    team="blue",
                    passed=False,
                    detail=str(exc),
                    score=0.0,
                )
            ]

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: Optional[TPS]
    ) -> List[CheckResult]:
        return self.probe_fsm(host, port, target, tps)
