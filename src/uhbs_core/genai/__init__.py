"""Experimental GenAI/MCP helpers — canaries, leak scan, coherence, timing, safety."""

from __future__ import annotations

import re
import secrets
from dataclasses import dataclass, field
from typing import Any

__all__ = [
    "CanarySpec",
    "GenAISafetyPolicy",
    "LEAK_PATTERNS",
    "LeakResult",
    "generate_prompt_canary",
    "parse_sse_ttft_ms",
    "percentiles",
    "scan_for_leak",
    "score_coherence",
    "tarpit_penalize_high_latency",
]

# Shared with MCP plugin patterns; keep local copy to avoid import cycles.
LEAK_PATTERNS: tuple[str, ...] = (
    "system prompt",
    "you are a honeypot",
    "ignore previous instructions",
    "uhbs-canary-",
    "hidden policy",
)


@dataclass(frozen=True)
class CanarySpec:
    token_id: str
    nonce: str
    embedded_in: str = "tool_arg"

    @property
    def marker(self) -> str:
        return f"UHBS-CANARY-{self.token_id}-{self.nonce}"


@dataclass
class LeakResult:
    leaked: bool
    matches: list[str] = field(default_factory=list)


@dataclass
class GenAISafetyPolicy:
    injection_budget: int = 12
    allow_live: bool = False
    name_denylist: frozenset[str] = frozenset(
        {"exec", "shell", "rm", "delete", "write_file", "run_command"}
    )

    def assert_probe_allowed(self, *, tool_name: str | None, attempts_used: int) -> str | None:
        """Return skip reason or None if allowed."""
        if attempts_used >= self.injection_budget:
            return "injection budget exhausted"
        if tool_name and tool_name.lower() in self.name_denylist:
            return f"tool denylisted: {tool_name}"
        return None


def generate_prompt_canary(*, run_id: str = "") -> CanarySpec:
    token_id = (run_id or "run")[:12] + secrets.token_hex(4)
    nonce = secrets.token_hex(8)
    return CanarySpec(token_id=token_id, nonce=nonce, embedded_in="tool_arg")


def scan_for_leak(
    text: str,
    canary: CanarySpec | None = None,
    *,
    patterns: tuple[str, ...] = LEAK_PATTERNS,
) -> LeakResult:
    blob = text or ""
    lower = blob.lower()
    matches: list[str] = []
    for pat in patterns:
        if pat.lower() in lower:
            matches.append(pat)
    if canary and canary.marker.lower() in lower:
        matches.append(canary.marker)
    if canary and canary.nonce.lower() in lower:
        matches.append(f"nonce:{canary.nonce}")
    return LeakResult(leaked=bool(matches), matches=matches)


def score_coherence(turns: list[dict[str, Any]]) -> tuple[int, int, float | None]:
    """Return (consistent, total, rate). Each turn needs expected + actual keys."""
    if not turns:
        return 0, 0, None
    consistent = 0
    for turn in turns:
        expected = turn.get("expected")
        actual = turn.get("actual")
        if expected is None or actual is None:
            continue
        if str(expected).strip() == str(actual).strip():
            consistent += 1
    total = len(turns)
    rate = round(consistent / total, 4) if total else None
    return consistent, total, rate


def percentiles(
    samples: list[float],
    ps: tuple[float, ...] = (50.0, 95.0),
) -> dict[str, float | None]:
    if not samples:
        return {f"p{int(p)}": None for p in ps}
    ordered = sorted(float(x) for x in samples)
    out: dict[str, float | None] = {}
    n = len(ordered)
    for p in ps:
        if n == 1:
            out[f"p{int(p)}"] = ordered[0]
            continue
        k = (p / 100.0) * (n - 1)
        f = int(k)
        c = min(f + 1, n - 1)
        if f == c:
            out[f"p{int(p)}"] = ordered[f]
        else:
            out[f"p{int(p)}"] = ordered[f] + (ordered[c] - ordered[f]) * (k - f)
    return out


def parse_sse_ttft_ms(chunks: list[tuple[float, bytes]]) -> float | None:
    """Given (elapsed_ms, chunk) pairs, return time of first SSE data line."""
    for elapsed_ms, chunk in chunks:
        text = chunk.decode("utf-8", errors="replace")
        if re.search(r"(?m)^data:\s*\S", text):
            return float(elapsed_ms)
    # Fallback: first non-comment, non-empty chunk
    for elapsed_ms, chunk in chunks:
        text = chunk.decode("utf-8", errors="replace").strip()
        if text and not text.startswith(":"):
            return float(elapsed_ms)
    return None


def tarpit_penalize_high_latency(timing_intent: str) -> bool:
    return timing_intent.strip().lower() != "tarpit"
