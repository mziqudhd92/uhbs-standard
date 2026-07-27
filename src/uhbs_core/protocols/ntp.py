from __future__ import annotations

from uhbs_core.models import CheckResult, TargetSpec
from uhbs_core.netutil import udp_transact
from uhbs_core.protocols.udp_base import UdpProtocolPlugin
from uhbs_core.tps import TPS

# NTP client mode (version 3) — 48-byte packet
_NTP_CLIENT = bytes([0x1B]) + bytes(47)
# OpenCanary monlist trigger: byte index 3 == 0x2a
_NTP_MONLIST = bytes([0x17, 0x00, 0x03, 0x2A]) + bytes(44)


class NTPPlugin(UdpProtocolPlugin):
    """NTP (UDP) client / monlist probe."""

    name = "ntp"
    families = ("it",)
    udp_probe_payload = _NTP_CLIENT

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        raw, _, err = udp_transact(host, port, b"\x00\x01", timeout=1.5)
        ok = not err
        return [
            CheckResult(
                id="ntp.fsm.short",
                team="blue",
                passed=ok,
                detail=(raw[:20].hex() if raw else (err or "udp accepted")),
                score=60.0 if ok else 0.0,
            )
        ]

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        raw, _, err = udp_transact(host, port, _NTP_CLIENT, timeout=1.5)
        replied = len(raw) >= 48
        ok = not err
        return [
            CheckResult(
                id="ntp.nego.client",
                team="blue",
                passed=ok,
                detail=(raw[:16].hex() if raw else (err or "no NTP reply (canary may be alert-only)")),
                score=100.0 if replied else (35.0 if ok else 0.0),
            )
        ]

    def probe_state(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        raw, _, err = udp_transact(host, port, _NTP_MONLIST, timeout=1.5)
        ok = not err
        return [
            CheckResult(
                id="ntp.state.monlist",
                team="red",
                passed=ok,
                detail=(raw[:20].hex() if raw else (err or "monlist sent (alert-only OK)")),
                score=70.0 if ok else 0.0,
            )
        ]
