"""PostgreSQL plugin framing helpers + offline stub probes."""

from __future__ import annotations

import socket
import struct
import threading

from uhbs_core.models import TargetSpec
from uhbs_core.protocols import get_plugin
from uhbs_core.protocols.postgres import (
    PostgresPlugin,
    build_password_message,
    build_ssl_request,
    build_startup_message,
)
from uhbs_core.tps import TPS


def test_postgres_plugin_resolves_and_alias() -> None:
    p = get_plugin("postgres")
    assert isinstance(p, PostgresPlugin)
    assert p.name == "postgres"
    assert get_plugin("postgresql").name == "postgres"


def test_startup_and_ssl_framing() -> None:
    startup = build_startup_message(user="alice", database="db1")
    assert startup[:4] == struct.pack("!I", len(startup))
    assert struct.unpack("!I", startup[4:8])[0] == 196608
    assert b"user\x00alice\x00" in startup
    assert b"database\x00db1\x00" in startup

    ssl = build_ssl_request()
    assert ssl == struct.pack("!II", 8, 80877103)

    pwd = build_password_message("secret")
    assert pwd[:1] == b"p"
    assert struct.unpack("!I", pwd[1:5])[0] == len(pwd) - 1


def test_postgres_nego_and_auth_deny_against_stub() -> None:
    # Multi-connection stub: SSL → 'N'; Startup → Auth cleartext; Password → ErrorResponse
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
                    first4 = conn.recv(4)
                    if len(first4) < 4:
                        continue
                    length = struct.unpack("!I", first4)[0]
                    rest = conn.recv(max(0, length - 4))
                    if length == 8 and rest == struct.pack("!I", 80877103):
                        conn.sendall(b"N")
                        continue
                    # Startup → AuthenticationCleartextPassword (type 3)
                    body = struct.pack("!I", 3)
                    conn.sendall(b"R" + struct.pack("!I", 8) + body)
                    # Optional password follow-up on same connection
                    try:
                        msg = conn.recv(65535)
                    except TimeoutError:
                        continue
                    if msg[:1] == b"p":
                        err = (
                            b"S"
                            + b"FATAL\x00"
                            + b"C"
                            + b"28P01\x00"
                            + b"M"
                            + b"password authentication failed\x00"
                            + b"\x00"
                        )
                        conn.sendall(b"E" + struct.pack("!I", 4 + len(err)) + err)
                except OSError:
                    pass
        srv.close()

    th = threading.Thread(target=_loop, daemon=True)
    th.start()
    try:
        target = TargetSpec(
            name="pg-stub",
            host=host,
            port=port,
            protocol="postgres",
            protocols=["postgres"],
        )
        tps = TPS(
            name="pg-stub",
            profile_class="Low-Interaction",
            protocol="postgres",
            protocols=["postgres"],
            strict_rfc_enforcement=True,
        )
        plugin = PostgresPlugin()
        nego = plugin.probe_negotiation(host, port, target, tps)
        assert {c.id for c in nego} >= {
            "postgres.nego.ssl_request",
            "postgres.nego.startup",
        }
        assert all(c.passed for c in nego), nego

        state = plugin.probe_state(host, port, target, tps)
        assert len(state) == 1
        assert state[0].id == "postgres.state.auth_deny"
        assert state[0].passed is True
        assert state[0].critical is True
    finally:
        stop.set()
        th.join(timeout=2.0)
