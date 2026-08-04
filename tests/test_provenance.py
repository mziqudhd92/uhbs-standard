"""Experimental host provenance — rate limits, hashing, attach."""

from __future__ import annotations

import json
from pathlib import Path

from click.testing import CliRunner

from uhbs_cli import provenance as prov_mod
from uhbs_cli.cli import main


def test_summarize_rate_limit_drops_overflow() -> None:
    events = [{"type": "exec", "pid": i, "redacted": True} for i in range(100)]
    report = prov_mod.summarize_events(
        events,
        collector={"name": "t", "placement": "sandbox_host", "threat_model": "container_root"},
        max_events=10,
        aggregation="by_type",
        platform="linux",
    )
    assert report["uhqs_unchanged"] is True
    assert report["summary"]["accepted"] == 10
    assert report["summary"]["dropped"] == 90
    assert report["summary"]["overflow"] is True
    assert report["digest"]["algorithm"] == "sha256"
    assert len(report["digest"]["value"]) == 64
    assert prov_mod.validate_report(report) == []


def test_not_applicable_non_linux() -> None:
    report = prov_mod.summarize_events(
        [{"type": "exec"}],
        platform="darwin",
    )
    assert report["status"] == "not_applicable"


def test_tamper_changes_digest() -> None:
    events = [
        {"type": "exec", "pid": 1, "probe_id": "d1", "redacted": True},
        {"type": "connect", "pid": 2, "probe_id": "d1", "redacted": True},
    ]
    a = prov_mod.summarize_events(events, max_events=50, platform="linux")
    b = prov_mod.summarize_events(
        events + [{"type": "mount", "pid": 3, "redacted": True}],
        max_events=50,
        platform="linux",
    )
    assert a["digest"]["value"] != b["digest"]["value"]


def test_attach_manifest(tmp_path: Path) -> None:
    events = [{"type": "exec", "pid": 1, "redacted": True}]
    report = prov_mod.summarize_events(events, platform="linux")
    manifest_path = tmp_path / "MANIFEST.json"
    updated = prov_mod.attach_digest_to_manifest(manifest_path, report)
    assert updated["experimental_provenance"]["digest"] == report["digest"]["value"]
    assert any(a.get("kind") == "experimental_provenance" for a in updated["artifacts"])


def test_provenance_example_cli(tmp_path: Path) -> None:
    runner = CliRunner()
    out = tmp_path / "p"
    result = runner.invoke(main, ["provenance", "example", "beginner", "--out", str(out)])
    assert result.exit_code == 0, result.output
    summary = tmp_path / "summary.json"
    result = runner.invoke(
        main,
        [
            "provenance",
            "summarize",
            str(out / "events.jsonl"),
            "--collector",
            str(out / "collector.json"),
            "--out",
            str(summary),
        ],
    )
    assert result.exit_code == 0, result.output
    data = json.loads(summary.read_text(encoding="utf-8"))
    assert data["summary"]["accepted"] >= 1
    result = runner.invoke(main, ["provenance", "validate", str(summary)])
    assert result.exit_code == 0, result.output
