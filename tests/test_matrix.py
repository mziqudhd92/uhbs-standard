"""Experimental five-dimension matrix — TDD coverage."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from uhbs_cli import matrix as matrix_mod
from uhbs_cli.cli import main
from uhbs_cli.scoring import assert_scorecard_integrity
from uhbs_core.uhqs_math import PROFILE_WEIGHTS, compute_uhqs

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "docs" / "conformance" / "fixtures" / "cowrie-low-interaction.scorecard.json"


def test_missing_dimension_not_silent_zero() -> None:
    data = matrix_mod.load_json(
        matrix_mod.packaged_data_dir() / "beginner" / "matrix-input.json"
    )
    report = matrix_mod.analyze(data)
    assert report["uhqs_unchanged"] is True
    assert report["dimensions"]["interaction_depth"]["status"] == "missing"
    assert report["dimensions"]["interaction_depth"]["score"] is None
    assert "interaction_depth" in report["composite"]["missing"]
    assert report["composite"]["present_count"] == 3
    assert report["composite"]["score"] == pytest.approx((72 + 81 + 65) / 3, rel=1e-3)


def test_equal_weight_all_present_and_sensitivity() -> None:
    data = matrix_mod.load_json(
        matrix_mod.packaged_data_dir() / "advanced" / "matrix-input.json"
    )
    report = matrix_mod.analyze(data)
    assert report["composite"]["present_count"] == 5
    assert report["composite"]["score"] == pytest.approx(
        (88 + 70 + 92 + 78 + 60) / 5, rel=1e-3
    )
    assert report["sensitivity"]["leave_one_out"]["resource_overhead"] is not None
    assert matrix_mod.validate_report(report) == []


def test_scored_without_score_errors() -> None:
    errors = matrix_mod.validate_input(
        {"dimensions": {"fingerprinting_resistance": {"status": "scored"}}}
    )
    assert any("score" in e for e in errors)


def test_matrix_example_cli(tmp_path: Path) -> None:
    runner = CliRunner()
    out = tmp_path / "m"
    result = runner.invoke(main, ["matrix", "example", "beginner", "--out", str(out)])
    assert result.exit_code == 0, result.output
    assert (out / "matrix-input.json").is_file()
    result = runner.invoke(
        main,
        ["matrix", "analyze", str(out / "matrix-input.json"), "--out", str(out / "r.json")],
    )
    assert result.exit_code == 0, result.output
    report = json.loads((out / "r.json").read_text(encoding="utf-8"))
    assert report["uhqs_unchanged"] is True


def test_matrix_does_not_change_uhqs_fixture() -> None:
    """Golden lock: analyzing matrix must not alter normative scorecard math."""
    scorecard = json.loads(FIXTURE.read_text(encoding="utf-8"))
    before = compute_uhqs(
        {k: scorecard["modules"][k]["score"] for k in "ABCDEF"},
        weights=PROFILE_WEIGHTS[scorecard["target"]["class"]],
    )
    # Matrix path is independent
    data = matrix_mod.load_json(
        matrix_mod.packaged_data_dir() / "beginner" / "matrix-input.json"
    )
    matrix_mod.analyze(data)
    after = compute_uhqs(
        {k: scorecard["modules"][k]["score"] for k in "ABCDEF"},
        weights=PROFILE_WEIGHTS[scorecard["target"]["class"]],
    )
    assert before.uhqs == after.uhqs
    assert assert_scorecard_integrity(scorecard) == []
