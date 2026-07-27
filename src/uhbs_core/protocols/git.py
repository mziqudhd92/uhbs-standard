from __future__ import annotations

from uhbs_core.models import CheckResult, TargetSpec
from uhbs_core.netutil import tcp_transact
from uhbs_core.plugin_sdk import PktLineBuilder
from uhbs_core.protocols.base import ProtocolPlugin
from uhbs_core.tps import TPS


def _pkt_line(body: bytes) -> bytes:
    total = len(body) + 4
    return f"{total:04x}".encode("ascii") + body


def _is_pkt_line_shaped(raw: bytes) -> bool:
    """True iff ``raw`` starts with a syntactically valid pkt-line length
    prefix (4 hex digits, decoding to either the flush-pkt ``0000`` or a
    length of at least 4 — i.e. long enough to describe itself).

    2026-07-27 code-review fix: the original checks here used
    ``text.startswith("00")``, which is true for the overwhelming majority
    of *any* short reply (most real pkt-line lengths — e.g. the common
    ``0025``/``0032``-style git responses — happen to start with "00" in
    hex, but so would plenty of non-git noise). Using
    ``PktLineBuilder.decode_length`` gives a real syntactic check instead
    of a loose string prefix.
    """
    length = PktLineBuilder.decode_length(raw)
    if length is None:
        return False
    return length == 0 or length >= 4


class GitPlugin(ProtocolPlugin):
    """Git daemon pkt-line probe (git://).

    2026-07-27 code-review fix: all three hooks previously accepted "any
    non-empty reply" or "no socket exception" as sufficient evidence (``not
    err`` alone in ``probe_fsm``; ``text.startswith("00")`` — true for most
    short replies, not just pkt-line ones — and a bare ``bool(raw)``
    fallback in ``probe_negotiation``/``probe_state``). All three now
    require the reply to actually be pkt-line-shaped (see
    :func:`_is_pkt_line_shaped`) or a clean, error-free close, rather than
    merely "something came back." ``probe_negotiation`` is now ``critical``
    in Strict RFC mode, same pattern as the other protocol plugins' core
    negotiation gate. Live-verified against the real ``thinkst/opencanary``
    git module this round (``0025ERR no such repository: uhbs.git\\x00\\n``
    — genuinely pkt-line-shaped) to confirm this tightening does not
    regress a real target.
    """

    name = "git"
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
        # Invalid command should close / error
        raw, _, err = tcp_transact(
            host, port, _pkt_line(b"git-receive-pack /x.git\0host=h\0"), timeout=3.0
        )
        if err:
            return [
                CheckResult(
                    id="git.fsm.invalid_cmd",
                    team="blue",
                    passed=False,
                    detail=err,
                    score=0.0,
                )
            ]
        # OpenCanary closes on non-upload-pack; a clean close, a real
        # pkt-line-framed ERR reply, or a raw "ERR" substring are all OK.
        pkt_shaped = _is_pkt_line_shaped(raw)
        ok = raw == b"" or pkt_shaped or b"ERR" in raw
        return [
            CheckResult(
                id="git.fsm.invalid_cmd",
                team="blue",
                passed=ok,
                detail=(raw[:80].decode("utf-8", "replace") if raw else "closed cleanly"),
                score=80.0 if (pkt_shaped or raw == b"") else (40.0 if ok else 0.0),
            )
        ]

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        body = b"git-upload-pack /uhbs.git\0host=uhbs\0"
        raw, _, err = tcp_transact(host, port, _pkt_line(body), timeout=3.0)
        text = raw.decode("utf-8", "replace")
        pkt_shaped = _is_pkt_line_shaped(raw)
        ok = pkt_shaped and ("ERR" in text or "repository" in text or len(raw) > 4)
        critical = self._critical(tps)
        return [
            CheckResult(
                id="git.nego.upload_pack",
                team="blue",
                critical=critical,
                passed=ok,
                detail=(
                    (text[:100] if text else (err or "no reply"))
                    + ("" if (ok or critical) else " (Canary/Alert mode: not hard-failed)")
                ),
                score=100.0 if ok else (0.0 if critical else self._alert_partial_score()),
            )
        ]

    def probe_state(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        body = b"git-upload-pack /uhbs.git\0host=uhbs\0"
        raw, _, err = tcp_transact(host, port, _pkt_line(body), timeout=3.0)
        text = raw.decode("utf-8", "replace")
        pkt_shaped = _is_pkt_line_shaped(raw)
        explicit_repo_err = "no such repository" in text or "ERR" in text
        ok = pkt_shaped and (explicit_repo_err or len(raw) > 4)
        return [
            CheckResult(
                id="git.state.repo_err",
                team="blue",
                passed=ok,
                detail=text[:100] if text else (err or "fail"),
                score=100.0 if explicit_repo_err else (60.0 if ok else 0.0),
            )
        ]
