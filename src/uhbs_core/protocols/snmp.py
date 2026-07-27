from __future__ import annotations

from uhbs_core.models import CheckResult, TargetSpec
from uhbs_core.netutil import udp_transact
from uhbs_core.protocols.udp_base import UdpProtocolPlugin
from uhbs_core.tps import TPS

# Minimal SNMPv1 GET for sysDescr.0 (community public) — BER-encoded.
# Hand-rolled fallback bytes (used whenever scapy is unavailable / raises).
_SNMP_GET_HANDROLLED = bytes.fromhex(
    "302602010004067075626c6963a01902040a0b0c0d020100020100300e300c06082b060102010101000500"
)

# --- Optional scapy-backed encoding (architecture review round 2, item 4) --
#
# scapy has zero required transitive dependencies (verified: scapy==2.7.0
# installs nothing else), so it's low-risk to offer, but it is an OPTIONAL
# extra (`pip install uhbs[scapy]`), NOT a hard dependency of this package
# or its Docker images — mirrors the same "optional extra" pattern
# OpenCanary itself uses for its own SNMP module. If scapy isn't installed,
# or its SNMP layer raises for any reason, this plugin transparently falls
# back to the pre-existing hand-rolled BER bytes above; either path
# produces a standards-shaped SNMPv1 GET request, so plugin behavior is
# unaffected either way.
try:
    from scapy.asn1.asn1 import ASN1_OID
    from scapy.layers.snmp import SNMP, SNMPget, SNMPvarbind

    _HAVE_SCAPY = True
except ImportError:  # pragma: no cover — exercised only when scapy is absent
    _HAVE_SCAPY = False


def _build_snmp_get() -> bytes:
    """SNMPv1 GET for sysDescr.0 (community 'public'), scapy-backed with
    a hand-rolled-bytes fallback (see module docstring above)."""
    if _HAVE_SCAPY:
        try:
            pkt = SNMP(
                community=b"public",
                PDU=SNMPget(varbindlist=[SNMPvarbind(oid=ASN1_OID("1.3.6.1.2.1.1.1.0"))]),
            )
            return bytes(pkt)
        except Exception:  # noqa: BLE001 — any scapy surprise, use the known-good fallback
            pass
    return _SNMP_GET_HANDROLLED


_SNMP_GET = _build_snmp_get()


class SNMPPlugin(UdpProtocolPlugin):
    """SNMP (UDP) GET probe."""

    name = "snmp"
    families = ("it", "ot")
    udp_probe_payload = _SNMP_GET

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        raw, _, err = udp_transact(host, port, b"\x30\x00", timeout=1.5)
        ok = not err
        return [
            CheckResult(
                id="snmp.fsm.truncated",
                team="blue",
                passed=ok,
                detail=(raw[:40].hex() if raw else (err or "no reply (udp accepted)")),
                score=70.0 if ok else 0.0,
            )
        ]

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        raw, _, err = udp_transact(host, port, _SNMP_GET, timeout=1.5)
        # Response typically starts with SEQUENCE 0x30
        replied = len(raw) >= 2 and raw[0] == 0x30
        ok = not err
        return [
            CheckResult(
                id="snmp.nego.get",
                team="blue",
                passed=ok,
                detail=(raw[:40].hex() if raw else (err or "no SNMP reply (canary may be alert-only)")),
                score=100.0 if replied else (35.0 if ok else 0.0),
            )
        ]
