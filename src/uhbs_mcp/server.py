"""UHBS MCP server (stdio).

Exposes validate/score/fixture tools and read-only schema/doc resources for
AI hosts (Cursor, Claude Desktop, VS Code, ChatGPT connectors, …).

Does **not** expose Docker lab execution — use the CLI/`uhbs lab` for live probes.
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator
from mcp.server.fastmcp import FastMCP

from uhbs_cli.scoring import (
    PROFILE_WEIGHTS,
    assert_scorecard_integrity,
    compute_uhqs,
    letter_grade,
    validate_weights,
    weights_for_class,
)
from uhbs_mcp import __version__
from uhbs_mcp.paths import repo_root, resolve_user_path, schema_dir

# stdio MCP: never write logs to stdout (corrupts JSON-RPC).
logging.basicConfig(stream=sys.stderr, level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger("uhbs_mcp")

INSTRUCTIONS = """\
UHBS (Universal Honeypot Benchmarking Standard) v4.2.2 — personal open-source
beta evaluation framework for honeypots / deception tech (Apache-2.0).

Not a consortium or adopted industry standard. Product names appear only under
docs/conformance/ as evaluation proof.

Use these tools to validate scorecards/profiles, recompute UHQS/δ_C from
uhqs_math.py, and list conformance fixtures. Prefer compute_uhqs /
validate_scorecard over inventing grades. Live Docker lab grading is CLI-only
(uhbs lab) — not exposed here.
"""

mcp = FastMCP(
    "uhbs",
    instructions=INSTRUCTIONS,
    website_url="https://mziqudhd92.github.io/uhbs-standard/",
)


def _load_schema(name: str) -> dict[str, Any]:
    path = schema_dir() / name
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _schema_errors(data: Any, schema_name: str) -> list[str]:
    schema = _load_schema(schema_name)
    validator = Draft202012Validator(schema)
    out: list[str] = []
    for err in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        loc = ".".join(str(p) for p in err.path) or "(root)"
        out.append(f"{loc}: {err.message}")
    return out


@mcp.tool(
    name="validate_scorecard",
    description=(
        "Validate a UHBS scorecard JSON against schemas/scorecard.schema.json. "
        "In strict mode, recomputes UHQS/δ_C/grade via uhqs_math and fails on drift."
    ),
)
def validate_scorecard(path: str, strict: bool = True) -> dict[str, Any]:
    """Validate a scorecard file on disk."""
    scorecard_path = resolve_user_path(path)
    if not scorecard_path.is_file():
        return {"ok": False, "path": str(scorecard_path), "errors": ["file not found"]}
    data = _load_json(scorecard_path)
    errors = _schema_errors(data, "scorecard.schema.json")
    integrity: list[str] = []
    if not errors and strict:
        integrity = assert_scorecard_integrity(data)
    ok = not errors and not integrity
    return {
        "ok": ok,
        "path": str(scorecard_path),
        "uhqs": data.get("uhqs"),
        "grade": data.get("grade"),
        "schema_errors": errors,
        "integrity_errors": integrity,
    }


@mcp.tool(
    name="validate_profile",
    description=(
        "Validate a Target Profile Specification (profile.yaml) against "
        "schemas/profile.schema.json, weight sum, and optional class→weight table."
    ),
)
def validate_profile(path: str, strict: bool = True) -> dict[str, Any]:
    """Validate a TPS profile YAML file."""
    profile_path = resolve_user_path(path)
    if not profile_path.is_file():
        return {"ok": False, "path": str(profile_path), "errors": ["file not found"]}
    data = _load_yaml(profile_path)
    errors = _schema_errors(data, "profile.schema.json")
    weight_errors: list[str] = []
    weights = data.get("module_weights") or {}
    ok_sum, total = validate_weights(weights)
    if not ok_sum:
        weight_errors.append(f"module_weights sum is {total:.6f}, expected 1.000 (±0.001)")
    profile_class = (data.get("target_metadata") or {}).get("class")
    if strict and profile_class in PROFILE_WEIGHTS:
        expected = PROFILE_WEIGHTS[profile_class]
        for key in ("w_A", "w_B", "w_C", "w_E", "w_F"):
            if abs(float(weights[key]) - expected[key]) > 0.001:
                weight_errors.append(
                    f"module_weights.{key}={weights[key]} does not match class "
                    f"{profile_class} (expected {expected[key]})"
                )
    ok = not errors and not weight_errors
    return {
        "ok": ok,
        "path": str(profile_path),
        "profile_class": profile_class,
        "weights_sum": total,
        "schema_errors": errors,
        "weight_errors": weight_errors,
    }


@mcp.tool(
    name="validate_evidence",
    description="Validate an evidence pack JSON against schemas/evidence-pack.schema.json.",
)
def validate_evidence(path: str) -> dict[str, Any]:
    """Validate an evidence pack file."""
    evidence_path = resolve_user_path(path)
    if not evidence_path.is_file():
        return {"ok": False, "path": str(evidence_path), "errors": ["file not found"]}
    data = _load_json(evidence_path)
    errors = _schema_errors(data, "evidence-pack.schema.json")
    return {"ok": not errors, "path": str(evidence_path), "schema_errors": errors}


@mcp.tool(
    name="compute_uhqs",
    description=(
        "Compute UHQS, δ_C, letter grade, and Safety Gate from module scores A–F "
        "using normative uhqs_math (same as `uhbs score`). Provide profile_class "
        "or omit to pass custom weights."
    ),
)
def compute_uhqs_tool(
    scores: dict[str, float],
    profile_class: str | None = None,
    weights: dict[str, float] | None = None,
) -> dict[str, Any]:
    """Recompute UHQS from module scores."""
    if weights is None:
        if not profile_class:
            return {
                "ok": False,
                "errors": ["Provide profile_class or weights (w_A,w_B,w_C,w_E,w_F)"],
            }
        if profile_class not in PROFILE_WEIGHTS:
            return {
                "ok": False,
                "errors": [f"Unknown profile_class {profile_class!r}"],
                "known_classes": sorted(PROFILE_WEIGHTS),
            }
        weights = dict(weights_for_class(profile_class))
    needed = {"A", "B", "C", "D", "E", "F"}
    missing = sorted(needed - set(scores))
    if missing:
        return {"ok": False, "errors": [f"Missing score keys: {missing}"]}
    result = compute_uhqs(scores=scores, weights=weights)
    return {
        "ok": True,
        "uhbs_version": __version__,
        "profile_class": profile_class,
        "weights": dict(weights),
        "delta_c": result.delta_c,
        "uhqs": result.uhqs,
        "grade": letter_grade(result.uhqs),
        "safety_gate_passed": result.safety_gate_passed,
        "weighted_sum": result.weighted_sum,
    }


@mcp.tool(
    name="list_profile_classes",
    description="List normative UHBS profile classes and their module weight tables.",
)
def list_profile_classes() -> dict[str, Any]:
    """Return class → weight map from uhqs_math."""
    return {
        "ok": True,
        "classes": {name: dict(w) for name, w in sorted(PROFILE_WEIGHTS.items())},
        "formula": "UHQS = δ_C · (w_A·S_A + w_B·S_B + w_C·S_C + w_E·S_E + w_F·S_F)",
        "delta_c": "1.0 if containment C ≥ 95 else (C/100)²",
    }


@mcp.tool(
    name="list_conformance_fixtures",
    description=(
        "List sanitized scorecard fixtures under docs/conformance/fixtures/ "
        "(evaluation proof labels only — not UHBS requirements)."
    ),
)
def list_conformance_fixtures() -> dict[str, Any]:
    """Enumerate conformance fixture scorecards."""
    fixtures_dir = repo_root() / "docs" / "conformance" / "fixtures"
    items: list[dict[str, Any]] = []
    if fixtures_dir.is_dir():
        for path in sorted(fixtures_dir.glob("*.scorecard.json")):
            try:
                data = _load_json(path)
            except (OSError, json.JSONDecodeError) as exc:
                items.append({"path": str(path.relative_to(repo_root())), "error": str(exc)})
                continue
            target = data.get("target") or {}
            items.append(
                {
                    "path": str(path.relative_to(repo_root())),
                    "name": target.get("name"),
                    "class": target.get("class"),
                    "uhqs": data.get("uhqs"),
                    "grade": data.get("grade"),
                }
            )
    return {"ok": True, "count": len(items), "fixtures": items}


@mcp.tool(
    name="get_scorecard_summary",
    description=(
        "Load a scorecard JSON and return a compact summary (modules, Safety Gate, "
        "UHQS/grade) without re-validating schema."
    ),
)
def get_scorecard_summary(path: str) -> dict[str, Any]:
    """Summarize a scorecard file."""
    scorecard_path = resolve_user_path(path)
    if not scorecard_path.is_file():
        return {"ok": False, "path": str(scorecard_path), "errors": ["file not found"]}
    data = _load_json(scorecard_path)
    modules = data.get("modules") or {}
    module_scores = {
        key: (modules.get(key) or {}).get("score") for key in ("A", "B", "C", "D", "E", "F")
    }
    gate = data.get("safety_gate") or {}
    target = data.get("target") or {}
    return {
        "ok": True,
        "path": str(scorecard_path),
        "target_name": target.get("name"),
        "class": target.get("class"),
        "uhqs": data.get("uhqs"),
        "grade": data.get("grade"),
        "module_scores": module_scores,
        "safety_gate": {
            "containment_score": gate.get("containment_score"),
            "delta_c": gate.get("delta_c"),
            "passed": gate.get("passed"),
        },
        "notes": data.get("notes"),
    }


@mcp.tool(
    name="list_lab_reports",
    description=(
        "List published lab report hubs under docs/conformance/reports/ "
        "(quick/full scorecards and tutorials)."
    ),
)
def list_lab_reports() -> dict[str, Any]:
    """Enumerate published honeypot report directories."""
    reports_root = repo_root() / "docs" / "conformance" / "reports"
    hubs: list[dict[str, Any]] = []
    if reports_root.is_dir():
        for path in sorted(reports_root.iterdir()):
            if not path.is_dir() or path.name.startswith("."):
                continue
            hubs.append(
                {
                    "name": path.name,
                    "hub": f"docs/conformance/reports/{path.name}/index.md",
                    "tutorial": f"docs/conformance/reports/{path.name}/TUTORIAL.md",
                    "has_quick": (path / "quick" / "SCORECARD.txt").is_file(),
                    "has_full": (path / "full" / "SCORECARD.txt").is_file(),
                }
            )
    return {"ok": True, "count": len(hubs), "reports": hubs}


@mcp.resource(
    "uhbs://schema/scorecard",
    name="scorecard_schema",
    title="UHBS scorecard JSON Schema",
    mime_type="application/schema+json",
    description="Official schemas/scorecard.schema.json",
)
def resource_scorecard_schema() -> str:
    return (schema_dir() / "scorecard.schema.json").read_text(encoding="utf-8")


@mcp.resource(
    "uhbs://schema/profile",
    name="profile_schema",
    title="UHBS TPS profile JSON Schema",
    mime_type="application/schema+json",
    description="Official schemas/profile.schema.json",
)
def resource_profile_schema() -> str:
    return (schema_dir() / "profile.schema.json").read_text(encoding="utf-8")


@mcp.resource(
    "uhbs://schema/evidence-pack",
    name="evidence_pack_schema",
    title="UHBS evidence-pack JSON Schema",
    mime_type="application/schema+json",
    description="Official schemas/evidence-pack.schema.json",
)
def resource_evidence_schema() -> str:
    return (schema_dir() / "evidence-pack.schema.json").read_text(encoding="utf-8")


@mcp.resource(
    "uhbs://docs/scoring-formula",
    name="scoring_formula",
    title="UHQS scoring formula (spec prose)",
    mime_type="text/markdown",
    description="docs/specification/scoring-formula.md",
)
def resource_scoring_formula() -> str:
    path = repo_root() / "docs" / "specification" / "scoring-formula.md"
    return path.read_text(encoding="utf-8")


@mcp.resource(
    "uhbs://docs/mcp",
    name="mcp_guide",
    title="UHBS MCP tooling guide",
    mime_type="text/markdown",
    description="docs/tooling/mcp.md — install and client config",
)
def resource_mcp_guide() -> str:
    path = repo_root() / "docs" / "tooling" / "mcp.md"
    if not path.is_file():
        return "# UHBS MCP\n\nSee repository docs/tooling/mcp.md\n"
    return path.read_text(encoding="utf-8")


@mcp.prompt(
    name="validate_and_explain_scorecard",
    title="Validate scorecard and explain UHQS",
    description="Workflow: validate a scorecard, then explain UHQS/δ_C without inventing math.",
)
def prompt_validate_scorecard(path: str) -> str:
    return (
        f"Use UHBS MCP tools (not invented formulas):\n"
        f"1. Call validate_scorecard with path={path!r} and strict=true.\n"
        f"2. Call get_scorecard_summary on the same path.\n"
        f"3. If integrity fails, call compute_uhqs with the module scores and target class.\n"
        f"4. Explain δ_C and the grade using uhqs://docs/scoring-formula.\n"
        f"Remind the reader UHBS is a personal beta framework, not a consortium standard."
    )


def main() -> None:
    """Entry point for ``uhbs-mcp`` / ``python -m uhbs_mcp`` (stdio transport)."""
    log.info("Starting UHBS MCP server v%s (stdio); root=%s", __version__, repo_root())
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
