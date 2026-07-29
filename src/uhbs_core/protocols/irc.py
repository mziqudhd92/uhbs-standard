from __future__ import annotations

import re
import socket

from uhbs_core.protocols.base import ProtocolPlugin

from ..models import CheckResult, TargetSpec
from ..rfc_probes import _recv_some, _transact
from ..tps import TPS

_NUMERIC_RE = re.compile(r"(?:^|\s)(\d{3})(?:\s|$)")


def extract_irc_numerics(text: str) -> list[int]:
    """Return IRC three-digit reply codes present in ``text`` (RFC 1459 / 2812)."""
    out: list[int] = []
    for line in text.splitlines():
        for match in _NUMERIC_RE.finditer(line):
            code = int(match.group(1))
            if 1 <= code <= 599:
                out.append(code)
    return out


def build_irc_registration(
    nick: str, user: str, realname: str, *, mode: str = "0", unused: str = "*"
) -> bytes:
    """NICK + USER registration sequence (RFC 2812 §3.1)."""
    nick_b = nick.encode("utf-8", "replace")
    user_b = user.encode("utf-8", "replace")
    real_b = realname.encode("utf-8", "replace")
    mode_b = mode.encode("ascii", "replace")
    unused_b = unused.encode("ascii", "replace")
    return (
        b"NICK " + nick_b + b"\r\nUSER " + user_b + b" " + mode_b + b" " + unused_b + b" :" + real_b + b"\r\n"
    )


def _decode_text(raw: bytes) -> str:
    return raw.decode("utf-8", "replace")


def _irc_lines(raw: bytes) -> list[str]:
    return [ln.strip() for ln in _decode_text(raw).splitlines() if ln.strip()]


def _looks_like_irc_line(line: str) -> bool:
    if line.startswith(":"):
        return True
    return bool(_NUMERIC_RE.search(line))


def _fsm_rejection(raw: bytes, err: str) -> tuple[float, str]:
    """Score invalid-command handling: ERROR / 4xx–5xx / clean close."""
    text = _decode_text(raw)
    upper = text.upper()
    nums = extract_irc_numerics(text)
    has_error_cmd = " ERROR " in f" {upper} " or upper.startswith("ERROR ")
    has_err_numeric = any(400 <= n < 600 for n in nums)
    closed_cleanly = raw == b"" and bool(err)
    if has_error_cmd or has_err_numeric:
        detail = text[:160] if text else f"numeric={nums}"
        return 100.0, detail
    if closed_cleanly:
        return 60.0, err or "connection closed on invalid input (no IRC ERROR/numeric)"
    if text and _looks_like_irc_line(_irc_lines(raw)[0] if _irc_lines(raw) else ""):
        return 40.0, text[:160]
    if text:
        return 20.0, text[:160]
    return 0.0, err or "no response"


def _ping_token(line: str) -> str | None:
    upper = f" {line.strip().upper()} "
    if " PING " not in upper:
        return None
    idx = upper.index(" PING ")
    rest = line.strip()[idx + 5 :].strip()
    if not rest:
        return None
    return rest.split()[0].lstrip(":")


def _irc_session(
    host: str,
    port: int,
    outbound: bytes,
    *,
    answer_ping: bool = True,
    timeout: float = 4.0,
) -> tuple[bytes, str]:
    """One TCP session: optional initial recv, PONG on server PING, then ``outbound``."""
    chunks: list[bytes] = []
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            sock.settimeout(timeout)
            initial = _recv_some(sock, timeout=min(timeout, 1.0))
            if initial:
                chunks.append(initial)
            if answer_ping and initial:
                for line in _irc_lines(initial):
                    token = _ping_token(line)
                    if token:
                        sock.sendall(f"PONG {token}\r\n".encode("ascii", "replace"))
                        chunks.append(_recv_some(sock, timeout=0.5))
                        break
            if outbound:
                sock.sendall(outbound)
                chunks.append(_recv_some(sock, timeout=timeout))
        return b"".join(chunks), ""
    except OSError as exc:
        return b"".join(chunks), str(exc)


class IRCPlugin(ProtocolPlugin):
    """RFC 1459 / RFC 2812 IRC — line-oriented registration and numeric replies."""

    name = "irc"
    families = ("it",)

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        raw, _, err = _transact(
            host,
            port,
            b"@@@UHBS_NOT_A_COMMAND\r\n",
            recv_first=True,
            timeout=4.0,
        )
        score, detail = _fsm_rejection(raw, err)
        return [
            CheckResult(
                id="irc.fsm.invalid_command",
                team="blue",
                passed=score >= 70.0,
                detail=detail,
                score=score,
                evidence=[raw[:400].decode("utf-8", "replace")] if raw else [],
            )
        ]

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        banner_raw, err_b = _irc_session(host, port, b"", answer_ping=True)
        banner_text = _decode_text(banner_raw)
        lines = _irc_lines(banner_raw)
        has_banner = any(
            ln.upper().find(" NOTICE ") >= 0 or ln.upper().find(" MOTD ") >= 0 for ln in lines
        ) or any(ln.startswith(":") for ln in lines)
        ping_seen = any("PING" in ln.upper() for ln in lines)
        pong_sent = ping_seen and b"PONG" in banner_raw
        banner_ok = has_banner or pong_sent or (bool(lines) and _looks_like_irc_line(lines[0]))

        nick = (target.user or "uhbsprobe").split("@")[0][:16]
        reg = build_irc_registration(nick, nick, "uhbs probe")
        reg_raw, err_r = _irc_session(host, port, reg, answer_ping=True)
        reg_text = _decode_text(reg_raw)
        nums = extract_irc_numerics(reg_text)
        welcome = any(1 <= n <= 5 for n in nums)
        reg_err = any(400 <= n < 600 for n in nums)
        reg_ok = welcome or reg_err

        banner_score = 100.0 if banner_ok else (35.0 if err_b and not banner_raw else 0.0)
        reg_score = 100.0 if reg_ok else (20.0 if reg_text else (0.0 if err_r else 10.0))

        return [
            CheckResult(
                id="irc.nego.banner_or_ping",
                team="blue",
                passed=banner_score >= 70.0,
                detail=banner_text[:120] if banner_text else (err_b or "no banner"),
                score=banner_score,
                evidence=[banner_text[:200]] if banner_text else [],
            ),
            CheckResult(
                id="irc.nego.registration_numerics",
                team="blue",
                passed=reg_score >= 70.0,
                detail=f"numerics={nums}" if nums else (reg_text[:120] if reg_text else (err_r or "none")),
                score=reg_score,
                evidence=[reg_text[:400]] if reg_text else [],
            ),
        ]

    def probe_state(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        nick = (target.user or "uhbsstate").split("@")[0][:16]
        reg = build_irc_registration(nick, nick, "uhbs state probe")
        raw, err = _irc_session(host, port, reg, answer_ping=True)
        text = _decode_text(raw)
        nums = extract_irc_numerics(text)
        welcome = any(1 <= n <= 5 for n in nums)
        nick_err = any(431 <= n <= 436 for n in nums)
        not_reg = 451 in nums
        ok = welcome or nick_err or (not_reg and len(nums) >= 1)
        detail = f"numerics={nums}" if nums else (text[:120] if text else (err or "no reply"))
        score = 100.0 if welcome else (70.0 if nick_err else (50.0 if ok else 20.0))
        return [
            CheckResult(
                id="irc.state.nick_user_handshake",
                team="blue",
                passed=score >= 70.0,
                detail=detail,
                score=score,
                evidence=[text[:400]] if text else [],
            )
        ]
