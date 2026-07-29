"""DHCPv4 (BOOTP) probes — RFC 2131 / RFC 2132."""

from __future__ import annotations

import struct

from uhbs_core.models import CheckResult, TargetSpec
from uhbs_core.netutil import udp_transact
from uhbs_core.protocols.udp_base import UdpProtocolPlugin
from uhbs_core.tps import TPS

BOOTREQUEST = 1
BOOTREPLY = 2
HTYPE_ETHERNET = 1
HLEN_ETHERNET = 6
DHCP_MAGIC = b"\x63\x82\x53\x63"

OPT_PAD = 0
OPT_SUBNET_MASK = 1
OPT_ROUTER = 3
OPT_DOMAIN_NAME = 15
OPT_DHCP_MESSAGE_TYPE = 53
OPT_SERVER_IDENTIFIER = 54
OPT_PARAMETER_REQUEST = 55
OPT_MAX_MESSAGE_SIZE = 57
OPT_END = 255

MSG_DISCOVER = 1
MSG_OFFER = 2
MSG_REQUEST = 3

_FIXED_HEADER_LEN = 236

# Locally administered MAC + stable xid for repeatable probes
_PROBE_MAC = bytes([0x02, 0x55, 0x48, 0x42, 0x53, 0x01])
_PROBE_XID = 0x55484253


def _pack_options(options: list[tuple[int, bytes]]) -> bytes:
    out = bytearray(DHCP_MAGIC)
    for code, data in options:
        if not data:
            continue
        out.extend((code, len(data)))
        out.extend(data)
    out.append(OPT_END)
    return bytes(out)


def _bootp_fixed(
    *,
    op: int,
    xid: int,
    flags: int,
    client_mac: bytes,
    yiaddr: bytes = b"\x00" * 4,
    siaddr: bytes = b"\x00" * 4,
) -> bytes:
    if len(client_mac) != HLEN_ETHERNET:
        raise ValueError("client_mac must be 6 bytes")
    header = struct.pack(
        "!BBBBIHH",
        op,
        HTYPE_ETHERNET,
        HLEN_ETHERNET,
        0,
        xid & 0xFFFFFFFF,
        0,
        flags & 0xFFFF,
    )
    header += b"\x00" * 4  # ciaddr
    header += yiaddr
    header += siaddr
    header += b"\x00" * 4  # giaddr
    header += client_mac + b"\x00" * 10
    header += b"\x00" * 64  # sname
    header += b"\x00" * 128  # file
    if len(header) != _FIXED_HEADER_LEN:
        raise AssertionError("BOOTP fixed header length mismatch")
    return header


def build_dhcp_discover(
    xid: int = _PROBE_XID,
    client_mac: bytes = _PROBE_MAC,
) -> bytes:
    """RFC 2131 DHCPDISCOVER (BOOTREQUEST + option 53=Discover)."""
    header = _bootp_fixed(
        op=BOOTREQUEST,
        xid=xid,
        flags=0x8000,
        client_mac=client_mac,
    )
    opts = _pack_options(
        [
            (OPT_DHCP_MESSAGE_TYPE, bytes([MSG_DISCOVER])),
            (OPT_PARAMETER_REQUEST, bytes([OPT_SUBNET_MASK, OPT_ROUTER, OPT_DOMAIN_NAME])),
            (OPT_MAX_MESSAGE_SIZE, struct.pack("!H", 1500)),
        ]
    )
    return header + opts


def build_dhcp_offer(
    xid: int,
    client_mac: bytes,
    *,
    yiaddr: bytes = b"\xc0\xa8\x0a\x0a",
    server_id: bytes = b"\xc0\xa8\x0a\x01",
    lease_seconds: int = 3600,
) -> bytes:
    """Minimal DHCPOFFER for lab stubs / offline tests."""
    if len(yiaddr) != 4 or len(server_id) != 4:
        raise ValueError("yiaddr and server_id must be 4 bytes")
    header = _bootp_fixed(
        op=BOOTREPLY,
        xid=xid,
        flags=0x0000,
        client_mac=client_mac,
        yiaddr=yiaddr,
        siaddr=server_id,
    )
    opts = _pack_options(
        [
            (OPT_DHCP_MESSAGE_TYPE, bytes([MSG_OFFER])),
            (OPT_SERVER_IDENTIFIER, server_id),
            (1, b"\xff\xff\xff\x00"),  # subnet mask
            (51, struct.pack("!I", lease_seconds & 0xFFFFFFFF)),
        ]
    )
    return header + opts


def parse_dhcp_options(blob: bytes) -> dict[int, bytes]:
    """Parse DHCP options (with or without leading magic cookie)."""
    if blob.startswith(DHCP_MAGIC):
        blob = blob[len(DHCP_MAGIC) :]
    opts: dict[int, bytes] = {}
    i = 0
    while i < len(blob):
        code = blob[i]
        if code == OPT_PAD:
            i += 1
            continue
        if code == OPT_END:
            break
        if i + 1 >= len(blob):
            break
        length = blob[i + 1]
        i += 2
        if i + length > len(blob):
            break
        opts[code] = blob[i : i + length]
        i += length
    return opts


def dhcp_message_type(packet: bytes) -> int | None:
    if len(packet) < _FIXED_HEADER_LEN + len(DHCP_MAGIC):
        return None
    opts = parse_dhcp_options(packet[_FIXED_HEADER_LEN :])
    raw = opts.get(OPT_DHCP_MESSAGE_TYPE)
    if not raw:
        return None
    return raw[0]


def is_dhcp_offer(packet: bytes) -> bool:
    """True when datagram looks like RFC 2131 DHCPOFFER."""
    if len(packet) < _FIXED_HEADER_LEN + len(DHCP_MAGIC):
        return False
    if packet[0] != BOOTREPLY:
        return False
    if packet[_FIXED_HEADER_LEN : _FIXED_HEADER_LEN + len(DHCP_MAGIC)] != DHCP_MAGIC:
        return False
    return dhcp_message_type(packet) == MSG_OFFER


_DISCOVER = build_dhcp_discover()


class DHCPPlugin(UdpProtocolPlugin):
    """DHCPv4 (UDP 67/68) DISCOVER/OFFER probe."""

    name = "dhcp"
    families = ("it",)
    udp_probe_payload = _DISCOVER

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        garbage = b"\xff\xfe" + bytes(range(48))
        raw, _, err = udp_transact(host, port, garbage, timeout=1.5)
        ok = not err
        score = 70.0 if ok else 0.0
        return [
            CheckResult(
                id="dhcp.fsm.garbage",
                team="blue",
                passed=score >= 70.0,
                detail=(raw[:24].hex() if raw else (err or "no reply (udp accepted)")),
                score=score,
            )
        ]

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        raw, _, err = udp_transact(host, port, _DISCOVER, timeout=2.0)
        if err:
            return [
                CheckResult(
                    id="dhcp.nego.discover",
                    team="blue",
                    passed=False,
                    detail=err,
                    score=0.0,
                )
            ]
        if is_dhcp_offer(raw):
            score = 100.0
            detail = f"offer xid={struct.unpack('!I', raw[4:8])[0]:08x} yiaddr={raw[16:20].hex()}"
        else:
            score = 35.0
            detail = (
                raw[:32].hex()
                if raw
                else "no DHCPOFFER (no server or alert-only canary)"
            )
        return [
            CheckResult(
                id="dhcp.nego.discover",
                team="blue",
                passed=score >= 70.0,
                detail=detail,
                score=score,
            )
        ]
