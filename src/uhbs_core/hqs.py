"""UHQS 4.0 scoring helpers."""

from __future__ import annotations

from typing import Dict, Iterable

from uhbs_core.models import DIMS, ModuleResult, average_scores, compute_hqs, compute_uhqs

__all__ = [
    "compute_hqs",
    "compute_uhqs",
    "average_scores",
    "scores_from_modules",
    "pass_status",
]


def scores_from_modules(modules: Iterable[ModuleResult]) -> Dict[str, float]:
    scores: Dict[str, float] = {d: 0.0 for d in DIMS}
    # Legacy → new
    alias = {
        "stealth": "protocol",
        "realism": "behavior",
        "efficiency": "scale",
        "telemetry": "telemetry",
        "containment": "containment",
        "static": "static",
        "protocol": "protocol",
        "behavior": "behavior",
        "scale": "scale",
    }
    for m in modules:
        if m.status == "SKIPPED":
            continue
        dim = alias.get(m.dimension, m.dimension)
        if dim in scores:
            scores[dim] = float(m.score)
    return scores


def pass_status(score: float, threshold: float = 70.0) -> str:
    if score >= threshold:
        return "PASSED"
    if score <= 0:
        return "FAILED"
    return "PARTIAL"
