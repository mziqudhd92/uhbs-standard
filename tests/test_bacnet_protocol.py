"""BACnet/IP (BVLC) Who-Is/I-Am offline stub probes."""

from __future__ import annotations

import socket
import threading

from uhbs_core.models import TargetSpec
from uhbs_core.protocols import get_plugin
from uhbs_core.protocols.bacnet import BACnetPlugin, build_bvlc_who_is, is_bvlc_iam
from uhbs_core.tps import TPS


def test_bacnet_plugin_resolves_and_aliases() -> None:
    p = get_plugin("bacnet")
    assert isinstance(p, BACnetPlugin)
    assert p.name == "bacnet"
    for alias in ("bacnet/ip", "bacnet-ip"):
        assert get_plugin(alias).name == "bacnet"


def test_bvlc_who_is_framing() -> None:
    who_is = build_bvlc_who_is()
    assert who_is[0] == 0x81  # BVLC type
    assert who_is[1] == 0x0B  # Original-Broadcast-NPDU


def test_is_bvlc_iam_rejects_non_bvlc_bytes() -> None:
    assert is_bvlc_iam(b"HTTP/1.1 200 OK\r\n") is False
    assert is_bvlc_iam(b"") is False


def _start_udp_stub(handler) -> tuple[socket.socket, str, int, threading.Event, threading.Thread]:
    srv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    srv.bind(("127.0.0.1", 0))
    host, port = srv.getsockname()
    stop = threading.Event()

    def _loop() -> None:
        srv.settimeout(0.5)
        while not stop.is_set():
            try:
                data, addr = srv.recvfrom(1024)
            except TimeoutError:
                continue
            handler(srv, data, addr)
        srv.close()

    th = threading.Thread(target=_loop, daemon=True)
    th.start()
    return srv, host, port, stop, th


def test_bacnet_probe_fsm_illegal_bvlc_stub() -> None:
    """A1 — an invalid/truncated BVLC function must not hang the harness."""

    def handler(srv: socket.socket, data: bytes, addr) -> None:
        # Never reply to garbage — canary is expected to ignore or close.
        return

    srv, host, port, stop, th = _start_udp_stub(handler)
    try:
        target = TargetSpec(
            name="bacnet-stub", host=host, port=port, protocol="bacnet", protocols=["bacnet"]
        )
        plugin = BACnetPlugin()
        checks = plugin.probe_fsm(host, port, target, None)
        assert checks[0].id == "bacnet.fsm.invalid_bvlc"
        assert checks[0].passed is True
    finally:
        stop.set()
        th.join(timeout=2.0)


def test_bacnet_probe_negotiation_who_is_i_am_stub() -> None:
    """A2 — Who-Is should be met with a BVLC I-Am-style reply."""

    def handler(srv: socket.socket, data: bytes, addr) -> None:
        if data.startswith(b"\x81\x0b"):
            # Minimal BVLC Original-Unicast-NPDU carrying an I-Am APDU (service 0x00).
            srv.sendto(b"\x81\x0a\x00\x08\x01\x00\x10\x00", addr)

    srv, host, port, stop, th = _start_udp_stub(handler)
    try:
        target = TargetSpec(
            name="bacnet-stub", host=host, port=port, protocol="bacnet", protocols=["bacnet"]
        )
        tps = TPS(
            name="bacnet-stub",
            profile_class="ICS-SCADA",
            protocol="bacnet",
            protocols=["bacnet"],
        )
        plugin = BACnetPlugin()
        checks = plugin.probe_negotiation(host, port, target, tps)
        assert checks[0].id == "bacnet.nego.who_is_iam"
        assert checks[0].passed is True
    finally:
        stop.set()
        th.join(timeout=2.0)


def test_bacnet_probe_state_critical_consistency_check_stub() -> None:
    """B1 — state gate: repeated Who-Is rounds must yield consistent BVLC replies.

    This check is ``critical`` — an inconsistent (or missing) reply pattern
    hard-fails the aggregate check-list score rather than being diluted by
    unrelated passing checks (mirrors the Modbus/S7comm data-integrity gates).
    """

    def handler(srv: socket.socket, data: bytes, addr) -> None:
        if data.startswith(b"\x81\x0b"):
            srv.sendto(b"\x81\x0a\x00\x08\x01\x00\x10\x00", addr)

    srv, host, port, stop, th = _start_udp_stub(handler)
    try:
        target = TargetSpec(
            name="bacnet-stub", host=host, port=port, protocol="bacnet", protocols=["bacnet"]
        )
        tps = TPS(
            name="bacnet-stub",
            profile_class="ICS-SCADA",
            protocol="bacnet",
            protocols=["bacnet"],
        )
        plugin = BACnetPlugin()
        checks = plugin.probe_state(host, port, target, tps)
        assert checks[0].id == "bacnet.state.who_is_consistent"
        assert checks[0].passed is True
        assert checks[0].critical is True
    finally:
        stop.set()
        th.join(timeout=2.0)


def test_bacnet_probe_state_critical_fails_on_silence() -> None:
    """The critical gate must actually fail (not soft-pass) when nothing replies."""

    def handler(srv: socket.socket, data: bytes, addr) -> None:
        return  # never reply

    srv, host, port, stop, th = _start_udp_stub(handler)
    try:
        target = TargetSpec(
            name="bacnet-stub", host=host, port=port, protocol="bacnet", protocols=["bacnet"]
        )
        tps = TPS(
            name="bacnet-stub",
            profile_class="ICS-SCADA",
            protocol="bacnet",
            protocols=["bacnet"],
            raw={"performance_baseline": {"probe_timeout_sec": 0.3}},
        )
        plugin = BACnetPlugin()
        checks = plugin.probe_state(host, port, target, tps)
        assert checks[0].passed is False
        assert checks[0].critical is True
    finally:
        stop.set()
        th.join(timeout=2.0)
