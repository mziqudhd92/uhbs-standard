"""Tests for alpha AEP SLM evaluator — must stay off by default."""

from __future__ import annotations

import json
import shutil
import threading
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

from uhbs_cli import aep as aep_mod
from uhbs_cli import aep_slm as slm
from uhbs_cli.cli import main

ROOT = Path(__file__).resolve().parents[1]
BEGINNER = ROOT / "examples" / "advanced-evidence" / "beginner"
PACKAGED_SLM = (
    Path(slm.__file__).resolve().parent / "data" / "advanced-evidence" / "slm"
)


def _unlock(cfg: dict) -> dict:
    cfg = json.loads(json.dumps(cfg))  # deep copy via JSON
    cfg["enabled"] = True
    cfg["activation"] = {
        "unlock_phrase": slm.UNLOCK_PHRASE,
        "acknowledge_alpha": True,
        "lab_sandbox_only": True,
        "no_production_targets": True,
        "no_uhqs_scoring_impact": True,
        "allow_local_model_calls": False,
    }
    return cfg


def _prepare_experiment(tmp_path: Path, *, trials_per_arm: int = 5) -> Path:
    exp_dir = tmp_path / "exp"
    shutil.copytree(BEGINNER, exp_dir)
    exp = yaml.safe_load((exp_dir / "experiment.yaml").read_text(encoding="utf-8"))
    exp["repetitions"]["planned_per_arm"] = trials_per_arm
    exp["repetitions"]["minimum_per_arm"] = trials_per_arm
    (exp_dir / "experiment.yaml").write_text(
        yaml.safe_dump(exp, sort_keys=False), encoding="utf-8"
    )
    return exp_dir


def test_packaged_slm_schema_and_locked_template_exist() -> None:
    schema_dir = Path(aep_mod.__file__).resolve().parent / "schemas"
    assert (schema_dir / "aep-slm.schema.json").is_file()
    assert (ROOT / "schemas" / "aep-slm.schema.json").is_file()
    assert (PACKAGED_SLM / "aep-slm.yaml").is_file()
    locked = yaml.safe_load((PACKAGED_SLM / "aep-slm.yaml").read_text(encoding="utf-8"))
    assert locked["enabled"] is False
    assert locked["status"] == "alpha"
    assert locked["activation"]["unlock_phrase"] != slm.UNLOCK_PHRASE
    assert slm.activation_blockers(locked)
    assert slm.validate_config(locked) == []


def test_default_template_is_locked() -> None:
    cfg = slm.default_config_template()
    assert cfg["enabled"] is False
    blockers = slm.activation_blockers(cfg)
    assert any("enabled" in b for b in blockers)
    assert any("unlock_phrase" in b for b in blockers)
    assert slm.validate_config(cfg) == []
    assert slm.validate_config(cfg, require_unlocked=True)


def test_cli_init_writes_disabled_config(tmp_path: Path) -> None:
    out = tmp_path / "aep-slm.yaml"
    runner = CliRunner()
    result = runner.invoke(main, ["aep", "slm", "init", "--out", str(out)])
    assert result.exit_code == 0, result.output
    data = yaml.safe_load(out.read_text(encoding="utf-8"))
    assert data["enabled"] is False
    assert "DISABLED" in result.output or "disabled" in result.output.lower()


def test_generate_refuses_default_config(tmp_path: Path) -> None:
    shutil.copytree(BEGINNER, tmp_path / "exp")
    cfg_path = tmp_path / "aep-slm.yaml"
    slm.write_init_config(cfg_path, experiment_path="exp/experiment.yaml")
    cfg = slm.load_config(cfg_path)
    cfg["paths"]["experiment"] = str(tmp_path / "exp" / "experiment.yaml")
    cfg["paths"]["output_trials"] = str(tmp_path / "slm-trials.jsonl")
    cfg["paths"]["output_run"] = str(tmp_path / "slm-run.json")
    cfg_path.write_text(yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8")

    runner = CliRunner()
    result = runner.invoke(main, ["aep", "slm", "generate", str(cfg_path)])
    assert result.exit_code != 0
    assert "blocked" in result.output.lower() or "enabled" in result.output.lower()
    assert not (tmp_path / "slm-trials.jsonl").exists()


def test_partial_unlock_still_blocked(tmp_path: Path) -> None:
    cfg = slm.default_config_template()
    cfg["enabled"] = True
    assert slm.activation_blockers(cfg)
    with pytest.raises(slm.AepSlmError, match="blocked"):
        slm.generate_trials(cfg, config_path=tmp_path / "x.yaml")


def test_mock_generate_after_explicit_unlock(tmp_path: Path) -> None:
    exp_dir = _prepare_experiment(tmp_path, trials_per_arm=5)
    exp = yaml.safe_load((exp_dir / "experiment.yaml").read_text(encoding="utf-8"))

    cfg = _unlock(slm.default_config_template())
    cfg["provider"] = "mock"
    cfg["paths"] = {
        "experiment": str(exp_dir / "experiment.yaml"),
        "output_trials": str(tmp_path / "slm-trials.jsonl"),
        "output_run": str(tmp_path / "slm-run.json"),
    }
    cfg_path = tmp_path / "aep-slm.yaml"
    cfg_path.write_text(yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8")

    result = slm.generate_trials(cfg, config_path=cfg_path, force=True)
    assert result["trial_count"] == 15
    trials = aep_mod.load_trials_jsonl(result["trials_path"])
    assert aep_mod.validate_trials(trials, exp) == []
    assert all(t.get("evaluator", {}).get("kind") == "slm" for t in trials)
    assert all(t.get("evaluator", {}).get("status") == "alpha" for t in trials)

    # Timestamps must match declared duration.
    for trial in trials:
        t0 = datetime.fromisoformat(trial["started_at"].replace("Z", "+00:00"))
        t1 = datetime.fromisoformat(trial["ended_at"].replace("Z", "+00:00"))
        assert (t1 - t0).total_seconds() == pytest.approx(
            float(trial["session_duration_seconds"]), abs=1.0
        )

    run = json.loads(Path(result["run_path"]).read_text(encoding="utf-8"))
    assert run["uhqs_unchanged"] is True
    assert run["status"] == "alpha"

    analysis = aep_mod.analyze(
        exp,
        trials,
        config=aep_mod.AnalyzeConfig(
            bootstrap_samples=50,
            confidence=0.95,
            seed=1,
            experiment_path=str(exp_dir / "experiment.yaml"),
            trials_path=str(result["trials_path"]),
        ),
    )
    assert analysis["uhqs_unchanged"] is True


def test_cli_generate_after_unlock(tmp_path: Path) -> None:
    exp_dir = _prepare_experiment(tmp_path, trials_per_arm=5)
    cfg = _unlock(slm.default_config_template())
    cfg["paths"] = {
        "experiment": str(exp_dir / "experiment.yaml"),
        "output_trials": str(tmp_path / "slm-trials.jsonl"),
        "output_run": str(tmp_path / "slm-run.json"),
    }
    cfg_path = tmp_path / "aep-slm.yaml"
    cfg_path.write_text(yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8")

    runner = CliRunner()
    result = runner.invoke(main, ["aep", "slm", "generate", str(cfg_path)])
    assert result.exit_code == 0, result.output
    assert (tmp_path / "slm-trials.jsonl").is_file()
    assert (tmp_path / "slm-run.json").is_file()


def test_openai_compatible_rejects_non_loopback() -> None:
    cfg = _unlock(slm.default_config_template())
    cfg["provider"] = "openai_compatible"
    cfg["activation"]["allow_local_model_calls"] = True
    cfg["endpoint"] = {"base_url": "http://example.com:8080"}
    errors = slm.validate_config(cfg)
    assert any("loopback" in e.lower() or "127.0.0.1" in e for e in errors)


def test_recorded_does_not_require_allow_local_model_calls() -> None:
    cfg = _unlock(slm.default_config_template())
    cfg["provider"] = "recorded"
    cfg["recorded_responses_path"] = "recorded.jsonl"
    cfg["activation"]["allow_local_model_calls"] = False
    assert not any(
        "allow_local_model_calls" in b for b in slm.activation_blockers(cfg)
    )
    assert slm.validate_config(cfg, require_unlocked=True) == []


def test_recorded_generate_and_exhausted(tmp_path: Path) -> None:
    exp_dir = _prepare_experiment(tmp_path, trials_per_arm=1)
    responses = tmp_path / "recorded.jsonl"
    # 3 arms × 1 trial
    rows = []
    for arm in ("decoy", "reference", "evaluator_control"):
        rows.append(
            {
                "response": {
                    "session_duration_seconds": 90.0 if arm == "decoy" else 40.0,
                    "exchanges": 3,
                    "attempts": 2,
                    "predicted_decoy": arm == "decoy",
                    "confidence": 0.8,
                    "evaluator_control_passed": True,
                    "unique_tools": ["shell"],
                    "unique_credentials": [],
                    "unique_payload_families": ["recon"],
                }
            }
        )
    responses.write_text(
        "\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8"
    )

    cfg = _unlock(slm.default_config_template())
    cfg["provider"] = "recorded"
    cfg["recorded_responses_path"] = str(responses)
    cfg["generation"]["trials_per_arm"] = 1
    cfg["paths"] = {
        "experiment": str(exp_dir / "experiment.yaml"),
        "output_trials": str(tmp_path / "slm-trials.jsonl"),
        "output_run": str(tmp_path / "slm-run.json"),
    }
    result = slm.generate_trials(cfg, config_path=tmp_path / "aep-slm.yaml", force=True)
    assert result["trial_count"] == 3

    cfg["generation"]["trials_per_arm"] = 2
    with pytest.raises(slm.AepSlmError, match="exhausted"):
        slm.generate_trials(cfg, config_path=tmp_path / "aep-slm.yaml", force=True)


def test_strict_bool_coercion_rejects_string_false() -> None:
    with pytest.raises(slm.AepSlmError, match="JSON boolean"):
        slm._trial_from_response(
            experiment_id="e1",
            arm="decoy",
            trial_index=1,
            parsed={
                "session_duration_seconds": 10,
                "exchanges": 1,
                "predicted_decoy": "false",
                "confidence": 0.5,
            },
            raw="{}",
            config=slm.default_config_template(),
        )


def test_strict_number_coercion_rejects_bool() -> None:
    with pytest.raises(slm.AepSlmError, match="JSON number|JSON integer"):
        slm._trial_from_response(
            experiment_id="e1",
            arm="decoy",
            trial_index=1,
            parsed={
                "session_duration_seconds": True,
                "exchanges": 1,
                "predicted_decoy": True,
                "confidence": 0.5,
            },
            raw="{}",
            config=slm.default_config_template(),
        )


def test_bad_prompt_template_raises_aep_slm_error() -> None:
    with pytest.raises(slm.AepSlmError, match="user_prompt_template format error"):
        slm._render_user_prompt(
            "Arm={arm} missing={nope}",
            arm="decoy",
            trial_index=1,
            seed=1,
        )


def test_openai_compatible_refuses_redirect() -> None:
    class Handler(BaseHTTPRequestHandler):
        def do_POST(self) -> None:  # noqa: N802
            self.send_response(302)
            self.send_header("Location", "http://example.com/evil")
            self.end_headers()

        def log_message(self, format: str, *args: object) -> None:  # noqa: A003
            return

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        cfg = _unlock(slm.default_config_template())
        cfg["provider"] = "openai_compatible"
        cfg["activation"]["allow_local_model_calls"] = True
        cfg["endpoint"] = {
            "base_url": f"http://127.0.0.1:{port}",
            "timeout_seconds": 2,
        }
        with pytest.raises(slm.AepSlmError, match="redirect"):
            slm._call_openai_compatible(
                cfg, system_prompt="sys", user_prompt="user"
            )
    finally:
        server.shutdown()
        server.server_close()


def test_openai_compatible_caps_response_body() -> None:
    # Slightly over the cap so the client aborts early; keep the body modest so
    # the ThreadingHTTPServer write does not race the client close as hard.
    huge = b"x" * (slm.MAX_MODEL_RESPONSE_BYTES + 4096)

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self) -> None:  # noqa: N802
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(huge)))
            self.end_headers()
            try:
                self.wfile.write(huge)
            except (BrokenPipeError, ConnectionResetError):
                # Client closed after the size-cap refusal — expected.
                return

        def log_message(self, format: str, *args: object) -> None:  # noqa: A003
            return

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        cfg = _unlock(slm.default_config_template())
        cfg["provider"] = "openai_compatible"
        cfg["activation"]["allow_local_model_calls"] = True
        cfg["endpoint"] = {
            "base_url": f"http://127.0.0.1:{port}",
            "timeout_seconds": 2,
        }
        with pytest.raises(slm.AepSlmError, match="exceeds"):
            slm._call_openai_compatible(
                cfg, system_prompt="sys", user_prompt="user"
            )
    finally:
        server.shutdown()
        server.server_close()


def test_status_cli_json_locked(tmp_path: Path) -> None:
    out = tmp_path / "aep-slm.yaml"
    slm.write_init_config(out)
    runner = CliRunner()
    result = runner.invoke(main, ["aep", "slm", "status", str(out), "--json"])
    assert result.exit_code == 0, result.output
    start = result.output.find("{")
    end = result.output.rfind("}")
    assert start >= 0 and end > start
    report = json.loads(result.output[start : end + 1])
    assert report["unlocked"] is False
    assert report["default_activation"] is False
    assert report["uhqs_unchanged"] is True


def test_module_import_has_no_eager_urllib() -> None:
    src = Path(slm.__file__).read_text(encoding="utf-8")
    # Top-level import block should not pull urllib (lazy inside helpers).
    head = src.split("def default_config_template")[0]
    assert "urllib" not in head
