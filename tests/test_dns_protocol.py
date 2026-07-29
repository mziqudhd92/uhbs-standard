"""DNS plugin — framing helpers + local UDP/TCP stub probes."""

from __future__ import annotations

import socket
import struct
import threading

from uhbs_core.models import TargetSpec
from uhbs_core.protocols import get_plugin, list_protocols
from uhbs_core.protocols.dns import (
    DNSPlugin,
    build_dns_query,
    encode_qname,
    parse_dns_header,
)
from uhbs_core.protocols.registry import register


def _ensure_dns_registered() -> None:
    register(DNSPlugin())


def test_dns_plugin_resolves_and_aliases() -> None:
    _ensure_dns_registered()
    assert "dns" in list_protocols()
    p = get_plugin("dns")
    assert isinstance(p, DNSPlugin)
    assert p.name == "dns"


def test_dns_framing_helpers() -> None:
    assert encode_qname(".") == b"\x00"
    assert encode_qname("example.com") == b"\x07example\x03com\x00"
    q = build_dns_query("example.com", txid=0x1234)
    assert len(q) > 12
    hdr = parse_dns_header(q)
    assert hdr is not None
    assert hdr["id"] == 0x1234
    assert hdr["qr"] == 0
    assert hdr["qdcount"] == 1


def test_dns_unreachable_does_not_raise() -> None:
    _ensure_dns_registered()
    t = TargetSpec(name="x", host="127.0.0.1", port=1, protocol="dns", protocols=["dns"])
    p = get_plugin("dns")
    for probe in (p.probe_fsm, p.probe_negotiation, p.probe_state):
        checks = probe("127.0.0.1", 1, t, None)
        assert isinstance(checks, list)
        assert checks


def _formerr(txid: int) -> bytes:
    return struct.pack("!HHHHHH", txid & 0xFFFF, 0x8101, 0, 0, 0, 0)


def _read_qname(data: bytes, offset: int) -> tuple[bytes, int] | None:
    """Return (wire qname bytes including root, next offset) or None."""
    start = offset
    while offset < len(data):
        ln = data[offset]
        offset += 1
        if ln == 0:
            return data[start:offset], offset
        if ln >= 192:
            return None
        offset += ln
    return None


def _serve_dns_udp() -> tuple[str, int, threading.Event, socket.socket]:
    srv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 0))
    host, port = srv.getsockname()
    stop = threading.Event()

    def _loop() -> None:
        srv.settimeout(0.5)
        while not stop.is_set():
            try:
                data, _addr = srv.recvfrom(65535)
            except TimeoutError:
                continue
            if len(data) < 12:
                txid = struct.unpack("!H", data[:2])[0] if len(data) >= 2 else 0
                srv.sendto(_formerr(txid), _addr)
                continue
            txid, flags, qd, an, ns, ar = struct.unpack("!HHHHHH", data[:12])
            if qd == 0 or qd > 1:
                srv.sendto(_formerr(txid), _addr)
                continue
            qname = _read_qname(data, 12)
            if qname is None:
                srv.sendto(_formerr(txid), _addr)
                continue
            qwire, end = qname
            if end + 4 > len(data):
                srv.sendto(_formerr(txid), _addr)
                continue
            qtype, qclass = struct.unpack("!HH", data[end : end + 4])
            question = data[12 : end + 4]
            # Minimal NOERROR response with one answer RR (A or AAAA).
            ans_rdata = b"\x5b\xb8\xd8\x22" if qtype == 1 else b"\x00" * 16
            ans_type = qtype if qtype in (1, 28) else 1
            answer = (
                b"\xc0\x0c"
                + struct.pack("!HHIH", ans_type, qclass, 60, len(ans_rdata))
                + ans_rdata
            )
            resp_flags = 0x8180  # QR=1, RD=1, RA=1, NOERROR
            header = struct.pack("!HHHHHH", txid, resp_flags, 1, 1, 0, 0)
            srv.sendto(header + question + answer, _addr)

    threading.Thread(target=_loop, daemon=True).start()
    return host, port, stop, srv


def _serve_dns_tcp(formerr_only: bool = False) -> tuple[str, int, threading.Event, socket.socket]:
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 0))
    srv.listen(8)
    host, port = srv.getsockname()
    stop = threading.Event()

    def _handle(conn: socket.socket) -> None:
        conn.settimeout(2.0)
        try:
            lenbuf = conn.recv(2)
            if len(lenbuf) < 2:
                return
            msg_len = struct.unpack("!H", lenbuf)[0]
            body = conn.recv(msg_len)
            if formerr_only or len(body) < 12:
                txid = struct.unpack("!H", body[:2])[0] if len(body) >= 2 else 0
                reply = _formerr(txid)
            else:
                txid = struct.unpack("!H", body[:2])[0]
                qname = _read_qname(body, 12)
                if qname is None:
                    reply = _formerr(txid)
                else:
                    qwire, end = qname
                    question = body[12 : end + 4]
                    answer = (
                        b"\xc0\x0c"
                        + struct.pack("!HHIH", 1, 1, 60, 4)
                        + b"\x5b\xb8\xd8\x22"
                    )
                    header = struct.pack("!HHHHHH", txid, 0x8180, 1, 1, 0, 0)
                    reply = header + question + answer
            conn.sendall(struct.pack("!H", len(reply)) + reply)
        except OSError:
            pass
        finally:
            conn.close()

    def _loop() -> None:
        srv.settimeout(0.5)
        while not stop.is_set():
            try:
                conn, _ = srv.accept()
            except TimeoutError:
                continue
            threading.Thread(target=_handle, args=(conn,), daemon=True).start()

    threading.Thread(target=_loop, daemon=True).start()
    return host, port, stop, srv


def test_dns_plugin_against_udp_stub() -> None:
    host, port, stop, srv = _serve_dns_udp()
    try:
        plugin = DNSPlugin()
        target = TargetSpec(name="stub", host=host, port=port, protocol="dns", protocols=["dns"])
        fsm = plugin.probe_fsm(host, port, target, None)
        by_id = {c.id: c for c in fsm}
        assert by_id["dns.fsm.truncated_header"].score >= 70.0
        assert by_id["dns.fsm.bad_qdcount"].score >= 70.0

        nego = plugin.probe_negotiation(host, port, target, None)
        udp_nego = next(c for c in nego if c.id == "dns.nego.udp_a")
        assert udp_nego.passed
        assert udp_nego.score >= 70.0

        state = plugin.probe_state(host, port, target, None)
        assert state[0].id == "dns.state.second_query"
        assert state[0].passed
    finally:
        stop.set()
        srv.close()


def test_dns_tcp_nego_against_stub() -> None:
    host, port, stop, srv = _serve_dns_tcp()
    try:
        plugin = DNSPlugin()
        target = TargetSpec(name="stub", host=host, port=port, protocol="dns", protocols=["dns"])
        nego = plugin.probe_negotiation(host, port, target, None)
        tcp_nego = next(c for c in nego if c.id == "dns.nego.tcp_a")
        assert tcp_nego.score >= 70.0
        assert tcp_nego.passed
    finally:
        stop.set()
        srv.close()
