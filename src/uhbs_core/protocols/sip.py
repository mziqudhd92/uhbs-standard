from __future__ import annotations

from uhbs_core.models import CheckResult, TargetSpec
from uhbs_core.netutil import udp_transact
from uhbs_core.protocols.udp_base import UdpProtocolPlugin
from uhbs_core.tps import TPS

_SIP_OPTIONS = (
    b"OPTIONS sip:uhbs@127.0.0.1 SIP/2.0\r\n"
    b"Via: SIP/2.0/UDP 127.0.0.1:5060;branch=z9hG4bK-uhbs\r\n"
    b"From: <sip:uhbs@127.0.0.1>;tag=uhbs\r\n"
    b"To: <sip:uhbs@127.0.0.1>\r\n"
    b"Call-ID: uhbs@127.0.0.1\r\n"
    b"CSeq: 1 OPTIONS\r\n"
    b"Contact: <sip:uhbs@127.0.0.1>\r\n"
    b"Max-Forwards: 70\r\n"
    b"Content-Length: 0\r\n"
    b"\r\n"
)


class SIPPlugin(UdpProtocolPlugin):
    """SIP (UDP) OPTIONS / INVITE probe."""

    name = "sip"
    families = ("it", "voip")
    udp_probe_payload = _SIP_OPTIONS

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        raw, _, err = udp_transact(host, port, b"NOTSIP garbage\r\n\r\n", timeout=1.5)
        # Accept silence (alert-only canaries) or SIP error
        ok = not err
        replied = b"SIP/2.0" in raw
        return [
            CheckResult(
                id="sip.fsm.invalid",
                team="blue",
                passed=ok,
                detail=(raw[:80].decode("utf-8", "replace") if raw else (err or "no reply (udp accepted)")),
                score=100.0 if replied else (60.0 if ok else 0.0),
            )
        ]

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        raw, _, err = udp_transact(host, port, _SIP_OPTIONS, timeout=1.5)
        replied = b"SIP/2.0" in raw
        ok = not err
        return [
            CheckResult(
                id="sip.nego.options",
                team="blue",
                passed=ok,
                detail=(raw[:100].decode("utf-8", "replace") if raw else (err or "no SIP reply (canary may be alert-only)")),
                score=100.0 if replied else (35.0 if ok else 0.0),
            )
        ]
