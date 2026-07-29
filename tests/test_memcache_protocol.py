"""Memcached text protocol plugin + offline stub probes."""

from __future__ import annotations

import socket
import threading

from uhbs_core.models import TargetSpec
from uhbs_core.protocols import get_plugin
from uhbs_core.protocols.memcache import (
    MemcachePlugin,
    build_get_command,
    build_set_command,
    is_memcache_error_reply,
    is_stats_reply,
    is_version_reply,
)
from uhbs_core.protocols.registry import register
from uhbs_core.tps import TPS


def _ensure_memcache_registered() -> None:
    register(MemcachePlugin())


def test_memcache_plugin_resolves() -> None:
    _ensure_memcache_registered()
    p = get_plugin("memcache")
    assert isinstance(p, MemcachePlugin)
    assert p.name == "memcache"


def test_set_and_get_framing() -> None:
    cmd = build_set_command(b"uhbs_marker", b"1", flags=0, exptime=60)
    assert cmd.startswith(b"set uhbs_marker 0 60 1\r\n")
    assert cmd.endswith(b"1\r\n")
    assert build_get_command(b"uhbs_marker") == b"get uhbs_marker\r\n"


def test_error_and_nego_parsers() -> None:
    assert is_memcache_error_reply(b"ERROR\r\n")
    assert is_memcache_error_reply(b"CLIENT_ERROR bad command line format\r\n")
    assert not is_memcache_error_reply(b"STORED\r\n")
    assert is_version_reply(b"VERSION 1.6.22\r\n")
    assert is_stats_reply(b"STAT pid 123\r\nEND\r\n")


def test_memcache_unreachable_does_not_raise() -> None:
    _ensure_memcache_registered()
    plugin = get_plugin("memcache")
    target = TargetSpec(
        name="x",
        host="127.0.0.1",
        port=1,
        protocol="memcache",
        protocols=["memcache"],
    )
    for probe in (
        plugin.probe_fsm,
        plugin.probe_negotiation,
        plugin.probe_state,
    ):
        checks = probe("127.0.0.1", 1, target, None)
        assert isinstance(checks, list)
        assert checks


def _serve_memcache_text() -> tuple[str, int, threading.Event, socket.socket]:
    store: dict[bytes, bytes] = {}
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
                    while True:
                        chunk = conn.recv(4096)
                        if not chunk:
                            break
                        buf += chunk
                        while b"\r\n" in buf:
                            line, buf = buf.split(b"\r\n", 1)
                            if not line:
                                continue
                            parts = line.split()
                            if not parts:
                                continue
                            verb = parts[0].upper()
                            if verb == b"VERSION":
                                conn.sendall(b"VERSION 1.0.0-uhbs-stub\r\n")
                                continue
                            if verb == b"STATS":
                                conn.sendall(b"STAT pid 1\r\nSTAT uptime 0\r\nEND\r\n")
                                continue
                            if verb == b"SET" and len(parts) >= 5:
                                key = parts[1]
                                nbytes = int(parts[4])
                                while len(buf) < nbytes + 2:
                                    more = conn.recv(4096)
                                    if not more:
                                        break
                                    buf += more
                                data = buf[:nbytes]
                                buf = buf[nbytes:]
                                if buf.startswith(b"\r\n"):
                                    buf = buf[2:]
                                store[key] = data
                                conn.sendall(b"STORED\r\n")
                                continue
                            if verb == b"GET":
                                keys = parts[1:]
                                out = b""
                                for key in keys:
                                    val = store.get(key)
                                    if val is not None:
                                        out += (
                                            b"VALUE "
                                            + key
                                            + b" 0 "
                                            + str(len(val)).encode("ascii")
                                            + b"\r\n"
                                            + val
                                            + b"\r\n"
                                        )
                                conn.sendall(out + b"END\r\n")
                                continue
                            if verb == b"QUIT":
                                break
                            conn.sendall(b"ERROR\r\n")
                except (TimeoutError, OSError):
                    pass

    threading.Thread(target=_loop, daemon=True).start()
    return host, port, stop, srv


def test_memcache_probes_against_stub() -> None:
    host, port, stop, srv = _serve_memcache_text()
    try:
        plugin = MemcachePlugin()
        target = TargetSpec(name="stub", host=host, port=port, protocol="memcache")
        tps = TPS(
            name="stub",
            profile_class="Low-Interaction",
            protocol="memcache",
            protocols=["memcache"],
            strict_rfc_enforcement=True,
        )

        fsm = plugin.probe_fsm(host, port, target, tps)
        assert len(fsm) == 1
        assert fsm[0].id == "memcache.fsm.invalid_verb"
        assert fsm[0].passed is True
        assert fsm[0].score >= 70.0

        nego = plugin.probe_negotiation(host, port, target, tps)
        by_id = {c.id: c for c in nego}
        assert by_id["memcache.nego.version"].passed
        assert by_id["memcache.nego.stats"].passed

        state = plugin.probe_state(host, port, target, tps)
        assert len(state) == 1
        assert state[0].id == "memcache.state.set_get"
        assert state[0].passed is True
    finally:
        stop.set()
        srv.close()
