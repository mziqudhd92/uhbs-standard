"""BACnet / MQTT / CoAP offline stub probes."""

from __future__ import annotations

import socket
import struct
import threading

from uhbs_core.models import TargetSpec
from uhbs_core.protocols import get_plugin
from uhbs_core.protocols.bacnet import BACnetPlugin, build_bvlc_who_is
from uhbs_core.protocols.coap import CoAPPlugin, build_get, is_coap_response
from uhbs_core.protocols.mqtt import MQTTPlugin, build_connect, is_connack
from uhbs_core.tps import TPS


def test_plugin_aliases() -> None:
    assert isinstance(get_plugin("bacnet"), BACnetPlugin)
    assert isinstance(get_plugin("mqtt"), MQTTPlugin)
    assert isinstance(get_plugin("coap"), CoAPPlugin)
    assert get_plugin("bacnet-ip").name == "bacnet"
    assert get_plugin("mqtts").name == "mqtt"


def test_mqtt_against_stub() -> None:
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 0))
    srv.listen(8)
    host, port = srv.getsockname()
    stop = threading.Event()

    def _loop() -> None:
        srv.settimeout(0.5)
        while not stop.is_set():
            try:
                conn, _ = srv.accept()
            except TimeoutError:
                continue
            with conn:
                conn.settimeout(2.0)
                try:
                    data = conn.recv(256)
                    if not data:
                        continue
                    if data[0] == 0x10:  # CONNECT
                        conn.sendall(b"\x20\x02\x00\x00")  # CONNACK
                        more = conn.recv(256)
                        if more and more[0] == 0x82:  # SUBSCRIBE
                            conn.sendall(b"\x90\x03\x00\x01\x00")  # SUBACK
                    # illegal type: ignore / close
                except OSError:
                    pass
        srv.close()

    th = threading.Thread(target=_loop, daemon=True)
    th.start()
    try:
        target = TargetSpec(
            name="mqtt-stub",
            host=host,
            port=port,
            protocol="mqtt",
            protocols=["mqtt"],
        )
        tps = TPS(
            name="mqtt",
            profile_class="Web-API",
            protocol="mqtt",
            protocols=["mqtt"],
            strict_rfc_enforcement=True,
        )
        plugin = MQTTPlugin()
        assert plugin.probe_negotiation(host, port, target, tps)[0].passed
        assert plugin.probe_state(host, port, target, tps)[0].passed
        assert is_connack(b"\x20\x02\x00\x00")
        assert build_connect().startswith(b"\x10")
    finally:
        stop.set()
        th.join(timeout=2.0)


def test_bacnet_against_stub() -> None:
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
            if data.startswith(b"\x81\x0b"):
                # minimal I-Am-ish BVLC reply
                srv.sendto(b"\x81\x0a\x00\x08\x01\x00\x10\x00", addr)
        srv.close()

    th = threading.Thread(target=_loop, daemon=True)
    th.start()
    try:
        target = TargetSpec(
            name="bacnet-stub",
            host=host,
            port=port,
            protocol="bacnet",
            protocols=["bacnet"],
        )
        tps = TPS(
            name="bacnet",
            profile_class="ICS-SCADA",
            protocol="bacnet",
            protocols=["bacnet"],
        )
        plugin = BACnetPlugin()
        assert plugin.probe_negotiation(host, port, target, tps)[0].passed
        assert plugin.probe_state(host, port, target, tps)[0].passed
        assert build_bvlc_who_is().startswith(b"\x81")
    finally:
        stop.set()
        th.join(timeout=2.0)


def test_coap_against_stub() -> None:
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
            if len(data) >= 4 and (data[0] >> 6) == 1:
                # ACK 2.05 Content
                msgid = data[2:4]
                srv.sendto(b"\x60\x45" + msgid, addr)
        srv.close()

    th = threading.Thread(target=_loop, daemon=True)
    th.start()
    try:
        target = TargetSpec(
            name="coap-stub",
            host=host,
            port=port,
            protocol="coap",
            protocols=["coap"],
        )
        tps = TPS(
            name="coap",
            profile_class="Web-API",
            protocol="coap",
            protocols=["coap"],
        )
        plugin = CoAPPlugin()
        assert plugin.probe_negotiation(host, port, target, tps)[0].passed
        assert plugin.probe_state(host, port, target, tps)[0].passed
        assert is_coap_response(b"\x60\x45\x12\x34")
        assert struct.unpack("!H", build_get()[2:4])[0] == 0x1234
    finally:
        stop.set()
        th.join(timeout=2.0)
