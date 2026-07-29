"""PJL plugin framing helpers + local stub probes."""

from __future__ import annotations

import re
import socket
import threading

from uhbs_core.models import TargetSpec
from uhbs_core.protocols import get_plugin, register
from uhbs_core.protocols.pjl import (
    UEL,
    PJLPlugin,
    build_echo,
    build_info_id,
    build_pjl_line,
    echo_roundtrip_ok,
    garbage_pjl_fidelity,
    info_id_response_ok,
    is_pjl_error_response,
)


def test_pjl_plugin_resolves_and_aliases() -> None:
    register(PJLPlugin())
    p = get_plugin("pjl")
    assert isinstance(p, PJLPlugin)
    assert p.name == "pjl"


def test_pjl_framing_helpers_offline() -> None:
    assert UEL == b"\x1b%-12345X"
    assert build_pjl_line("@PJL INFO ID") == b"@PJL INFO ID\r\n"
    assert build_info_id(prefix_uel=True).startswith(UEL)
    assert build_echo("x", prefix_uel=False).startswith(b'@PJL ECHO="x"')
    assert is_pjl_error_response("@PJL ERROR CODE=10001\r\n")
    assert info_id_response_ok(b'@PJL INFO ID\r\n"Model 9"\r\n')
    assert echo_roundtrip_ok(b'@PJL ECHO="uhbs_nego_echo"\r\n', "uhbs_nego_echo")
    score, _ = garbage_pjl_fidelity(b"", b"garbage\r\n", "")
    assert score >= 70.0
    score_bad, _ = garbage_pjl_fidelity(
        b'@PJL INFO ID\r\n"Fake"\r\n', b"garbage\r\n", ""
    )
    assert score_bad < 70.0


def test_pjl_unreachable_does_not_raise() -> None:
    target = TargetSpec(name="x", host="127.0.0.1", port=1, protocol="pjl")
    plugin = PJLPlugin()
    for probe in (plugin.probe_fsm, plugin.probe_negotiation, plugin.probe_state):
        checks = probe("127.0.0.1", 1, target, None)
        assert isinstance(checks, list)
        assert checks
        assert all(hasattr(c, "score") for c in checks)


def _serve_pjl(
    *, echo_garbage_as_info: bool = False
) -> tuple[str, int, threading.Event, socket.socket]:
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
                    data = conn.recv(8192)
                    if not data:
                        continue
                    text = data.decode("utf-8", "replace")
                    upper = text.upper()
                    if "INFO ID" in upper:
                        conn.sendall(b'@PJL INFO ID\r\n"UHBS Stub Printer"\r\n')
                        continue
                    echo_m = re.search(r'ECHO="([^"]*)"', text, re.I)
                    if echo_m or "ECHO" in upper:
                        marker = echo_m.group(1) if echo_m else "uhbs"
                        conn.sendall(f'@PJL ECHO="{marker}"\r\n'.encode())
                        continue
                    if "@PJL" not in upper and UEL not in data:
                        if echo_garbage_as_info:
                            conn.sendall(b'@PJL INFO ID\r\n"Fake"\r\n')
                        else:
                            conn.sendall(b"@PJL ERROR CODE=10001\r\n")
                        continue
                    conn.sendall(b"@PJL ERROR CODE=10002\r\n")
                except (TimeoutError, OSError):
                    pass

    threading.Thread(target=_loop, daemon=True).start()
    return host, port, stop, srv


def test_pjl_probes_against_stub() -> None:
    host, port, stop, srv = _serve_pjl()
    try:
        target = TargetSpec(
            name="pjl-stub",
            host=host,
            port=port,
            protocol="pjl",
            protocols=["pjl"],
            annotations={"pjl_echo_marker": "uhbs_state_marker"},
        )
        plugin = PJLPlugin()
        fsm = plugin.probe_fsm(host, port, target, None)
        assert fsm[0].id == "pjl.fsm.garbage_no_uel"
        assert fsm[0].passed

        nego = plugin.probe_negotiation(host, port, target, None)
        by_id = {c.id: c for c in nego}
        assert by_id["pjl.nego.info_id"].passed
        assert by_id["pjl.nego.echo"].passed

        state = plugin.probe_state(host, port, target, None)
        assert state[0].id == "pjl.state.echo_roundtrip"
        assert state[0].passed
    finally:
        stop.set()
        srv.close()


def test_pjl_fsm_fails_when_garbage_gets_info_id() -> None:
    host, port, stop, srv = _serve_pjl(echo_garbage_as_info=True)
    try:
        plugin = PJLPlugin()
        target = TargetSpec(name="bad", host=host, port=port, protocol="pjl")
        fsm = plugin.probe_fsm(host, port, target, None)
        assert fsm[0].passed is False
        assert fsm[0].score < 70.0
    finally:
        stop.set()
        srv.close()
