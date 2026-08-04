"""CoAP (RFC 7252) GET/response offline stub probes over UDP."""

from __future__ import annotations

import socket
import struct
import threading

from uhbs_core.models import TargetSpec
from uhbs_core.protocols import get_plugin
from uhbs_core.protocols.coap import CoAPPlugin, build_get, is_coap_response
from uhbs_core.tps import TPS


def test_coap_plugin_resolves_and_aliases() -> None:
    p = get_plugin("coap")
    assert isinstance(p, CoAPPlugin)
    assert p.name == "coap"
    assert get_plugin("coaps").name == "coap"


def test_build_get_is_well_formed() -> None:
    req = build_get(msg_id=0x1234)
    ver = (req[0] >> 6) & 0x03
    assert ver == 1
    assert req[1] == 0x01  # GET code
    assert struct.unpack("!H", req[2:4])[0] == 0x1234


def test_is_coap_response_accepts_valid_rejects_garbage() -> None:
    assert is_coap_response(b"\x60\x45\x12\x34") is True  # ACK, 2.05 Content
    assert is_coap_response(b"") is False
    assert is_coap_response(b"\x00") is False


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


def test_coap_probe_fsm_malformed_stub() -> None:
    """A1 — a malformed CoAP datagram must not hang the harness."""

    def handler(srv: socket.socket, data: bytes, addr) -> None:
        return  # silently ignore malformed input

    srv, host, port, stop, th = _start_udp_stub(handler)
    try:
        target = TargetSpec(
            name="coap-stub", host=host, port=port, protocol="coap", protocols=["coap"]
        )
        plugin = CoAPPlugin()
        checks = plugin.probe_fsm(host, port, target, None)
        assert checks[0].id == "coap.fsm.malformed"
        assert checks[0].passed is True
    finally:
        stop.set()
        th.join(timeout=2.0)


def test_coap_probe_negotiation_get_response_stub() -> None:
    """A2 — a confirmable GET should be met with a valid CoAP response."""

    def handler(srv: socket.socket, data: bytes, addr) -> None:
        if len(data) >= 4 and (data[0] >> 6) == 1:
            msgid = data[2:4]
            srv.sendto(b"\x60\x45" + msgid, addr)  # ACK, 2.05 Content

    srv, host, port, stop, th = _start_udp_stub(handler)
    try:
        target = TargetSpec(
            name="coap-stub", host=host, port=port, protocol="coap", protocols=["coap"]
        )
        tps = TPS(
            name="coap-stub",
            profile_class="Web-API",
            protocol="coap",
            protocols=["coap"],
        )
        plugin = CoAPPlugin()
        checks = plugin.probe_negotiation(host, port, target, tps)
        assert checks[0].id == "coap.nego.get"
        assert checks[0].passed is True
    finally:
        stop.set()
        th.join(timeout=2.0)


def test_coap_probe_state_consistent_response_codes_stub() -> None:
    """B1 — two independent GETs must yield consistent response codes."""

    def handler(srv: socket.socket, data: bytes, addr) -> None:
        if len(data) >= 4 and (data[0] >> 6) == 1:
            msgid = data[2:4]
            srv.sendto(b"\x60\x45" + msgid, addr)

    srv, host, port, stop, th = _start_udp_stub(handler)
    try:
        target = TargetSpec(
            name="coap-stub", host=host, port=port, protocol="coap", protocols=["coap"]
        )
        tps = TPS(
            name="coap-stub",
            profile_class="Web-API",
            protocol="coap",
            protocols=["coap"],
        )
        plugin = CoAPPlugin()
        checks = plugin.probe_state(host, port, target, tps)
        assert checks[0].id == "coap.state.get_consistent"
        assert checks[0].passed is True
        assert checks[0].critical is True
    finally:
        stop.set()
        th.join(timeout=2.0)


def test_coap_probe_negotiation_fails_on_silence() -> None:
    def handler(srv: socket.socket, data: bytes, addr) -> None:
        return  # never reply

    srv, host, port, stop, th = _start_udp_stub(handler)
    try:
        target = TargetSpec(
            name="coap-stub", host=host, port=port, protocol="coap", protocols=["coap"]
        )
        tps = TPS(
            name="coap-stub",
            profile_class="Web-API",
            protocol="coap",
            protocols=["coap"],
            raw={"performance_baseline": {"probe_timeout_sec": 0.3}},
        )
        plugin = CoAPPlugin()
        checks = plugin.probe_negotiation(host, port, target, tps)
        assert checks[0].passed is False
    finally:
        stop.set()
        th.join(timeout=2.0)
