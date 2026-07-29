from __future__ import annotations

import re

from uhbs_core.protocols.base import ProtocolPlugin

from ..models import CheckResult, TargetSpec
from ..rfc_probes import _port_open, _transact
from ..tps import TPS

_HTTP_STATUS = re.compile(rb"^HTTP/1\.[01] (\d{3})", re.MULTILINE)
# Safe absolute-form target — no successful egress required for scoring.
_SAFE_ABS_URI = b"http://bench.invalid/uhbs-proxy-probe"
_CONNECT_AUTHORITY = b"example.com:443"


def parse_http_status_code(raw: bytes) -> int | None:
    """First HTTP/1.x status code in ``raw``, if any."""
    m = _HTTP_STATUS.search(raw)
    return int(m.group(1)) if m else None


def is_connect_tunnel_established(raw: bytes) -> bool:
    """True when the reply looks like RFC 9110 §9.3.6 tunnel success (200)."""
    code = parse_http_status_code(raw)
    if code != 200:
        return False
    tail = raw[:160].lower()
    return b"connection established" in tail or raw.lstrip().startswith(b"HTTP/1.")


def _fsm_score_invalid_proxy_reply(raw: bytes) -> tuple[float, str]:
    code = parse_http_status_code(raw)
    tunnel = is_connect_tunnel_established(raw)
    if tunnel:
        return 15.0, f"status={code} (invalid request got CONNECT 200)"
    if code is not None and code >= 400:
        return 100.0, f"status={code}"
    if code is not None and code < 400:
        return 25.0, f"status={code} (expected 4xx for malformed proxy request)"
    if raw == b"":
        return 60.0, "connection closed without tunnel 200"
    return 30.0, raw[:100].decode("utf-8", "replace")


def _proxy_status_ok(raw: bytes, err: str) -> tuple[bool, float, str]:
    code = parse_http_status_code(raw)
    if code is not None:
        detail = f"HTTP/1.x status={code}"
        return True, 100.0, detail
    if raw:
        return False, 20.0, raw[:80].decode("utf-8", "replace")
    return False, 0.0, err or "no HTTP status line"


class HttpProxyPlugin(ProtocolPlugin):
    """RFC 9110/9112 forward HTTP proxy — absolute-form and CONNECT (§9.3.6)."""

    name = "httpproxy"
    families = ("it", "web")

    def _unreachable(self, hook: str, detail: str) -> list[CheckResult]:
        return [
            CheckResult(
                id=f"httpproxy.{hook}.unreachable",
                team="blue",
                passed=False,
                detail=detail,
                score=0.0,
            )
        ]

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        if not _port_open(host, port):
            return self._unreachable("fsm", f"httpproxy port {port} closed")

        invalid_connect = (
            b"CONNECT HTTP/1.1\r\n"
            b"Host: \r\n"
            b"Proxy-Connection: Keep-Alive\r\n\r\n"
        )
        raw_c, _, err_c = _transact(host, port, invalid_connect, recv_first=False)
        score_c, detail_c = _fsm_score_invalid_proxy_reply(raw_c)
        if not raw_c and err_c:
            detail_c = err_c

        bad_abs = (
            b"GET ://not-a-valid-uri HTTP/1.1\r\n"
            b"Host: bench.invalid\r\n"
            b"Connection: close\r\n\r\n"
        )
        raw_g, _, err_g = _transact(host, port, bad_abs, recv_first=False)
        score_g, detail_g = _fsm_score_invalid_proxy_reply(raw_g)
        if not raw_g and err_g:
            detail_g = err_g

        return [
            CheckResult(
                id="httpproxy.fsm.invalid_connect",
                team="red",
                passed=score_c >= 70.0,
                detail=detail_c,
                score=score_c,
                evidence=[raw_c[:200].decode("utf-8", "replace")] if raw_c else [],
            ),
            CheckResult(
                id="httpproxy.fsm.bad_absolute_uri",
                team="red",
                passed=score_g >= 70.0,
                detail=detail_g,
                score=score_g,
                evidence=[raw_g[:200].decode("utf-8", "replace")] if raw_g else [],
            ),
        ]

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        if not _port_open(host, port):
            return self._unreachable("nego", f"httpproxy port {port} closed")

        options_req = (
            b"OPTIONS " + _SAFE_ABS_URI + b" HTTP/1.1\r\n"
            b"Host: bench.invalid\r\n"
            b"Connection: close\r\n\r\n"
        )
        raw_o, _, err_o = _transact(host, port, options_req, recv_first=False)
        ok_o, score_o, detail_o = _proxy_status_ok(raw_o, err_o)

        get_req = (
            b"GET " + _SAFE_ABS_URI + b" HTTP/1.1\r\n"
            b"Host: bench.invalid\r\n"
            b"Connection: close\r\n\r\n"
        )
        raw_g, _, err_g = _transact(host, port, get_req, recv_first=False)
        ok_g, score_g, detail_g = _proxy_status_ok(raw_g, err_g)

        return [
            CheckResult(
                id="httpproxy.nego.options_absolute",
                team="blue",
                passed=ok_o,
                detail=detail_o,
                score=score_o,
                evidence=[raw_o[:200].decode("utf-8", "replace")] if raw_o else [],
            ),
            CheckResult(
                id="httpproxy.nego.get_absolute",
                team="blue",
                passed=ok_g,
                detail=detail_g,
                score=score_g,
                evidence=[raw_g[:200].decode("utf-8", "replace")] if raw_g else [],
            ),
        ]

    def probe_state(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        if not _port_open(host, port):
            return self._unreachable("state", f"httpproxy port {port} closed")

        connect_req = (
            b"CONNECT " + _CONNECT_AUTHORITY + b" HTTP/1.1\r\n"
            b"Host: " + _CONNECT_AUTHORITY + b"\r\n"
            b"Connection: close\r\n\r\n"
        )
        raw1, _, err1 = _transact(host, port, connect_req, recv_first=False)
        raw2, _, err2 = _transact(host, port, connect_req, recv_first=False)
        code1 = parse_http_status_code(raw1)
        code2 = parse_http_status_code(raw2)
        if code1 is not None and code1 == code2:
            ok = True
            score = 100.0
            detail = f"consistent CONNECT status={code1}"
        elif code1 is None and code2 is None and not raw1 and not raw2:
            ok = False
            score = 0.0
            detail = err1 or err2 or "no HTTP responses"
        elif code1 is not None and code2 is not None:
            ok = False
            score = 30.0
            detail = f"inconsistent CONNECT status {code1} vs {code2}"
        else:
            ok = False
            score = 20.0
            detail = (
                f"CONNECT replies code1={code1} code2={code2} "
                f"err1={err1[:40] if err1 else ''} err2={err2[:40] if err2 else ''}"
            )
        return [
            CheckResult(
                id="httpproxy.state.connect_consistent",
                team="blue",
                passed=ok,
                detail=detail,
                score=score,
                evidence=(
                    [
                        raw1[:120].decode("utf-8", "replace"),
                        raw2[:120].decode("utf-8", "replace"),
                    ]
                    if raw1 or raw2
                    else []
                ),
            )
        ]
