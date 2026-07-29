"""HTTP forward-proxy plugin — offline helpers + local TCP stub."""

from __future__ import annotations

import socket
import threading

from uhbs_core.models import TargetSpec
from uhbs_core.protocols import get_plugin
from uhbs_core.protocols.httpproxy import (
    HttpProxyPlugin,
    is_connect_tunnel_established,
    parse_http_status_code,
)
from uhbs_core.protocols.registry import register


def test_httpproxy_plugin_resolves() -> None:
    register(HttpProxyPlugin())
    p = get_plugin("httpproxy")
    assert isinstance(p, HttpProxyPlugin)
    assert p.name == "httpproxy"


def test_httpproxy_helpers_offline() -> None:
    assert parse_http_status_code(b"HTTP/1.1 502 Bad Gateway\r\n\r\n") == 502
    assert parse_http_status_code(b"garbage") is None
    assert is_connect_tunnel_established(
        b"HTTP/1.1 200 Connection established\r\n\r\n"
    )
    assert not is_connect_tunnel_established(b"HTTP/1.1 403 Forbidden\r\n\r\n")


def test_httpproxy_unreachable_does_not_raise() -> None:
    plugin = HttpProxyPlugin()
    target = TargetSpec(
        name="closed",
        host="127.0.0.1",
        port=1,
        protocol="httpproxy",
        protocols=["httpproxy"],
    )
    for hook in (
        plugin.probe_fsm,
        plugin.probe_negotiation,
        plugin.probe_state,
    ):
        checks = hook("127.0.0.1", 1, target, None)
        assert isinstance(checks, list)
        assert len(checks) >= 1
        assert all(c.id.startswith("httpproxy.") for c in checks)


def _serve_forward_proxy() -> tuple[str, int, threading.Event, socket.socket]:
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 0))
    srv.listen(8)
    host, port = srv.getsockname()
    stop = threading.Event()

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
                    while b"\r\n\r\n" not in buf and len(buf) < 8192:
                        chunk = conn.recv(4096)
                        if not chunk:
                            break
                        buf += chunk
                    first = buf.split(b"\r\n", 1)[0].decode("ascii", "replace")
                    parts = first.split()
                    method = parts[0].upper() if parts else ""
                    target = parts[1] if len(parts) > 1 else ""

                    if method == "CONNECT" and target.upper() == "HTTP/1.1":
                        conn.sendall(b"HTTP/1.1 400 Bad Request\r\nConnection: close\r\n\r\n")
                    elif method == "CONNECT" and target == "example.com:443":
                        conn.sendall(b"HTTP/1.1 403 Forbidden\r\nConnection: close\r\n\r\n")
                    elif method == "GET" and target.startswith("://"):
                        conn.sendall(b"HTTP/1.1 400 Bad Request\r\nConnection: close\r\n\r\n")
                    elif method == "OPTIONS":
                        conn.sendall(
                            b"HTTP/1.1 200 OK\r\n"
                            b"Allow: GET, HEAD, OPTIONS, CONNECT\r\n"
                            b"Connection: close\r\n\r\n"
                        )
                    elif method == "GET" and target.startswith("http://"):
                        conn.sendall(b"HTTP/1.1 502 Bad Gateway\r\nConnection: close\r\n\r\n")
                    else:
                        conn.sendall(b"HTTP/1.1 501 Not Implemented\r\nConnection: close\r\n\r\n")
                except (TimeoutError, OSError):
                    pass

    threading.Thread(target=_loop, daemon=True).start()
    return host, port, stop, srv


def test_httpproxy_probes_against_stub() -> None:
    host, port, stop, srv = _serve_forward_proxy()
    try:
        plugin = HttpProxyPlugin()
        target = TargetSpec(name="stub", host=host, port=port, protocol="httpproxy")
        fsm = {c.id: c for c in plugin.probe_fsm(host, port, target, None)}
        assert fsm["httpproxy.fsm.invalid_connect"].passed
        assert fsm["httpproxy.fsm.invalid_connect"].score >= 70.0
        assert fsm["httpproxy.fsm.bad_absolute_uri"].passed

        nego = {c.id: c for c in plugin.probe_negotiation(host, port, target, None)}
        assert nego["httpproxy.nego.options_absolute"].passed
        assert nego["httpproxy.nego.get_absolute"].passed
        assert nego["httpproxy.nego.get_absolute"].score == 100.0

        state = plugin.probe_state(host, port, target, None)
        assert state[0].id == "httpproxy.state.connect_consistent"
        assert state[0].passed
        assert "403" in state[0].detail
    finally:
        stop.set()
        srv.close()


def test_fsm_fails_when_stub_accepts_invalid_connect_tunnel() -> None:
    """Regression: invalid CONNECT must not score as tunnel 200."""
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 0))
    srv.listen(1)
    host, port = srv.getsockname()
    stop = threading.Event()

    def _bad() -> None:
        conn, _ = srv.accept()
        with conn:
            conn.recv(4096)
            conn.sendall(b"HTTP/1.1 200 Connection established\r\n\r\n")

    threading.Thread(target=_bad, daemon=True).start()
    try:
        plugin = HttpProxyPlugin()
        target = TargetSpec(name="bad", host=host, port=port, protocol="httpproxy")
        fsm = plugin.probe_fsm(host, port, target, None)
        invalid = next(c for c in fsm if c.id == "httpproxy.fsm.invalid_connect")
        assert not invalid.passed
        assert invalid.score < 70.0
    finally:
        stop.set()
        srv.close()
