"""BACnet/IP (BVLC) experimental plugin — Who-Is / I-Am style UDP probes."""

from __future__ import annotations

import socket
import struct
import time

from uhbs_core.models import CheckResult, TargetSpec
from uhbs_core.protocols.udp_base import UdpProtocolPlugin
from uhbs_core.tps import TPS


def _ot_timeout(tps: TPS | None, default: float = 2.0) -> float:
    if tps and isinstance(tps.raw, dict):
        for block in (tps.raw.get("performance_baseline"), tps.raw.get("experimental"), tps.raw):
            if isinstance(block, dict) and "probe_timeout_sec" in block:
                try:
                    return float(block["probe_timeout_sec"])
                except (TypeError, ValueError):
                    pass
    return default


def build_bvlc_who_is() -> bytes:
    """Minimal BVLC Original-Broadcast-NPDU + Who-Is (service 0x08)."""
    # BVLC: type=0x81, function=0x0b (Original-Broadcast-NPDU), length
    npdu = b"\x01\x20\xff\xff\x00\xff\x10\x08"  # version, ctrl, DNET/DADR/hop, APDU Who-Is
    length = 4 + len(npdu)
    return b"\x81\x0b" + struct.pack("!H", length) + npdu


def is_bvlc_iam(raw: bytes) -> bool:
    # Accept any BVLC reply (type 0x81) of reasonable length.
    return len(raw) >= 6 and raw[0] == 0x81


class BACnetPlugin(UdpProtocolPlugin):
    name = "bacnet"
    families = ("ot", "ics", "scada", "iot")

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        timeout = _ot_timeout(tps)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        ok = False
        detail = "no response"
        try:
            # Truncated / invalid BVLC — expect ignore or clean error, not hang
            sock.sendto(b"\x81\xff\x00\x04", (host, port))
            try:
                sock.recvfrom(512)
            except TimeoutError:
                ok = True
                detail = "invalid BVLC ignored (timeout)"
            else:
                ok = True
                detail = "invalid BVLC elicited response"
        except OSError as exc:
            detail = str(exc)
        finally:
            sock.close()
        return [
            CheckResult(
                id="bacnet.fsm.invalid_bvlc",
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
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        ok = False
        detail = "no I-Am"
        try:
            sock.sendto(build_bvlc_who_is(), (host, port))
            raw, _ = sock.recvfrom(1024)
            ok = is_bvlc_iam(raw)
            detail = f"recv={raw[:16].hex()} ok={ok}"
        except TimeoutError:
            detail = "Who-Is timeout"
        except OSError as exc:
            detail = str(exc)
        finally:
            sock.close()
        return [
            CheckResult(
                id="bacnet.nego.who_is_iam",
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
        # Two Who-Is rounds should remain consistent (same BVLC type replies)
        timeout = _ot_timeout(tps)
        replies: list[bytes] = []
        for _ in range(2):
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(timeout)
            try:
                sock.sendto(build_bvlc_who_is(), (host, port))
                raw, _ = sock.recvfrom(1024)
                replies.append(raw)
            except OSError:
                pass
            finally:
                sock.close()
            time.sleep(0.01)
        ok = len(replies) == 2 and all(r[:1] == b"\x81" for r in replies)
        return [
            CheckResult(
                id="bacnet.state.who_is_consistent",
                team="blue",
                passed=ok,
                detail=f"replies={len(replies)}",
                score=100.0 if ok else 0.0,
                critical=True,
            )
        ]
