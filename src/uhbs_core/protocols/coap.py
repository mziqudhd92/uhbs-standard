"""CoAP experimental plugin — confirmable GET over UDP."""

from __future__ import annotations

import socket
import struct

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


def build_get(path: str = ".well-known/core", msg_id: int = 0x1234) -> bytes:
    """RFC 7252 CON GET with Uri-Path options."""
    # ver=1 type=0 (CON) tkl=0 code=0.01 (GET) msgid
    header = b"\x40\x01" + struct.pack("!H", msg_id)
    options = b""
    prev = 0
    for segment in path.strip("/").split("/"):
        raw = segment.encode("utf-8")
        delta = 11 - prev  # Uri-Path = 11
        prev = 11
        if delta < 13 and len(raw) < 13:
            options += bytes([(delta << 4) | len(raw)]) + raw
        else:
            # simplified: only short segments
            options += bytes([(min(delta, 12) << 4) | min(len(raw), 12)]) + raw[:12]
    return header + options


def is_coap_response(raw: bytes) -> bool:
    if len(raw) < 4:
        return False
    ver = (raw[0] >> 6) & 0x03
    code = raw[1]
    return ver == 1 and code != 0


class CoAPPlugin(UdpProtocolPlugin):
    name = "coap"
    families = ("iot", "ot")

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        timeout = _ot_timeout(tps)
        ok = False
        detail = "hang?"
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        try:
            sock.sendto(b"\xff\xff\xff\xff", (host, port))
            try:
                sock.recvfrom(512)
            except TimeoutError:
                ok = True
                detail = "malformed ignored"
            else:
                ok = True
                detail = "malformed elicited response"
        except OSError as exc:
            detail = str(exc)
        finally:
            sock.close()
        return [
            CheckResult(
                id="coap.fsm.malformed",
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
        detail = "no response"
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        try:
            sock.sendto(build_get(), (host, port))
            raw, _ = sock.recvfrom(1024)
            ok = is_coap_response(raw)
            detail = f"recv={raw[:8].hex()} ok={ok}"
        except TimeoutError:
            detail = "GET timeout"
        except OSError as exc:
            detail = str(exc)
        finally:
            sock.close()
        return [
            CheckResult(
                id="coap.nego.get",
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
        codes: list[int] = []
        for mid in (0x1111, 0x2222):
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(timeout)
            try:
                sock.sendto(build_get(msg_id=mid), (host, port))
                raw, _ = sock.recvfrom(1024)
                if is_coap_response(raw):
                    codes.append(raw[1])
            except OSError:
                pass
            finally:
                sock.close()
        ok = len(codes) == 2 and codes[0] == codes[1]
        return [
            CheckResult(
                id="coap.state.get_consistent",
                team="blue",
                passed=ok,
                detail=f"codes={codes}",
                score=100.0 if ok else 0.0,
                critical=True,
            )
        ]
