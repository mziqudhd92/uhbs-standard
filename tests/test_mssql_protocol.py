"""TDS (MssqlPlugin) framing helpers + offline stub probes."""

from __future__ import annotations

import socket
import struct
import threading

from uhbs_core.models import TargetSpec
from uhbs_core.protocols.mssql import (
    MssqlPlugin,
    build_prelogin_packet,
    format_prelogin_detail,
    parse_prelogin_options,
    tds_packet_length,
    tds_packet_type,
)
from uhbs_core.protocols.registry import get_plugin, register
from uhbs_core.tps import TPS


def test_mssql_plugin_resolves() -> None:
    register(MssqlPlugin())
    p = get_plugin("mssql")
    assert isinstance(p, MssqlPlugin)
    assert p.name == "mssql"


def test_mssql_aliases_resolve() -> None:
    register(MssqlPlugin())
    for alias in ("tds", "sqlserver", "sql-server"):
        assert get_plugin(alias).name == "mssql"


def test_prelogin_framing_and_parse_roundtrip() -> None:
    pkt = build_prelogin_packet(encryption=0x02)
    assert pkt[0] == 0x12
    assert pkt[1] == 0x01
    assert struct.unpack(">H", pkt[2:4])[0] == len(pkt)
    assert tds_packet_type(pkt) == 0x12
    assert tds_packet_length(pkt) == len(pkt)

    opts = parse_prelogin_options(pkt)
    assert 0x00 in opts
    assert len(opts[0x00]) == 6
    assert opts[0x01] == bytes([0x02])
    assert format_prelogin_detail(opts).startswith("VERSION=")
    assert "ENCRYPTION=ENCRYPT_NOT_SUP" in format_prelogin_detail(opts)


def test_mssql_unreachable_does_not_raise() -> None:
    target = TargetSpec(
        name="x",
        host="127.0.0.1",
        port=1,
        protocol="mssql",
        protocols=["mssql"],
    )
    plugin = MssqlPlugin()
    fsm = plugin.probe_fsm("127.0.0.1", 1, target, None)
    nego = plugin.probe_negotiation("127.0.0.1", 1, target, None)
    assert isinstance(fsm, list) and fsm
    assert isinstance(nego, list) and nego
    assert fsm[0].id == "mssql.fsm.invalid_framing"


def test_mssql_nego_and_fsm_against_stub() -> None:
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 0))
    srv.listen(8)
    host, port = srv.getsockname()
    stop = threading.Event()
    prelogin_reply = build_prelogin_packet(encryption=0x00)

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
                    data = conn.recv(4096)
                    if not data:
                        continue
                    if data and data[0] == 0x12 and len(data) >= 8:
                        conn.sendall(prelogin_reply)
                    # garbage / truncated — close without hanging
                except OSError:
                    pass
        srv.close()

    th = threading.Thread(target=_loop, daemon=True)
    th.start()
    try:
        target = TargetSpec(
            name="tds-stub",
            host=host,
            port=port,
            protocol="mssql",
            protocols=["mssql"],
        )
        tps = TPS(
            name="tds-stub",
            profile_class="Low-Interaction",
            protocol="mssql",
            protocols=["mssql"],
            strict_rfc_enforcement=True,
        )
        plugin = MssqlPlugin()
        fsm = plugin.probe_fsm(host, port, target, tps)
        assert fsm[0].passed is True

        nego = plugin.probe_negotiation(host, port, target, tps)
        assert len(nego) == 1
        assert nego[0].id == "mssql.nego.prelogin"
        assert nego[0].passed is True
        assert "ENCRYPTION=ENCRYPT_OFF" in nego[0].detail
    finally:
        stop.set()
        th.join(timeout=2.0)
