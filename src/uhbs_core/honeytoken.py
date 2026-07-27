"""Honeytoken / out-of-band (OOB) telemetry validation groundwork.

Architecture-review item 3 (2026-07-27). Scoped honestly, per this
repository's "no fake pass" rule:

WHAT THIS MODULE IS
====================
A small library of realistic-*looking* honeytoken payloads
(:func:`generate_honeytoken`), a generic helper to embed one in whatever a
plugin is already sending (:func:`inject_honeytoken`), and a pluggable
"did an alert fire for this token" checker (:func:`verify_oob_alert`) with
one concrete adapter (:class:`FileTailLogSource`) plus a generic
:class:`CallbackLogSource` escape hatch for anything else (webhook poll,
SIEM query, …).

WHAT THIS MODULE IS **NOT**
============================
It is **not** a zero-config honeytoken detector. UHBS's lab harness has no
standard way to reach into a honeypot's actual alerting backend — that is
operator-specific (a JSON log file, a webhook, a SIEM query). We searched
the existing codebase for a reusable log-tailing utility before writing
this: the closest existing precedent is ``uhbs_core.test_safety``'s D1
egress-gateway-canary check, which reads an operator-provided path from
``UHBS_EGRESS_GATEWAY_LOG`` and scans for lines containing ``HIT``. That
check is single-purpose (egress-gateway canary hits, not honeytoken IDs)
and lives inside Module D's safety-gate scoring, so we do not import or
repurpose it here — instead we follow the *same convention*
(operator supplies a path/callback; we do not invent log-file discovery)
in a honeytoken-specific, standalone adapter.

Full honeytoken/OOB testing therefore requires the harness operator to
point :func:`verify_oob_alert` at the honeypot's actual alert log file (via
:class:`FileTailLogSource`) or alerting pipeline (via
:class:`CallbackLogSource` wrapping, e.g., a webhook poll or SIEM query).
This module provides the plumbing, not a magic detector — and it is
deliberately **opt-in**: nothing here is called from any existing plugin's
default probe path, so no existing test suddenly requires a log source.

The generated honeytoken *values* below (fake AWS-access-key-shaped
strings, fake API tokens, a bait-file-path convention) are randomly
generated, syntactically-plausible decoys — they are not provisioned in
any real cloud account and will not, by themselves, trigger any live
third-party leak-detection service. Their only job is to look enticing
enough for an attacker/scanner script to try to use, log, or exfiltrate —
detection of that attempt is entirely the honeypot's/operator's job, which
is exactly the OOB gap this module's docstring is being honest about.
"""

from __future__ import annotations

import os
import secrets
import string
import time
import uuid
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .models import CheckResult

# --- honeytoken generation ---------------------------------------------------

_ALNUM_UPPER = string.ascii_uppercase + string.digits
_HEX = string.hexdigits[:16]  # 0-9a-f


def _rand(alphabet: str, n: int) -> str:
    return "".join(secrets.choice(alphabet) for _ in range(n))


def _new_token_id() -> str:
    return f"uhbs-{uuid.uuid4().hex[:16]}"


@dataclass
class Honeytoken:
    token_id: str
    kind: str
    value: str
    # Secondary field for kinds that pair a public/secret value (e.g. AWS
    # access key id + secret key) — empty string when not applicable.
    secondary_value: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


def _make_aws_access_key(token_id: str) -> Honeytoken:
    # AKIA-prefixed 20-char access key id is the standard AWS *shape* (this
    # is a well-known public format, not a secret we're leaking) — the
    # value itself is freshly random and not tied to any real account.
    access_key_id = "AKIA" + _rand(_ALNUM_UPPER, 16)
    secret_key = _rand(string.ascii_letters + string.digits + "+/", 40)
    return Honeytoken(
        token_id=token_id,
        kind="aws_access_key",
        value=access_key_id,
        secondary_value=secret_key,
        metadata={"format": "aws_access_key_id+secret_access_key", "region_hint": "us-east-1"},
    )


def _make_api_token(token_id: str) -> Honeytoken:
    value = "sk_live_" + _rand(_HEX, 32)
    return Honeytoken(token_id=token_id, kind="api_token", value=value)


def _make_bait_file(token_id: str) -> Honeytoken:
    # Convention, not a real system file — the "_bait" suffix + embedded
    # token id both signal "this is UHBS's canary," should the honeypot's
    # own log ever need to disambiguate multiple concurrent probe runs.
    canary_string = f"UHBS-CANARY-{token_id}"
    path = f"/etc/shadow_bait_{token_id}"
    return Honeytoken(
        token_id=token_id,
        kind="bait_file",
        value=path,
        secondary_value=canary_string,
        metadata={"canary_string": canary_string},
    )


_GENERATORS: dict[str, Callable[[str], Honeytoken]] = {
    "aws_access_key": _make_aws_access_key,
    "api_token": _make_api_token,
    "bait_file": _make_bait_file,
}


def generate_honeytoken(kind: str = "api_token", *, token_id: str | None = None) -> Honeytoken:
    """Generate one realistic-*looking* honeytoken payload.

    ``kind`` in {"aws_access_key", "api_token", "bait_file"}.
    """
    if kind not in _GENERATORS:
        raise ValueError(f"unknown honeytoken kind {kind!r}; choose from {sorted(_GENERATORS)}")
    return _GENERATORS[kind](token_id or _new_token_id())


# --- injection ---------------------------------------------------------------


def inject_honeytoken(
    session_send_fn: Callable[[str], Any],
    token: Honeytoken,
    *,
    render: Callable[[Honeytoken], str] | None = None,
) -> str:
    """Embed ``token`` in whatever a plugin is already sending.

    ``session_send_fn`` is any protocol-specific "send this string" closure
    the calling plugin already has (write to an SSH command, an HTTP
    header/body, an FTP filename, …) — this helper does not know or care
    about the protocol; it just renders the token to text (via ``render``,
    defaulting to ``token.value``) and calls the callback once.

    Returns ``token.token_id`` so the caller can later pass the same id to
    :func:`verify_oob_alert`.
    """
    text = render(token) if render is not None else token.value
    session_send_fn(text)
    return token.token_id


# --- pluggable "did an alert fire" log source --------------------------------


class LogSource(ABC):
    """Abstract, pluggable "does an alert referencing this token exist" check.

    UHBS has no standard alert-log format, so this is intentionally a thin
    interface — implement it against whatever the honeypot under test
    actually exposes (file, webhook poll, SIEM API, …).
    """

    @abstractmethod
    def check(self, token_id: str) -> tuple[bool, str]:
        """Return ``(found, detail)``. Called repeatedly by
        :func:`verify_oob_alert` until ``timeout_s`` elapses or ``found``.
        """


class FileTailLogSource(LogSource):
    """Default adapter: poll a local file for a line mentioning ``token_id``.

    Only considers bytes appended *after* construction (tracked via the
    file size at ``__init__`` time), so a stale historical log entry from
    an earlier run cannot produce a false "alert fired" result — this
    mirrors the intent, though not the code, of the existing D1
    egress-gateway-log check in ``test_safety.py`` (see module docstring).
    """

    def __init__(self, path: str | Path):
        self.path = Path(path)
        try:
            self._start_offset = self.path.stat().st_size
        except OSError:
            self._start_offset = 0

    def check(self, token_id: str) -> tuple[bool, str]:
        if not self.path.is_file():
            return False, f"log file not found: {self.path}"
        try:
            with self.path.open("rb") as f:
                f.seek(self._start_offset)
                new_bytes = f.read()
        except OSError as exc:
            return False, f"log read error: {exc}"
        text = new_bytes.decode("utf-8", errors="replace")
        for line in text.splitlines():
            if token_id in line:
                return True, line.strip()[:200]
        return False, "no matching line yet"


class CallbackLogSource(LogSource):
    """Generic escape hatch: wrap any operator-supplied ``check`` callable.

    Use this for a webhook poll, a SIEM query, or anything else UHBS has
    no built-in adapter for. The callback must have the same
    ``(token_id) -> (found, detail)`` shape as :meth:`LogSource.check`.
    """

    def __init__(self, fn: Callable[[str], tuple[bool, str]]):
        self._fn = fn

    def check(self, token_id: str) -> tuple[bool, str]:
        return self._fn(token_id)


def verify_oob_alert(
    log_source: LogSource,
    token_id: str,
    timeout_s: float = 0.5,
    *,
    poll_interval_s: float = 0.05,
) -> CheckResult:
    """Poll ``log_source`` for an alert mentioning ``token_id`` within
    ``timeout_s``. Honest by construction: with no ``log_source`` wired to
    a real honeypot alert channel, this will simply — correctly — report
    "no alert observed," not a fabricated pass.
    """
    start = time.monotonic()
    last_detail = "no alert observed"
    while True:
        found, detail = log_source.check(token_id)
        if found:
            return CheckResult(
                id="honeytoken.oob_alert",
                team="blue",
                passed=True,
                detail=detail or f"alert for token_id={token_id} observed",
                score=100.0,
                evidence=[detail[:200]] if detail else [],
            )
        if detail:
            last_detail = detail
        elapsed = time.monotonic() - start
        if elapsed >= timeout_s:
            break
        time.sleep(min(poll_interval_s, max(0.0, timeout_s - elapsed)))
    return CheckResult(
        id="honeytoken.oob_alert",
        team="blue",
        passed=False,
        detail=f"no alert for token_id={token_id} within {timeout_s}s ({last_detail})",
        score=0.0,
    )


def file_tail_log_source_from_env(env_var: str = "UHBS_HONEYTOKEN_LOG") -> LogSource | None:
    """Convenience: build a :class:`FileTailLogSource` from an env var,
    mirroring the ``UHBS_EGRESS_GATEWAY_LOG`` convention already used by
    Module D's safety-gate check, but for a separate, honeytoken-specific
    variable so the two concerns never collide. Returns ``None`` if unset
    — callers should treat that as "OOB verification not configured,"
    not as a failure.
    """
    path = os.environ.get(env_var, "").strip()
    return FileTailLogSource(path) if path else None
