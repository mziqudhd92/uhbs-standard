from __future__ import annotations

from uhbs_core.protocols.base import ProtocolPlugin

from ..models import CheckResult, TargetSpec
from ..rfc_probes import _transact
from ..tps import TPS


class RedisPlugin(ProtocolPlugin):
    name = "redis"
    families = ("it", "database")

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        """A1 — an unknown/invalid RESP verb must be rejected with a real
        RESP error reply (``-ERR ...``), not silently accepted or echoed.

        Architecture note (2026-07-27 review): the previous version set
        ``passed=True`` for several reply shapes (``-``, ``+``, empty,
        ``*``) but only ever assigned ``score=100`` for the ``-ERR`` case —
        every other "passing" shape scored 40. A boolean that says "pass"
        while the number says "40/100" is a contract violation for anything
        consuming this data downstream (dashboards, other agents, CI
        gates). ``passed`` is now derived directly from the score band
        (``passed = score >= 70``) so the two can never disagree.
        """
        raw, _, err = _transact(host, port, b"Garbage\r\n", recv_first=False)
        text = raw.decode("utf-8", "replace")
        is_resp_error = text.startswith("-") or "ERR" in text
        closed_cleanly = raw == b"" or bool(err)
        if is_resp_error:
            score = 100.0
            detail = text[:120]
        elif closed_cleanly:
            score = 60.0  # didn't crash/hang, but also didn't emit a real RESP error
            detail = err or "connection closed on invalid verb (no RESP error emitted)"
        else:
            score = 20.0  # replied, but not with a real RESP error — weak fidelity
            detail = text[:120]
        return [
            CheckResult(
                id="redis.fsm.invalid_verb",
                team="blue",
                passed=score >= 70.0,
                detail=detail,
                score=score,
            )
        ]

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
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
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
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
