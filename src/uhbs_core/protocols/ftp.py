from __future__ import annotations

from uhbs_core.protocols.base import ProtocolPlugin

from ..models import CheckResult, TargetSpec
from ..rfc_probes import _transact
from ..tps import TPS


class FTPPlugin(ProtocolPlugin):
    name = "ftp"
    families = ("it",)

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        # RETR before login → 530
        raw, _, err = _transact(host, port, b"RETR secret\r\nQUIT\r\n", recv_first=True)
        text = raw.decode("utf-8", "replace")
        ok = "530" in text or "503" in text or "550" in text
        return [
            CheckResult(
                id="ftp.fsm.retr_before_auth",
                team="blue",
                passed=ok,
                detail=text[:120] if text else (err or "no response"),
                score=100.0 if ok else 0.0,
            )
        ]

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        raw, _, err = _transact(host, port, b"", recv_first=True)
        text = raw.decode("utf-8", "replace")
        ok = text.startswith("220")
        return [
            CheckResult(
                id="ftp.nego.banner_220",
                team="blue",
                passed=ok,
                detail=text[:120] if text else (err or "no banner"),
                score=100.0 if ok else 0.0,
            )
        ]

    def probe_state(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        raw, _, err = _transact(
            host,
            port,
            b"USER anonymous\r\nPASS guest@\r\nPWD\r\nQUIT\r\n",
            recv_first=True,
        )
        text = raw.decode("utf-8", "replace")
        ok = "230" in text or "331" in text
        return [
            CheckResult(
                id="ftp.state.login_pwd",
                team="blue",
                passed=ok,
                detail=text[:160] if text else (err or "fail"),
                score=100.0 if ok else 30.0,
            )
        ]
