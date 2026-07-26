from __future__ import annotations

from typing import List, Optional

from ..models import CheckResult, TargetSpec
from ..rfc_probes import _transact
from ..tps import TPS
from uhbs_core.protocols.base import ProtocolPlugin


class RedisPlugin(ProtocolPlugin):
    name = "redis"
    families = ("it", "database")

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: Optional[TPS]
    ) -> List[CheckResult]:
        # Nested/invalid RESP should error, not crash
        raw, _, err = _transact(host, port, b"Garbage\r\n", recv_first=False)
        text = raw.decode("utf-8", "replace")
        ok = text.startswith("-") or text.startswith("+") or raw == b"" or text.startswith("*")
        return [
            CheckResult(
                id="redis.fsm.invalid_verb",
                team="blue",
                passed=ok or bool(err),
                detail=text[:120] if text else (err or "closed"),
                score=100.0 if (text.startswith("-") or "ERR" in text) else 40.0,
            )
        ]

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: Optional[TPS]
    ) -> List[CheckResult]:
        raw, _, err = _transact(host, port, b"PING\r\n", recv_first=False)
        text = raw.decode("utf-8", "replace")
        ok = "PONG" in text or text.startswith("+")
        return [
            CheckResult(
                id="redis.nego.ping",
                team="blue",
                passed=ok,
                detail=text[:80] if text else (err or "no pong"),
                score=100.0 if ok else 0.0,
            )
        ]

    def probe_state(
        self, host: str, port: int, target: TargetSpec, tps: Optional[TPS]
    ) -> List[CheckResult]:
        raw, _, err = _transact(
            host,
            port,
            b"SET uhbs_marker 1\r\nGET uhbs_marker\r\n",
            recv_first=False,
        )
        text = raw.decode("utf-8", "replace")
        ok = "uhbs_marker" in text or "$1" in text or "+OK" in text
        return [
            CheckResult(
                id="redis.state.set_get",
                team="blue",
                passed=ok,
                detail=text[:120] if text else (err or "fail"),
                score=100.0 if ok else 20.0,
            )
        ]
