"""Normative UHQS 4.0 math — single source of truth for CLI and UHBS-Lab.

UHQS = δ_C · (w_A·S_A + w_B·S_B + w_C·S_C + w_E·S_E + w_F·S_F)
δ_C  = 1.0 if C ≥ 95 else (C/100)²

Both ``uhbs_cli.scoring`` and ``uhbs_core.models`` MUST import from here.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

# Letter keys (scorecards / CLI) ↔ dimension keys (harness)
LETTER_TO_DIM = {
    "A": "protocol",
    "B": "behavior",
    "C": "telemetry",
    "D": "containment",
    "E": "scale",
    "F": "static",
}
DIM_TO_LETTER = {v: k for k, v in LETTER_TO_DIM.items()}

# Legacy aliases accepted when normalizing harness score maps
DIM_ALIASES = {
    "protocol": "protocol",
    "behavior": "behavior",
    "telemetry": "telemetry",
    "containment": "containment",
    "scale": "scale",
    "static": "static",
    "stealth": "protocol",
    "realism": "behavior",
    "efficiency": "scale",
    "A": "protocol",
    "B": "behavior",
    "C": "telemetry",
    "D": "containment",
    "E": "scale",
    "F": "static",
}

WEIGHT_KEYS = ("w_A", "w_B", "w_C", "w_E", "w_F")
SCORE_KEYS = ("A", "B", "C", "D", "E", "F")
DIM_KEYS = ("protocol", "behavior", "telemetry", "containment", "scale", "static")

# Grade band thresholds (letter → long harness label)
GRADE_BANDS: tuple[tuple[float, str, str], ...] = (
    (90.0, "A", "GRADE A (Enterprise Grade)"),
    (80.0, "B", "GRADE B (Production Candidate)"),
    (70.0, "C", "GRADE C (Lab / Limited)"),
    (50.0, "D", "GRADE D (Needs Remediation)"),
    (0.0, "F", "GRADE F (Fail)"),
)

# Profile-adaptive weights (§5.3) — letter-key form (normative for scorecards)
PROFILE_WEIGHTS: dict[str, dict[str, float]] = {
    "POSIX-Shell": {"w_A": 0.20, "w_B": 0.25, "w_C": 0.20, "w_E": 0.15, "w_F": 0.20},
    "GenAI-Shell": {"w_A": 0.20, "w_B": 0.25, "w_C": 0.20, "w_E": 0.15, "w_F": 0.20},
    "Low-Interaction": {"w_A": 0.30, "w_B": 0.15, "w_C": 0.25, "w_E": 0.10, "w_F": 0.20},
    "ICS-SCADA": {"w_A": 0.35, "w_B": 0.20, "w_C": 0.15, "w_E": 0.10, "w_F": 0.20},
    "Web-API": {"w_A": 0.25, "w_B": 0.20, "w_C": 0.20, "w_E": 0.15, "w_F": 0.20},
    "Database": {"w_A": 0.25, "w_B": 0.25, "w_C": 0.20, "w_E": 0.10, "w_F": 0.20},
}


def weights_for_class(profile_class: str) -> dict[str, float]:
    return dict(PROFILE_WEIGHTS.get(profile_class, PROFILE_WEIGHTS["POSIX-Shell"]))


def weights_for_class_dims(profile_class: str) -> dict[str, float]:
    """Weights keyed by dimension names for harness report code."""
    letter = weights_for_class(profile_class)
    return {
        "protocol": letter["w_A"],
        "behavior": letter["w_B"],
        "telemetry": letter["w_C"],
        "scale": letter["w_E"],
        "static": letter["w_F"],
    }


def validate_weights(weights: Mapping[str, float], tol: float = 0.001) -> tuple[bool, float]:
    total = float(sum(float(weights[k]) for k in WEIGHT_KEYS))
    return abs(total - 1.0) <= tol, total


def safety_gate(containment_score: float) -> tuple[float, bool]:
    """Return (δ_C, passed) from Module D containment score C."""
    c = float(containment_score)
    if c >= 95:
        return 1.0, True
    return (c / 100.0) ** 2, False


def letter_grade(uhqs: float) -> str:
    for threshold, letter, _long in GRADE_BANDS:
        if uhqs >= threshold:
            return letter
    return "F"


def grade_for(uhqs: float) -> str:
    """Long-form grade string used by harness SCORECARD.txt."""
    for threshold, _letter, long in GRADE_BANDS:
        if uhqs >= threshold:
            return long
    return "GRADE F (Fail)"


def normalize_module_scores(scores: Mapping[str, float]) -> dict[str, float]:
    """Normalize letter or dimension keys to A–F. Raises KeyError if any module missing."""
    by_dim: dict[str, float] = {}
    for key, value in scores.items():
        dim = DIM_ALIASES.get(str(key))
        if dim is None:
            continue
        by_dim[dim] = float(value)

    missing = [DIM_TO_LETTER[d] for d in DIM_KEYS if d not in by_dim]
    if missing:
        raise KeyError(f"Missing module scores: {', '.join(missing)}")

    return {DIM_TO_LETTER[d]: by_dim[d] for d in DIM_KEYS}


@dataclass(frozen=True)
class UhqsComputation:
    """Canonical UHQS computation result (shared by CLI and harness)."""

    scores: dict[str, float]  # A–F
    weights: dict[str, float]  # w_*
    weighted_sum: float
    delta_c: float
    uhqs: float
    safety_gate_passed: bool
    containment_measured: bool


def compute_uhqs(
    scores: Mapping[str, float],
    weights: Mapping[str, float] | None = None,
    *,
    profile_class: str | None = None,
    containment_measured: bool = True,
) -> UhqsComputation:
    """Compute UHQS from module scores.

    ``scores`` may use letter keys (A–F) or dimension keys (protocol, …).
    Missing modules raise ``KeyError`` — never silently default to 0.0.
    """
    normalized = normalize_module_scores(scores)

    if weights is None:
        if not profile_class:
            raise ValueError("Provide weights or profile_class")
        weights = weights_for_class(profile_class)

    ok, total = validate_weights(weights)
    if not ok:
        raise ValueError(f"module_weights must sum to 1.0 (±0.001); got {total}")

    weighted = (
        float(weights["w_A"]) * normalized["A"]
        + float(weights["w_B"]) * normalized["B"]
        + float(weights["w_C"]) * normalized["C"]
        + float(weights["w_E"]) * normalized["E"]
        + float(weights["w_F"]) * normalized["F"]
    )

    if not containment_measured:
        delta_c, passed = 1.0, True
    else:
        delta_c, passed = safety_gate(normalized["D"])

    uhqs = round(delta_c * weighted, 2)
    return UhqsComputation(
        scores=normalized,
        weights={k: float(weights[k]) for k in WEIGHT_KEYS},
        weighted_sum=round(weighted, 6),
        delta_c=round(delta_c, 6),
        uhqs=uhqs,
        safety_gate_passed=passed,
        containment_measured=containment_measured,
    )
