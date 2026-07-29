"""MongoDB wire protocol plugin — offline framing tests + local stub."""

from __future__ import annotations

import socket
import struct
import threading

from uhbs_core.models import TargetSpec
from uhbs_core.protocols import get_plugin
from uhbs_core.protocols.mongodb import (
    MongoDBPlugin,
    build_hello_op_msg,
    build_invalid_opcode_frame,
    build_op_query_is_master,
    build_ping_op_msg,
    build_truncated_header,
    looks_like_hello_reply,
    looks_like_ping_reply,
    parse_msg_header,
)
from uhbs_core.protocols.registry import register


def _register_mongodb_plugin() -> None:
    register(MongoDBPlugin())


def test_mongodb_plugin_resolves() -> None:
    _register_mongodb_plugin()
    p = get_plugin("mongodb")
    assert isinstance(p, MongoDBPlugin)
    assert p.name == "mongodb"


def test_mongodb_unreachable_does_not_raise() -> None:
    _register_mongodb_plugin()
    target = TargetSpec(
        name="x",
        host="127.0.0.1",
        port=1,
        protocol="mongodb",
        protocols=["mongodb"],
    )
    plugin = get_plugin("mongodb")
    for probe in (plugin.probe_fsm, plugin.probe_negotiation, plugin.probe_state):
        checks = probe("127.0.0.1", 1, target, None)
        assert isinstance(checks, list)
        assert checks


def test_hello_and_query_framing() -> None:
    hello = build_hello_op_msg()
    hdr = parse_msg_header(hello)
    assert hdr is not None
    assert hdr["opcode"] == 2013
    assert hdr["length"] == len(hello)
    assert b"hello\x00" in hello
    assert b"admin" in hello

    query = build_op_query_is_master()
    qhdr = parse_msg_header(query)
    assert qhdr is not None
    assert qhdr["opcode"] == 2004
    assert b"admin.$cmd" in query
    assert b"isMaster" in query

    assert build_invalid_opcode_frame()[:4] == struct.pack("<i", 16)
    assert len(build_truncated_header()) == 8


def _build_stub_hello_bson() -> bytes:
    parts = [
        b"\x10ok\x00" + struct.pack("<i", 1),
        b"\x08isMaster\x00\x01",
        b"\x10maxWireVersion\x00" + struct.pack("<i", 17),
    ]
    body = b"".join(parts) + b"\x00"
    return struct.pack("<i", 4 + len(body)) + body


def _build_stub_ping_bson() -> bytes:
    parts = [b"\x10ok\x00" + struct.pack("<i", 1)]
    body = b"".join(parts) + b"\x00"
    return struct.pack("<i", 4 + len(body)) + body


def _reply_op_msg(doc: bytes, *, response_to: int) -> bytes:
    section = b"\x00" + doc
    body = struct.pack("<I", 0) + section
    length = 16 + len(body)
    header = struct.pack("<iiii", length, response_to, response_to, 2013)
    return header + body


def _reply_op_query(doc: bytes, *, response_to: int) -> bytes:
    flags = 0
    cursor_id = 0
    start = 0
    n = 1
    body = (
        struct.pack("<i", flags)
        + struct.pack("<q", cursor_id)
        + struct.pack("<ii", start, n)
        + doc
    )
    length = 16 + len(body)
    header = struct.pack("<iiii", length, response_to, response_to, 1)
    return header + body


def _serve_mongodb_stub() -> tuple[str, int, threading.Event, socket.socket]:
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 0))
    srv.listen(8)
    host, port = srv.getsockname()
    stop = threading.Event()
    hello_doc = _build_stub_hello_bson()
    ping_doc = _build_stub_ping_bson()

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
                    while True:
                        chunk = conn.recv(4096)
                        if not chunk:
                            break
                        buf += chunk
                        while len(buf) >= 16:
                            hdr = parse_msg_header(buf)
                            if hdr is None:
                                break
                            need = hdr["length"]
                            if len(buf) < need:
                                break
                            frame = buf[:need]
                            buf = buf[need:]
                            req_id = hdr["request_id"]
                            opcode = hdr["opcode"]
                            if opcode == 0x00DEAD00:
                                break
                            if opcode == 2013:
                                if b"ping\x00" in frame:
                                    conn.sendall(
                                        _reply_op_msg(ping_doc, response_to=req_id)
                                    )
                                else:
                                    conn.sendall(
                                        _reply_op_msg(hello_doc, response_to=req_id)
                                    )
                                continue
                            if opcode == 2004:
                                conn.sendall(
                                    _reply_op_query(hello_doc, response_to=req_id)
                                )
                                continue
                            conn.close()
                            break
                except (TimeoutError, OSError):
                    pass

    threading.Thread(target=_loop, daemon=True).start()
    return host, port, stop, srv


def test_mongodb_probes_against_stub() -> None:
    _register_mongodb_plugin()
    host, port, stop, srv = _serve_mongodb_stub()
    try:
        assert looks_like_hello_reply(_build_stub_hello_bson()) is False  # needs header
        plugin = MongoDBPlugin()
        target = TargetSpec(name="stub", host=host, port=port, protocol="mongodb")
        fsm = plugin.probe_fsm(host, port, target, None)
        nego = plugin.probe_negotiation(host, port, target, None)
        state = plugin.probe_state(host, port, target, None)
        assert all(c.passed for c in fsm), fsm
        assert all(c.passed for c in nego), nego
        assert state[0].id == "mongodb.state.hello_ping"
        assert state[0].passed
        assert looks_like_ping_reply(_reply_op_msg(_build_stub_ping_bson(), response_to=2))
    finally:
        stop.set()
        srv.close()


def test_offline_reply_heuristics() -> None:
    hello = _reply_op_msg(_build_stub_hello_bson(), response_to=1)
    ping = _reply_op_msg(_build_stub_ping_bson(), response_to=2)
    assert looks_like_hello_reply(hello)
    assert looks_like_ping_reply(ping)
    assert build_ping_op_msg()[12:16] == struct.pack("<i", 2013)
