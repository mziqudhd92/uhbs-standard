from __future__ import annotations

from uhbs_core.models import CheckResult, TargetSpec
from uhbs_core.netutil import udp_transact
from uhbs_core.protocols.udp_base import UdpProtocolPlugin
from uhbs_core.tps import TPS

_TFTP_RRQ = b"\x00\x01uhbs.txt\x00octet\x00"
_TFTP_WRQ = b"\x00\x02uhbs.txt\x00octet\x00"


class TFTPPlugin(UdpProtocolPlugin):
    """TFTP (UDP) RRQ/WRQ probe."""

    name = "tftp"
    families = ("it",)
    udp_probe_payload = _TFTP_RRQ

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        raw, _, err = udp_transact(host, port, b"\x00\xff", timeout=1.5)
        ok = not err
        return [
            CheckResult(
                id="tftp.fsm.bad_opcode",
                team="blue",
                passed=ok,
                detail=(raw[:20].hex() if raw else (err or "udp accepted")),
                score=60.0 if ok else 0.0,
            )
        ]

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        raw, _, err = udp_transact(host, port, _TFTP_RRQ, timeout=1.5)
        # DATA(3) / ERROR(5) / OACK(6)
        replied = len(raw) >= 2 and raw[1] in (3, 5, 6)
        ok = not err
        return [
            CheckResult(
                id="tftp.nego.rrq",
                team="blue",
                passed=ok,
                detail=(raw[:40].hex() if raw else (err or "no TFTP reply (canary may be alert-only)")),
                score=100.0 if replied else (35.0 if ok else 0.0),
            )
        ]

    def probe_state(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        raw, _, err = udp_transact(host, port, _TFTP_WRQ, timeout=1.5)
        ok = not err
        return [
            CheckResult(
                id="tftp.state.wrq",
                team="blue",
                passed=ok,
                detail=(raw[:40].hex() if raw else (err or "wrq sent")),
                score=70.0 if ok else 0.0,
            )
        ]
