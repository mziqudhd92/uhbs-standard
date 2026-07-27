from __future__ import annotations

from uhbs_core.models import CheckResult, TargetSpec
from uhbs_core.netutil import tcp_transact
from uhbs_core.protocols.base import ProtocolPlugin
from uhbs_core.tps import TPS


class MySQLPlugin(ProtocolPlugin):
    """MySQL wire protocol (handshake / auth deny)."""

    name = "mysql"
    families = ("it", "database")

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        # Truncated/garbage client packet after greeting
        raw, _, err = tcp_transact(
            host, port, b"\x01\x00\x00\x01\xff", timeout=3.0, recv_first=True
        )
        # Surviving without hang is enough for FSM trunc
        ok = bool(raw) or not err
        return [
            CheckResult(
                id="mysql.fsm.truncated_auth",
                team="blue",
                passed=ok,
                detail=(raw[:80].hex() if raw else (err or "closed")),
                score=80.0 if ok else 0.0,
            )
        ]

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        raw, _, err = tcp_transact(host, port, b"", timeout=3.0, recv_first=True)
        # Handshake starts with protocol version 0x0a in payload after 4-byte hdr
        # 2026-07-27 code-review fix: both banner substrings are now checked
        # case-insensitively (previously "MariaDB" was checked against the
        # raw, non-lowered bytes, so a lowercase "mariadb" banner variant
        # would have been missed).
        ok = len(raw) >= 5 and (
            raw[4] == 0x0A or b"mysql" in raw.lower() or b"mariadb" in raw.lower()
        )
        return [
            CheckResult(
                id="mysql.nego.handshake",
                team="blue",
                passed=ok,
                detail=(raw[5:40].decode("utf-8", "replace") if len(raw) > 5 else (err or "no greeting")),
                score=100.0 if ok else 0.0,
            )
        ]

    def probe_state(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        """B1 — after the handshake, an unrecognized user must be denied.

        Marked ``critical`` in Strict RFC mode (architecture review,
        2026-07-27): same rationale as FTP's ``retr_before_auth`` — auth
        rejection is a security gate, not a cosmetic behavioral nuance.

        Dual-engine evaluation mode (round 2, item 1): in Canary/Alert mode
        (``tps.strict_rfc_enforcement=False``) a low-interaction canary that
        doesn't implement a real auth-deny error packet is not treated as a
        hard-failed security gate — it's scored as non-critical partial
        credit instead, same pattern as ``smb.py``/``telnet.py``.
        """
        strict = tps is None or tps.strict_rfc_enforcement
        greeting, _, err = tcp_transact(host, port, b"", timeout=3.0, recv_first=True)
        if err and not greeting:
            return [
                CheckResult(
                    id="mysql.state.auth_deny",
                    team="blue",
                    critical=strict,
                    passed=False,
                    detail=err,
                    score=0.0 if strict else 35.0,
                )
            ]
        # Capability flags + max packet + charset + reserved + user\0
        user = b"uhbs\x00"
        auth = (
            b"\x85\xa2\x1a\x00"  # client caps (approx)
            + b"\x00\x00\x00\x01"  # max packet
            + b"\x21"  # charset
            + (b"\x00" * 23)
            + user
            + b"\x00"  # empty password len
        )
        pkt = len(auth).to_bytes(3, "little") + b"\x01" + auth
        raw, _, err2 = tcp_transact(host, port, pkt, timeout=3.0, recv_first=True)
        text = raw.decode("utf-8", "replace")
        # ERR packet: header + 0xff
        denied = (len(raw) > 4 and raw[4] == 0xFF) or b"Access denied" in raw or b"28000" in raw
        return [
            CheckResult(
                id="mysql.state.auth_deny",
                team="blue",
                critical=strict,
                passed=denied,
                detail=(
                    (text[:120] if text else (err2 or f"greet={len(greeting)}"))
                    + ("" if (denied or strict) else " (Canary/Alert mode: not hard-failed)")
                ),
                score=100.0 if denied else (0.0 if strict else 35.0),
            )
        ]
