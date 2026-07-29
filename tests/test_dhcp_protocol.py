"""DHCPv4 plugin — offline framing + local UDP stub."""

from __future__ import annotations

import socket
import struct
import threading

from uhbs_core.models import TargetSpec
from uhbs_core.protocols import get_plugin, register
from uhbs_core.protocols.dhcp import (
    BOOTREQUEST,
    MSG_DISCOVER,
    MSG_OFFER,
    DHCPPlugin,
    build_dhcp_discover,
    build_dhcp_offer,
    dhcp_message_type,
    is_dhcp_offer,
    parse_dhcp_options,
)

register(DHCPPlugin())


def test_dhcp_plugin_resolves() -> None:
    p = get_plugin("dhcp")
    assert isinstance(p, DHCPPlugin)
    assert p.name == "dhcp"


def test_dhcp_unreachable_does_not_raise() -> None:
    target = TargetSpec(
        name="x",
        host="127.0.0.1",
        port=1,
        protocol="dhcp",
        protocols=["dhcp"],
    )
    plugin = get_plugin("dhcp")
    fsm = plugin.probe_fsm("127.0.0.1", 1, target, None)
    nego = plugin.probe_negotiation("127.0.0.1", 1, target, None)
    assert isinstance(fsm, list) and fsm
    assert isinstance(nego, list) and nego
    assert fsm[0].id == "dhcp.fsm.garbage"
    assert nego[0].id == "dhcp.nego.discover"


def test_dhcp_discover_and_offer_framing_offline() -> None:
    mac = bytes([0x02, 0x11, 0x22, 0x33, 0x44, 0x55])
    xid = 0xAABBCCDD
    discover = build_dhcp_discover(xid=xid, client_mac=mac)
    assert len(discover) > 236
    assert discover[0] == BOOTREQUEST
    assert struct.unpack("!I", discover[4:8])[0] == xid
    assert discover[28:34] == mac
    assert discover[236:240] == b"\x63\x82\x53\x63"
    opts = parse_dhcp_options(discover[236:])
    assert opts[53] == bytes([MSG_DISCOVER])

    offer = build_dhcp_offer(xid, mac)
    assert is_dhcp_offer(offer)
    assert dhcp_message_type(offer) == MSG_OFFER
    assert struct.unpack("!I", offer[4:8])[0] == xid
    assert offer[28:34] == mac
    offer_opts = parse_dhcp_options(offer[236:])
    assert offer_opts[53] == bytes([MSG_OFFER])
    assert offer_opts[54] == b"\xc0\xa8\x0a\x01"


def _serve_dhcp_offer() -> tuple[str, int, threading.Event, socket.socket]:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("127.0.0.1", 0))
    host, port = sock.getsockname()
    stop = threading.Event()

    def _loop() -> None:
        sock.settimeout(0.5)
        while not stop.is_set():
            try:
                data, addr = sock.recvfrom(65535)
            except TimeoutError:
                continue
            if len(data) < 236 or data[0] != BOOTREQUEST:
                continue
            if dhcp_message_type(data) != MSG_DISCOVER:
                continue
            xid = struct.unpack("!I", data[4:8])[0]
            mac = data[28:34]
            reply = build_dhcp_offer(xid, mac)
            sock.sendto(reply, addr)

    threading.Thread(target=_loop, daemon=True).start()
    return host, port, stop, sock


def test_dhcp_plugin_against_offer_stub() -> None:
    host, port, stop, sock = _serve_dhcp_offer()
    try:
        target = TargetSpec(
            name="dhcp-stub",
            host=host,
            port=port,
            protocol="dhcp",
            protocols=["dhcp"],
        )
        plugin = DHCPPlugin()
        fsm = plugin.probe_fsm(host, port, target, None)
        assert fsm[0].passed is True

        nego = plugin.probe_negotiation(host, port, target, None)
        assert nego[0].id == "dhcp.nego.discover"
        assert nego[0].passed is True
        assert nego[0].score >= 70.0
        assert "offer" in nego[0].detail.lower()
    finally:
        stop.set()
        sock.close()
