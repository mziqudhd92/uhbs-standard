"""Conformance fixtures from UHBS-Lab harness runs (class math + named proof labels)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from uhbs_cli.scoring import (
    PROFILE_WEIGHTS,
    assert_scorecard_integrity,
    compute_uhqs,
    letter_grade,
    weights_for_class,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "docs" / "conformance" / "fixtures"


@pytest.mark.parametrize(
    "name,expected_uhqs,expected_grade",
    [
        # Full-lab fixtures (regraded 2026-07-27 after Module A 0–100 rescale).
        ("cowrie-low-interaction.scorecard.json", 61.37, "D"),
        ("posix-shell-lab.scorecard.json", 80.33, "B"),
        ("espot-web-api.scorecard.json", 63.33, "D"),
        ("miniprint-low-interaction.scorecard.json", 50.43, "D"),
        ("conpot-ics-scada.scorecard.json", 55.4, "D"),
        ("opencanary-web-api.scorecard.json", 66.02, "D"),
        ("opencanary-ftp.scorecard.json", 61.5, "D"),
        ("opencanary-ssh.scorecard.json", 35.64, "F"),
        ("opencanary-telnet.scorecard.json", 64.9, "D"),
        ("opencanary-redis.scorecard.json", 53.72, "D"),
        ("endlessh-low-interaction.scorecard.json", 54.07, "D"),
        ("safety-gate-fail.scorecard.json", 0.0, "F"),
    ],
)
def test_conformance_fixture_integrity(
    name: str, expected_uhqs: float, expected_grade: str
) -> None:
    path = FIXTURES / name
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["uhqs"] == expected_uhqs
    assert data["grade"] == expected_grade
    errors = assert_scorecard_integrity(data)
    assert errors == [], errors


def test_cowrie_matches_low_interaction_weights() -> None:
    data = json.loads((FIXTURES / "cowrie-low-interaction.scorecard.json").read_text())
    expected = PROFILE_WEIGHTS["Low-Interaction"]
    for key, val in expected.items():
        assert abs(data["weights"][key] - val) < 1e-9


def test_posix_lab_meets_production_baseline() -> None:
    data = json.loads((FIXTURES / "posix-shell-lab.scorecard.json").read_text())
    assert data["uhqs"] > 80
    assert letter_grade(data["uhqs"]) == "B"


def test_harness_formula_low_interaction_worked_example() -> None:
    """Anonymous LI scores A=23.5…F=69.0 → 46.97 (not the live Cowrie fixture)."""
    weights = weights_for_class("Low-Interaction")
    scores = {"A": 23.5, "B": 42.5, "C": 57.0, "D": 100.0, "E": 55.0, "F": 69.0}
    result = compute_uhqs(scores, weights)
    assert result.uhqs == 46.97
    assert result.delta_c == 1.0


def test_grade_band_d_starts_at_50() -> None:
    assert letter_grade(50.0) == "D"
    assert letter_grade(49.99) == "F"
    assert letter_grade(70.0) == "C"
    assert letter_grade(80.0) == "B"
