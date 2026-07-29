"""Universal Honeypot Benchmarking Standard CLI."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

import click
import yaml
from jsonschema import Draft202012Validator

from uhbs_cli import __version__
from uhbs_cli.scoring import (
    PROFILE_WEIGHTS,
    assert_scorecard_integrity,
    compute_uhqs,
    letter_grade,
    validate_weights,
    weights_for_class,
)


def _repo_root() -> Path:
    """Resolve the UHBS checkout root (editable layout or UHBS_ROOT)."""
    env = os.environ.get("UHBS_ROOT")
    if env:
        return Path(env)
    # src/uhbs_cli/cli.py → repo root (editable / Docker source tree)
    return Path(__file__).resolve().parents[2]


def _schema_dir() -> Path:
    """Locate JSON Schemas for profile/scorecard/evidence validation."""
    env = os.environ.get("UHBS_SCHEMA_DIR")
    if env:
        return Path(env)
    return _repo_root() / "schemas"


ROOT = _repo_root()
SCHEMA_DIR = _schema_dir()


def _load_schema(name: str) -> dict[str, Any]:
    path = _schema_dir() / name
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


@click.group()
@click.version_option(__version__, prog_name="uhbs")
def main() -> None:
    """UHBS — validate profiles/scorecards and compute UHQS."""


@main.command("validate-profile")
@click.argument("profile", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--strict/--no-strict",
    default=True,
    help="Enforce class→weight table match (default: on).",
)
def validate_profile(profile: Path, strict: bool) -> None:
    """Validate a TPS profile.yaml against the official schema."""
    data = _load_yaml(profile)
    schema = _load_schema("profile.schema.json")
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
    if errors:
        for err in errors:
            loc = ".".join(str(p) for p in err.path) or "(root)"
            click.echo(f"ERROR {loc}: {err.message}", err=True)
        sys.exit(1)

    weights = data.get("module_weights", {})
    ok, total = validate_weights(weights)
    if not ok:
        click.echo(
            f"ERROR module_weights: sum is {total:.6f}, expected 1.000 (±0.001)",
            err=True,
        )
        sys.exit(1)

    profile_class = (data.get("target_metadata") or {}).get("class")
    if strict and profile_class in PROFILE_WEIGHTS:
        expected = PROFILE_WEIGHTS[profile_class]
        for key in ("w_A", "w_B", "w_C", "w_E", "w_F"):
            if abs(float(weights[key]) - expected[key]) > 0.001:
                click.echo(
                    f"ERROR module_weights.{key}: {weights[key]} does not match "
                    f"class {profile_class} (expected {expected[key]})",
                    err=True,
                )
                sys.exit(1)

    click.echo(f"OK  {profile} — valid UHBS TPS profile (weights sum={total:.3f})")


@main.command("validate-scorecard")
@click.argument("scorecard", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--strict/--no-strict",
    default=True,
    help="Recompute UHQS/δ_C/grade and enforce class weights (default: on).",
)
def validate_scorecard(scorecard: Path, strict: bool) -> None:
    """Validate a scorecard JSON against the official schema."""
    data = _load_json(scorecard)
    schema = _load_schema("scorecard.schema.json")
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
    if errors:
        for err in errors:
            loc = ".".join(str(p) for p in err.path) or "(root)"
            click.echo(f"ERROR {loc}: {err.message}", err=True)
        sys.exit(1)

    if strict:
        integrity = assert_scorecard_integrity(data)
        if integrity:
            for msg in integrity:
                click.echo(f"ERROR integrity: {msg}", err=True)
            sys.exit(1)

    click.echo(f"OK  {scorecard} — valid UHBS scorecard (UHQS={data.get('uhqs')})")


@main.command("validate-evidence")
@click.argument("evidence", type=click.Path(exists=True, path_type=Path))
def validate_evidence(evidence: Path) -> None:
    """Validate an evidence pack against the official schema."""
    data = _load_json(evidence)
    schema = _load_schema("evidence-pack.schema.json")
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
    if errors:
        for err in errors:
            loc = ".".join(str(p) for p in err.path) or "(root)"
            click.echo(f"ERROR {loc}: {err.message}", err=True)
        sys.exit(1)
    click.echo(f"OK  {evidence} — valid UHBS evidence pack")


@main.command("score")
@click.option(
    "--profile",
    "profile_path",
    type=click.Path(exists=True, path_type=Path),
    help="TPS profile.yaml providing module weights.",
)
@click.option(
    "--class",
    "profile_class",
    type=click.Choice(sorted(PROFILE_WEIGHTS.keys())),
    help="Profile class (uses normative weight table when --profile omitted).",
)
@click.option(
    "--scores",
    "scores_path",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="JSON object with module scores A,B,C,D,E,F.",
)
def score_cmd(
    profile_path: Path | None,
    profile_class: str | None,
    scores_path: Path,
) -> None:
    """Compute UHQS from module scores and profile weights."""
    scores = _load_json(scores_path)
    if profile_path:
        profile = _load_yaml(profile_path)
        weights = profile["module_weights"]
        profile_class = (profile.get("target_metadata") or {}).get("class") or profile_class
    elif profile_class:
        weights = weights_for_class(profile_class)
    else:
        raise click.UsageError("Provide --profile or --class")

    result = compute_uhqs(scores=scores, weights=weights)
    click.echo(
        json.dumps(
            {
                "uhbs_version": "4.3.0",
                "profile_class": profile_class,
                "delta_c": result.delta_c,
                "uhqs": result.uhqs,
                "grade": letter_grade(result.uhqs),
                "safety_gate_passed": result.safety_gate_passed,
                "weighted_sum": result.weighted_sum,
            },
            indent=2,
        )
    )


@main.command(
    "lab",
    context_settings={"ignore_unknown_options": True, "allow_extra_args": True},
)
@click.pass_context
def lab_cmd(ctx: click.Context) -> None:
    """Run the UHBS-Lab reference harness (requires: pip install 'uhbs[lab]')."""
    try:
        from uhbs_core.run_benchmark import main as lab_main
    except ImportError as exc:  # pragma: no cover
        raise click.ClickException(
            "uhbs-core lab harness unavailable. Install with: pip install 'uhbs[lab]'"
        ) from exc
    raise SystemExit(lab_main(tuple(ctx.args)))


if __name__ == "__main__":
    main()
