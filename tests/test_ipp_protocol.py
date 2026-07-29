"""IPP plugin framing + local HTTP/IPP stub probes."""

from __future__ import annotations

import socket
import struct
import threading

from uhbs_core.models import TargetSpec
from uhbs_core.protocols import get_plugin
from uhbs_core.protocols.ipp import (
    IppPlugin,
    build_get_printer_attributes_request,
    build_http_ipp_post,
    build_ipp_message,
    build_malformed_ipp_request,
    ipp_status_code,
    is_client_error_ipp,
    is_successful_ipp,
    split_http_response,
)
from uhbs_core.protocols.registry import register


def test_ipp_plugin_resolves_and_aliases() -> None:
    register(IppPlugin())
    p = get_plugin("ipp")
    assert isinstance(p, IppPlugin)
    assert p.name == "ipp"
    assert get_plugin("ipps").name == "ipp"


def test_ipp_framing_helpers_offline() -> None:
    req = build_get_printer_attributes_request("ipp://127.0.0.1/ipp/print")
    assert req[:2] == b"\x01\x01"
    assert struct.unpack("!H", req[2:4])[0] == 0x000B
    assert req.endswith(b"\x03")
    assert b"printer-uri" in req
    assert b"attributes-charset" in req

    bad = build_malformed_ipp_request()
    assert bad[:2] == b"\x02\x00"

    http = build_http_ipp_post(req, host="127.0.0.1:631")
    assert http.startswith(b"POST /ipp/print HTTP/1.1")
    assert b"Content-Type: application/ipp" in http
    assert http.endswith(req)

    ok_body = build_ipp_message(
        operation_or_status=0x0000,
        request_id=1,
        attribute_groups=bytes([0x04, 0x03]),
    )
    assert is_successful_ipp(ipp_status_code(ok_body))
    assert is_client_error_ipp(0x0400)


def test_ipp_unreachable_does_not_raise() -> None:
    register(IppPlugin())
    target = TargetSpec(name="x", host="127.0.0.1", port=1, protocol="ipp")
    plugin = get_plugin("ipp")
    for fn in (plugin.probe_fsm, plugin.probe_negotiation):
        checks = fn("127.0.0.1", 1, target, None)
        assert isinstance(checks, list)
        assert checks


def _serve_ipp_stub() -> tuple[str, int, threading.Event, socket.socket]:
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 0))
    srv.listen(8)
    host, port = srv.getsockname()
    stop = threading.Event()

    def _ipp_response(status: int, request_id: int) -> bytes:
        body = build_ipp_message(
            operation_or_status=status,
            request_id=request_id,
            attribute_groups=bytes([0x04, 0x03]),
        )
        return (
            b"HTTP/1.1 200 OK\r\n"
            b"Content-Type: application/ipp\r\n"
            + f"Content-Length: {len(body)}\r\n".encode()
            + b"Connection: close\r\n\r\n"
            + body
        )

    def _client_error(status: int, request_id: int, http_code: int = 400) -> bytes:
        body = build_ipp_message(
            operation_or_status=status,
            request_id=request_id,
            attribute_groups=bytes([0x04, 0x03]),
        )
        return (
            f"HTTP/1.1 {http_code} Bad Request\r\n".encode()
            + b"Content-Type: application/ipp\r\n"
            + f"Content-Length: {len(body)}\r\n".encode()
            + b"Connection: close\r\n\r\n"
            + body
        )

    def _loop() -> None:
        srv.settimeout(0.5)
        while not stop.is_set():
            try:
                conn, _ = srv.accept()
            except TimeoutError:
                continue
            with conn:
                conn.settimeout(2.0)
                try:
                    buf = b""
                    while b"\r\n\r\n" not in buf and len(buf) < 65536:
                        chunk = conn.recv(4096)
                        if not chunk:
                            break
                        buf += chunk
                    if b"\r\n\r\n" not in buf:
                        continue
                    header, rest = buf.split(b"\r\n\r\n", 1)
                    clen = 0
                    for line in header.decode("latin-1", "replace").split("\r\n"):
                        if line.lower().startswith("content-length:"):
                            clen = int(line.split(":", 1)[1].strip())
                    body = rest
                    while len(body) < clen:
                        more = conn.recv(4096)
                        if not more:
                            break
                        body += more
                    body = body[:clen]

                    if len(body) < 4:
                        conn.sendall(_client_error(0x0400, 1))
                        continue
                    major, minor = body[0], body[1]
                    op = struct.unpack("!H", body[2:4])[0]
                    req_id = struct.unpack("!I", body[4:8])[0] if len(body) >= 8 else 1

                    if major != 1 or minor != 1:
                        conn.sendall(_client_error(0x040B, req_id))
                        continue
                    if body[:4] == b"\xff\xfe\xfd\xfc":
                        conn.sendall(_client_error(0x0400, req_id))
                        continue
                    if op == 0x000B:
                        conn.sendall(_ipp_response(0x0000, req_id))
                    else:
                        conn.sendall(_client_error(0x0400, req_id))
                except (TimeoutError, OSError, ValueError):
                    pass

    threading.Thread(target=_loop, daemon=True).start()
    return host, port, stop, srv


def test_ipp_plugin_against_stub() -> None:
    host, port, stop, srv = _serve_ipp_stub()
    try:
        plugin = IppPlugin()
        target = TargetSpec(name="stub", host=host, port=port, protocol="ipp")
        fsm = plugin.probe_fsm(host, port, target, None)
        nego = plugin.probe_negotiation(host, port, target, None)
        by_id = {c.id: c for c in fsm + nego}
        assert by_id["ipp.fsm.version_not_supported"].passed
        assert by_id["ipp.fsm.malformed_body"].passed
        assert by_id["ipp.nego.get_printer_attributes"].passed
        assert by_id["ipp.nego.get_printer_attributes"].score >= 70.0

        # Round-trip parse on a synthetic response
        req = build_get_printer_attributes_request(f"ipp://{host}:{port}/ipp/print")
        raw = build_http_ipp_post(req, host=f"{host}:{port}")
        from uhbs_core.rfc_probes import _transact

        resp, _, _ = _transact(host, port, raw, recv_first=False)
        http_st, body = split_http_response(resp)
        assert http_st == 200
        assert is_successful_ipp(ipp_status_code(body))
    finally:
        stop.set()
        srv.close()
