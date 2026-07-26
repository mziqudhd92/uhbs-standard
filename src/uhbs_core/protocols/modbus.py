from __future__ import annotations

import socket
import struct

from uhbs_core.protocols.base import ProtocolPlugin

from ..models import CheckResult, TargetSpec
from ..tps import TPS


def _mbap_read_holding(trans_id: int = 1, unit: int = 1, address: int = 0, count: int = 1) -> bytes:
    """Modbus TCP Read Holding Registers (FC 0x03)."""
    pdu = struct.pack(">BHH", 0x03, address, count)
    length = len(pdu) + 1  # unit id + pdu
    return struct.pack(">HHHB", trans_id, 0, length, unit) + pdu


class ModbusPlugin(ProtocolPlugin):
    """OT/ICS Modbus TCP — UHBS industrial profile support."""

    name = "modbus"
    families = ("ot", "ics", "scada")

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        # Invalid function code should yield exception response (0x80|fc) or close
        try:
            with socket.create_connection((host, port), timeout=3.0) as s:
                s.settimeout(2.0)
                bad = struct.pack(">HHHBB", 1, 0, 2, 1, 0x7F)  # illegal FC
                s.sendall(bad)
                try:
                    resp = s.recv(256)
                except TimeoutError:
                    resp = b""
                # Exception: function code has high bit set, or connection closed
                ok = (len(resp) >= 9 and resp[7] >= 0x80) or resp == b""
                return [
                    CheckResult(
                        id="modbus.fsm.illegal_function",
                        team="blue",
                        passed=ok,
                        detail=f"resp={resp[:16].hex() if resp else 'closed'}",
                        score=100.0 if ok else 20.0,
                    )
                ]
        except OSError as exc:
            return [
                CheckResult(
                    id="modbus.fsm.connect",
                    team="blue",
                    passed=False,
                    detail=str(exc),
                    score=0.0,
                )
            ]

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        # Valid read holding registers
        try:
            with socket.create_connection((host, port), timeout=3.0) as s:
                s.settimeout(2.0)
                s.sendall(_mbap_read_holding())
                resp = s.recv(256)
                ok = len(resp) >= 9 and resp[7] == 0x03
                return [
                    CheckResult(
                        id="modbus.nego.read_holding",
                        team="blue",
                        passed=ok,
                        detail=f"resp={resp[:20].hex() if resp else 'empty'}",
                        score=100.0 if ok else 30.0,
                    )
                ]
        except OSError as exc:
            return [
                CheckResult(
                    id="modbus.nego.connect",
                    team="blue",
                    passed=False,
                    detail=str(exc),
                    score=0.0,
                )
            ]

    def probe_state(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        # Write single register (FC 0x06) then read back (best-effort)
        try:
            with socket.create_connection((host, port), timeout=3.0) as s:
                s.settimeout(2.0)
                pdu = struct.pack(">BHH", 0x06, 0, 0x1234)
                req = struct.pack(">HHHB", 2, 0, len(pdu) + 1, 1) + pdu
                s.sendall(req)
                try:
                    s.recv(256)
                except TimeoutError:
                    pass
                s.sendall(_mbap_read_holding(trans_id=3))
                resp = s.recv(256)
                ok = len(resp) >= 9
                return [
                    CheckResult(
                        id="modbus.state.write_read",
                        team="blue",
                        passed=ok,
                        detail="write/read exchange completed" if ok else "no response",
                        score=100.0 if ok else 25.0,
                    )
                ]
        except OSError as exc:
            return [
                CheckResult(
                    id="modbus.state.connect",
                    team="blue",
                    passed=False,
                    detail=str(exc),
                    score=0.0,
                )
            ]
