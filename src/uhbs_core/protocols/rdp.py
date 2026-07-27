from __future__ import annotations

from uhbs_core.models import CheckResult, TargetSpec
from uhbs_core.netutil import tcp_transact
from uhbs_core.protocols.base import ProtocolPlugin
from uhbs_core.tps import TPS

# Typical X.224 Connection Request (cookie) — OpenCanary replies with NLA-ish PDU
_RDP_CR = (
    b"\x03\x00\x00\x2c\x27\xe0\x00\x00\x00\x00\x00"
    b"Cookie: mstshash=uhbs\r\n"
    b"\x01\x00\x08\x00\x03\x00\x00\x00"
)

# TPKT (ITU-T T.123 / RFC 1006) version byte — every real RDP/X.224 message,
# request or reply, is wrapped in a TPKT header that starts with this byte.
_TPKT_VERSION = b"\x03\x00"


def _looks_like_tpkt(raw: bytes) -> bool:
    return raw.startswith(_TPKT_VERSION)


class RDPPlugin(ProtocolPlugin):
    """RDP / X.224 connection-request probe.

    2026-07-27 code-review fix: ``probe_fsm``'s ``ok = not err`` and
    ``probe_state``'s ``ok = bool(raw1) or bool(raw2) or not (err1 and err2)``
    were both tautologies — "the TCP connect didn't raise an exception" is
    true for almost any open port running almost anything, RDP or not. Both
    are now gated on the response actually being TPKT-shaped (the mandatory
    ``\\x03\\x00`` version-byte header every real X.224 message carries,
    request or reply — see ITU-T T.123 / RFC 1006), or on a clean
    close/no-reply (an acceptable, non-crashing response to a truncated
    frame, same pattern already used in ``smb.py``/``ftp.py``). Live-
    verified against the real ``thinkst/opencanary`` RDP module this round
    (``030000130ed000001234000209080002000000`` — genuinely TPKT-shaped) to
    confirm this tightening does not regress a real target.

    ``probe_negotiation`` (the X.224 Connection Confirm check) is now
    ``critical`` in Strict RFC mode, same rationale/pattern as
    ``smb.nego.dialect_header``/``mysql.state.auth_deny``: a target that
    cannot prove it holds a genuine RDP/X.224 stack should not have that
    fact averaged away by an unrelated passing check.
    """

    name = "rdp"
    families = ("it",)

    @staticmethod
    def _critical(tps: TPS | None) -> bool:
        return tps is None or tps.strict_rfc_enforcement

    @staticmethod
    def _alert_partial_score() -> float:
        return 35.0

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        raw, _, err = tcp_transact(host, port, b"\x03\x00\x00\x01", timeout=3.0)
        if err:
            return [
                CheckResult(
                    id="rdp.fsm.truncated",
                    team="blue",
                    passed=False,
                    detail=err,
                    score=0.0,
                )
            ]
        # A clean, error-free close/no-reply to a truncated frame is an
        # acceptable non-crashing outcome; a TPKT-shaped reply is stronger.
        ok = raw == b"" or _looks_like_tpkt(raw)
        return [
            CheckResult(
                id="rdp.fsm.truncated",
                team="blue",
                passed=ok,
                detail=(
                    (raw[:40].hex() if raw else "closed cleanly, no error")
                    if ok
                    else f"non-TPKT response to truncated frame: resp={raw[:40].hex()}"
                ),
                score=70.0 if _looks_like_tpkt(raw) else (50.0 if raw == b"" else 0.0),
            )
        ]

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        raw, _, err = tcp_transact(host, port, _RDP_CR, timeout=3.0)
        # OpenCanary: 030000130ed000001234000209080002000000
        ok = _looks_like_tpkt(raw) or b"\x0e\xd0" in raw
        critical = self._critical(tps)
        if ok:
            return [
                CheckResult(
                    id="rdp.nego.x224",
                    team="blue",
                    critical=critical,
                    passed=True,
                    detail=(raw[:40].hex() if raw else (err or "no reply")),
                    score=100.0,
                )
            ]
        return [
            CheckResult(
                id="rdp.nego.x224",
                team="blue",
                critical=critical,
                passed=False,
                detail=(
                    (raw[:40].hex() if raw else (err or "no reply"))
                    + ("" if critical else " (Canary/Alert mode: not hard-failed)")
                ),
                score=0.0 if critical else self._alert_partial_score(),
            )
        ]

    def probe_state(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        # Second exchange often yields failure / close on canaries — this
        # checks consistency (does the stack keep answering TPKT-shaped
        # replies across a second, slightly different request), not merely
        # "did a TCP error occur."
        raw1, _, err1 = tcp_transact(host, port, _RDP_CR, timeout=3.0)
        raw2, _, err2 = tcp_transact(
            host, port, _RDP_CR + b"\x00\x01\x00\x04", timeout=3.0
        )
        tpkt1, tpkt2 = _looks_like_tpkt(raw1), _looks_like_tpkt(raw2)
        ok = tpkt1 or tpkt2
        return [
            CheckResult(
                id="rdp.state.nla_fail",
                team="blue",
                passed=ok,
                detail=f"r1={raw1[:20].hex()} r2={raw2[:20].hex()} e={err1 or err2 or '-'}",
                score=80.0 if tpkt1 else (60.0 if tpkt2 else 20.0),
            )
        ]
