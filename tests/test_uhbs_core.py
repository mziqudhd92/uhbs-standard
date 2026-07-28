"""Tests for uhbs_core package surface."""

from __future__ import annotations

import json
from pathlib import Path

from uhbs_core import __version__
from uhbs_core.hqs import pass_status, scores_from_modules
from uhbs_core.manifest import write_manifest
from uhbs_core.models import ModuleResult, compute_uhqs
from uhbs_core.protocols import list_protocols
from uhbs_core.tps import PROFILES_DIR, load_tps, resolve_tps_path


def test_version_matches_spec() -> None:
    assert __version__ == "4.2.2"


def test_protocol_plugins_registered() -> None:
    names = set(list_protocols())
    assert {
        "ssh",
        "http",
        "mcp",
        "modbus",
        "s7comm",
        "generic",
        "mysql",
        "postgres",
        "pop3",
        "rdp",
        "sip",
        "snmp",
        "ntp",
        "tftp",
        "vnc",
        "git",
        "smb",
    }.issubset(names)


def test_tps_profiles_packaged() -> None:
    assert PROFILES_DIR.is_dir()
    path = resolve_tps_path("posix_shell_ssh")
    assert path is not None and path.exists()
    tps = load_tps(path)
    assert tps.profile_class in {"POSIX-Shell", "GenAI-Shell", "Low-Interaction"}

    mcp_path = resolve_tps_path("mcp_server")
    assert mcp_path is not None and mcp_path.exists()
    mcp_tps = load_tps(mcp_path)
    assert mcp_tps.profile_class == "Web-API"
    assert "mcp" in [p.lower() for p in mcp_tps.protocols]


def test_uhqs_matches_cli_math() -> None:
    # Anonymous Low-Interaction worked example (NOT live Cowrie fixture 48.70).
    # models.weights_for_class returns DIM_* keys consumed by compute_uhqs
    scores = {
        "protocol": 23.5,
        "behavior": 42.5,
        "telemetry": 57.0,
        "containment": 100.0,
        "scale": 55.0,
        "static": 69.0,
    }
    result = compute_uhqs(scores, target="li-baseline", profile_class="Low-Interaction")
    assert result.uhqs == 46.97
    assert result.delta_c == 1.0


def test_scores_from_modules_and_pass_status() -> None:
    mods = [
        ModuleResult(module="A", dimension="protocol", score=80, status="PASSED"),
        ModuleResult(module="B", dimension="behavior", score=10, status="PARTIAL"),
    ]
    scores = scores_from_modules(mods)
    assert scores["protocol"] == 80
    assert pass_status(80) == "PASSED"
    assert pass_status(10) == "PARTIAL"


def test_manifest_writer(tmp_path: Path) -> None:
    (tmp_path / "report.json").write_text('{"ok": true}\n', encoding="utf-8")
    (tmp_path / "SCORECARD.txt").write_text("UHQS\n", encoding="utf-8")
    dest = write_manifest(tmp_path, extra={"target": "unit"})
    data = json.loads(dest.read_text(encoding="utf-8"))
    assert data["uhbs_version"] == "4.2.2"
    paths = {a["path"] for a in data["artifacts"]}
    assert "report.json" in paths
    assert "SCORECARD.txt" in paths
    assert all(len(a["sha256"]) == 64 for a in data["artifacts"])
