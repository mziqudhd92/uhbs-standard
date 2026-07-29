from __future__ import annotations

import re

from uhbs_core.protocols.base import ProtocolPlugin

from ..models import CheckResult, TargetSpec
from ..rfc_probes import RFCSuiteResult, _port_open, _transact
from ..tps import TPS

_IMAP_TAGGED = re.compile(rb"(?m)^(\S+) (OK|NO|BAD)\b")
_IMAP_UNTAGGED_OK = re.compile(rb"(?m)^\* OK\b")


def _imap_tagged_codes(data: bytes) -> list[str]:
    return [m.group(2).decode("ascii") for m in _IMAP_TAGGED.finditer(data)]


def _imap_greeting_ok(data: bytes) -> bool:
    return bool(_IMAP_UNTAGGED_OK.search(data))


def probe_imap_rfc3501(host: str, port: int) -> RFCSuiteResult:
    """RFC 3501 / 9051 IMAP4 — greeting, CAPABILITY, auth-gated verbs, BAD/NO on errors."""
    suite = RFCSuiteResult(protocol="imap", rfc="RFC 3501 / RFC 9051")
    if not _port_open(host, port):
        suite.skipped = True
        suite.skip_reason = f"imap port {port} closed"
        return suite

    greet, _, err = _transact(host, port, b"", recv_first=True)
    greet_ok = _imap_greeting_ok(greet)
    suite.checks.append(
        CheckResult(
            id="rfc3501.greeting_ok",
            team="blue",
            passed=greet_ok,
            detail=(greet[:160].decode("utf-8", "replace") if greet else err or "no greeting"),
            score=100.0 if greet_ok else 0.0,
        )
    )

    script = b"A001 CAPABILITY\r\nA002 LOGOUT\r\n"
    raw, _, err = _transact(host, port, script, recv_first=True)
    text = raw.decode("utf-8", "replace")
    tagged = _imap_tagged_codes(raw)
    capa_ok = _imap_greeting_ok(raw) and bool(
        re.search(r"(?mi)^\* CAPABILITY\b", text) or re.search(r"IMAP4", text, re.I)
    )
    capa_tag_ok = "OK" in tagged
    capa_pass = capa_ok and capa_tag_ok
    suite.checks.append(
        CheckResult(
            id="rfc3501.capability",
            team="blue",
            passed=capa_pass,
            detail=(
                "untagged CAPABILITY + tagged OK"
                if capa_pass
                else f"capa_ok={capa_ok} tagged={tagged}"
            ),
            score=100.0 if capa_pass else (40.0 if capa_ok or capa_tag_ok else 0.0),
            evidence=[text[:400]],
        )
    )

    script = b"A001 SELECT INBOX\r\nA002 LOGOUT\r\n"
    raw, _, err = _transact(host, port, script, recv_first=True)
    tagged = _imap_tagged_codes(raw)
    preauth_select = "NO" in tagged or "BAD" in tagged
    closed = raw == b"" and bool(err)
    preauth_pass = preauth_select or closed
    score = 100.0 if preauth_select else (60.0 if closed else 0.0)
    suite.checks.append(
        CheckResult(
            id="rfc3501.preauth_select",
            team="blue",
            passed=score >= 70.0,
            detail=(
                "SELECT rejected before auth (NO/BAD or close)"
                if preauth_pass
                else f"tagged={tagged}"
            ),
            score=score,
            evidence=[raw[:300].decode("utf-8", "replace")],
        )
    )

    script = b"A001 FETCH 1 (FLAGS)\r\nA002 LOGOUT\r\n"
    raw, _, err = _transact(host, port, script, recv_first=True)
    tagged = _imap_tagged_codes(raw)
    preauth_fetch = "NO" in tagged or "BAD" in tagged
    closed = raw == b"" and bool(err)
    preauth_fetch_pass = preauth_fetch or closed
    score = 100.0 if preauth_fetch else (60.0 if closed else 0.0)
    suite.checks.append(
        CheckResult(
            id="rfc3501.preauth_fetch",
            team="blue",
            passed=score >= 70.0,
            detail=(
                "FETCH rejected before SELECT/auth (NO/BAD or close)"
                if preauth_fetch_pass
                else f"tagged={tagged}"
            ),
            score=score,
        )
    )

    script = b"A001 FOOBAR\r\nA002 LOGOUT\r\n"
    raw, _, err = _transact(host, port, script, recv_first=True)
    tagged = _imap_tagged_codes(raw)
    unknown_ok = "BAD" in tagged or "NO" in tagged
    closed = raw == b"" and bool(err)
    unknown_pass = unknown_ok or closed
    score = 100.0 if unknown_ok else (60.0 if closed else 20.0)
    suite.checks.append(
        CheckResult(
            id="rfc3501.unknown_command",
            team="blue",
            passed=score >= 70.0,
            detail=(
                "unknown verb → BAD/NO or close"
                if unknown_pass
                else f"tagged={tagged}"
            ),
            score=score,
        )
    )

    return suite


class IMAPPlugin(ProtocolPlugin):
    """RFC 3501 / 9051 IMAP4 — tagged commands, untagged OK greeting, CAPABILITY."""

    name = "imap"
    families = ("it", "mail")

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        suite = probe_imap_rfc3501(host, port)
        if suite.skipped:
            return [
                CheckResult(
                    id="imap.fsm.skipped",
                    team="blue",
                    passed=False,
                    detail=suite.skip_reason,
                    score=0.0,
                )
            ]
        return [
            c
            for c in suite.checks
            if "preauth" in c.id or "unknown" in c.id
        ]

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        suite = probe_imap_rfc3501(host, port)
        if suite.skipped:
            return [
                CheckResult(
                    id="imap.nego.skipped",
                    team="blue",
                    passed=False,
                    detail=suite.skip_reason,
                    score=0.0,
                )
            ]
        return [c for c in suite.checks if "greeting" in c.id or "capability" in c.id]

    def probe_state(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        user = (target.user or "uhbs").replace("\\", "\\\\").replace('"', '\\"')
        password = (target.password or "uhbs").replace("\\", "\\\\").replace('"', '\\"')
        # LOGIN — document auth gate: invalid creds must not yield tagged OK LOGIN.
        script = (
            f'A001 LOGIN "{user}" "{password}"\r\n'
            f"A002 CAPABILITY\r\n"
            f"A003 LOGOUT\r\n"
        ).encode("ascii", "replace")
        raw, _, err = _transact(host, port, script, recv_first=True)
        text = raw.decode("utf-8", "replace")
        login_m = re.search(r"(?m)^A001 (OK|NO|BAD)\b", text)
        if login_m:
            code = login_m.group(1)
            score = 100.0
            if code == "OK":
                detail = "LOGIN tagged OK (auth transition)"
            else:
                detail = f"LOGIN auth gate: tagged {code}"
            passed = True
        elif raw == b"" and err:
            score = 70.0
            passed = True
            detail = "connection closed on LOGIN (auth gate)"
        else:
            score = 30.0
            passed = False
            detail = text[:120] if text else (err or "no tagged LOGIN response")
        return [
            CheckResult(
                id="imap.state.login_gate",
                team="blue",
                passed=passed and score >= 70.0,
                detail=detail,
                score=score,
                evidence=[text[:400]] if text else [],
            )
        ]
