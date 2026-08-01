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
from uhbs_core.termui import echo_error, echo_info, echo_ok, echo_warn


def _repo_root() -> Path:
    """Resolve the UHBS checkout root (editable layout or UHBS_ROOT)."""
    env = os.environ.get("UHBS_ROOT")
    if env:
        return Path(env)
    # src/uhbs_cli/cli.py → repo root (editable / Docker source tree)
    return Path(__file__).resolve().parents[2]


def _schema_dir() -> Path:
    """Locate JSON Schemas for profile/scorecard/evidence validation.

    Prefer ``UHBS_SCHEMA_DIR``, then schemas shipped inside the installed
    ``uhbs_cli`` package (PyPI wheel), then a source checkout's ``schemas/``.
    """
    env = os.environ.get("UHBS_SCHEMA_DIR")
    if env:
        return Path(env)
    packaged = Path(__file__).resolve().parent / "schemas"
    if (packaged / "scorecard.schema.json").is_file():
        return packaged
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
@click.pass_context
def main(ctx: click.Context) -> None:
    """UHBS — validate profiles/scorecards and compute UHQS (lab/sandbox evaluation)."""
    # Show once per invocation when a subcommand runs (not for bare --help/--version).
    if ctx.invoked_subcommand is not None:
        from uhbs_core.notices import print_lab_sandbox_notice

        print_lab_sandbox_notice()


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
            echo_error(f"ERROR {loc}: {err.message}")
        sys.exit(1)

    weights = data.get("module_weights", {})
    ok, total = validate_weights(weights)
    if not ok:
        echo_error(f"ERROR module_weights: sum is {total:.6f}, expected 1.000 (±0.001)")
        sys.exit(1)

    profile_class = (data.get("target_metadata") or {}).get("class")
    if strict and profile_class in PROFILE_WEIGHTS:
        expected = PROFILE_WEIGHTS[profile_class]
        for key in ("w_A", "w_B", "w_C", "w_E", "w_F"):
            if abs(float(weights[key]) - expected[key]) > 0.001:
                echo_error(
                    f"ERROR module_weights.{key}: {weights[key]} does not match "
                    f"class {profile_class} (expected {expected[key]})"
                )
                sys.exit(1)

    echo_ok(f"OK  {profile} — valid UHBS TPS profile (weights sum={total:.3f})")


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
            echo_error(f"ERROR {loc}: {err.message}")
        sys.exit(1)

    if strict:
        integrity = assert_scorecard_integrity(data)
        if integrity:
            for msg in integrity:
                echo_error(f"ERROR integrity: {msg}")
            sys.exit(1)

    echo_ok(f"OK  {scorecard} — valid UHBS scorecard (UHQS={data.get('uhqs')})")


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
            echo_error(f"ERROR {loc}: {err.message}")
        sys.exit(1)
    echo_ok(f"OK  {evidence} — valid UHBS evidence pack")


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
                "uhbs_version": "4.3.6",
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


@main.group("aep")
def aep_group() -> None:
    """Advanced Evidence Profile — offline analysis only (optional).

    Requires local experiment/trial files. Never launches attacks, probes,
    containers, or network connections. Does not change UHQS.
    """


@aep_group.command("init")
@click.option("--name", default="aep-experiment", show_default=True)
@click.option(
    "--class",
    "profile_class",
    type=click.Choice(sorted(PROFILE_WEIGHTS.keys())),
    default="Web-API",
    show_default=True,
)
@click.option("--trials", default=5, show_default=True, type=click.IntRange(min=1))
@click.option("--seed", default=42, show_default=True, type=int)
@click.option(
    "--out",
    "out_dir",
    type=click.Path(path_type=Path),
    default=Path("aep-experiment"),
    show_default=True,
)
@click.option(
    "--force/--no-force",
    default=False,
    show_default=True,
    help="Overwrite existing experiment.yaml / trials.jsonl in --out.",
)
def aep_init(
    name: str,
    profile_class: str,
    trials: int,
    seed: int,
    out_dir: Path,
    force: bool,
) -> None:
    """Create an experiment manifest + synthetic trial template (local files)."""
    from uhbs_cli import aep as aep_mod

    try:
        aep_mod.reject_forbidden_cli_values(name, str(out_dir))
        paths = aep_mod.write_init_bundle(
            out_dir,
            name=name,
            profile_class=profile_class,
            trials=trials,
            seed=seed,
            force=force,
        )
    except aep_mod.AepError as exc:
        raise click.ClickException(str(exc)) from exc
    echo_ok(f"OK  wrote {paths['experiment']}")
    echo_ok(f"OK  wrote {paths['trials']}")
    echo_ok(f"OK  wrote {paths['readme']}")
    echo_warn("AEP is offline analysis only — replace synthetic trials before publishing.")


@aep_group.command("example")
@click.argument("name", type=click.Choice(["beginner", "advanced", "template"]))
@click.option(
    "--out",
    "out_dir",
    type=click.Path(path_type=Path),
    default=None,
    help="Destination directory (default: ./aep-<name>).",
)
@click.option(
    "--force/--no-force",
    default=False,
    show_default=True,
    help="Overwrite existing files in --out.",
)
def aep_example(name: str, out_dir: Path | None, force: bool) -> None:
    """Copy a packaged synthetic AEP example (works after pip install)."""
    from uhbs_cli import aep as aep_mod

    target = out_dir or Path(f"aep-{name}")
    try:
        aep_mod.reject_forbidden_cli_values(str(target))
        written = aep_mod.export_example_bundle(name, target, force=force)
    except aep_mod.AepError as exc:
        raise click.ClickException(str(exc)) from exc
    echo_ok(f"OK  wrote packaged example '{name}' to {written}")
    echo_info("Next: uhbs aep validate experiment.yaml  (from that directory)")


@aep_group.command("validate")
@click.argument("experiment", type=click.Path(exists=True, path_type=Path))
@click.option("--strict/--no-strict", default=True, show_default=True)
@click.option("--json", "as_json", is_flag=True, help="Emit machine-readable result.")
def aep_validate(experiment: Path, strict: bool, as_json: bool) -> None:
    """Validate an AEP experiment manifest."""
    from uhbs_cli import aep as aep_mod

    try:
        aep_mod.reject_forbidden_cli_values(str(experiment))
        data = aep_mod.load_yaml(experiment)
        errors = aep_mod.validate_experiment(data, strict=strict)
    except aep_mod.AepError as exc:
        raise click.ClickException(str(exc)) from exc
    if as_json:
        click.echo(json.dumps({"ok": not errors, "errors": errors}, indent=2))
    elif errors:
        for err in errors:
            echo_error(f"ERROR {err}")
        sys.exit(1)
    else:
        echo_ok(f"OK  {experiment} — valid AEP experiment manifest")
    if errors:
        sys.exit(1)


@aep_group.command("validate-trials")
@click.argument("trials", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--experiment",
    "experiment_path",
    type=click.Path(exists=True, path_type=Path),
    help="Optional experiment manifest for cross-checks.",
)
@click.option("--strict/--no-strict", default=True, show_default=True)
@click.option("--json", "as_json", is_flag=True)
def aep_validate_trials(
    trials: Path,
    experiment_path: Path | None,
    strict: bool,
    as_json: bool,
) -> None:
    """Validate AEP trial events (JSONL)."""
    from uhbs_cli import aep as aep_mod

    try:
        aep_mod.reject_forbidden_cli_values(
            str(trials), str(experiment_path) if experiment_path else None
        )
        rows = aep_mod.load_trials_jsonl(trials)
        experiment = aep_mod.load_yaml(experiment_path) if experiment_path else None
        errors = aep_mod.validate_trials(rows, experiment, strict=strict)
    except aep_mod.AepError as exc:
        raise click.ClickException(str(exc)) from exc
    if as_json:
        click.echo(
            json.dumps({"ok": not errors, "n": len(rows), "errors": errors}, indent=2)
        )
    elif errors:
        for err in errors:
            echo_error(f"ERROR {err}")
        sys.exit(1)
    else:
        echo_ok(f"OK  {trials} — {len(rows)} valid AEP trial event(s)")
    if errors:
        sys.exit(1)


@aep_group.command("analyze")
@click.option(
    "--experiment",
    "experiment_path",
    required=True,
    type=click.Path(exists=True, path_type=Path),
)
@click.option(
    "--trials",
    "trials_path",
    required=True,
    type=click.Path(exists=True, path_type=Path),
)
@click.option(
    "--scorecard",
    "scorecard_path",
    type=click.Path(exists=True, path_type=Path),
    help="Optional local scorecard path (linked only; never mutated).",
)
@click.option("--bootstrap-samples", default=1000, show_default=True, type=click.IntRange(min=0))
@click.option("--confidence", default=0.95, show_default=True, type=float)
@click.option("--seed", default=42, show_default=True, type=int)
@click.option(
    "--out",
    "out_path",
    type=click.Path(path_type=Path),
    default=Path("advanced-evidence.json"),
    show_default=True,
)
def aep_analyze(
    experiment_path: Path,
    trials_path: Path,
    scorecard_path: Path | None,
    bootstrap_samples: int,
    confidence: float,
    seed: int,
    out_path: Path,
) -> None:
    """Compute informative AEP metrics from local evidence files."""
    from uhbs_cli import aep as aep_mod

    try:
        aep_mod.reject_forbidden_cli_values(
            str(experiment_path),
            str(trials_path),
            str(scorecard_path) if scorecard_path else None,
            str(out_path),
        )
        if not (0.0 < confidence < 1.0):
            raise aep_mod.AepError("--confidence must be between 0 and 1 (exclusive)")
        experiment = aep_mod.load_yaml(experiment_path)
        exp_errors = aep_mod.validate_experiment(experiment, strict=True)
        if exp_errors:
            for err in exp_errors:
                echo_error(f"ERROR experiment: {err}")
            sys.exit(1)
        rows = aep_mod.load_trials_jsonl(trials_path)
        trial_errors = aep_mod.validate_trials(rows, experiment, strict=True)
        if trial_errors:
            for err in trial_errors:
                echo_error(f"ERROR trials: {err}")
            sys.exit(1)
        if scorecard_path is not None:
            # Ensure scorecard exists and looks like UHBS scorecard JSON; do not mutate.
            scorecard = aep_mod.load_json(scorecard_path)
            if not isinstance(scorecard, dict) or "uhqs" not in scorecard:
                raise aep_mod.AepError(
                    f"{scorecard_path}: --scorecard must be a UHBS scorecard JSON "
                    "object containing uhqs (AEP never mutates it)"
                )
        result = aep_mod.analyze(
            experiment,
            rows,
            config=aep_mod.AnalyzeConfig(
                bootstrap_samples=bootstrap_samples,
                confidence=confidence,
                seed=seed,
                experiment_path=str(experiment_path),
                trials_path=str(trials_path),
                scorecard_ref=str(scorecard_path) if scorecard_path else None,
            ),
        )
        schema_errors = aep_mod.validate_schema(result, "advanced-evidence.schema.json")
        if schema_errors:
            for err in schema_errors:
                echo_error(f"ERROR output schema: {err}")
            sys.exit(1)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=2, sort_keys=True)
            fh.write("\n")
    except aep_mod.AepError as exc:
        raise click.ClickException(str(exc)) from exc

    echo_ok(f"OK  wrote {out_path}")
    echo_info(
        f"status={result['status']} control={result['control_status']} "
        f"warnings={len(result.get('warnings') or [])}"
    )
    echo_info("UHQS unchanged — AEP writes a separate evidence addendum only.")


@aep_group.command("report")
@click.argument("evidence", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--format",
    "fmt",
    type=click.Choice(["json", "markdown"]),
    default="markdown",
    show_default=True,
)
@click.option(
    "--include-methodology/--no-include-methodology",
    default=True,
    show_default=True,
)
@click.option(
    "--out",
    "out_path",
    type=click.Path(path_type=Path),
    default=None,
    help="Output path (default: stdout for markdown; required for json overwrite).",
)
def aep_report(
    evidence: Path,
    fmt: str,
    include_methodology: bool,
    out_path: Path | None,
) -> None:
    """Render an Advanced Evidence Addendum from analysis JSON."""
    from uhbs_cli import aep as aep_mod

    try:
        aep_mod.reject_forbidden_cli_values(
            str(evidence), str(out_path) if out_path else None
        )
        data = aep_mod.load_json(evidence)
        errors = aep_mod.validate_schema(data, "advanced-evidence.schema.json")
        if errors:
            for err in errors:
                echo_error(f"ERROR {err}")
            sys.exit(1)
        if fmt == "json":
            text = json.dumps(data, indent=2, sort_keys=True) + "\n"
            target = out_path or Path("advanced-evidence.json")
        else:
            text = aep_mod.render_markdown(
                data, include_methodology=include_methodology
            )
            target = out_path
            if target is None:
                click.echo(text, nl=False)
                return
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        echo_ok(f"OK  wrote {target}")
    except aep_mod.AepError as exc:
        raise click.ClickException(str(exc)) from exc


@aep_group.group("slm")
def aep_slm_group() -> None:
    """Alpha SLM evaluator for AEP trials (opt-in; disabled by default).

    Not activated until you edit a local aep-slm.yaml (enabled + unlock phrase
    + attestations). Does not change UHQS. Lab/sandbox only.
    """


@aep_slm_group.command("init")
@click.option(
    "--out",
    "out_path",
    type=click.Path(path_type=Path),
    default=Path("aep-slm.yaml"),
    show_default=True,
    help="Path for the disabled-by-default alpha config.",
)
@click.option(
    "--experiment",
    "experiment_path",
    default="experiment.yaml",
    show_default=True,
    help="Relative/local path recorded under paths.experiment.",
)
@click.option(
    "--force/--no-force",
    default=False,
    show_default=True,
    help="Overwrite an existing config file.",
)
def aep_slm_init(out_path: Path, experiment_path: str, force: bool) -> None:
    """Write a disabled alpha SLM config (must edit file to activate)."""
    from uhbs_cli import aep_slm as slm

    try:
        path = slm.write_init_config(
            out_path, force=force, experiment_path=experiment_path
        )
    except slm.AepSlmError as exc:
        raise click.ClickException(str(exc)) from exc
    echo_ok(f"OK  wrote {path}")
    echo_warn(
        "AEP SLM is ALPHA and DISABLED. Edit the YAML (enabled, unlock_phrase, "
        "activation.*) before uhbs aep slm generate."
    )


@aep_slm_group.command("validate")
@click.argument("config", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--require-unlocked/--allow-locked",
    default=False,
    show_default=True,
    help="Fail if activation gates are not fully unlocked.",
)
@click.option("--json", "as_json", is_flag=True, help="Emit machine-readable status.")
def aep_slm_validate(config: Path, require_unlocked: bool, as_json: bool) -> None:
    """Validate an aep-slm.yaml and report whether generation is unlocked."""
    from uhbs_cli import aep_slm as slm

    try:
        data = slm.load_config(config)
        errors = slm.validate_config(data, require_unlocked=require_unlocked)
        report = slm.status_report(data)
    except slm.AepSlmError as exc:
        raise click.ClickException(str(exc)) from exc
    if as_json:
        click.echo(json.dumps(report, indent=2, sort_keys=True))
    else:
        if report["schema_ok"]:
            echo_ok("OK  schema")
        else:
            for err in report["schema_errors"]:
                echo_error(f"ERROR {err}")
        if report["unlocked"]:
            echo_ok("OK  activation unlocked (generate permitted)")
        else:
            echo_warn("LOCKED  generation blocked until you edit the config:")
            for blocker in report["activation_blockers"]:
                echo_warn(f"  - {blocker}")
        echo_info("UHQS unchanged — SLM output is AEP trial evidence only.")
    if errors:
        sys.exit(1)


@aep_slm_group.command("status")
@click.argument("config", type=click.Path(exists=True, path_type=Path))
@click.option("--json", "as_json", is_flag=True)
def aep_slm_status(config: Path, as_json: bool) -> None:
    """Show activation status for an alpha SLM config (never runs a model)."""
    from uhbs_cli import aep_slm as slm

    try:
        data = slm.load_config(config)
        report = slm.status_report(data)
    except slm.AepSlmError as exc:
        raise click.ClickException(str(exc)) from exc
    if as_json:
        click.echo(json.dumps(report, indent=2, sort_keys=True))
        return
    echo_info(f"status={report['status']} provider={report['provider']}")
    echo_info(f"enabled={report['enabled']} unlocked={report['unlocked']}")
    if report["activation_blockers"]:
        echo_warn("Activation blockers:")
        for blocker in report["activation_blockers"]:
            echo_warn(f"  - {blocker}")
    else:
        echo_ok("No activation blockers")
    if report["schema_errors"]:
        for err in report["schema_errors"]:
            echo_error(f"ERROR {err}")
        sys.exit(1)


@aep_slm_group.command("generate")
@click.argument("config", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--force/--no-force",
    default=False,
    show_default=True,
    help="Overwrite existing output_trials / output_run paths.",
)
def aep_slm_generate(config: Path, force: bool) -> None:
    """Generate AEP trials from an unlocked alpha SLM config.

    Refuses default/locked configs. Lab/sandbox only. Does not change UHQS.
    """
    from uhbs_cli import aep_slm as slm

    try:
        data = slm.load_config(config)
        result = slm.generate_trials(data, config_path=config, force=force)
    except slm.AepSlmError as exc:
        raise click.ClickException(str(exc)) from exc
    echo_ok(f"OK  wrote {result['trials_path']} ({result['trial_count']} trials)")
    echo_ok(f"OK  wrote {result['run_path']}")
    echo_warn(
        "Next (offline): uhbs aep validate-trials … && uhbs aep analyze … "
        "(UHQS unchanged)"
    )


if __name__ == "__main__":
    main()
