"""Response jitter / timing side-channel metrics (opt-in scorer).

Architecture-review item 4 (2026-07-27).

Formula (as specified by the reviewer)::

    S_jitter = 1 - abs(sigma_decoy - sigma_real) / sigma_real

...scaled to 0-100 and clipped at both ends. ``sigma_real`` is a
*configurable* reference standard deviation for what "realistic" jitter
looks like for a given operation class — see :data:`REFERENCE_JITTER_SIGMA_MS`.

HONESTY NOTE — these reference constants are illustrative, not measured
=========================================================================
The values in :data:`REFERENCE_JITTER_SIGMA_MS` (e.g. "~5-50ms for
auth/hash operations", "~0.1-2ms for simple echo") are reasonable
*illustrative* defaults drawn from general operational experience with
password-hashing costs (bcrypt/scrypt/PBKDF2 rounds) and simple
request/response round trips — they are **not** empirically measured
industry constants, and this module does not claim otherwise. The
honest, rigorous source of ``sigma_real`` for a given target/profile-class
should be the *actual* observed jitter of a real reference daemon —
exactly what the concurrently-developed baseline-daemon tests (another
in-flight architecture-review item, not part of this module) are
positioned to produce. **Follow-up integration point:** once that baseline
infrastructure lands, callers should prefer measuring ``sigma_real`` from
the gold/reference daemon (e.g. via this same sampler run against
``tps.gold_baseline_host``) and pass *that* into
:func:`score_timing_jitter` instead of a hardcoded constant. This module
does not perform that integration itself — it only exposes the constants
and the scorer, deliberately decoupled, so that follow-up wiring is a
one-line change at each call site rather than a rewrite here.

Sampling helpers below **reuse** ``netutil.py``'s existing
``tcp_transact``/``udp_transact``/``sample_udp_latencies`` rather than
opening raw sockets directly — this module only adds the *repeated-sample
+ scoring* orchestration on top.
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass, field

from .models import CheckResult
from .netutil import sample_udp_latencies, tcp_transact

# Illustrative, NOT measured — see module docstring.
REFERENCE_JITTER_SIGMA_MS: dict[str, float] = {
    # Password/key-derivation-backed auth exchanges (SSH password auth,
    # FTP USER/PASS, MySQL native-password handshake, …): bcrypt/PBKDF2/
    # scrypt-class costs typically introduce noticeable, variable delay.
    "auth_hash": 25.0,
    # Cheaper cryptographic/handshake compute (TLS/SSH KEX, non-hashed auth
    # negotiation): some jitter, much less than a deliberate slow-hash.
    "handshake": 8.0,
    # Trivial echo/ping-shaped request-response with no real compute.
    "echo": 0.5,
}

# A run whose *every* sample is below this absolute latency is "suspiciously
# instant" for an operation that should carry real compute/auth cost — the
# classic honeypot tell described in the architecture review, independent
# of how the sigma-ratio score works out.
DEFAULT_NEAR_ZERO_THRESHOLD_MS = 1.0
DEFAULT_NEAR_ZERO_PENALTY_SCORE = 15.0


@dataclass
class JitterSampleSet:
    host: str
    port: int
    samples_ms: list[float] = field(default_factory=list)
    errors: int = 0


def sample_tcp_jitter(
    host: str,
    port: int,
    payload: bytes = b"",
    *,
    samples: int = 30,
    timeout: float = 3.0,
) -> JitterSampleSet:
    """Repeated-timing sampler over TCP, reusing ``netutil.tcp_transact``."""
    result = JitterSampleSet(host=host, port=port)
    for _ in range(max(1, samples)):
        _, rtt_ms, err = tcp_transact(host, port, payload, timeout=timeout)
        if err:
            result.errors += 1
        else:
            result.samples_ms.append(rtt_ms)
    return result


def sample_udp_jitter(
    host: str,
    port: int,
    payload: bytes = b"\x00",
    *,
    samples: int = 30,
    timeout: float = 1.5,
) -> JitterSampleSet:
    """Repeated-timing sampler over UDP, reusing ``netutil.sample_udp_latencies``."""
    lat, errors = sample_udp_latencies(host, port, samples, payload=payload, timeout=timeout)
    return JitterSampleSet(host=host, port=port, samples_ms=lat, errors=errors)


def score_timing_jitter(
    samples: list[float],
    expected_sigma_ms: float,
    *,
    near_zero_threshold_ms: float = DEFAULT_NEAR_ZERO_THRESHOLD_MS,
    near_zero_penalty_score: float = DEFAULT_NEAR_ZERO_PENALTY_SCORE,
    pass_threshold: float = 50.0,
) -> CheckResult:
    """Score a list of latency samples (ms) against a reference sigma (ms).

    ``S_jitter = 1 - abs(sigma_decoy - sigma_real) / sigma_real``, scaled to
    0-100 and clipped to that range, per the reviewer's formula.

    An explicit near-zero-jitter penalty caps the score when *every* sample
    is below ``near_zero_threshold_ms`` — the classic "auth/hash op
    responded suspiciously instantly every single time" honeypot tell —
    independent of how the sigma-ratio math alone works out.
    """
    if expected_sigma_ms <= 0:
        raise ValueError(
            "expected_sigma_ms must be > 0 — pass a REFERENCE_JITTER_SIGMA_MS "
            "entry or a measured baseline-daemon sigma, not 0"
        )
    if len(samples) < 2:
        return CheckResult(
            id="jitter.timing.insufficient_samples",
            team="red",
            passed=False,
            detail=f"need >=2 samples to compute jitter, got {len(samples)}",
            score=0.0,
        )

    sigma_decoy = statistics.pstdev(samples)
    ratio_score = max(0.0, 1.0 - abs(sigma_decoy - expected_sigma_ms) / expected_sigma_ms) * 100.0

    near_zero = sigma_decoy < near_zero_threshold_ms and all(
        s < near_zero_threshold_ms for s in samples
    )
    score = min(ratio_score, near_zero_penalty_score) if near_zero else ratio_score
    passed = score >= pass_threshold and not near_zero

    detail = (
        f"sigma_decoy={sigma_decoy:.3f}ms expected_sigma_ref={expected_sigma_ms:.3f}ms "
        f"S_jitter={ratio_score:.1f}"
    )
    if near_zero:
        detail += (
            " — near-zero-jitter penalty applied (every sample "
            f"<{near_zero_threshold_ms}ms; suspiciously uniform for an operation "
            "expected to carry real compute/auth cost)"
        )

    return CheckResult(
        id="jitter.timing.sigma_match",
        team="red",
        passed=passed,
        detail=detail,
        score=round(score, 2),
        evidence=[
            f"n={len(samples)}",
            f"min={min(samples):.3f}ms",
            f"max={max(samples):.3f}ms",
        ],
    )


def probe_and_score_jitter(
    host: str,
    port: int,
    expected_sigma_ms: float,
    *,
    use_udp: bool = False,
    payload: bytes = b"",
    samples: int = 30,
    timeout: float = 3.0,
) -> CheckResult:
    """Convenience one-call helper: sample then score.

    Plugins that want to opt into this probe without wiring the sampler
    and scorer separately can call this directly.
    """
    sampler = sample_udp_jitter if use_udp else sample_tcp_jitter
    sample_set = sampler(
        host, port, payload or (b"\x00" if use_udp else b""), samples=samples, timeout=timeout
    )
    if not sample_set.samples_ms:
        return CheckResult(
            id="jitter.timing.unreachable",
            team="red",
            passed=False,
            detail=f"no successful samples ({sample_set.errors} errors)",
            score=0.0,
        )
    return score_timing_jitter(sample_set.samples_ms, expected_sigma_ms)
