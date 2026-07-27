"""Unit tests for the Module A/B circuit-breaker + geometric-mean aggregator.

Covers the 2026-07-27 architecture review remediation:
  - critical=True + passed=False hard-caps the whole list to 0.0
  - geometric mean (not arithmetic mean) punishes a low outlier hard
  - legacy all-zero-score / booleans-only fallback still works

...and the 2026-07-27 code-review follow-up: the integrity gate that closes
the "passed=True, score=0.0 silently scores 100.0" loophole the legacy
fallback used to allow (see check_scoring.py's docstring, gate #2).
"""

from __future__ import annotations

import math

from uhbs_core.check_scoring import score_checks
from uhbs_core.models import CheckResult


def _cr(score: float, passed: bool = True, critical: bool = False) -> CheckResult:
    return CheckResult(id="t", team="blue", passed=passed, score=score, critical=critical)


def test_empty_list_scores_zero() -> None:
    assert score_checks([]) == 0.0


def test_circuit_breaker_zeroes_out_despite_other_passes() -> None:
    checks = [
        _cr(100.0, passed=True),
        _cr(100.0, passed=True),
        _cr(0.0, passed=False, critical=True),  # gate failure
    ]
    assert score_checks(checks) == 0.0


def test_non_critical_failure_does_not_trip_breaker() -> None:
    checks = [_cr(100.0, passed=True), _cr(0.0, passed=False, critical=False)]
    result = score_checks(checks)
    assert result > 0.0  # not hard-capped, just dragged down by geometric mean


def test_geometric_mean_punishes_outlier_harder_than_arithmetic_mean() -> None:
    checks = [_cr(0.0, passed=False), _cr(100.0), _cr(100.0)]
    result = score_checks(checks)
    arithmetic_mean = (0.0 + 100.0 + 100.0) / 3  # == 33.33
    assert result < arithmetic_mean
    # sanity: matches the documented ~17 ballpark (floor=0.5)
    expected = math.exp((math.log(0.5) + math.log(100.0) + math.log(100.0)) / 3)
    assert abs(result - expected) < 0.01


def test_all_pass_scores_full_from_scores() -> None:
    checks = [_cr(100.0), _cr(100.0)]
    assert score_checks(checks) == 100.0


def test_legacy_boolean_only_fallback_all_failed() -> None:
    # The legacy pass-rate fallback is now only reachable when every check
    # is passed=False/score=0.0 (any passed=True + score=0.0 check trips
    # the integrity gate below first) — this is the one case left that
    # still exercises it, and it trivially evaluates to 0.0.
    checks = [
        CheckResult(id="a", team="blue", passed=False, score=0.0),
        CheckResult(id="b", team="blue", passed=False, score=0.0),
    ]
    assert score_checks(checks) == 0.0


def test_passed_true_with_zero_score_is_not_a_silent_free_pass() -> None:
    # Regression guard for the 2026-07-27 code-review finding: this exact
    # shape (passed=True, score=0.0 — e.g. a plugin bug that forgot to set
    # score) used to fall through to the legacy fallback above and score a
    # silent 100.0. It must now zero the whole list instead.
    checks = [CheckResult(id="a", team="blue", passed=True, score=0.0, critical=False)]
    assert score_checks(checks) == 0.0


def test_passed_true_with_zero_score_zeroes_even_when_mixed_with_real_passes() -> None:
    checks = [
        CheckResult(id="a", team="blue", passed=True, score=100.0),
        CheckResult(id="b", team="blue", passed=True, score=0.0, critical=False),
    ]
    assert score_checks(checks) == 0.0


def test_integrity_gate_also_catches_passed_false_with_near_perfect_score() -> None:
    # The other half of the disagreement: passed=False but score says the
    # check basically succeeded.
    checks = [CheckResult(id="a", team="blue", passed=False, score=95.0, critical=False)]
    assert score_checks(checks) == 0.0


def test_integrity_gate_does_not_flag_legitimate_low_but_passing_scores() -> None:
    # Sanity: intentional low-but-passing partial credit (above the 15.0
    # floor) must NOT trip the integrity gate. Timing "N/A" / soft-partial
    # checks may still use this shape.
    checks = [CheckResult(id="a", team="blue", passed=True, score=50.0, critical=False)]
    assert score_checks(checks) == 50.0
