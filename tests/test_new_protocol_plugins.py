"""Smoke tests for new protocol plugins (offline / no live target)."""

from __future__ import annotations

from uhbs_core.models import TargetSpec
from uhbs_core.protocols import get_plugin
from uhbs_core.protocols.smb import (
    _build_negotiate_request,
    _direct_tcp_unwrap,
    _direct_tcp_wrap,
    _is_smb_header,
)
from uhbs_core.protocols.telnet import _negate_options


def test_new_plugins_resolve() -> None:
    for name in ("mysql", "rdp", "sip", "snmp", "ntp", "tftp", "vnc", "git", "smb"):
        p = get_plugin(name)
        assert p.name == name


def test_udp_plugins_survive_unreachable() -> None:
    t = TargetSpec(name="x", host="127.0.0.1", port=1, protocol="sip", protocols=["sip"])
    for name in ("sip", "snmp", "ntp", "tftp"):
        p = get_plugin(name)
        # Port 1 unlikely to accept; plugins must not raise
        checks = p.probe_negotiation("127.0.0.1", 1, t, None)
        assert isinstance(checks, list)
        assert checks


def test_smb_header_matcher_rejects_non_smb_bytes() -> None:
    # Architecture-review regression guard: this must NEVER be a hardcoded
    # True — random bytes must not look like a real SMB1/SMB2 header.
    is_smb, family = _is_smb_header(b"HTTP/1.1 200 OK\r\n")
    assert is_smb is False
    assert family == ""


def test_smb_header_matcher_accepts_real_smb_markers() -> None:
    is_smb1, fam1 = _is_smb_header(b"\xff\x53\x4d\x42\x72\x00\x00\x00\x00")
    is_smb2, fam2 = _is_smb_header(b"\xfe\x53\x4d\x42\x40\x00\x00\x00")
    assert is_smb1 and fam1 == "SMB1"
    assert is_smb2 and fam2 == "SMB2/3"


def test_smb_negotiate_request_is_well_formed() -> None:
    # Regression guard for the 2026-07-27 empty-response bug: every outbound
    # SMB PDU must be wrapped in the 4-byte Direct TCP transport length
    # header (type=0x00 + 24-bit big-endian length) BEFORE the raw SMB1
    # header, or a real SMB stack (live-verified against Samba 4.13.7)
    # misreads our SMB magic bytes as a bogus length and hangs/closes
    # without replying.
    req = _build_negotiate_request()
    assert req[0] == 0x00  # Direct TCP transport message type
    smb_len = int.from_bytes(req[1:4], "big")
    pdu = req[4:]
    assert smb_len == len(pdu)
    assert pdu[:4] == b"\xff\x53\x4d\x42"  # \xffSMB
    assert pdu[4] == 0x72  # SMB_COM_NEGOTIATE
    assert b"NT LM 0.12" in pdu
    assert b"SMB 2.???" in pdu


def test_direct_tcp_wrap_roundtrip() -> None:
    pdu = b"\xff\x53\x4d\x42\x72" + b"\x00" * 10
    framed = _direct_tcp_wrap(pdu)
    assert framed[:4] == b"\x00\x00\x00\x0f"
    assert _direct_tcp_unwrap(framed) == pdu
    # Unframed/bare data (no 0x00 type byte) passes through untouched —
    # tolerant of servers/canaries that reply without the wrapper.
    assert _direct_tcp_unwrap(pdu) == pdu


def test_telnet_negate_options_replies_do_with_wont() -> None:
    # Server sends IAC DO ECHO (option 1); we must reply IAC WONT ECHO.
    server_frame = bytes([0xFF, 0xFD, 0x01])
    reply = _negate_options(server_frame)
    assert reply == bytes([0xFF, 0xFC, 0x01])


def test_telnet_negate_options_replies_will_with_dont() -> None:
    server_frame = bytes([0xFF, 0xFB, 0x03])  # IAC WILL SUPPRESS-GA
    reply = _negate_options(server_frame)
    assert reply == bytes([0xFF, 0xFE, 0x03])
