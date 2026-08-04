"""MQTT experimental plugin — CONNECT/CONNACK + subscribe sanity over TCP."""

from __future__ import annotations

import socket
import struct
import time

from uhbs_core.models import CheckResult, TargetSpec
from uhbs_core.protocols.base import ProtocolPlugin
from uhbs_core.tps import TPS


def _ot_timeout(tps: TPS | None, default: float = 3.0) -> float:
    if tps and isinstance(tps.raw, dict):
        for block in (tps.raw.get("performance_baseline"), tps.raw.get("experimental"), tps.raw):
            if isinstance(block, dict) and "probe_timeout_sec" in block:
                try:
                    return float(block["probe_timeout_sec"])
                except (TypeError, ValueError):
                    pass
    return default


def build_connect(client_id: str = "uhbs") -> bytes:
    """MQTT 3.1.1 CONNECT with clean session."""
    proto = b"\x00\x04MQTT\x04\x02\x00\x3c"  # name, level 4, flags clean, keepalive 60
    cid = client_id.encode("utf-8")
    payload = proto + struct.pack("!H", len(cid)) + cid
    remaining = len(payload)
    # remaining length encoded as single byte for small packets
    return b"\x10" + bytes([remaining]) + payload


def is_connack(raw: bytes) -> bool:
    return len(raw) >= 4 and raw[0] == 0x20 and raw[3] == 0x00


class MQTTPlugin(ProtocolPlugin):
    name = "mqtt"
    families = ("iot", "ot", "messaging")

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        timeout = _ot_timeout(tps)
        ok = False
        detail = "no response"
        try:
            with socket.create_connection((host, port), timeout=timeout) as sock:
                sock.settimeout(timeout)
                sock.sendall(b"\xff\x00")  # illegal MQTT type
                try:
                    data = sock.recv(64)
                    ok = True
                    detail = f"illegal type response len={len(data)}"
                except TimeoutError:
                    ok = True
                    detail = "illegal type ignored/closed"
        except OSError as exc:
            detail = str(exc)
        return [
            CheckResult(
                id="mqtt.fsm.illegal_type",
                team="red",
                passed=ok,
                detail=detail,
                score=100.0 if ok else 20.0,
            )
        ]

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        timeout = _ot_timeout(tps)
        ok = False
        detail = "no CONNACK"
        try:
            with socket.create_connection((host, port), timeout=timeout) as sock:
                sock.settimeout(timeout)
                sock.sendall(build_connect())
                raw = sock.recv(64)
                ok = is_connack(raw)
                detail = f"recv={raw[:8].hex()} ok={ok}"
        except OSError as exc:
            detail = str(exc)
        return [
            CheckResult(
                id="mqtt.nego.connack",
                team="blue",
                passed=ok,
                detail=detail,
                score=100.0 if ok else 0.0,
                critical=bool(tps and tps.strict_rfc_enforcement),
            )
        ]

    def probe_state(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        timeout = _ot_timeout(tps)
        ok = False
        detail = "session failed"
        try:
            with socket.create_connection((host, port), timeout=timeout) as sock:
                sock.settimeout(timeout)
                sock.sendall(build_connect("uhbs-state"))
                raw = sock.recv(64)
                if not is_connack(raw):
                    detail = "CONNACK failed"
                else:
                    # SUBSCRIBE topic uhbs/test qos0
                    topic = b"uhbs/test"
                    pkt_id = b"\x00\x01"
                    payload = pkt_id + struct.pack("!H", len(topic)) + topic + b"\x00"
                    rem = len(payload)
                    sock.sendall(b"\x82" + bytes([rem]) + payload)
                    suback = sock.recv(64)
                    ok = len(suback) >= 4 and suback[0] == 0x90
                    detail = f"suback={suback[:6].hex()} ok={ok}"
                    time.sleep(0.01)
        except OSError as exc:
            detail = str(exc)
        return [
            CheckResult(
                id="mqtt.state.subscribe",
                team="blue",
                passed=ok,
                detail=detail,
                score=100.0 if ok else 0.0,
                critical=True,
            )
        ]
