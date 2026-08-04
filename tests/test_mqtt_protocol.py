"""MQTT CONNECT/CONNACK + SUBSCRIBE offline stub probes."""

from __future__ import annotations

import socket
import threading

from uhbs_core.models import TargetSpec
from uhbs_core.protocols import get_plugin
from uhbs_core.protocols.mqtt import MQTTPlugin, build_connect, is_connack
from uhbs_core.tps import TPS


def test_mqtt_plugin_resolves_and_aliases() -> None:
    p = get_plugin("mqtt")
    assert isinstance(p, MQTTPlugin)
    assert p.name == "mqtt"
    assert get_plugin("mqtts").name == "mqtt"


def test_build_connect_is_well_formed() -> None:
    req = build_connect("uhbs-probe")
    assert req[0] == 0x10  # CONNECT packet type
    assert b"MQTT" in req
    assert b"uhbs-probe" in req


def test_is_connack_accepts_success_rejects_garbage() -> None:
    assert is_connack(b"\x20\x02\x00\x00") is True
    assert is_connack(b"HTTP/1.1") is False
    assert is_connack(b"") is False


def _start_tcp_stub(handler) -> tuple[socket.socket, str, int, threading.Event, threading.Thread]:
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
                    handler(conn)
                except OSError:
                    pass
        srv.close()

    th = threading.Thread(target=_loop, daemon=True)
    th.start()
    return srv, host, port, stop, th


def test_mqtt_probe_fsm_illegal_type_stub() -> None:
    """A1 — an illegal MQTT control packet type must not hang the harness."""

    def handler(conn: socket.socket) -> None:
        conn.recv(64)
        # Broker either closes the connection or ignores — never hangs.

    srv, host, port, stop, th = _start_tcp_stub(handler)
    try:
        target = TargetSpec(
            name="mqtt-stub", host=host, port=port, protocol="mqtt", protocols=["mqtt"]
        )
        plugin = MQTTPlugin()
        checks = plugin.probe_fsm(host, port, target, None)
        assert checks[0].id == "mqtt.fsm.illegal_type"
        assert checks[0].passed is True
    finally:
        stop.set()
        th.join(timeout=2.0)


def test_mqtt_probe_negotiation_connect_connack_stub() -> None:
    """A2 — CONNECT must be met with a CONNACK (return code accepted)."""

    def handler(conn: socket.socket) -> None:
        data = conn.recv(256)
        if data and data[0] == 0x10:
            conn.sendall(b"\x20\x02\x00\x00")  # CONNACK, accepted

    srv, host, port, stop, th = _start_tcp_stub(handler)
    try:
        target = TargetSpec(
            name="mqtt-stub", host=host, port=port, protocol="mqtt", protocols=["mqtt"]
        )
        tps = TPS(
            name="mqtt-stub",
            profile_class="Web-API",
            protocol="mqtt",
            protocols=["mqtt"],
            strict_rfc_enforcement=True,
        )
        plugin = MQTTPlugin()
        checks = plugin.probe_negotiation(host, port, target, tps)
        assert checks[0].id == "mqtt.nego.connack"
        assert checks[0].passed is True
        assert checks[0].critical is True
    finally:
        stop.set()
        th.join(timeout=2.0)


def test_mqtt_probe_state_subscribe_roundtrip_stub() -> None:
    """B1 — CONNECT/CONNACK then SUBSCRIBE/SUBACK sanity round-trip."""

    def handler(conn: socket.socket) -> None:
        data = conn.recv(256)
        if not data or data[0] != 0x10:
            return
        conn.sendall(b"\x20\x02\x00\x00")  # CONNACK
        more = conn.recv(256)
        if more and more[0] == 0x82:  # SUBSCRIBE
            conn.sendall(b"\x90\x03\x00\x01\x00")  # SUBACK

    srv, host, port, stop, th = _start_tcp_stub(handler)
    try:
        target = TargetSpec(
            name="mqtt-stub", host=host, port=port, protocol="mqtt", protocols=["mqtt"]
        )
        tps = TPS(
            name="mqtt-stub",
            profile_class="Web-API",
            protocol="mqtt",
            protocols=["mqtt"],
        )
        plugin = MQTTPlugin()
        checks = plugin.probe_state(host, port, target, tps)
        assert checks[0].id == "mqtt.state.subscribe"
        assert checks[0].passed is True
        assert checks[0].critical is True
    finally:
        stop.set()
        th.join(timeout=2.0)


def test_mqtt_probe_negotiation_fails_without_connack() -> None:
    def handler(conn: socket.socket) -> None:
        conn.recv(256)
        conn.sendall(b"\x00\x00\x00\x00")  # not a CONNACK

    srv, host, port, stop, th = _start_tcp_stub(handler)
    try:
        target = TargetSpec(
            name="mqtt-stub", host=host, port=port, protocol="mqtt", protocols=["mqtt"]
        )
        plugin = MQTTPlugin()
        checks = plugin.probe_negotiation(host, port, target, None)
        assert checks[0].passed is False
    finally:
        stop.set()
        th.join(timeout=2.0)
