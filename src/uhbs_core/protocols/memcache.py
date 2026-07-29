from __future__ import annotations

from uhbs_core.protocols.base import ProtocolPlugin

from ..models import CheckResult, TargetSpec
from ..rfc_probes import _transact
from ..tps import TPS

_MARKER_KEY = b"uhbs_marker"


def build_set_command(
    key: bytes,
    value: bytes,
    *,
    flags: int = 0,
    exptime: int = 60,
) -> bytes:
    """Memcached text ``set`` with CRLF-terminated value block."""
    header = (
        b"set "
        + key
        + b" "
        + str(flags).encode("ascii")
        + b" "
        + str(exptime).encode("ascii")
        + b" "
        + str(len(value)).encode("ascii")
        + b"\r\n"
    )
    return header + value + b"\r\n"


def build_get_command(key: bytes) -> bytes:
    return b"get " + key + b"\r\n"


def is_memcache_error_reply(raw: bytes) -> bool:
    """True when the server emitted ERROR or CLIENT_ERROR (text protocol)."""
    for line in raw.splitlines():
        u = line.strip().upper()
        if u == b"ERROR" or u.startswith(b"CLIENT_ERROR"):
            return True
    return False


def is_version_reply(raw: bytes) -> bool:
    return b"VERSION" in raw.upper()


def is_stats_reply(raw: bytes) -> bool:
    upper = raw.upper()
    return b"STAT" in upper and b"END" in upper


class MemcachePlugin(ProtocolPlugin):
    """Memcached text protocol (get/set/stats/version/error replies)."""

    name = "memcache"
    families = ("it", "database")

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        raw, _, err = _transact(host, port, b"UHBS_INVALID_VERB\r\n", recv_first=False)
        text = raw.decode("utf-8", "replace")
        if is_memcache_error_reply(raw):
            score = 100.0
            detail = text[:120]
        elif raw == b"" or bool(err):
            score = 60.0
            detail = err or "connection closed on invalid verb (no ERROR reply)"
        else:
            score = 20.0
            detail = text[:120] or "unexpected reply to invalid verb"
        return [
            CheckResult(
                id="memcache.fsm.invalid_verb",
                team="blue",
                passed=score >= 70.0,
                detail=detail,
                score=score,
            )
        ]

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        checks: list[CheckResult] = []
        ver_raw, _, ver_err = _transact(host, port, b"version\r\n", recv_first=False)
        ver_text = ver_raw.decode("utf-8", "replace")
        ver_ok = is_version_reply(ver_raw)
        checks.append(
            CheckResult(
                id="memcache.nego.version",
                team="blue",
                passed=ver_ok,
                detail=ver_text[:80] if ver_text else (ver_err or "no version reply"),
                score=100.0 if ver_ok else 0.0,
            )
        )

        stats_raw, _, stats_err = _transact(host, port, b"stats\r\n", recv_first=False)
        stats_text = stats_raw.decode("utf-8", "replace")
        stats_ok = is_stats_reply(stats_raw)
        checks.append(
            CheckResult(
                id="memcache.nego.stats",
                team="blue",
                passed=stats_ok,
                detail=stats_text[:120] if stats_text else (stats_err or "no stats reply"),
                score=100.0 if stats_ok else 0.0,
            )
        )
        return checks

    def probe_state(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        script = build_set_command(_MARKER_KEY, b"1") + build_get_command(_MARKER_KEY)
        raw, _, err = _transact(host, port, script, recv_first=False)
        text = raw.decode("utf-8", "replace")
        upper = raw.upper()
        ok = (
            b"STORED" in upper
            and b"VALUE" in upper
            and _MARKER_KEY.upper() in upper
            and b"END" in upper
        )
        return [
            CheckResult(
                id="memcache.state.set_get",
                team="blue",
                passed=ok,
                detail=text[:160] if text else (err or "set/get failed"),
                score=100.0 if ok else 20.0,
            )
        ]
