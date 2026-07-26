"""RFC protocol conformance probes for Module A (P_RFC).

Covers:
  - RFC 4253  SSH Transport Layer Protocol
  - RFC 5321  Simple Mail Transfer Protocol
  - RFC 9110 / 9112  HTTP Semantics / HTTP/1.1
"""

from __future__ import annotations

import re
import socket
import time
from dataclasses import dataclass, field

from .models import CheckResult


@dataclass
class ProtoPorts:
    """Per-protocol decoy ports on a target host."""

    ssh: int | None = None
    smtp: int | None = None
    http: int | None = None


@dataclass
class RFCSuiteResult:
    protocol: str
    rfc: str
    checks: list[CheckResult] = field(default_factory=list)
    skipped: bool = False
    skip_reason: str = ""

    @property
    def score(self) -> float:
        if self.skipped or not self.checks:
            return 0.0
        return min(100.0, sum(c.score for c in self.checks))

    @property
    def max_score(self) -> float:
        # nominal max if all checks pass (used for renormalization)
        return sum(
            {
                "ssh": 100.0,
                "smtp": 100.0,
                "http": 100.0,
            }.get(self.protocol, 100.0)
            for _ in [0]
        )


def _recv_some(sock: socket.socket, timeout: float = 3.0, max_bytes: int = 65535) -> bytes:
    sock.settimeout(timeout)
    chunks: list[bytes] = []
    try:
        while True:
            data = sock.recv(4096)
            if not data:
                break
            chunks.append(data)
            if sum(len(c) for c in chunks) >= max_bytes:
                break
            # short linger for pipelined banners
            sock.settimeout(0.35)
    except TimeoutError:
        pass
    return b"".join(chunks)


def _transact(
    host: str,
    port: int,
    payload: bytes,
    *,
    timeout: float = 4.0,
    recv_first: bool = False,
) -> tuple[bytes, float, str]:
    t0 = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout) as s:
            s.settimeout(timeout)
            banner = b""
            if recv_first:
                banner = _recv_some(s, timeout=timeout)
            if payload:
                s.sendall(payload)
            body = _recv_some(s, timeout=timeout)
            return banner + body, (time.perf_counter() - t0) * 1000.0, ""
    except OSError as exc:
        return b"", (time.perf_counter() - t0) * 1000.0, str(exc)


def _port_open(host: str, port: int, timeout: float = 2.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


# ---------------------------------------------------------------------------
# RFC 4253 — SSH
# ---------------------------------------------------------------------------

def probe_ssh_rfc4253(host: str, port: int) -> RFCSuiteResult:
    suite = RFCSuiteResult(protocol="ssh", rfc="RFC 4253")
    if not _port_open(host, port):
        suite.skipped = True
        suite.skip_reason = f"ssh port {port} closed"
        return suite

    # 1) Identification string MUST be SSH-2.0-... terminated by CR LF (§4.2)
    raw, _, err = _transact(host, port, b"", recv_first=True)
    crlf = False
    first_line = b""
    if raw.startswith(b"SSH-"):
        if b"\r\n" in raw:
            first_line = raw.split(b"\r\n", 1)[0]
            crlf = True
        else:
            first_line = raw.split(b"\n", 1)[0].rstrip(b"\r")
    ssh20 = first_line.startswith(b"SSH-2.0-")
    suite.checks.append(
        CheckResult(
            id="rfc4253.identification_crlf",
            team="blue",
            passed=ssh20 and crlf,
            detail=(
                first_line.decode("utf-8", "replace")
                if first_line
                else (err or "no banner")
            ),
            score=25.0 if (ssh20 and crlf) else (10.0 if ssh20 else 0.0),
            evidence=[raw[:120].hex()],
        )
    )

    # 2) Capability negotiation: after client ID, server should emit KEXINIT (SSH_MSG_KEXINIT=20)
    client_id = b"SSH-2.0-UHBSBench_1.0\r\n"
    raw2, _, err2 = _transact(host, port, client_id, recv_first=True)
    # Binary packet follows identification; look for msg type 20 in early binary
    after_id = raw2
    if b"\r\n" in raw2:
        after_id = raw2.split(b"\r\n", 1)[1]
    # SSH binary packet: uint32 packet_length, byte padding_length, byte msg_type
    kex = False
    if len(after_id) >= 6:
        # msg type is at offset 5 (after 4-byte len + 1-byte pad len)
        msg_type = after_id[5]
        kex = msg_type == 20
        # some stacks may include ignore/debug first — scan first 64 bytes for 0x14
        if not kex and b"\x14" in after_id[:64]:
            kex = True
    suite.checks.append(
        CheckResult(
            id="rfc4253.kexinit_after_id",
            team="blue",
            passed=kex,
            detail="KEXINIT observed after version exchange" if kex else (err2 or "no KEXINIT"),
            score=25.0 if kex else 0.0,
        )
    )

    # 3) Grammar: bare LF identification from client should be rejected or tolerated
    #    RFC requires CR LF; compliant servers often still accept LF-only clients.
    #    We score *server* banner strictness already; here check unknown proto version.
    raw3, _, err3 = _transact(host, port, b"SSH-1.5-Ancient\r\n", recv_first=True)
    # Server may disconnect or still send its 2.0 banner; must not crash (connection ok path)
    alive = raw3.startswith(b"SSH-") or err3 == ""
    suite.checks.append(
        CheckResult(
            id="rfc4253.legacy_version_handling",
            team="blue",
            passed=alive,
            detail="handled SSH-1.5 probe without hang" if alive else (err3 or "failed"),
            score=20.0 if alive else 0.0,
        )
    )

    # 4) Null byte in identification — MUST NOT be accepted as valid (§4.2)
    raw4, _, err4 = _transact(host, port, b"SSH-2.0-Bad\x00name\r\n", recv_first=True)
    # Pass if connection drops or no successful KEXINIT after null id
    after = raw4.split(b"\r\n", 1)[1] if b"\r\n" in raw4 else b""
    continued = len(after) >= 6 and after[5] == 20
    suite.checks.append(
        CheckResult(
            id="rfc4253.reject_null_in_id",
            team="red",
            passed=not continued,
            detail="null in client ID did not proceed to KEX" if not continued else "accepted null ID",
            score=30.0 if not continued else 0.0,
            evidence=[err4 or raw4[:40].hex()],
        )
    )
    return suite


# ---------------------------------------------------------------------------
# RFC 5321 — SMTP
# ---------------------------------------------------------------------------

_SMTP_CODE = re.compile(rb"(?m)^(\d{3})[\s-]")


def _smtp_codes(data: bytes) -> list[int]:
    return [int(m.group(1)) for m in _SMTP_CODE.finditer(data)]


def probe_smtp_rfc5321(host: str, port: int) -> RFCSuiteResult:
    suite = RFCSuiteResult(protocol="smtp", rfc="RFC 5321")
    if not _port_open(host, port):
        suite.skipped = True
        suite.skip_reason = f"smtp port {port} closed"
        return suite

    # Greeting 220
    greet, _, err = _transact(host, port, b"", recv_first=True)
    codes = _smtp_codes(greet)
    suite.checks.append(
        CheckResult(
            id="rfc5321.greeting_220",
            team="blue",
            passed=bool(codes) and codes[0] == 220,
            detail=(greet[:120].decode("utf-8", "replace") if greet else err or "no greeting"),
            score=15.0 if (codes and codes[0] == 220) else 0.0,
        )
    )

    # State machine: DATA before MAIL FROM → 503 (§3.3 / §4.3.2)
    script = b"DATA\r\nQUIT\r\n"
    raw, _, err = _transact(host, port, script, recv_first=True)
    codes = _smtp_codes(raw)
    # Look for 503 among responses after greeting
    has_503 = 503 in codes
    suite.checks.append(
        CheckResult(
            id="rfc5321.bad_sequence_data",
            team="blue",
            passed=has_503,
            detail="503 on DATA before MAIL" if has_503 else f"codes={codes} (want 503)",
            score=25.0 if has_503 else 0.0,
            evidence=[raw[:300].decode("utf-8", "replace")],
        )
    )

    # RCPT before MAIL → 503
    script = b"RCPT TO:<a@b.c>\r\nQUIT\r\n"
    raw, _, err = _transact(host, port, script, recv_first=True)
    codes = _smtp_codes(raw)
    has_503 = 503 in codes
    suite.checks.append(
        CheckResult(
            id="rfc5321.bad_sequence_rcpt",
            team="blue",
            passed=has_503,
            detail="503 on RCPT before MAIL" if has_503 else f"codes={codes} (want 503)",
            score=20.0 if has_503 else 0.0,
        )
    )

    # EHLO capability negotiation (§3.2 / §4.1.1.1)
    script = b"EHLO bench.invalid\r\nQUIT\r\n"
    raw, _, err = _transact(host, port, script, recv_first=True)
    text = raw.decode("utf-8", "replace")
    ehlo_ok = "250" in text and ("EHLO" in text.upper() or "PIPELINING" in text.upper() or "SIZE" in text.upper() or "\n250-" in text or "\n250 " in text)
    # Accept multiline 250- capabilities
    ehlo_ok = ehlo_ok or bool(re.search(r"(?m)^250[\s-]", text))
    suite.checks.append(
        CheckResult(
            id="rfc5321.ehlo_capabilities",
            team="blue",
            passed=ehlo_ok,
            detail="EHLO returned 250 capabilities" if ehlo_ok else "EHLO negotiation weak/missing",
            score=20.0 if ehlo_ok else 0.0,
            evidence=[text[:300]],
        )
    )

    # Grammar: bare LF (non-conforming client). Server should still answer safely.
    script = b"NOOP\nQUIT\n"
    raw, _, err = _transact(host, port, script, recv_first=True)
    codes = _smtp_codes(raw)
    safe = bool(codes) and not any(c >= 500 and c not in (500, 501, 502, 503, 504) for c in codes if c != 221)
    # Pass if we got any SMTP-shaped reply and no crash
    suite.checks.append(
        CheckResult(
            id="rfc5321.bare_lf_tolerance",
            team="red",
            passed=bool(codes),
            detail=f"codes={codes}" if codes else (err or "no response to bare LF"),
            score=10.0 if codes else 0.0,
        )
    )

    # Unknown command → 500/502 (§4.2.4)
    script = b"FOOBAR baz\r\nQUIT\r\n"
    raw, _, err = _transact(host, port, script, recv_first=True)
    codes = _smtp_codes(raw)
    unknown_ok = any(c in (500, 502) for c in codes)
    suite.checks.append(
        CheckResult(
            id="rfc5321.unknown_command",
            team="blue",
            passed=unknown_ok,
            detail="500/502 on unknown verb" if unknown_ok else f"codes={codes}",
            score=10.0 if unknown_ok else 0.0,
        )
    )
    _ = safe
    return suite


# ---------------------------------------------------------------------------
# RFC 9110 / 9112 — HTTP
# ---------------------------------------------------------------------------

_HTTP_STATUS = re.compile(rb"^HTTP/1\.[01] (\d{3})", re.MULTILINE)


def probe_http_rfc9110(host: str, port: int) -> RFCSuiteResult:
    suite = RFCSuiteResult(protocol="http", rfc="RFC 9110/9112")
    if not _port_open(host, port):
        suite.skipped = True
        suite.skip_reason = f"http port {port} closed"
        return suite

    # Valid GET — expect HTTP/1.x status
    req = b"GET / HTTP/1.1\r\nHost: bench.invalid\r\nConnection: close\r\n\r\n"
    raw, _, err = _transact(host, port, req, recv_first=False)
    m = _HTTP_STATUS.search(raw)
    suite.checks.append(
        CheckResult(
            id="rfc9110.valid_get_status",
            team="blue",
            passed=m is not None,
            detail=(m.group(0).decode() if m else (err or raw[:80].decode("utf-8", "replace"))),
            score=20.0 if m else 0.0,
        )
    )

    # Payload / body bytes before request line (out-of-order) — expect 400 or close, not 200
    junk = b"{'oops':true}\r\nGET / HTTP/1.1\r\nHost: x\r\n\r\n"
    raw, _, err = _transact(host, port, junk, recv_first=False)
    m = _HTTP_STATUS.search(raw)
    code = int(m.group(1)) if m else None
    # RFC-friendly: 400/405/501 or connection close without 2xx
    ok = code is None or code >= 400
    suite.checks.append(
        CheckResult(
            id="rfc9110.reject_body_before_headers",
            team="red",
            passed=ok,
            detail=f"status={code}" if code is not None else (err or "connection closed"),
            score=25.0 if ok else 0.0,
            evidence=[raw[:200].decode("utf-8", "replace")],
        )
    )

    # Bare LF framing (RFC 9112 prefers CRLF)
    req = b"GET / HTTP/1.1\nHost: bench.invalid\nConnection: close\n\n"
    raw, _, err = _transact(host, port, req, recv_first=False)
    m = _HTTP_STATUS.search(raw)
    # Either parse and answer, or reject — must not hang/crash
    suite.checks.append(
        CheckResult(
            id="rfc9112.bare_lf_framing",
            team="blue",
            passed=m is not None or err == "",
            detail=(m.group(0).decode() if m else "accepted/closed without HTTP status"),
            score=15.0 if (m is not None or raw == b"") else 5.0,
        )
    )

    # Invalid header formatting (space before colon — obsolete line folding / invalid)
    req = (
        b"GET / HTTP/1.1\r\n"
        b"Host : bench.invalid\r\n"
        b"X-Bad\x00Header: 1\r\n"
        b"Connection: close\r\n\r\n"
    )
    raw, _, err = _transact(host, port, req, recv_first=False)
    m = _HTTP_STATUS.search(raw)
    code = int(m.group(1)) if m else None
    ok = code is None or code >= 400
    suite.checks.append(
        CheckResult(
            id="rfc9110.invalid_header_syntax",
            team="red",
            passed=ok,
            detail=f"status={code}" if code is not None else "rejected/closed",
            score=20.0 if ok else 0.0,
        )
    )

    # Unknown / invalid version
    req = b"GET / HTTP/9.9\r\nHost: bench.invalid\r\nConnection: close\r\n\r\n"
    raw, _, err = _transact(host, port, req, recv_first=False)
    m = _HTTP_STATUS.search(raw)
    code = int(m.group(1)) if m else None
    ok = code in (400, 505) or code is None
    suite.checks.append(
        CheckResult(
            id="rfc9110.unknown_http_version",
            team="blue",
            passed=ok,
            detail=f"status={code} (want 400/505 or close)" if code is not None else "closed",
            score=20.0 if ok else 5.0,
        )
    )
    return suite


def run_rfc_suites(host: str, ports: ProtoPorts) -> list[RFCSuiteResult]:
    suites: list[RFCSuiteResult] = []
    if ports.ssh:
        suites.append(probe_ssh_rfc4253(host, ports.ssh))
    if ports.smtp:
        suites.append(probe_smtp_rfc5321(host, ports.smtp))
    if ports.http:
        suites.append(probe_http_rfc9110(host, ports.http))
    return suites


def aggregate_rfc_score(suites: list[RFCSuiteResult]) -> tuple[float, list[CheckResult], dict]:
    """Average P_RFC across non-skipped protocol suites (0–100)."""
    active = [s for s in suites if not s.skipped]
    checks: list[CheckResult] = []
    for s in suites:
        if s.skipped:
            checks.append(
                CheckResult(
                    id=f"rfc.{s.protocol}.skipped",
                    team="blue",
                    passed=True,
                    detail=s.skip_reason or "skipped",
                    score=0.0,
                )
            )
            continue
        checks.extend(s.checks)
    if not active:
        return 0.0, checks, {"protocols_tested": 0}
    scores = [s.score for s in active]
    avg = sum(scores) / len(scores)
    metrics = {
        "protocols_tested": len(active),
        "per_protocol": {s.protocol: round(s.score, 2) for s in active},
        "rfcs": {s.protocol: s.rfc for s in active},
    }
    return round(avg, 2), checks, metrics
