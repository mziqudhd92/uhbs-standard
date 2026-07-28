"""UHQS scoring helpers for UHBS v4.2.0 (CLI / scorecard validation).

Normative math lives in ``uhbs_core.uhqs_math`` — this module re-exports the
CLI-facing API and adds scorecard integrity checks.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from uhbs_core.uhqs_math import (
    PROFILE_WEIGHTS,
    SCORE_KEYS,
    WEIGHT_KEYS,
    letter_grade,
    safety_gate,
    validate_weights,
    weights_for_class,
)
from uhbs_core.uhqs_math import (
    compute_uhqs as _compute_uhqs,
)

__all__ = [
    "PROFILE_WEIGHTS",
    "SCORE_KEYS",
    "WEIGHT_KEYS",
    "UhqsResult",
    "assert_scorecard_integrity",
    "compute_uhqs",
    "letter_grade",
    "safety_gate",
    "validate_weights",
    "weights_for_class",
]


@dataclass(frozen=True)
class UhqsResult:
    weighted_sum: float
    delta_c: float
    uhqs: float
    safety_gate_passed: bool


def compute_uhqs(
    scores: Mapping[str, float],
    weights: Mapping[str, float],
) -> UhqsResult:
    result = _compute_uhqs(scores, weights)
    return UhqsResult(
        weighted_sum=result.weighted_sum,
        delta_c=result.delta_c,
        uhqs=result.uhqs,
        safety_gate_passed=result.safety_gate_passed,
    )


def assert_scorecard_integrity(
    scorecard: Mapping,
    *,
    uhqs_tol: float = 0.01,
    delta_tol: float = 0.0001,
) -> list[str]:
    """Recompute UHQS/δ_C/grade; return list of integrity errors (empty = OK)."""
    errors: list[str] = []
    modules = scorecard.get("modules") or {}
    weights = scorecard.get("weights")
    target = scorecard.get("target") or {}
    profile_class = target.get("class")

    if not weights and profile_class:
        weights = weights_for_class(str(profile_class))
    if not weights:
        return ["missing weights and target.class"]

    try:
        scores = {
            "A": float(modules["A"]["score"]),
            "B": float(modules["B"]["score"]),
            "C": float(modules["C"]["score"]),
            "D": float(modules["D"]["score"]),
            "E": float(modules["E"]["score"]),
            "F": float(modules["F"]["score"]),
        }
    except (KeyError, TypeError, ValueError) as exc:
        return [f"modules incomplete: {exc}"]

    d_mod = modules.get("D") or {}
    containment_measured = bool(scorecard.get("containment_measured", True))
    if str(d_mod.get("status", "")).upper() in {"SKIPPED", "N/A", "NOT_RUN"}:
        containment_measured = False
    if scorecard.get("containment_measured") is False:
        containment_measured = False

    # Class→weight enforcement when both present
    if profile_class and profile_class in PROFILE_WEIGHTS:
        expected = PROFILE_WEIGHTS[profile_class]
        for k in WEIGHT_KEYS:
            if abs(float(weights[k]) - expected[k]) > 0.001:
                errors.append(
                    f"weights.{k}={weights[k]} does not match class {profile_class} "
                    f"(expected {expected[k]})"
                )

    result = _compute_uhqs(
        scores, weights, containment_measured=containment_measured
    )
    declared_uhqs = float(scorecard.get("uhqs", -1))
    if abs(declared_uhqs - result.uhqs) > uhqs_tol:
        errors.append(f"uhqs={declared_uhqs} != recomputed {result.uhqs}")

    gate = scorecard.get("safety_gate") or {}
    if "delta_c" in gate and abs(float(gate["delta_c"]) - result.delta_c) > delta_tol:
        errors.append(f"safety_gate.delta_c={gate['delta_c']} != recomputed {result.delta_c}")
    if "passed" in gate and bool(gate["passed"]) != result.safety_gate_passed:
        errors.append(
            f"safety_gate.passed={gate['passed']} != recomputed {result.safety_gate_passed}"
        )
    if (
        containment_measured
        and "containment_score" in gate
        and abs(float(gate["containment_score"]) - scores["D"]) > 0.01
    ):
        errors.append("safety_gate.containment_score != modules.D.score")

    declared_grade = str(scorecard.get("grade", ""))
    expected_grade = letter_grade(result.uhqs)
    if declared_grade and declared_grade != expected_grade:
        errors.append(f"grade={declared_grade} != recomputed {expected_grade}")

    return errors
