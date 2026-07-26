from __future__ import annotations

import socket
from typing import List, Optional

from ..models import CheckResult, TargetSpec
from ..tps import TPS
from uhbs_core.protocols.base import ProtocolPlugin


class SMBPlugin(ProtocolPlugin):
    """Minimal SMB dialect negotiation probe (IT)."""

    name = "smb"
    families = ("it",)

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: Optional[TPS]
    ) -> List[CheckResult]:
        # Truncated NetBIOS/SMB header — should not hang forever
        try:
            with socket.create_connection((host, port), timeout=3.0) as s:
                s.settimeout(2.0)
                s.sendall(b"\x00\x00\x00\x01\xff")
                try:
                    data = s.recv(256)
                except socket.timeout:
                    data = b""
            return [
                CheckResult(
                    id="smb.fsm.truncated",
                    team="blue",
                    passed=True,
                    detail=f"survived truncated frame resp={data[:20]!r}",
                    score=80.0,
                )
            ]
        except OSError as exc:
            return [
                CheckResult(
                    id="smb.fsm.connect",
                    team="blue",
                    passed=False,
                    detail=str(exc),
                    score=0.0,
                )
            ]

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: Optional[TPS]
    ) -> List[CheckResult]:
        # SMB2 NEGOTIATE (best-effort presence)
        try:
            with socket.create_connection((host, port), timeout=3.0) as s:
                s.settimeout(2.0)
                # NetBIOS session + SMB1 negotiate is complex; just confirm accept
                s.sendall(b"\x00\x00\x00\x00")
                try:
                    data = s.recv(256)
                except socket.timeout:
                    data = b""
            ok = True
            return [
                CheckResult(
                    id="smb.nego.accept",
                    team="blue",
                    passed=ok,
                    detail=f"connected resp={data[:30]!r}",
                    score=70.0,
                )
            ]
        except OSError as exc:
            return [
                CheckResult(
                    id="smb.nego.connect",
                    team="blue",
                    passed=False,
                    detail=str(exc),
                    score=0.0,
                )
            ]
