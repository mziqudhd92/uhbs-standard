"""Tests for optional Advanced Evidence Profile (offline analysis only)."""

from __future__ import annotations

import ast
import json
import socket
import subprocess
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

from uhbs_cli import aep as aep_mod
from uhbs_cli.cli import main
from uhbs_cli.scoring import assert_scorecard_integrity

ROOT = Path(__file__).resolve().parents[1]
BEGINNER = ROOT / "examples" / "advanced-evidence" / "beginner"
ADVANCED = ROOT / "examples" / "advanced-evidence" / "advanced"
COWRIE = ROOT / "docs" / "conformance" / "fixtures" / "cowrie-low-interaction.scorecard.json"

FORBIDDEN_IMPORT_ROOTS = {
    "socket",
    "ssl",
    "http",
    "urllib",
    "requests",
    "httpx",
    "aiohttp",
    "paramiko",
    "subprocess",
    "asyncio",
    "docker",
    "kubernetes",
    "uhbs_core",
    "uhbs_mcp",
}


def test_packaged_aep_schemas_exist() -> None:
    schema_dir = Path(aep_mod.__file__).resolve().parent / "schemas"
    for name in (
        "aep-experiment.schema.json",
        "aep-trial.schema.json",
        "aep-slm.schema.json",
        "advanced-evidence.schema.json",
    ):
        assert (schema_dir / name).is_file(), name


def test_aep_module_import_policy() -> None:
    src = Path(aep_mod.__file__).read_text(encoding="utf-8")
    tree = ast.parse(src)
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    bad = sorted(imported & FORBIDDEN_IMPORT_ROOTS)
    assert bad == [], f"AEP module must not import {bad}"


def test_beginner_example_end_to_end(tmp_path: Path) -> None:
    experiment = yaml.safe_load((BEGINNER / "experiment.yaml").read_text(encoding="utf-8"))
    assert aep_mod.validate_experiment(experiment) == []
    trials = aep_mod.load_trials_jsonl(BEGINNER / "trials.jsonl")
    assert aep_mod.validate_trials(trials, experiment) == []
    result = aep_mod.analyze(
        experiment,
        trials,
        config=aep_mod.AnalyzeConfig(
            bootstrap_samples=200,
            confidence=0.95,
            seed=7,
            experiment_path=str(BEGINNER / "experiment.yaml"),
            trials_path=str(BEGINNER / "trials.jsonl"),
            scorecard_ref=str(BEGINNER / "linked-scorecard.json"),
        ),
    )
    assert result["uhqs_unchanged"] is True
    assert result["status"] in {"valid", "inconclusive"}
    assert result["metrics"]["dtdr"]["value"] is not None
    assert result["metrics"]["dtdr"]["value"] > 1.0
    assert result["metrics"]["vod"]["details"]["delta_uhqs_forbidden"] is True
    assert aep_mod.validate_schema(result, "advanced-evidence.schema.json") == []

    out = tmp_path / "advanced-evidence.json"
    out.write_text(json.dumps(result), encoding="utf-8")
    md = aep_mod.render_markdown(result)
    assert "does **not** change UHQS" in md
    assert "Informative only" in md
    assert "lab / sandbox" in md.lower() or "laboratory" in md.lower()
    assert "10.1145/3314058.3314067" in md  # Zhu 2019 credit
    assert "does not imply endorsement" in md.lower()


def test_analyze_deterministic() -> None:
    experiment = yaml.safe_load((BEGINNER / "experiment.yaml").read_text(encoding="utf-8"))
    trials = aep_mod.load_trials_jsonl(BEGINNER / "trials.jsonl")
    cfg = aep_mod.AnalyzeConfig(bootstrap_samples=100, seed=123)
    a = aep_mod.analyze(experiment, trials, config=cfg)
    b = aep_mod.analyze(experiment, trials, config=cfg)
    # generated_at differs — compare metrics only
    assert a["metrics"] == b["metrics"]
    assert a["status"] == b["status"]


def test_refuse_without_reference() -> None:
    experiment = aep_mod.default_experiment_template(
        name="no-ref", profile_class="Web-API", trials=3, seed=1
    )
    trials = [
        aep_mod.example_trial_line(
            experiment_id=experiment["experiment_id"],
            trial_id=f"decoy-{i}",
            arm="decoy",
            duration=100,
        )
        for i in range(3)
    ]
    with pytest.raises(aep_mod.AepError, match="reference"):
        aep_mod.analyze(experiment, trials)


def test_missing_utility_blocks_vod() -> None:
    experiment = aep_mod.default_experiment_template(
        name="no-util", profile_class="Web-API", trials=3, seed=1
    )
    experiment["utility"]["weights"] = {}
    # bypass schema for unit metric behavior
    trials = []
    for arm, dur in (("decoy", 100.0), ("reference", 50.0)):
        for i in range(3):
            row = aep_mod.example_trial_line(
                experiment_id=experiment["experiment_id"],
                trial_id=f"{arm}-{i}",
                arm=arm,
                duration=dur,
            )
            trials.append(row)
    vod = aep_mod.compute_vod(
        trials, experiment, bootstrap_samples=10, confidence=0.95, seed=1
    )
    assert vod["status"] == "not_computed"
    assert vod["value"] is None


def test_control_failed_status() -> None:
    experiment = aep_mod.default_experiment_template(
        name="ctrl-fail", profile_class="Web-API", trials=3, seed=1
    )
    experiment["primary_outcome"] = "vod"
    trials = []
    for arm, dur in (("decoy", 100.0), ("reference", 50.0)):
        for i in range(3):
            trials.append(
                aep_mod.example_trial_line(
                    experiment_id=experiment["experiment_id"],
                    trial_id=f"{arm}-{i}",
                    arm=arm,
                    duration=dur,
                )
            )
    ctrl = aep_mod.example_trial_line(
        experiment_id=experiment["experiment_id"],
        trial_id="ctrl-1",
        arm="evaluator_control",
        duration=30,
    )
    ctrl["evaluator_control_passed"] = False
    trials.append(ctrl)
    result = aep_mod.analyze(
        experiment, trials, config=aep_mod.AnalyzeConfig(bootstrap_samples=50, seed=2)
    )
    assert result["status"] == "control_failed"
    assert result["control_status"] == "failed"


def test_censored_dtdr_uses_km() -> None:
    experiment = aep_mod.default_experiment_template(
        name="cens", profile_class="Low-Interaction", trials=5, seed=1
    )
    trials = []
    for i in range(5):
        d = aep_mod.example_trial_line(
            experiment_id=experiment["experiment_id"],
            trial_id=f"d-{i}",
            arm="decoy",
            duration=600 if i == 4 else 200 + i,
            censored=(i == 4),
        )
        r = aep_mod.example_trial_line(
            experiment_id=experiment["experiment_id"],
            trial_id=f"r-{i}",
            arm="reference",
            duration=80 + i,
            censored=False,
        )
        trials.extend([d, r])
    dtdr = aep_mod.compute_dtdr(trials, bootstrap_samples=50, confidence=0.95, seed=1)
    assert dtdr["details"]["estimator"] == "kaplan_meier_median_ratio"
    assert dtdr["status"] in {"valid", "inconclusive"}


def test_cli_rejects_url_inputs() -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        ["aep", "validate", "https://example.com/experiment.yaml"],
    )
    assert result.exit_code != 0
    assert "URL" in result.output or "local" in result.output.lower() or result.exit_code == 2


def test_cli_rejects_host_port_string() -> None:
    with pytest.raises(aep_mod.AepError, match="host:port"):
        aep_mod.reject_forbidden_cli_values("evil.example:2222")


def test_cli_beginner_analyze(tmp_path: Path) -> None:
    runner = CliRunner()
    out = tmp_path / "advanced-evidence.json"
    result = runner.invoke(
        main,
        [
            "aep",
            "analyze",
            "--experiment",
            str(BEGINNER / "experiment.yaml"),
            "--trials",
            str(BEGINNER / "trials.jsonl"),
            "--scorecard",
            str(BEGINNER / "linked-scorecard.json"),
            "--bootstrap-samples",
            "100",
            "--seed",
            "7",
            "--out",
            str(out),
        ],
    )
    assert result.exit_code == 0, result.output
    assert out.is_file()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["uhqs_unchanged"] is True

    md_out = tmp_path / "ADVANCED-EVIDENCE.md"
    report = runner.invoke(
        main,
        ["aep", "report", str(out), "--format", "markdown", "--out", str(md_out)],
    )
    assert report.exit_code == 0, report.output
    assert "UHQS" in md_out.read_text(encoding="utf-8")


def test_offline_safety_blocks_socket_and_subprocess(monkeypatch: pytest.MonkeyPatch) -> None:
    def boom(*_a, **_k):  # pragma: no cover
        raise AssertionError("network/process should not be used by AEP")

    monkeypatch.setattr(socket, "socket", boom)
    monkeypatch.setattr(socket, "create_connection", boom)
    monkeypatch.setattr(subprocess, "Popen", boom)
    monkeypatch.setattr(subprocess, "run", boom)
    monkeypatch.setattr(subprocess, "call", boom)

    experiment = yaml.safe_load((BEGINNER / "experiment.yaml").read_text(encoding="utf-8"))
    trials = aep_mod.load_trials_jsonl(BEGINNER / "trials.jsonl")
    result = aep_mod.analyze(
        experiment, trials, config=aep_mod.AnalyzeConfig(bootstrap_samples=20, seed=1)
    )
    assert result["uhqs_unchanged"] is True


def test_uhqs_fixtures_unchanged_by_aep() -> None:
    before = json.loads(COWRIE.read_text(encoding="utf-8"))
    uhqs_before = before["uhqs"]
    grade_before = before["grade"]
    assert assert_scorecard_integrity(before) == []

    # Analyze unrelated AEP data; scorecard file must remain byte-identical
    raw = COWRIE.read_bytes()
    experiment = yaml.safe_load((BEGINNER / "experiment.yaml").read_text(encoding="utf-8"))
    trials = aep_mod.load_trials_jsonl(BEGINNER / "trials.jsonl")
    _ = aep_mod.analyze(
        experiment,
        trials,
        config=aep_mod.AnalyzeConfig(
            bootstrap_samples=10,
            seed=1,
            scorecard_ref=str(COWRIE),
        ),
    )
    assert COWRIE.read_bytes() == raw
    after = json.loads(COWRIE.read_text(encoding="utf-8"))
    assert after["uhqs"] == uhqs_before
    assert after["grade"] == grade_before


def test_advanced_example_validates() -> None:
    experiment = yaml.safe_load((ADVANCED / "experiment.yaml").read_text(encoding="utf-8"))
    assert aep_mod.validate_experiment(experiment) == []
    trials = aep_mod.load_trials_jsonl(ADVANCED / "trials.jsonl")
    errors = aep_mod.validate_trials(trials, experiment)
    assert errors == [], errors
    result = aep_mod.analyze(
        experiment, trials, config=aep_mod.AnalyzeConfig(bootstrap_samples=50, seed=99)
    )
    assert result["metrics"]["fsv"]["global_scalar_emitted"] is False
    assert "protocol" in result["metrics"]["fsv"]["layers"]


def test_aep_init_writes_bundle(tmp_path: Path) -> None:
    runner = CliRunner()
    out = tmp_path / "bundle"
    result = runner.invoke(
        main,
        [
            "aep",
            "init",
            "--name",
            "unit-init",
            "--class",
            "ICS-SCADA",
            "--trials",
            "2",
            "--seed",
            "3",
            "--out",
            str(out),
        ],
    )
    assert result.exit_code == 0, result.output
    assert (out / "experiment.yaml").is_file()
    assert (out / "trials.jsonl").is_file()
    v = runner.invoke(main, ["aep", "validate", str(out / "experiment.yaml")])
    assert v.exit_code == 0, v.output
    # Second init without --force must refuse overwrite
    refused = runner.invoke(
        main,
        ["aep", "init", "--name", "unit-init", "--out", str(out)],
    )
    assert refused.exit_code != 0


def test_aep_init_trials_one_is_valid(tmp_path: Path) -> None:
    runner = CliRunner()
    out = tmp_path / "t1"
    result = runner.invoke(
        main,
        ["aep", "init", "--trials", "1", "--out", str(out)],
    )
    assert result.exit_code == 0, result.output
    vt = runner.invoke(
        main,
        [
            "aep",
            "validate-trials",
            str(out / "trials.jsonl"),
            "--experiment",
            str(out / "experiment.yaml"),
        ],
    )
    assert vt.exit_code == 0, vt.output
    an = runner.invoke(
        main,
        [
            "aep",
            "analyze",
            "--experiment",
            str(out / "experiment.yaml"),
            "--trials",
            str(out / "trials.jsonl"),
            "--bootstrap-samples",
            "20",
            "--out",
            str(tmp_path / "out.json"),
        ],
    )
    # n=1 per arm is inconclusive for DTDR, but schema write must succeed
    assert an.exit_code == 0, an.output


def test_analyze_without_scorecard_succeeds(tmp_path: Path) -> None:
    runner = CliRunner()
    out = tmp_path / "advanced-evidence.json"
    result = runner.invoke(
        main,
        [
            "aep",
            "analyze",
            "--experiment",
            str(ADVANCED / "experiment.yaml"),
            "--trials",
            str(ADVANCED / "trials.jsonl"),
            "--bootstrap-samples",
            "20",
            "--seed",
            "1",
            "--out",
            str(out),
        ],
    )
    assert result.exit_code == 0, result.output
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["provenance"]["scorecard_ref"] is None
    assert data["uhqs_unchanged"] is True


def test_template_example_analyzes(tmp_path: Path) -> None:
    runner = CliRunner()
    out = tmp_path / "tmpl"
    export = runner.invoke(main, ["aep", "example", "template", "--out", str(out)])
    assert export.exit_code == 0, export.output
    result = runner.invoke(
        main,
        [
            "aep",
            "analyze",
            "--experiment",
            str(out / "experiment.yaml"),
            "--trials",
            str(out / "trials.jsonl"),
            "--bootstrap-samples",
            "20",
            "--out",
            str(tmp_path / "tmpl-out.json"),
        ],
    )
    assert result.exit_code == 0, result.output


def test_unvalidated_scorecard_ref_not_in_provenance() -> None:
    experiment = yaml.safe_load((BEGINNER / "experiment.yaml").read_text(encoding="utf-8"))
    assert experiment.get("scorecard_ref")
    trials = aep_mod.load_trials_jsonl(BEGINNER / "trials.jsonl")
    result = aep_mod.analyze(
        experiment,
        trials,
        config=aep_mod.AnalyzeConfig(bootstrap_samples=20, seed=1),
    )
    assert result["provenance"]["scorecard_ref"] is None
    assert any("not validated" in w for w in result["warnings"])


def test_aep_example_exports_packaged_beginner(tmp_path: Path) -> None:
    runner = CliRunner()
    out = tmp_path / "exported"
    result = runner.invoke(
        main,
        ["aep", "example", "beginner", "--out", str(out)],
    )
    assert result.exit_code == 0, result.output
    assert (out / "experiment.yaml").is_file()
    assert (out / "trials.jsonl").is_file()
    assert (out / "linked-scorecard.json").is_file()
    assert aep_mod.packaged_data_dir().joinpath("beginner", "experiment.yaml").is_file()


def test_uhbs_schema_dir_env(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    schema_dir = tmp_path / "schemas"
    schema_dir.mkdir()
    # Point at real packaged schemas via copy of one file missing others → expect error
    monkeypatch.setenv("UHBS_SCHEMA_DIR", str(schema_dir))
    with pytest.raises(aep_mod.AepError, match="schema not found"):
        aep_mod.load_schema("aep-experiment.schema.json")
    # Restore by copying real schemas
    real = Path(aep_mod.__file__).resolve().parent / "schemas"
    for name in (
        "aep-experiment.schema.json",
        "aep-trial.schema.json",
        "advanced-evidence.schema.json",
    ):
        (schema_dir / name).write_text(
            (real / name).read_text(encoding="utf-8"), encoding="utf-8"
        )
    schema = aep_mod.load_schema("aep-experiment.schema.json")
    assert schema["title"]


def test_empty_yaml_rejected(tmp_path: Path) -> None:
    path = tmp_path / "empty.yaml"
    path.write_text("", encoding="utf-8")
    with pytest.raises(aep_mod.AepError, match="empty"):
        aep_mod.load_yaml(path)


def test_forbidden_fields_in_experiment() -> None:
    experiment = aep_mod.default_experiment_template(
        name="bad", profile_class="Web-API", trials=2, seed=1
    )
    experiment["host"] = "10.0.0.1"  # type: ignore[typeddict-item]
    errors = aep_mod.validate_experiment(experiment)
    assert any("forbidden field" in e for e in errors)
