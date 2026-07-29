"""Bluetooth RFCOMM plugin — offline framing + local TCP stub."""

from __future__ import annotations

import socket
import struct
import threading

from uhbs_core.models import TargetSpec
from uhbs_core.protocols import get_plugin, registry
from uhbs_core.protocols.bluetooth import (
    BluetoothPlugin,
    build_rfcomm_dm,
    build_rfcomm_frame,
    build_rfcomm_sabm,
    build_rfcomm_ua,
    build_rfcomm_uih,
    build_sdp_service_search_request,
    decode_rfcomm_frame,
    is_rfcomm_sabm,
    is_rfcomm_ua,
    is_sdp_service_search_response,
    local_bluetooth_adapter_available,
    probe_path_available,
    rfcomm_fcs,
)
from uhbs_core.tps import TPS


def _register_bluetooth() -> None:
    if "bluetooth" not in registry.list_protocols():
        registry.register(BluetoothPlugin())


def test_bluetooth_plugin_resolves() -> None:
    _register_bluetooth()
    p = get_plugin("bluetooth")
    assert isinstance(p, BluetoothPlugin)
    assert p.name == "bluetooth"


def test_rfcomm_encode_decode_roundtrip() -> None:
    sabm = build_rfcomm_sabm(dlci=0)
    parsed = decode_rfcomm_frame(sabm)
    assert parsed is not None
    assert parsed["dlci"] == 0
    assert parsed["control"] == 0x2F
    assert parsed["info"] == b""
    assert is_rfcomm_sabm(sabm)

    ua = build_rfcomm_ua(dlci=0)
    assert is_rfcomm_ua(ua)

    payload = b"\x01\x02\x03"
    uih = build_rfcomm_uih(dlci=1, cr=True, payload=payload)
    uih_parsed = decode_rfcomm_frame(uih)
    assert uih_parsed is not None
    assert uih_parsed["info"] == payload

    header = bytes([0x03, 0x2F, 0x01])
    assert rfcomm_fcs(header) == sabm[-1]

    long_info = b"x" * 200
    long_frame = build_rfcomm_frame(dlci=2, cr=False, control=0xEF, info=long_info)
    long_parsed = decode_rfcomm_frame(long_frame)
    assert long_parsed is not None
    assert long_parsed["info"] == long_info


def test_sdp_service_search_request_shape() -> None:
    req = build_sdp_service_search_request(uuid16=0x0100, transaction_id=0x0042)
    assert req[0] == 0x02
    assert struct.unpack("!H", req[1:3])[0] == 0x0042
    assert is_sdp_service_search_response(b"\x03\x00\x01\x00\x00") is True
    assert is_sdp_service_search_response(b"\x02") is False


def test_unreachable_does_not_raise_soft_skip() -> None:
    _register_bluetooth()
    plugin = get_plugin("bluetooth")
    target = TargetSpec(name="x", host="127.0.0.1", port=1, protocol="bluetooth")
    if probe_path_available("127.0.0.1", 1):
        return  # environment has BT adapter or odd open port — skip assertion
    fsm = plugin.probe_fsm("127.0.0.1", 1, target, None)
    nego = plugin.probe_negotiation("127.0.0.1", 1, target, None)
    assert fsm[0].id == "bluetooth.fsm.skipped"
    assert fsm[0].passed is False
    assert fsm[0].score == 50.0
    assert nego[0].passed is False
    assert nego[0].score == 50.0
    assert "skipped" in fsm[0].detail.lower() or "RFCOMM" in fsm[0].detail


def _serve_rfcomm_stub() -> tuple[str, int, threading.Event, socket.socket]:
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 0))
    srv.listen(8)
    host, port = srv.getsockname()
    stop = threading.Event()

    def _ss_resp(transaction_id: int) -> bytes:
        params = struct.pack("!HHB", 1, 0, 0)
        return struct.pack("!BHH", 0x03, transaction_id, len(params)) + params

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
                    buf = b""
                    while True:
                        chunk = conn.recv(4096)
                        if not chunk:
                            break
                        buf += chunk
                        while True:
                            frame = decode_rfcomm_frame(buf)
                            if not frame:
                                break
                            buf = buf[len(frame["frame"]) :]
                            ctrl = frame["control"]
                            dlci = frame["dlci"]
                            if ctrl == 0x2F:
                                conn.sendall(build_rfcomm_ua(dlci=dlci, cr=False))
                            elif ctrl == 0x00:
                                conn.sendall(build_rfcomm_dm(dlci=dlci, cr=False))
                            elif (
                                ctrl == 0xEF
                                and frame["info"]
                                and frame["info"][0] == 0x02
                            ):
                                tid = struct.unpack("!H", frame["info"][1:3])[0]
                                resp = _ss_resp(tid)
                                conn.sendall(
                                    build_rfcomm_uih(
                                        dlci=dlci, cr=False, payload=resp
                                    )
                                )
                except (TimeoutError, OSError):
                    pass

    threading.Thread(target=_loop, daemon=True).start()
    return host, port, stop, srv


def test_bluetooth_probes_against_rfcomm_stub() -> None:
    _register_bluetooth()
    host, port, stop, srv = _serve_rfcomm_stub()
    try:
        target = TargetSpec(
            name="bt-stub",
            host=host,
            port=port,
            protocol="bluetooth",
            protocols=["bluetooth"],
            annotations={"rfcomm_channel": 3},
        )
        tps = TPS(
            name="bt-stub",
            profile_class="Low-Interaction",
            protocol="bluetooth",
            protocols=["bluetooth"],
        )
        plugin = BluetoothPlugin()
        assert probe_path_available(host, port)

        fsm = plugin.probe_fsm(host, port, target, tps)
        assert fsm[0].id == "bluetooth.fsm.invalid_frame"
        assert fsm[0].passed

        nego = plugin.probe_negotiation(host, port, target, tps)
        by_id = {c.id: c for c in nego}
        assert by_id["bluetooth.nego.sabm_ua"].passed
        assert by_id["bluetooth.nego.sdp_search"].passed

        state = plugin.probe_state(host, port, target, tps)
        assert state[0].id == "bluetooth.state.dlci_sabm"
        assert state[0].passed
    finally:
        stop.set()
        srv.close()


def test_local_adapter_probe_is_boolean() -> None:
    assert isinstance(local_bluetooth_adapter_available(), bool)
