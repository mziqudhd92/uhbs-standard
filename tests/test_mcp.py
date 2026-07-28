"""Tests for UHBS MCP tool helpers (no live stdio host required)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

pytest.importorskip("mcp")

from uhbs_mcp.server import (  # noqa: E402
    compute_uhqs_tool,
    get_scorecard_summary,
    list_conformance_fixtures,
    list_lab_reports,
    list_profile_classes,
    validate_profile,
    validate_scorecard,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "docs" / "conformance" / "fixtures" / "opencanary-web-api.scorecard.json"


def test_validate_scorecard_fixture() -> None:
    result = validate_scorecard(str(FIXTURE), strict=True)
    assert result["ok"] is True
    assert result["uhqs"] == 66.02
    assert result["grade"] == "D"


def test_compute_uhqs_web_api() -> None:
    # Formula smoke test with fixed module scores (not the live OpenCanary fixture).
    result = compute_uhqs_tool(
        scores={"A": 21.5, "B": 82.5, "C": 55.0, "D": 90.0, "E": 100.0, "F": 70.0},
        profile_class="Web-API",
    )
    assert result["ok"] is True
    assert result["uhqs"] == 50.12
    assert result["grade"] == "D"
    assert result["delta_c"] == 0.81
    assert result["safety_gate_passed"] is False


def test_list_profile_classes() -> None:
    result = list_profile_classes()
    assert result["ok"] is True
    assert "Web-API" in result["classes"]
    assert abs(sum(result["classes"]["Web-API"].values()) - 1.0) < 0.001


def test_list_conformance_fixtures() -> None:
    result = list_conformance_fixtures()
    assert result["ok"] is True
    assert result["count"] >= 5
    names = {item.get("path", "") for item in result["fixtures"]}
    assert any(p.endswith("opencanary-web-api.scorecard.json") for p in names)


def test_get_scorecard_summary() -> None:
    result = get_scorecard_summary(str(FIXTURE))
    assert result["ok"] is True
    assert result["uhqs"] == 66.02
    assert result["module_scores"]["A"] == 100.0


def test_list_lab_reports() -> None:
    result = list_lab_reports()
    assert result["ok"] is True
    names = {r["name"] for r in result["reports"]}
    assert "opencanary" in names
    assert "espot" in names


def test_validate_profile_template() -> None:
    path = ROOT / "templates" / "profile.yaml"
    result = validate_profile(str(path), strict=True)
    assert result["ok"] is True


def test_server_json_present() -> None:
    data = json.loads((ROOT / "server.json").read_text(encoding="utf-8"))
    assert data["name"] == "io.github.mziqudhd92/uhbs"
    assert data["version"] == "4.2.1"
    assert data["packages"][0]["transport"]["type"] == "stdio"
