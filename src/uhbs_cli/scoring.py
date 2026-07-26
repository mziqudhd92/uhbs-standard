"""UHQS scoring helpers for UHBS v4.0.

Normative math MUST match the reference harness `lib/models.py` compute_uhqs:
  UHQS = δ_C · (w_A·S_A + w_B·S_B + w_C·S_C + w_E·S_E + w_F·S_F)
  δ_C = 1.0 if C ≥ 95 else (C/100)²
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

WEIGHT_KEYS = ("w_A", "w_B", "w_C", "w_E", "w_F")
SCORE_KEYS = ("A", "B", "C", "D", "E", "F")

# Profile-adaptive weights (§5.3) — MUST match reference harness PROFILE_WEIGHTS
PROFILE_WEIGHTS: dict[str, dict[str, float]] = {
    "POSIX-Shell": {"w_A": 0.20, "w_B": 0.25, "w_C": 0.20, "w_E": 0.15, "w_F": 0.20},
    "GenAI-Shell": {"w_A": 0.20, "w_B": 0.25, "w_C": 0.20, "w_E": 0.15, "w_F": 0.20},
    "Low-Interaction": {"w_A": 0.30, "w_B": 0.15, "w_C": 0.25, "w_E": 0.10, "w_F": 0.20},
    "ICS-SCADA": {"w_A": 0.35, "w_B": 0.20, "w_C": 0.15, "w_E": 0.10, "w_F": 0.20},
    "Web-API": {"w_A": 0.25, "w_B": 0.20, "w_C": 0.20, "w_E": 0.15, "w_F": 0.20},
    "Database": {"w_A": 0.25, "w_B": 0.25, "w_C": 0.20, "w_E": 0.10, "w_F": 0.20},
}


@dataclass(frozen=True)
class UhqsResult:
    weighted_sum: float
    delta_c: float
    uhqs: float
    safety_gate_passed: bool


def weights_for_class(profile_class: str) -> dict[str, float]:
    return dict(PROFILE_WEIGHTS.get(profile_class, PROFILE_WEIGHTS["POSIX-Shell"]))


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
    # Two decimals — MUST match reference harness round(..., 2)
    uhqs = round(delta_c * weighted, 2)
    return UhqsResult(
        weighted_sum=round(weighted, 6),
        delta_c=round(delta_c, 6),
        uhqs=uhqs,
        safety_gate_passed=passed,
    )


def letter_grade(uhqs: float) -> str:
    """Letter grade bands — MUST match reference harness grade_for()."""
    if uhqs >= 90:
        return "A"
    if uhqs >= 80:
        return "B"
    if uhqs >= 70:
        return "C"
    if uhqs >= 50:
        return "D"
    return "F"


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

    # Class→weight enforcement when both present
    if profile_class and profile_class in PROFILE_WEIGHTS:
        expected = PROFILE_WEIGHTS[profile_class]
        for k in WEIGHT_KEYS:
            if abs(float(weights[k]) - expected[k]) > 0.001:
                errors.append(
                    f"weights.{k}={weights[k]} does not match class {profile_class} "
                    f"(expected {expected[k]})"
                )

    result = compute_uhqs(scores, weights)
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
    if "containment_score" in gate and abs(float(gate["containment_score"]) - scores["D"]) > 0.01:
        errors.append("safety_gate.containment_score != modules.D.score")

    declared_grade = str(scorecard.get("grade", ""))
    expected_grade = letter_grade(result.uhqs)
    if declared_grade and declared_grade != expected_grade:
        errors.append(f"grade={declared_grade} != recomputed {expected_grade}")

    return errors
