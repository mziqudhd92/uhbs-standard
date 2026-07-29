"""Bluetooth RFCOMM multiplexer framing (Core Spec Vol 3 Part F) over TCP lab forwards.

Wire checks target TCP-exposed RFCOMM honeypot proxies (common in lab setups).
Native AF_BLUETOOTH is optional; when neither TCP nor an adapter is available,
probes soft-skip without raising.
"""

from __future__ import annotations

import socket
import struct
from pathlib import Path

from uhbs_core.models import CheckResult, TargetSpec
from uhbs_core.netutil import tcp_transact
from uhbs_core.protocols.base import ProtocolPlugin
from uhbs_core.rfc_probes import _transact
from uhbs_core.tps import TPS

# GSM 07.10 / RFCOMM UIH and multiplexer controls (P/F set).
_RFCOMM_SABM = 0x2F
_RFCOMM_UA = 0x63
_RFCOMM_DM = 0x0F
_RFCOMM_UIH = 0xEF

_SOFT_SKIP_DETAIL = (
    "RFCOMM probe skipped: target TCP port unreachable and no local Bluetooth "
    "adapter — use a TCP-forwarded RFCOMM decoy or native BT in lab"
)


def rfcomm_fcs(header_and_info: bytes) -> int:
    """8-bit FCS over Address + Control + Length (+ Information)."""
    fcs = 0xFF
    for byte in header_and_info:
        fcs ^= byte
        for _ in range(8):
            if fcs & 1:
                fcs = (fcs >> 1) ^ 0xE0
            else:
                fcs >>= 1
    return (~fcs) & 0xFF


def build_rfcomm_address(*, dlci: int, cr: bool = True) -> int:
    """EA=1 address field for a 6-bit DLCI."""
    return ((dlci & 0x3F) << 2) | ((1 if cr else 0) << 1) | 1


def build_rfcomm_length_field(info_len: int) -> bytes:
    if info_len < 128:
        return bytes([(info_len << 1) | 1])
    return bytes([((info_len & 0x7F) << 1), (info_len >> 7) & 0xFF])


def build_rfcomm_frame(
    *,
    dlci: int,
    cr: bool,
    control: int,
    info: bytes = b"",
) -> bytes:
    """Encode one RFCOMM frame (no HDLC flags — Bluetooth RFCOMM over L2CAP)."""
    addr = build_rfcomm_address(dlci=dlci, cr=cr)
    header = bytes([addr, control]) + build_rfcomm_length_field(len(info)) + info
    return header + bytes([rfcomm_fcs(header)])


def build_rfcomm_sabm(*, dlci: int = 0, cr: bool = True) -> bytes:
    return build_rfcomm_frame(dlci=dlci, cr=cr, control=_RFCOMM_SABM)


def build_rfcomm_uih(*, dlci: int, cr: bool, payload: bytes) -> bytes:
    return build_rfcomm_frame(dlci=dlci, cr=cr, control=_RFCOMM_UIH, info=payload)


def build_rfcomm_ua(*, dlci: int = 0, cr: bool = False) -> bytes:
    """UA response (responder direction)."""
    return build_rfcomm_frame(dlci=dlci, cr=cr, control=_RFCOMM_UA)


def build_rfcomm_dm(*, dlci: int = 0, cr: bool = False) -> bytes:
    return build_rfcomm_frame(dlci=dlci, cr=cr, control=_RFCOMM_DM)


def _read_length(data: bytes, pos: int) -> tuple[int, int]:
    if pos >= len(data):
        return 0, pos
    b0 = data[pos]
    if b0 & 1:
        return b0 >> 1, pos + 1
    if pos + 1 >= len(data):
        return 0, pos
    b1 = data[pos + 1]
    return (b0 >> 1) | (b1 << 7), pos + 2


def decode_rfcomm_frame(buf: bytes) -> dict | None:
    """Parse the first RFCOMM frame in ``buf``; verify FCS when complete."""
    if len(buf) < 4:
        return None
    addr = buf[0]
    if not (addr & 1):
        return None
    cr = bool((addr >> 1) & 1)
    dlci = addr >> 2
    control = buf[1]
    info_len, idx = _read_length(buf, 2)
    need = idx + info_len + 1
    if len(buf) < need:
        return None
    info = buf[idx : idx + info_len]
    fcs = buf[idx + info_len]
    header = buf[: idx + info_len]
    if rfcomm_fcs(header) != fcs:
        return None
    return {
        "dlci": dlci,
        "cr": cr,
        "control": control,
        "info": info,
        "frame": buf[:need],
    }


def is_rfcomm_ua(raw: bytes) -> bool:
    frame = decode_rfcomm_frame(raw)
    return frame is not None and frame["control"] == _RFCOMM_UA


def is_rfcomm_dm(raw: bytes) -> bool:
    frame = decode_rfcomm_frame(raw)
    return frame is not None and frame["control"] == _RFCOMM_DM


def is_rfcomm_sabm(raw: bytes) -> bool:
    frame = decode_rfcomm_frame(raw)
    return frame is not None and frame["control"] == _RFCOMM_SABM


def build_sdp_service_search_request(
    *,
    uuid16: int = 0x0100,
    transaction_id: int = 1,
    max_records: int = 10,
) -> bytes:
    """Minimal Bluetooth SDP ServiceSearchRequest (PDU id 0x02)."""
    uuid_de = bytes([0x19, (uuid16 >> 8) & 0xFF, uuid16 & 0xFF])
    pattern = bytes([0x35, len(uuid_de)]) + uuid_de
    params = pattern + struct.pack("!H", max_records) + b"\x00"
    return struct.pack("!BHH", 0x02, transaction_id, len(params)) + params


def is_sdp_service_search_response(payload: bytes) -> bool:
    return len(payload) >= 1 and payload[0] == 0x03


def tcp_rfcomm_reachable(host: str, port: int, *, timeout: float = 2.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def local_bluetooth_adapter_available() -> bool:
    if hasattr(socket, "AF_BLUETOOTH"):
        try:
            sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_RAW, socket.BTPROTO_HCI)
            sock.close()
            return True
        except OSError:
            pass
    try:
        bt_class = Path("/sys/class/bluetooth")
        if bt_class.is_dir():
            return any(bt_class.iterdir())
    except OSError:
        pass
    return False


def probe_path_available(host: str, port: int) -> bool:
    return tcp_rfcomm_reachable(host, port) or local_bluetooth_adapter_available()


def _uih_info_from_buffer(raw: bytes) -> bytes:
    pos = 0
    while pos < len(raw):
        frame = decode_rfcomm_frame(raw[pos:])
        if not frame:
            break
        pos += len(frame["frame"])
        if frame["control"] == _RFCOMM_UIH:
            return frame["info"]
    return raw


def _rfcomm_channel_from_target(target: TargetSpec) -> int:
    ann = target.annotations or {}
    for key in ("rfcomm_channel", "bluetooth_channel", "bt_channel"):
        if key in ann and ann[key] is not None:
            return int(ann[key]) & 0x3F
    return 1


def _soft_skip(check_id: str) -> CheckResult:
    return CheckResult(
        id=check_id,
        team="blue",
        passed=True,
        detail=_SOFT_SKIP_DETAIL,
        score=50.0,
    )


class BluetoothPlugin(ProtocolPlugin):
    """Bluetooth RFCOMM (+ optional SDP over UIH) for decoy grading."""

    name = "bluetooth"
    families = ("it",)

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        if not probe_path_available(host, port):
            return [_soft_skip("bluetooth.fsm.skipped")]

        # Invalid control + wrong FCS — must not answer with UA (accept DM/close/nothing).
        junk = bytes([0x03, 0x00, 0x01, 0x00])
        raw, _, err = _transact(host, port, junk, recv_first=False, timeout=3.0)
        if is_rfcomm_ua(raw):
            score = 20.0
            detail = "UA on invalid RFCOMM frame (weak fidelity)"
        elif is_rfcomm_dm(raw) or (not raw and err):
            score = 100.0
            detail = "reject or close on invalid frame"
        elif not raw:
            score = 80.0
            detail = err or "no UA on garbage (acceptable)"
        else:
            score = 70.0
            detail = f"reply len={len(raw)} (no UA)"
        return [
            CheckResult(
                id="bluetooth.fsm.invalid_frame",
                team="blue",
                passed=score >= 70.0,
                detail=detail,
                score=score,
            )
        ]

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        if not probe_path_available(host, port):
            return [_soft_skip("bluetooth.nego.skipped")]

        sabm = build_rfcomm_sabm(dlci=0, cr=True)
        raw, _, err = _transact(host, port, sabm, recv_first=False, timeout=3.0)
        ua_ok = is_rfcomm_ua(raw)
        checks: list[CheckResult] = [
            CheckResult(
                id="bluetooth.nego.sabm_ua",
                team="blue",
                passed=ua_ok,
                detail=(
                    f"DLCI0 SABM→UA len={len(raw)}"
                    if raw
                    else (err or "no UA after SABM")
                ),
                score=100.0 if ua_ok else 30.0,
            )
        ]

        if ua_ok:
            sdp = build_sdp_service_search_request()
            uih = build_rfcomm_uih(dlci=0, cr=True, payload=sdp)
            sdp_raw, _, sdp_err = _transact(host, port, sabm + uih, timeout=3.0)
            info = _uih_info_from_buffer(sdp_raw)
            sdp_ok = is_sdp_service_search_response(info)
            checks.append(
                CheckResult(
                    id="bluetooth.nego.sdp_search",
                    team="blue",
                    passed=sdp_ok,
                    detail=(
                        "SDP ServiceSearchResponse"
                        if sdp_ok
                        else (sdp_err or "no SDP SSResp in UIH payload")
                    ),
                    score=100.0 if sdp_ok else 50.0,
                )
            )
        return checks

    def probe_state(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        if not probe_path_available(host, port):
            return [_soft_skip("bluetooth.state.skipped")]

        sabm = build_rfcomm_sabm()
        raw, _, err = tcp_transact(host, port, sabm, timeout=3.0)
        if not is_rfcomm_ua(raw):
            return [
                CheckResult(
                    id="bluetooth.state.mux",
                    team="blue",
                    passed=False,
                    detail=err or "mux not established (no UA)",
                    score=30.0,
                )
            ]
        channel = _rfcomm_channel_from_target(target)
        sabm_ch = build_rfcomm_sabm(dlci=channel, cr=True)
        ch_raw, _, ch_err = _transact(host, port, sabm_ch, recv_first=False, timeout=3.0)
        ok = is_rfcomm_ua(ch_raw)
        return [
            CheckResult(
                id="bluetooth.state.dlci_sabm",
                team="blue",
                passed=ok,
                detail=(
                    f"DLCI{channel} SABM→UA"
                    if ok
                    else (ch_err or "no UA on channel SABM")
                ),
                score=100.0 if ok else 40.0,
            )
        ]
