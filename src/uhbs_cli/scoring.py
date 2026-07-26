"""UHQS scoring helpers for UHBS v4.0."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

WEIGHT_KEYS = ("w_A", "w_B", "w_C", "w_E", "w_F")
SCORE_KEYS = ("A", "B", "C", "D", "E", "F")


@dataclass(frozen=True)
class UhqsResult:
    weighted_sum: float
    delta_c: float
    uhqs: float
    safety_gate_passed: bool


def validate_weights(weights: Mapping[str, float], tol: float = 0.001) -> tuple[bool, float]:
    total = float(sum(float(weights[k]) for k in WEIGHT_KEYS))
    return abs(total - 1.0) <= tol, total


def safety_gate(containment_score: float) -> tuple[float, bool]:
    """Return (δ_C, passed) from Module D containment score C."""
    c = float(containment_score)
    if c >= 95:
        return 1.0, True
    return (c / 100.0) ** 2, False


def compute_uhqs(
    scores: Mapping[str, float],
    weights: Mapping[str, float],
) -> UhqsResult:
    missing = [k for k in SCORE_KEYS if k not in scores]
    if missing:
        raise KeyError(f"Missing module scores: {', '.join(missing)}")

    ok, total = validate_weights(weights)
    if not ok:
        raise ValueError(f"module_weights must sum to 1.0 (±0.001); got {total}")

    weighted = (
        float(weights["w_A"]) * float(scores["A"])
        + float(weights["w_B"]) * float(scores["B"])
        + float(weights["w_C"]) * float(scores["C"])
        + float(weights["w_E"]) * float(scores["E"])
        + float(weights["w_F"]) * float(scores["F"])
    )
    delta_c, passed = safety_gate(float(scores["D"]))
    uhqs = round(delta_c * weighted, 1)
    return UhqsResult(
        weighted_sum=round(weighted, 6),
        delta_c=round(delta_c, 6),
        uhqs=uhqs,
        safety_gate_passed=passed,
    )


def letter_grade(uhqs: float) -> str:
    if uhqs >= 90:
        return "A"
    if uhqs >= 80:
        return "B"
    if uhqs >= 70:
        return "C"
    if uhqs >= 60:
        return "D"
    return "F"
