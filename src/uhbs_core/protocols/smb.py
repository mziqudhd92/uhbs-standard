from __future__ import annotations

import struct

from uhbs_core.models import CheckResult, TargetSpec
from uhbs_core.netutil import tcp_transact
from uhbs_core.protocols.base import ProtocolPlugin
from uhbs_core.tps import TPS

# --- SMB "Direct TCP transport" framing (MS-SMB2 §2.1) ---
#
# Root cause of the 2026-07-27 empty-response bug: even on TCP :445 (no
# legacy NBSS/NetBIOS session-establishment handshake), SMB messages are
# still wrapped in a 4-byte length-prefix header before the raw SMB PDU:
#   byte 0    = message type, MUST be 0x00 ("session message")
#   bytes 1-3 = big-endian 24-bit length of the following SMB message
# Without this prefix, a real SMB stack (confirmed live against Samba
# 4.13.7 / dperson-samba) reads the first 4 bytes of *our* raw SMB header
# ("\xffSMB") as if they were the length-prefix: byte0=0xff (invalid
# message type) and bytes1-3 decoded as a ~5MB length. Samba then blocks
# waiting to read that many bytes, hits EOF when we stop sending, and logs
# `read_fd_with_timeout ... NT_STATUS_END_OF_FILE` — which is exactly what
# was observed — and closes without ever replying. This is now fixed by
# wrapping every outbound SMB PDU below, and by stripping the same 4-byte
# prefix before inspecting the reply's SMB1/SMB2 magic bytes.


def _direct_tcp_wrap(smb_pdu: bytes) -> bytes:
    """Prepend the mandatory 4-byte Direct TCP transport length header."""
    if len(smb_pdu) > 0xFFFFFF:
        raise ValueError("SMB PDU too large for 24-bit Direct TCP length field")
    length_be24 = struct.pack(">I", len(smb_pdu))[1:]  # top 3 bytes, big-endian
    return b"\x00" + length_be24 + smb_pdu


def _direct_tcp_unwrap(data: bytes) -> bytes:
    """Strip the 4-byte Direct TCP transport header if present.

    Tolerant of a bare/short reply (some servers/canaries won't frame
    correctly either) — callers only use this to locate the SMB magic
    bytes, not to fully reassemble a message.
    """
    if len(data) >= 4 and data[0] == 0x00:
        return data[4:]
    return data


# Header (32 bytes): b"\xffSMB" + command(1) + status(4) + flags(1) +
# flags2(2) + pid_hi(2) + security(8) + reserved(2) + tid(2) + pid_lo(2) +
# uid(2) + mid(2)
_SMB1_HEADER = (
    b"\xff\x53\x4d\x42"  # \xffSMB
    + b"\x72"  # SMB_COM_NEGOTIATE
    + b"\x00\x00\x00\x00"  # status
    + b"\x18"  # flags
    + b"\x01\x00"  # flags2
    + b"\x00\x00"  # pid_hi
    + b"\x00" * 8  # security features
    + b"\x00\x00"  # reserved
    + b"\x00\x00"  # tid
    + b"\xff\xff"  # pid_lo
    + b"\x00\x00"  # uid
    + b"\x00\x00"  # mid
)

# Dialect list mirrors what real clients (and nmap's smb-os-discovery probe)
# offer — including "SMB 2.???", which is what makes a modern Samba/Windows
# server upgrade its *reply* to a native SMB2 NEGOTIATE response instead of
# an SMB1 one. Sending this real dialect list — not random bytes — is what
# lets us tell a genuine SMB stack apart from "TCP port is open."
_DIALECTS = [
    b"PC NETWORK PROGRAM 1.0",
    b"LANMAN1.0",
    b"Windows for Workgroups 3.1a",
    b"LM1.2X002",
    b"LANMAN2.1",
    b"NT LM 0.12",
    b"SMB 2.002",
    b"SMB 2.???",
]


def _build_negotiate_pdu() -> bytes:
    """Raw SMB1 NEGOTIATE PDU (no Direct TCP framing — see ``_build_negotiate_request``)."""
    body = b"".join(b"\x02" + d + b"\x00" for d in _DIALECTS)
    word_count = b"\x00"
    byte_count = struct.pack("<H", len(body))
    return _SMB1_HEADER + word_count + byte_count + body


def _build_negotiate_request() -> bytes:
    """Wire-ready SMB1 NEGOTIATE request: Direct TCP header + SMB1 PDU."""
    return _direct_tcp_wrap(_build_negotiate_pdu())


def _is_smb_header(data: bytes) -> tuple[bool, str]:
    """Return (is_real_smb, dialect_family) for a raw response.

    Strips the Direct TCP transport length-prefix first (see module
    docstring) before checking for the SMB1 (``\\xffSMB``) or SMB2/3
    (``\\xfeSMB``) magic bytes.
    """
    payload = _direct_tcp_unwrap(data)
    if len(payload) >= 4 and payload[:4] == b"\xfe\x53\x4d\x42":
        return True, "SMB2/3"
    if len(payload) >= 4 and payload[:4] == b"\xff\x53\x4d\x42":
        return True, "SMB1"
    return False, ""


class SMBPlugin(ProtocolPlugin):
    """SMB1/SMB2 dialect negotiation probe (IT).

    Architecture note (2026-07-27 review, round 1): this plugin previously
    returned ``passed=True`` unconditionally on the happy path — i.e. it
    measured "TCP port is open," not SMB negotiation, and could never fail.
    That is a false-positive risk for a benchmark harness and has been
    replaced with a real SMB1 NEGOTIATE request + response-header
    validation. The negotiation check is marked ``critical=True``: a target
    that cannot prove it holds a genuine SMB stack should not have its SMB
    grade "averaged up" by an unrelated passing check elsewhere in the list.

    Architecture note (round 2, same day): the first fix omitted the
    mandatory 4-byte "Direct TCP transport" length-prefix (MS-SMB2 §2.1)
    that wraps every SMB message even on TCP :445 with no legacy NBSS
    handshake. Live-verified against a real Samba 4.13.7 daemon: without
    the prefix, Samba read our raw SMB1 magic bytes as a bogus ~5MB length
    field and closed the connection (`NT_STATUS_END_OF_FILE` in smbd logs)
    without ever replying. Every outbound PDU is now wrapped via
    ``_direct_tcp_wrap`` / unwrapped via ``_direct_tcp_unwrap``.

    Named-state sequence (FSM formalization, see architecture review round
    2, item 3) — this plugin now follows an explicit, fail-fast sequence
    rather than independent probes:

        Connect -> Negotiate (Direct-TCP-framed SMB1 PDU) -> Assert
        SMB1/SMB2 magic bytes in the unwrapped reply

    ``probe_negotiation`` is the canonical implementation of that sequence;
    ``probe_fsm``/``probe_state`` reuse the same wrap/unwrap/assert helpers
    so the three hooks cannot silently drift out of sync with each other.
    """

    name = "smb"
    families = ("it",)

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        # Truncated/garbage frame — a well-behaved stack should not hang or
        # crash; it may reply with an SMB error header or simply close.
        raw, _, err = tcp_transact(host, port, b"\x00\x00\x00\x01\xff", timeout=3.0)
        if err:
            return [
                CheckResult(
                    id="smb.fsm.connect",
                    team="blue",
                    passed=False,
                    detail=err,
                    score=0.0,
                )
            ]
        is_smb, family = _is_smb_header(raw)
        # Silence/close on a malformed frame is an acceptable, non-crashing
        # outcome; an SMB-shaped error response is a stronger signal.
        ok = raw == b"" or is_smb
        return [
            CheckResult(
                id="smb.fsm.truncated_frame",
                team="blue",
                passed=ok,
                detail=(
                    f"smb_header={family}" if is_smb else f"resp={raw[:20]!r} (no crash/hang)"
                ),
                score=80.0 if is_smb else (60.0 if raw == b"" else 20.0),
            )
        ]

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        """Connect -> Negotiate -> Assert (see class docstring FSM)."""
        raw, _, err = tcp_transact(host, port, _build_negotiate_request(), timeout=3.0)
        if err:
            return [
                CheckResult(
                    id="smb.nego.dialect_header",
                    team="blue",
                    critical=self._critical(tps),
                    passed=False,
                    detail=err,
                    score=0.0 if self._critical(tps) else self._alert_partial_score(),
                )
            ]
        is_smb, family = _is_smb_header(raw)
        if is_smb:
            return [
                CheckResult(
                    id="smb.nego.dialect_header",
                    team="blue",
                    critical=self._critical(tps),
                    passed=True,
                    detail=f"real {family} negotiate response ({_direct_tcp_unwrap(raw)[:4]!r})",
                    score=100.0,
                )
            ]
        # No real SMB header — behavior differs by evaluation engine (see
        # Dual-Engine Evaluation Mode, architecture review round 2 item 1).
        return [
            CheckResult(
                id="smb.nego.dialect_header",
                team="blue",
                critical=self._critical(tps),
                passed=False,
                detail=(
                    f"no SMB1/SMB2 header in response — resp={raw[:20]!r}"
                    + ("" if self._critical(tps) else " (Canary/Alert mode: not hard-failed)")
                ),
                score=0.0 if self._critical(tps) else self._alert_partial_score(),
            )
        ]

    def probe_state(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        # Negotiate twice on independent connections — a real stack should
        # answer consistently (same dialect family) both times.
        raw1, _, err1 = tcp_transact(host, port, _build_negotiate_request(), timeout=3.0)
        raw2, _, err2 = tcp_transact(host, port, _build_negotiate_request(), timeout=3.0)
        ok1, fam1 = _is_smb_header(raw1)
        ok2, fam2 = _is_smb_header(raw2)
        ok = ok1 and ok2 and fam1 == fam2
        return [
            CheckResult(
                id="smb.state.consistent_negotiate",
                team="blue",
                passed=ok,
                detail=(
                    f"session1={fam1 or 'none'} session2={fam2 or 'none'} "
                    f"errs=({err1 or '-'},{err2 or '-'})"
                ),
                score=100.0 if ok else (30.0 if (ok1 or ok2) else 0.0),
            )
        ]

    # --- Dual-engine evaluation mode helpers -------------------------------
    #
    # Strict RFC Mode (default; TPS.strict_rfc_enforcement=True, which every
    # shipped TPS file sets today): missing the real SMB dialect header is
    # a hard critical-gate failure (score 0.0, trips the Module A/B circuit
    # breaker in uhbs_core.check_scoring).
    #
    # Canary/Alert Mode (TPS.strict_rfc_enforcement=False): for low-
    # interaction, log-only decoys that are not expected to implement full
    # SMB dialect negotiation, the same missing signal is scored as
    # explicit partial credit ("alert-only, not penalized as broken") and
    # NOT marked critical, so it cannot trip the circuit breaker — mirrors
    # the pattern already used for silent UDP protocols in udp_base.py.

    @staticmethod
    def _critical(tps: TPS | None) -> bool:
        return tps is None or tps.strict_rfc_enforcement

    @staticmethod
    def _alert_partial_score() -> float:
        return 35.0
