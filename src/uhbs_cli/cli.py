"""Universal Honeypot Benchmarking Standard CLI."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import click
import yaml
from jsonschema import Draft202012Validator

from uhbs_cli import __version__
from uhbs_cli.scoring import compute_uhqs, letter_grade, validate_weights

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "schemas"


def _load_schema(name: str) -> dict[str, Any]:
    path = SCHEMA_DIR / name
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
def validate_profile(profile: Path) -> None:
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

    click.echo(f"OK  {profile} — valid UHBS TPS profile (weights sum={total:.3f})")


@main.command("validate-scorecard")
@click.argument("scorecard", type=click.Path(exists=True, path_type=Path))
def validate_scorecard(scorecard: Path) -> None:
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
    click.echo(f"OK  {scorecard} — valid UHBS scorecard (UHQS={data.get('uhqs')})")


@main.command("score")
@click.option(
    "--profile",
    "profile_path",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="TPS profile.yaml providing module weights.",
)
@click.option(
    "--scores",
    "scores_path",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="JSON object with module scores A,B,C,D,E,F.",
)
def score_cmd(profile_path: Path, scores_path: Path) -> None:
    """Compute UHQS from module scores and profile weights."""
    profile = _load_yaml(profile_path)
    scores = _load_json(scores_path)
    weights = profile["module_weights"]
    result = compute_uhqs(scores=scores, weights=weights)
    click.echo(
        json.dumps(
            {
                "uhbs_version": "4.0.0",
                "delta_c": result.delta_c,
                "uhqs": result.uhqs,
                "grade": letter_grade(result.uhqs),
                "safety_gate_passed": result.safety_gate_passed,
                "weighted_sum": result.weighted_sum,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
