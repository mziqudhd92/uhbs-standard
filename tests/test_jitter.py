"""Deterministic offline unit tests for uhbs_core.jitter.

Every test here feeds synthetic sample lists directly to
``score_timing_jitter`` — no sockets, no timing dependence, fully
reproducible.
"""

from __future__ import annotations

import pytest

from uhbs_core.jitter import (
    DEFAULT_NEAR_ZERO_PENALTY_SCORE,
    REFERENCE_JITTER_SIGMA_MS,
    score_timing_jitter,
)


def test_identical_real_and_decoy_sigma_scores_near_100() -> None:
    # pstdev([75, 125]) == 25.0 exactly.
    expected_sigma = 25.0
    result = score_timing_jitter([75.0, 125.0], expected_sigma)
    assert result.score == pytest.approx(100.0, abs=0.01)
    assert result.passed is True


def test_huge_sigma_mismatch_scores_low_and_fails() -> None:
    # All-identical samples -> sigma_decoy = 0, far from a 25ms reference.
    result = score_timing_jitter([50.0] * 10, 25.0)
    assert result.score == pytest.approx(0.0, abs=0.01)
    assert result.passed is False


def test_near_zero_jitter_on_auth_class_op_is_penalized() -> None:
    samples = [0.01, 0.02, 0.015, 0.03, 0.01, 0.02]  # all << 1ms
    result = score_timing_jitter(samples, REFERENCE_JITTER_SIGMA_MS["auth_hash"])
    assert result.score <= DEFAULT_NEAR_ZERO_PENALTY_SCORE
    assert result.passed is False
    assert "near-zero-jitter penalty" in result.detail


def test_near_zero_penalty_actively_caps_score_below_raw_ratio() -> None:
    # Hand-pick samples/reference so the raw sigma-ratio score alone would
    # exceed the near-zero penalty cap, to prove the cap is doing real work
    # and not just coinciding with an already-low ratio score.
    samples = [0.1, 0.2, 0.15, 0.05, 0.3, 0.1]  # all < 1ms
    expected_sigma = REFERENCE_JITTER_SIGMA_MS["echo"]  # 0.5ms
    import statistics

    sigma_decoy = statistics.pstdev(samples)
    raw_ratio_score = max(0.0, 1.0 - abs(sigma_decoy - expected_sigma) / expected_sigma) * 100.0
    assert raw_ratio_score > DEFAULT_NEAR_ZERO_PENALTY_SCORE  # precondition for this test

    result = score_timing_jitter(samples, expected_sigma)
    assert result.score == pytest.approx(DEFAULT_NEAR_ZERO_PENALTY_SCORE, abs=0.01)
    assert result.score < raw_ratio_score


def test_realistic_echo_jitter_is_not_penalized() -> None:
    # Small but non-near-zero jitter around the echo reference (~0.5ms) —
    # some samples exceed the 1ms near-zero threshold, so no penalty fires.
    samples = [0.3, 0.9, 1.2, 0.4, 1.1, 0.6]
    result = score_timing_jitter(samples, REFERENCE_JITTER_SIGMA_MS["echo"])
    assert "penalty" not in result.detail


def test_insufficient_samples_returns_explicit_zero_score() -> None:
    result = score_timing_jitter([5.0], 10.0)
    assert result.score == 0.0
    assert result.passed is False
    assert "insufficient" in result.id


def test_expected_sigma_must_be_positive() -> None:
    with pytest.raises(ValueError):
        score_timing_jitter([1.0, 2.0, 3.0], 0.0)
    with pytest.raises(ValueError):
        score_timing_jitter([1.0, 2.0, 3.0], -5.0)


def test_moderate_mismatch_scores_between_extremes() -> None:
    # sigma_decoy = 10ms vs a 25ms auth reference -> ratio = 1 - 15/25 = 0.4 -> 40
    samples = [15.0, 35.0]  # pstdev == 10.0
    result = score_timing_jitter(samples, 25.0)
    assert result.score == pytest.approx(40.0, abs=0.01)
    assert result.passed is False  # below the 50-point pass bar
