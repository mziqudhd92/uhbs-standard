"""Modbus TCP framing helpers + offline stub probes (OT/ICS hardening)."""

from __future__ import annotations

import contextlib
import socket
import struct
import threading

from uhbs_core.models import TargetSpec
from uhbs_core.protocols import get_plugin
from uhbs_core.protocols.modbus import (
    ModbusPlugin,
    _mbap_read_holding,
    _mbap_write_single,
    _modbus_config,
)
from uhbs_core.tps import TPS


def test_modbus_plugin_resolves() -> None:
    p = get_plugin("modbus")
    assert isinstance(p, ModbusPlugin)
    assert p.name == "modbus"


def test_modbus_config_defaults_when_no_tps() -> None:
    cfg = _modbus_config(None)
    assert cfg == {
        "unit": 1,
        "address": 0,
        "timeout": 4.0,
        "strict": True,
        "delay_ms": 0.0,
    }


def test_modbus_config_reads_performance_baseline_overrides() -> None:
    tps = TPS(
        name="modbus-stub",
        profile_class="ICS-SCADA",
        protocol="modbus",
        protocols=["modbus"],
        raw={
            "performance_baseline": {
                "modbus_unit_id": 7,
                "modbus_register_address": 42,
                "probe_timeout_sec": 0.75,
                "strict_frame_validation": False,
                "inter_probe_delay_ms": 5,
            }
        },
    )
    cfg = _modbus_config(tps)
    assert cfg["unit"] == 7
    assert cfg["address"] == 42
    assert cfg["timeout"] == 0.75
    assert cfg["strict"] is False
    assert cfg["delay_ms"] == 5.0


def test_modbus_config_reads_top_level_experimental_block() -> None:
    tps = TPS(
        name="modbus-stub",
        profile_class="ICS-SCADA",
        protocol="modbus",
        protocols=["modbus"],
        raw={"experimental": {"modbus_unit_id": 9, "strict_frame_validation": False}},
    )
    cfg = _modbus_config(tps)
    assert cfg["unit"] == 9
    assert cfg["strict"] is False
    # Untouched keys keep their documented defaults.
    assert cfg["address"] == 0
    assert cfg["timeout"] == 4.0


def _start_stub_server(
    handler,
) -> tuple[socket.socket, str, int, threading.Event, threading.Thread]:
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
                conn.settimeout(3.0)
                with contextlib.suppress(OSError):
                    handler(conn)
        srv.close()

    th = threading.Thread(target=_loop, daemon=True)
    th.start()
    return srv, host, port, stop, th


def test_mbap_illegal_function_stub() -> None:
    """A1 — illegal function code should be met with an exception reply or close."""

    def handler(conn: socket.socket) -> None:
        first = conn.recv(4096)
        if not first:
            return
        # Exception response: echo unit/func with high bit set + exception code
        trans_id, proto_id, _length, unit = struct.unpack(">HHHB", first[:7])
        fc = first[7]
        exc_pdu = struct.pack(">BB", fc | 0x80, 0x01)
        length = len(exc_pdu) + 1
        conn.sendall(struct.pack(">HHHB", trans_id, proto_id, length, unit) + exc_pdu)

    srv, host, port, stop, th = _start_stub_server(handler)
    try:
        target = TargetSpec(
            name="modbus-stub", host=host, port=port, protocol="modbus", protocols=["modbus"]
        )
        plugin = ModbusPlugin()
        checks = plugin.probe_fsm(host, port, target, None)
        assert checks[0].id == "modbus.fsm.illegal_function"
        assert checks[0].passed is True
    finally:
        stop.set()
        th.join(timeout=2.0)


def test_mbap_fc03_read_holding_stub() -> None:
    """A2 — a valid FC03 read must be acknowledged with function code 0x03."""

    def handler(conn: socket.socket) -> None:
        first = conn.recv(4096)
        if not first:
            return
        trans_id, proto_id, _length, unit = struct.unpack(">HHHB", first[:7])
        fc = first[7]
        assert fc == 0x03
        pdu = struct.pack(">BBH", 0x03, 2, 0x00AB)
        length = len(pdu) + 1
        conn.sendall(struct.pack(">HHHB", trans_id, proto_id, length, unit) + pdu)

    srv, host, port, stop, th = _start_stub_server(handler)
    try:
        target = TargetSpec(
            name="modbus-stub", host=host, port=port, protocol="modbus", protocols=["modbus"]
        )
        plugin = ModbusPlugin()
        checks = plugin.probe_negotiation(host, port, target, None)
        assert checks[0].id == "modbus.nego.read_holding"
        assert checks[0].passed is True
    finally:
        stop.set()
        th.join(timeout=2.0)


def test_mbap_fc06_fc03_roundtrip_stub() -> None:
    """B1 — write single register then read it back; value must roundtrip."""
    register_store = {"value": 0}

    def handler(conn: socket.socket) -> None:
        # Write
        first = conn.recv(4096)
        if not first:
            return
        trans_id, proto_id, _length, unit = struct.unpack(">HHHB", first[:7])
        fc = first[7]
        assert fc == 0x06
        address, value = struct.unpack(">HH", first[8:12])
        register_store["value"] = value
        conn.sendall(first)  # FC06 echoes the request back verbatim per spec

        # Read
        second = conn.recv(4096)
        if not second:
            return
        trans_id2, proto_id2, _length2, unit2 = struct.unpack(">HHHB", second[:7])
        fc2 = second[7]
        assert fc2 == 0x03
        pdu = struct.pack(">BBH", 0x03, 2, register_store["value"])
        length = len(pdu) + 1
        conn.sendall(struct.pack(">HHHB", trans_id2, proto_id2, length, unit2) + pdu)

    srv, host, port, stop, th = _start_stub_server(handler)
    try:
        target = TargetSpec(
            name="modbus-stub", host=host, port=port, protocol="modbus", protocols=["modbus"]
        )
        tps = TPS(
            name="modbus-stub",
            profile_class="ICS-SCADA",
            protocol="modbus",
            protocols=["modbus"],
        )
        plugin = ModbusPlugin()
        checks = plugin.probe_state(host, port, target, tps)
        assert checks[0].id == "modbus.state.write_read"
        assert checks[0].passed is True
        assert checks[0].critical is True
        assert register_store["value"] == 0x1234
    finally:
        stop.set()
        th.join(timeout=2.0)


def test_modbus_tps_register_override_used_on_wire() -> None:
    """TPS ``modbus_register_address``/``modbus_unit_id`` must reach the wire."""
    seen: dict[str, int] = {}

    def handler(conn: socket.socket) -> None:
        first = conn.recv(4096)
        if not first:
            return
        trans_id, proto_id, _length, unit = struct.unpack(">HHHB", first[:7])
        fc = first[7]
        address = struct.unpack(">H", first[8:10])[0]
        seen["unit"] = unit
        seen["address"] = address
        if fc == 0x03:
            pdu = struct.pack(">BBH", 0x03, 2, 0x0000)
            length = len(pdu) + 1
            conn.sendall(struct.pack(">HHHB", trans_id, proto_id, length, unit) + pdu)

    srv, host, port, stop, th = _start_stub_server(handler)
    try:
        target = TargetSpec(
            name="modbus-stub", host=host, port=port, protocol="modbus", protocols=["modbus"]
        )
        tps = TPS(
            name="modbus-stub",
            profile_class="ICS-SCADA",
            protocol="modbus",
            protocols=["modbus"],
            raw={
                "performance_baseline": {
                    "modbus_unit_id": 5,
                    "modbus_register_address": 99,
                }
            },
        )
        plugin = ModbusPlugin()
        checks = plugin.probe_negotiation(host, port, target, tps)
        assert checks[0].passed is True
        assert seen["unit"] == 5
        assert seen["address"] == 99
    finally:
        stop.set()
        th.join(timeout=2.0)


def test_modbus_probe_timeout_field_used() -> None:
    """A very small ``probe_timeout_sec`` must actually bound the socket wait.

    The stub server intentionally never replies; with a short TPS-configured
    timeout the probe must return promptly (well under the test harness's own
    generous timeout) rather than hanging on the platform default.
    """
    import time

    def handler(conn: socket.socket) -> None:
        conn.recv(4096)
        time.sleep(5.0)  # never reply in time

    srv, host, port, stop, th = _start_stub_server(handler)
    try:
        target = TargetSpec(
            name="modbus-stub", host=host, port=port, protocol="modbus", protocols=["modbus"]
        )
        tps = TPS(
            name="modbus-stub",
            profile_class="ICS-SCADA",
            protocol="modbus",
            protocols=["modbus"],
            raw={"performance_baseline": {"probe_timeout_sec": 0.2}},
        )
        plugin = ModbusPlugin()
        t0 = time.perf_counter()
        checks = plugin.probe_negotiation(host, port, target, tps)
        elapsed = time.perf_counter() - t0
        assert checks[0].passed is False
        assert elapsed < 3.0
    finally:
        stop.set()
        th.join(timeout=2.0)


def test_modbus_state_soft_fails_when_strict_frame_validation_false() -> None:
    """Canary/Alert mode: a broken write/read roundtrip is scored, not hard-critical."""

    def handler(conn: socket.socket) -> None:
        first = conn.recv(4096)
        if not first:
            return
        # Never acknowledge the write correctly (garbage function code byte).
        trans_id, proto_id, _length, unit = struct.unpack(">HHHB", first[:7])
        bad_pdu = struct.pack(">BB", 0x00, 0x00)
        length = len(bad_pdu) + 1
        conn.sendall(struct.pack(">HHHB", trans_id, proto_id, length, unit) + bad_pdu)

    srv, host, port, stop, th = _start_stub_server(handler)
    try:
        target = TargetSpec(
            name="modbus-stub", host=host, port=port, protocol="modbus", protocols=["modbus"]
        )
        tps = TPS(
            name="modbus-stub",
            profile_class="ICS-SCADA",
            protocol="modbus",
            protocols=["modbus"],
            raw={"performance_baseline": {"strict_frame_validation": False}},
        )
        plugin = ModbusPlugin()
        checks = plugin.probe_state(host, port, target, tps)
        assert checks[0].passed is False
        assert checks[0].critical is False
        assert checks[0].score == 35.0
    finally:
        stop.set()
        th.join(timeout=2.0)


def test_mbap_helpers_encode_unit_and_address() -> None:
    read_req = _mbap_read_holding(unit=3, address=17, count=1)
    assert read_req[6] == 3  # unit id byte
    assert struct.unpack(">H", read_req[8:10])[0] == 17

    write_req = _mbap_write_single(unit=4, address=21, value=0x55AA)
    assert write_req[6] == 4
    assert struct.unpack(">H", write_req[8:10])[0] == 21
    assert struct.unpack(">H", write_req[10:12])[0] == 0x55AA
