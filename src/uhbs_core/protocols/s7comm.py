"""S7comm over ISO-on-TCP (TPKT + COTP) — Siemens industrial protocol.

P0 checks mirror the ICS Modbus / RDP shape:

* A1 — truncated TPKT must not hang the harness
* A2 — COTP Connection Request → Connection Confirm (PDU type ``0xD0``)
* B1 — S7 Setup Communication (``0xF0``) after COTP CC

Wire references: RFC 1006 (TPKT), ISO 8073/COTP, S7comm (Wireshark
``s7comm`` / Snap7-compatible CR + Setup PDUs).
"""

from __future__ import annotations

import socket
import struct

from uhbs_core.models import CheckResult, TargetSpec
from uhbs_core.netutil import tcp_transact
from uhbs_core.protocols.base import ProtocolPlugin
from uhbs_core.tps import TPS


def build_tpkt(payload: bytes) -> bytes:
    """RFC 1006 TPKT header (version=3) + payload."""
    total = 4 + len(payload)
    return b"\x03\x00" + struct.pack("!H", total) + payload


def build_cotp_cr(
    *,
    src_tsap: bytes = b"\x01\x00",
    dst_tsap: bytes = b"\x01\x02",
    dst_ref: int = 0,
    src_ref: int = 1,
) -> bytes:
    """COTP Connection Request for S7 (class 0) with SRC/DST TSAP parameters.

    Default DST TSAP ``01 02`` = rack 0 / slot 2 (common S7-300/400 probe).
    """
    # LI = length of COTP header after LI byte (excluding LI itself).
    # Fixed CR fields (10 bytes after LI) + C1(4) + C2(4) = 18 → LI=0x11
    params = (
        b"\xc1\x02" + src_tsap  # SRC-TSAP
        + b"\xc2\x02" + dst_tsap  # DST-TSAP
    )
    cotp = (
        b"\x11"  # LI
        + b"\xe0"  # CR
        + struct.pack("!HH", dst_ref, src_ref)
        + b"\x00"  # class/options
        + params
    )
    return build_tpkt(cotp)


def build_s7_setup_communication(pdu_ref: int = 0x0400) -> bytes:
    """S7 Job: Setup Communication (function 0xF0) inside COTP DT + TPKT."""
    # S7 header: protocol_id=0x32, rosctr=Job(0x01), ...
    s7 = (
        b"\x32\x01\x00\x00"
        + struct.pack("!H", pdu_ref)
        + b"\x00\x08"  # param length
        + b"\x00\x00"  # data length
        + b"\xf0\x00"  # Setup Communication
        + b"\x00\x01\x00\x01\x01\xe0"  # max AmQ calling/called, PDU=480
    )
    cotp_dt = b"\x02\xf0\x80" + s7  # LI=2, DT, TPDU-nr/EOT
    return build_tpkt(cotp_dt)


def is_tpkt(raw: bytes) -> bool:
    return len(raw) >= 4 and raw[0] == 0x03 and raw[1] == 0x00


def is_cotp_cc(raw: bytes) -> bool:
    """COTP Connection Confirm: TPKT + LI + PDU type 0xD0."""
    if not is_tpkt(raw) or len(raw) < 6:
        return False
    # COTP header starts at offset 4; PDU type is second byte (after LI)
    return raw[5] == 0xD0


def is_s7_setup_ack(raw: bytes) -> bool:
    """Accept TPKT frames that carry S7 protocol id 0x32 (optionally Setup 0xF0)."""
    if not is_tpkt(raw):
        return False
    idx = raw.find(b"\x32")
    if idx < 0 or idx + 1 >= len(raw):
        return False
    # Prefer Setup function; any S7 Job/Ack Data reply also counts for B1.
    return b"\xf0" in raw[idx:] or raw[idx + 1] in (0x01, 0x02, 0x03)


def _recv_all(sock: socket.socket, timeout: float = 4.0) -> bytes:
    sock.settimeout(timeout)
    chunks: list[bytes] = []
    try:
        while True:
            part = sock.recv(4096)
            if not part:
                break
            chunks.append(part)
            # TPKT length known — stop once complete
            buf = b"".join(chunks)
            if is_tpkt(buf) and len(buf) >= 4:
                need = struct.unpack("!H", buf[2:4])[0]
                if len(buf) >= need:
                    break
            # otherwise one shot is enough for most PLCs/honeypots
            if len(buf) >= 4:
                break
    except TimeoutError:
        pass
    return b"".join(chunks)


class S7commPlugin(ProtocolPlugin):
    """Siemens S7comm (ISO-on-TCP port 102)."""

    name = "s7comm"
    families = ("ot", "ics", "scada")

    @staticmethod
    def _strict(tps: TPS | None) -> bool:
        return tps is None or tps.strict_rfc_enforcement

    @staticmethod
    def _probe_timeout(tps: TPS | None, default: float) -> float:
        """Optional TPS override (``performance_baseline.probe_timeout_sec``).

        Mirrors the OT/ICS Modbus hardening knob so operators can tune S7comm
        socket timeouts (slow real PLCs, rate-limited decoys) without a code
        change. Missing/malformed values keep the existing per-call default.
        """
        if tps is None:
            return default
        raw = tps.raw or {}
        perf = raw.get("performance_baseline") or {}
        value = perf.get("probe_timeout_sec")
        if value is None:
            return default
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        timeout = self._probe_timeout(tps, 3.0)
        # Truncated TPKT length claim — must not hang.
        junk = b"\x03\x00\x00\x10\x11"  # claims 16 bytes, only 1 follows
        raw, _, err = tcp_transact(host, port, junk, timeout=timeout, recv_first=False)
        if err and not raw and "timed out" in err.lower():
            ok = False
        elif not raw and not err:
            ok = True
        else:
            ok = bool(raw) or not err
        return [
            CheckResult(
                id="s7comm.fsm.truncated_tpkt",
                team="blue",
                passed=ok,
                detail=(
                    f"tpkt={is_tpkt(raw)} len={len(raw)}"
                    if raw
                    else (err or "closed")
                ),
                score=80.0 if ok else 0.0,
            )
        ]

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        strict = self._strict(tps)
        timeout = self._probe_timeout(tps, 4.0)
        cr = build_cotp_cr()
        raw, _, err = tcp_transact(host, port, cr, timeout=timeout, recv_first=False)
        ok = is_cotp_cc(raw) or (is_tpkt(raw) and b"\xd0" in raw[:16])
        detail = raw[:40].hex() if raw else (err or "no COTP CC")
        if ok:
            return [
                CheckResult(
                    id="s7comm.nego.cotp_cc",
                    team="blue",
                    critical=strict,
                    passed=True,
                    detail=f"COTP CC ok ({detail})",
                    score=100.0,
                )
            ]
        return [
            CheckResult(
                id="s7comm.nego.cotp_cc",
                team="blue",
                critical=strict,
                passed=False,
                detail=(
                    detail
                    + ("" if strict else " (Canary/Alert mode: not hard-failed)")
                ),
                score=0.0 if strict else 35.0,
            )
        ]

    def probe_state(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        """B1 — COTP CR/CC then S7 Setup Communication.

        Dual-engine: Strict RFC marks Setup failure ``critical``; Canary mode
        soft-scores decoys that only speak COTP (or ignore S7 PDUs).
        """
        strict = self._strict(tps)
        connect_timeout = self._probe_timeout(tps, 8.0)
        recv_timeout = self._probe_timeout(tps, 6.0)
        last_err = "no COTP CC before Setup"
        for _attempt in range(2):
            try:
                with socket.create_connection(
                    (host, int(port)), timeout=connect_timeout
                ) as s:
                    s.sendall(build_cotp_cr())
                    cc = _recv_all(s, timeout=recv_timeout)
                    if not (is_cotp_cc(cc) or (is_tpkt(cc) and b"\xd0" in cc[:16])):
                        last_err = (
                            f"no COTP CC before Setup: "
                            f"{cc[:40].hex() if cc else 'empty'}"
                        )
                        continue
                    s.sendall(build_s7_setup_communication())
                    setup = _recv_all(s, timeout=recv_timeout)
                    ok = is_s7_setup_ack(setup)
                    return [
                        CheckResult(
                            id="s7comm.state.setup_communication",
                            team="blue",
                            critical=strict,
                            passed=ok,
                            detail=(
                                (
                                    f"Setup ack ({setup[:48].hex()})"
                                    if ok
                                    else (
                                        f"no S7 Setup ack: "
                                        f"{setup[:48].hex() if setup else 'empty'}"
                                    )
                                )
                                + (
                                    ""
                                    if (ok or strict)
                                    else " (Canary/Alert mode: not hard-failed)"
                                )
                            ),
                            score=100.0 if ok else (0.0 if strict else 35.0),
                        )
                    ]
            except OSError as exc:
                last_err = str(exc)[:160]
                continue
        return [
            CheckResult(
                id="s7comm.state.setup_communication",
                team="blue",
                critical=strict,
                passed=False,
                detail=last_err,
                score=0.0 if strict else 35.0,
            )
        ]
