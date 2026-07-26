from __future__ import annotations

import socket

from uhbs_core.protocols.base import ProtocolPlugin

from ..models import CheckResult, TargetSpec
from ..tps import TPS


class GenericTCPPlugin(ProtocolPlugin):
    """Fallback for any unknown protocol — connect + banner + fuzz only."""

    name = "generic"
    families = ("any",)

    def __init__(self, name: str = "generic") -> None:
        self.name = name or "generic"

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        try:
            with socket.create_connection((host, port), timeout=3.0) as s:
                s.settimeout(2.0)
                try:
                    banner = s.recv(512)
                except TimeoutError:
                    banner = b""
                return [
                    CheckResult(
                        id=f"{self.name}.fsm.connect",
                        team="blue",
                        passed=True,
                        detail=f"connected; banner={banner[:60]!r}",
                        score=70.0,
                    )
                ]
        except OSError as exc:
            return [
                CheckResult(
                    id=f"{self.name}.fsm.connect",
                    team="blue",
                    passed=False,
                    detail=str(exc),
                    score=0.0,
                )
            ]

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        return self.probe_fsm(host, port, target, tps)
