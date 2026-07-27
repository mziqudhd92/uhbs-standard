from __future__ import annotations

import socket

from uhbs_core.protocols.base import ProtocolPlugin

from ..models import CheckResult, TargetSpec
from ..rfc_probes import _transact
from ..tps import TPS


def _recv_line(s: socket.socket, timeout: float = 2.0) -> str:
    s.settimeout(timeout)
    try:
        return s.recv(512).decode("utf-8", "replace")
    except TimeoutError:
        return ""


class FTPPlugin(ProtocolPlugin):
    """RFC 959 FTP control-channel probe.

    Named-state sequence (FSM formalization, architecture review round 2,
    item 3) — a documented, fail-fast sequential pattern, deliberately
    *not* a generic state-machine engine, spread across this plugin's
    three ``ProtocolPlugin`` hooks (the harness invokes A1/A2/B1 as
    independent probes, each on its own connection):

        Connect -> Banner(220)                    [probe_negotiation, A2]
                -> Unauthenticated RETR rejected    [probe_fsm, A1 — critical]
                -> USER -> PASS -> PWD               [probe_state, B1]

    Within ``probe_state`` the USER -> PASS -> PWD sub-sequence walks ONE
    connection step by step with an explicit expected-reply-code check and
    an early return on the first mismatch, rather than firing all three
    commands blind and grepping the combined output for "230 or 331
    anywhere" (which could false-positive on a coincidental substring
    match in an unrelated banner line).
    """

    name = "ftp"
    families = ("it",)

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        """A1 — unauthenticated ``RETR`` must be rejected (530/503/550).

        Marked ``critical=True`` (architecture review, 2026-07-27): this is
        the canonical FTP security gate — a canary that lets an
        unauthenticated client pull files is a real fidelity/security
        failure and must not be averaged away by unrelated passing checks
        (e.g. a correct banner) elsewhere in Module A.
        """
        raw, _, err = _transact(host, port, b"RETR secret\r\nQUIT\r\n", recv_first=True)
        text = raw.decode("utf-8", "replace")
        ok = "530" in text or "503" in text or "550" in text
        return [
            CheckResult(
                id="ftp.fsm.retr_before_auth",
                team="blue",
                critical=True,
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
        """FSM steps: USER -> PASS -> PWD, one connection, fail-fast.

        Each step is checked against its RFC 959-mandated reply code
        before proceeding to the next; the first step that doesn't match
        short-circuits the whole check with a detail string naming which
        step failed (rather than reporting only a final pass/fail).
        """
        try:
            with socket.create_connection((host, port), timeout=3.0) as s:
                _recv_line(s)  # 220 banner — already covered by probe_negotiation

                s.sendall(b"USER anonymous\r\n")
                user_resp = _recv_line(s)
                if "230" in user_resp:
                    # Some canaries log in anonymous users without a
                    # password prompt at all — treat as an accelerated
                    # PASS step rather than a failure of this one.
                    pass_resp = user_resp
                elif "331" in user_resp:
                    s.sendall(b"PASS guest@\r\n")
                    pass_resp = _recv_line(s)
                    if "230" not in pass_resp:
                        return [
                            CheckResult(
                                id="ftp.state.login_pwd",
                                team="blue",
                                passed=False,
                                detail=f"PASS step failed: {pass_resp[:120] or 'no response'}",
                                score=30.0,
                            )
                        ]
                else:
                    return [
                        CheckResult(
                            id="ftp.state.login_pwd",
                            team="blue",
                            passed=False,
                            detail=f"USER step failed: {user_resp[:120] or 'no response'}",
                            score=30.0,
                        )
                    ]

                s.sendall(b"PWD\r\n")
                pwd_resp = _recv_line(s)
                s.sendall(b"QUIT\r\n")
                ok = "257" in pwd_resp
                return [
                    CheckResult(
                        id="ftp.state.login_pwd",
                        team="blue",
                        passed=ok,
                        detail=(
                            f"USER={user_resp.strip()[:60]!r} PASS={pass_resp.strip()[:60]!r} "
                            f"PWD={pwd_resp.strip()[:60]!r}"
                        ),
                        score=100.0 if ok else 60.0,  # login worked; PWD step is a lesser signal
                    )
                ]
        except OSError as exc:
            return [
                CheckResult(
                    id="ftp.state.login_pwd",
                    team="blue",
                    passed=False,
                    detail=str(exc),
                    score=0.0,
                )
            ]
