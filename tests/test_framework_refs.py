"""Optional scorecard framework_refs (D3FEND / Engage) schema checks."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from click.testing import CliRunner
from jsonschema import Draft202012Validator

from uhbs_cli.cli import _schema_dir, main

FIXTURES = Path(__file__).resolve().parents[1] / "docs" / "conformance" / "fixtures"
HELLPOT = FIXTURES / "hellpot-web-api.scorecard.json"


def _scorecard_schema() -> dict:
    return json.loads((_schema_dir() / "scorecard.schema.json").read_text(encoding="utf-8"))


def test_tagged_hellpot_fixture_validates_strict() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["validate-scorecard", str(HELLPOT), "--strict"])
    assert result.exit_code == 0, result.output
    assert "UHQS=43.87" in result.output


def test_framework_refs_accepts_valid_tags() -> None:
    data = json.loads(HELLPOT.read_text(encoding="utf-8"))
    assert "framework_refs" in data
    Draft202012Validator(_scorecard_schema()).validate(data)


def test_framework_refs_rejects_bad_d3fend_id() -> None:
    data = copy.deepcopy(json.loads(HELLPOT.read_text(encoding="utf-8")))
    data["framework_refs"] = {"d3fend": ["NOT-A-D3-ID"]}
    errors = list(Draft202012Validator(_scorecard_schema()).iter_errors(data))
    assert errors
    assert any("d3fend" in list(e.path) or "D3-" in e.message for e in errors)


def test_framework_refs_rejects_unknown_engage_goal() -> None:
    data = copy.deepcopy(json.loads(HELLPOT.read_text(encoding="utf-8")))
    data["framework_refs"] = {"engage_goals": ["HackBack"]}
    errors = list(Draft202012Validator(_scorecard_schema()).iter_errors(data))
    assert errors


def test_framework_refs_accepts_attack_technique_and_subtechnique() -> None:
    data = copy.deepcopy(json.loads(HELLPOT.read_text(encoding="utf-8")))
    data["framework_refs"]["attack"] = ["T1595", "T1059.004"]
    Draft202012Validator(_scorecard_schema()).validate(data)


def test_framework_refs_rejects_bad_attack_id() -> None:
    data = copy.deepcopy(json.loads(HELLPOT.read_text(encoding="utf-8")))
    data["framework_refs"] = {"attack": ["TA0011"]}
    errors = list(Draft202012Validator(_scorecard_schema()).iter_errors(data))
    assert errors
