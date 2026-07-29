"""HP PJL (Printer Job Language) on raw TCP (JetDirect-style port 9100).

Wire references: HP PJL Technical Reference — UEL ``\\x1b%-12345X``,
``@PJL INFO ID``, ``@PJL ECHO``, job boundaries. Many listeners accept
bare ``@PJL ...\\r\\n`` without a leading UEL on port 9100.
"""

from __future__ import annotations

import re

from uhbs_core.models import CheckResult, TargetSpec
from uhbs_core.netutil import tcp_transact
from uhbs_core.protocols.base import ProtocolPlugin
from uhbs_core.tps import TPS

UEL = b"\x1b%-12345X"


def build_pjl_line(command: str, *, prefix_uel: bool = False) -> bytes:
    """Encode one PJL command line (CRLF-terminated)."""
    line = command if command.endswith("\r\n") else command + "\r\n"
    raw = line.encode("ascii", "replace")
    if prefix_uel:
        return UEL + raw
    return raw


def build_info_id(*, prefix_uel: bool = False) -> bytes:
    return build_pjl_line("@PJL INFO ID", prefix_uel=prefix_uel)


def build_echo(marker: str, *, prefix_uel: bool = False) -> bytes:
    safe = re.sub(r"[^\x20-\x7e]", "?", marker)[:64]
    return build_pjl_line(f'@PJL ECHO="{safe}"', prefix_uel=prefix_uel)


def _text(raw: bytes) -> str:
    return raw.decode("utf-8", "replace")


def is_pjl_error_response(text: str) -> bool:
    upper = text.upper()
    return "@PJL ERROR" in upper or ("@PJL" in upper and "UNKNOWN" in upper)


def info_id_response_ok(raw: bytes) -> bool:
    text = _text(raw)
    upper = text.upper()
    if "@PJL" not in upper:
        return False
    if "INFO ID" in upper:
        return True
    # Many devices return a quoted model string after INFO ID
    return '"' in text and len(text.strip()) >= 4


def echo_roundtrip_ok(raw: bytes, marker: str) -> bool:
    return marker in _text(raw)


def garbage_pjl_fidelity(raw: bytes, garbage: bytes, err: str) -> tuple[float, str]:
    """Score A1 — non-PJL garbage without UEL must not get a helpful PJL identity."""
    text = _text(raw)
    g = garbage.decode("ascii", "replace").strip().lower()
    if is_pjl_error_response(text):
        return 100.0, text[:120]
    if err and not raw:
        return 85.0, err[:120]
    if not raw and not err:
        return 85.0, "no response (ignored)"
    upper = text.upper()
    if "@PJL" in upper and ("INFO ID" in upper or ('"' in text and "ECHO" not in upper)):
        return 25.0, text[:120]
    if g and g in text.lower():
        return 35.0, text[:120]
    if raw:
        return 55.0, text[:120]
    return 70.0, err or "closed"


class PJLPlugin(ProtocolPlugin):
    """Raw TCP PJL / JetDirect printer decoys."""

    name = "pjl"
    families = ("it",)

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        garbage = b"UHBS_NOT_PJL_GARBAGE\xff\r\n"
        raw, _, err = tcp_transact(host, port, garbage, timeout=3.0, recv_first=False)
        score, detail = garbage_pjl_fidelity(raw, garbage, err)
        return [
            CheckResult(
                id="pjl.fsm.garbage_no_uel",
                team="blue",
                passed=score >= 70.0,
                detail=detail,
                score=score,
                **({"evidence": [_text(raw)[:400]]} if raw else {}),
            )
        ]

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        checks: list[CheckResult] = []

        id_raw, _, id_err = tcp_transact(
            host, port, build_info_id(), timeout=4.0, recv_first=False
        )
        id_ok = info_id_response_ok(id_raw)
        checks.append(
            CheckResult(
                id="pjl.nego.info_id",
                team="blue",
                passed=id_ok,
                detail=(
                    _text(id_raw)[:120]
                    if id_raw
                    else (id_err or "no INFO ID response")
                ),
                score=100.0 if id_ok else 0.0,
                **({"evidence": [_text(id_raw)[:400]]} if id_raw else {}),
            )
        )

        marker = "uhbs_nego_echo"
        echo_raw, _, echo_err = tcp_transact(
            host, port, build_echo(marker), timeout=4.0, recv_first=False
        )
        echo_ok = echo_roundtrip_ok(echo_raw, marker)
        checks.append(
            CheckResult(
                id="pjl.nego.echo",
                team="blue",
                passed=echo_ok,
                detail=(
                    _text(echo_raw)[:120]
                    if echo_raw
                    else (echo_err or "no ECHO response")
                ),
                score=100.0 if echo_ok else 0.0,
                **({"evidence": [_text(echo_raw)[:400]]} if echo_raw else {}),
            )
        )
        return checks

    def probe_state(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        marker = (target.annotations.get("pjl_echo_marker") or "uhbs_marker_rt").strip()
        if not marker:
            marker = "uhbs_marker_rt"
        raw, _, err = tcp_transact(
            host, port, build_echo(marker), timeout=4.0, recv_first=False
        )
        ok = echo_roundtrip_ok(raw, marker)
        return [
            CheckResult(
                id="pjl.state.echo_roundtrip",
                team="blue",
                passed=ok,
                detail=_text(raw)[:120] if raw else (err or "ECHO round-trip failed"),
                score=100.0 if ok else 20.0,
                **({"evidence": [_text(raw)[:400]]} if raw else {}),
            )
        ]
