from __future__ import annotations

import socket
import struct

from uhbs_core.protocols.base import ProtocolPlugin

from ..models import CheckResult, TargetSpec
from ..tps import TPS

# --- Optional scapy-backed MBAP encoding (architecture review round 2,
# item 4) ---------------------------------------------------------------
#
# scapy has zero required transitive dependencies (verified: scapy==2.7.0
# installs nothing else), so it's low-risk to offer, but it is an OPTIONAL
# extra (`pip install uhbs[scapy]`), NOT a hard dependency of this package
# or its Docker images. Byte-for-byte verified (this review round) that
# ``scapy.contrib.modbus``'s MBAP + FC0x03/FC0x06 encoding is IDENTICAL to
# the pre-existing hand-rolled ``struct.pack`` bytes below for the same
# inputs, so swapping backends changes nothing about wire behavior. If
# scapy isn't installed, or its Modbus layer raises for any reason, both
# helpers transparently fall back to the hand-rolled bytes.
try:
    from scapy.contrib.modbus import (
        ModbusADURequest,
        ModbusPDU03ReadHoldingRegistersRequest,
        ModbusPDU06WriteSingleRegisterRequest,
    )

    _HAVE_SCAPY = True
except ImportError:  # pragma: no cover — exercised only when scapy is absent
    _HAVE_SCAPY = False


def _mbap_read_holding_handrolled(
    trans_id: int = 1, unit: int = 1, address: int = 0, count: int = 1
) -> bytes:
    pdu = struct.pack(">BHH", 0x03, address, count)
    length = len(pdu) + 1  # unit id + pdu
    return struct.pack(">HHHB", trans_id, 0, length, unit) + pdu


def _mbap_write_single_handrolled(
    trans_id: int = 2, unit: int = 1, address: int = 0, value: int = 0
) -> bytes:
    pdu = struct.pack(">BHH", 0x06, address, value)
    length = len(pdu) + 1
    return struct.pack(">HHHB", trans_id, 0, length, unit) + pdu


def _mbap_read_holding(trans_id: int = 1, unit: int = 1, address: int = 0, count: int = 1) -> bytes:
    """Modbus TCP Read Holding Registers (FC 0x03) — scapy-backed, hand-rolled fallback."""
    if _HAVE_SCAPY:
        try:
            pkt = ModbusADURequest(transId=trans_id, unitId=unit) / (
                ModbusPDU03ReadHoldingRegistersRequest(startAddr=address, quantity=count)
            )
            return bytes(pkt)
        except Exception:  # noqa: BLE001 — any scapy surprise, use the known-good fallback
            pass
    return _mbap_read_holding_handrolled(trans_id, unit, address, count)


def _mbap_write_single(
    trans_id: int = 2, unit: int = 1, address: int = 0, value: int = 0
) -> bytes:
    """Modbus TCP Write Single Register (FC 0x06) — scapy-backed, hand-rolled fallback."""
    if _HAVE_SCAPY:
        try:
            pkt = ModbusADURequest(transId=trans_id, unitId=unit) / (
                ModbusPDU06WriteSingleRegisterRequest(registerAddr=address, registerValue=value)
            )
            return bytes(pkt)
        except Exception:  # noqa: BLE001 — any scapy surprise, use the known-good fallback
            pass
    return _mbap_write_single_handrolled(trans_id, unit, address, value)


class ModbusPlugin(ProtocolPlugin):
    """OT/ICS Modbus TCP — UHBS industrial profile support.

    Named-state sequence (FSM formalization, architecture review round 2,
    item 3) — a documented, fail-fast sequential pattern, deliberately not
    a generic state-machine engine. This plugin's data-integrity gate
    (``probe_state``) was already close to this shape; the steps below are
    now explicit named checkpoints with an early return the moment any one
    of them doesn't hold, instead of only asserting a response "arrived":

        Connect -> Write register 0 = 0x1234 (FC 0x06)
                -> Read holding register 0 (FC 0x03)
                -> Assert read_value == 0x1234

    ``probe_fsm``/``probe_negotiation`` are separate, simpler probes (A1
    illegal-function-code handling, A2 valid read) and are not part of this
    named sequence.
    """

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
        """B1 — write single register (FC 0x06), read it back, and assert
        the read-back value actually equals what was written.

        Architecture note (2026-07-27 review): this previously only checked
        that *a* response of plausible length arrived — a static canary
        that ignores writes entirely and always echoes a fixed dummy
        register value would have scored 100/100 for "data-plane
        statefulness" it does not actually have. This check is marked
        ``critical=True``: real value equality is the whole point of a
        data-integrity gate and must not be diluted by unrelated checks.
        """
        write_value = 0x1234

        # --- FSM step 1: Connect -----------------------------------------
        try:
            s = socket.create_connection((host, port), timeout=3.0)
        except OSError as exc:
            return [
                CheckResult(
                    id="modbus.state.connect",
                    team="blue",
                    critical=True,
                    passed=False,
                    detail=str(exc),
                    score=0.0,
                )
            ]

        try:
            s.settimeout(2.0)

            # --- FSM step 2: Write register 0 = 0x1234 (FC 0x06) --------
            req = _mbap_write_single(trans_id=2, unit=1, address=0, value=write_value)
            s.sendall(req)
            try:
                write_resp = s.recv(256)
            except TimeoutError:
                write_resp = b""
            if len(write_resp) < 8 or write_resp[7] != 0x06:
                return [
                    CheckResult(
                        id="modbus.state.write_read",
                        team="blue",
                        critical=True,
                        passed=False,
                        detail=(
                            "write step (FC 0x06) failed/unacknowledged: "
                            f"resp={write_resp[:16].hex() if write_resp else 'empty'}"
                        ),
                        score=0.0,
                    )
                ]

            # --- FSM step 3: Read holding register 0 (FC 0x03) ----------
            s.sendall(_mbap_read_holding(trans_id=3))
            try:
                resp = s.recv(256)
            except TimeoutError:
                resp = b""
        finally:
            s.close()

        # MBAP(7) + unit(1) + func(1) + byte_count(1) + register(2) = 11 bytes minimum
        if len(resp) < 11 or resp[7] != 0x03:
            return [
                CheckResult(
                    id="modbus.state.write_read",
                    team="blue",
                    critical=True,
                    passed=False,
                    detail=(
                        "read step (FC 0x03) short/invalid: "
                        f"resp={resp[:16].hex() if resp else 'empty'}"
                    ),
                    score=0.0,
                )
            ]

        # --- FSM step 4: Assert read_value == 0x1234 -------------------
        read_value = struct.unpack(">H", resp[9:11])[0]
        ok = read_value == write_value
        return [
            CheckResult(
                id="modbus.state.write_read",
                team="blue",
                critical=True,
                passed=ok,
                detail=f"wrote=0x{write_value:04x} read_back=0x{read_value:04x}",
                score=100.0 if ok else 0.0,
            )
        ]
