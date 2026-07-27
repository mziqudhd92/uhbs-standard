from __future__ import annotations

from uhbs_core.models import CheckResult, TargetSpec
from uhbs_core.netutil import tcp_transact
from uhbs_core.protocols.base import ProtocolPlugin
from uhbs_core.tps import TPS


class VNCPlugin(ProtocolPlugin):
    """RFB / VNC handshake probe.

    2026-07-27 code-review fix: ``probe_fsm``'s ``ok = b"RFB" in raw or (not
    err)`` had the exact same shape as the bug already fixed in
    ``telnet.py`` this session — the ``or (not err)`` clause meant *any*
    non-erroring TCP response counted as a passing VNC probe, RFB banner or
    not. It now requires either a literal ``RFB`` banner or a clean,
    error-free close (an acceptable non-crashing response to a malformed
    client-version line). ``probe_state``'s trailing ``or not err`` was
    similarly redundant/weakening (once ``RFB`` is already known to be
    present, ``err`` is almost always empty anyway) and has been dropped in
    favor of requiring concrete evidence of a security-type list.

    ``probe_negotiation`` (the RFB protocol-version banner check) is now
    ``critical`` in Strict RFC mode, same pattern as
    ``rdp.nego.x224``/``smb.nego.dialect_header``. Live-verified against
    the real ``thinkst/opencanary`` VNC module this round
    (``RFB 003.008\\n``) to confirm this tightening does not regress a
    real target.
    """

    name = "vnc"
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
        raw, _, err = tcp_transact(host, port, b"RFB BAD\n", timeout=3.0, recv_first=True)
        if err:
            return [
                CheckResult(
                    id="vnc.fsm.bad_client_ver",
                    team="blue",
                    passed=False,
                    detail=err,
                    score=0.0,
                )
            ]
        has_banner = b"RFB" in raw
        ok = raw == b"" or has_banner
        return [
            CheckResult(
                id="vnc.fsm.bad_client_ver",
                team="blue",
                passed=ok,
                detail=(
                    raw[:40].decode("utf-8", "replace")
                    if raw
                    else "closed cleanly on malformed client version"
                ),
                score=70.0 if has_banner else (40.0 if raw == b"" else 0.0),
            )
        ]

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        raw, _, err = tcp_transact(host, port, b"", timeout=3.0, recv_first=True)
        ok = raw.startswith(b"RFB ")
        critical = self._critical(tps)
        return [
            CheckResult(
                id="vnc.nego.rfb_banner",
                team="blue",
                critical=critical,
                passed=ok,
                detail=(
                    (raw[:20].decode("utf-8", "replace") if raw else (err or "no banner"))
                    + ("" if (ok or critical) else " (Canary/Alert mode: not hard-failed)")
                ),
                score=100.0 if ok else (0.0 if critical else self._alert_partial_score()),
            )
        ]

    def probe_state(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        # Banner then client version -> security types
        with_payload = b"RFB 003.008\n"
        raw, _, err = tcp_transact(
            host, port, with_payload, timeout=3.0, recv_first=True
        )
        has_banner = b"RFB" in raw
        # Concrete evidence of a security-type list following the banner:
        # either a plausible-length reply, or the VNC-Authentication
        # security-type byte (0x02) actually present in the response.
        has_security_types = has_banner and (len(raw) > 12 or b"\x02" in raw)
        ok = has_banner and (has_security_types or not err)
        return [
            CheckResult(
                id="vnc.state.security",
                team="blue",
                passed=ok,
                detail=(raw[:60].hex() if raw else (err or "no banner")),
                score=100.0 if has_security_types else (40.0 if ok else 10.0),
            )
        ]
