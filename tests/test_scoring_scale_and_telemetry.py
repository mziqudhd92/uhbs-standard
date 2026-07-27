"""Regression tests for Module A score-scale + Module C JSONL + TPS P95 defaults.

Covers the 2026-07-27 "leading honeypot scores F unfairly" remediation:
  1. RFC / timing CheckResult scores are 0–100 (geometric mean stays meaningful)
  2. ``*.json`` files that are actually JSONL parse as events, not 1 malformed
  3. Class/protocol-aware Module E P95 defaults (SSH ≠ 100ms)
"""

from __future__ import annotations

import json
from pathlib import Path

from uhbs_core.check_scoring import score_checks
from uhbs_core.models import CheckResult
from uhbs_core.rfc_probes import RFCSuiteResult
from uhbs_core.test_telemetry import _iter_records
from uhbs_core.tps import (
    CLASS_DEFAULT_P95_MS,
    default_p95_latency_ms,
    default_tps_for_class,
    load_tps,
)


def test_perfect_ssh_rfc_suite_scores_near_100_not_25() -> None:
    """Partial-point scores (25+25+20+30) used to cap a perfect suite at ~25
    under geometric mean. Normalized 0–100 checks must score ~100."""
    checks = [
        CheckResult(id="rfc4253.identification_crlf", team="blue", passed=True, score=100.0),
        CheckResult(id="rfc4253.kexinit_after_id", team="blue", passed=True, score=100.0),
        CheckResult(id="rfc4253.legacy_version_handling", team="blue", passed=True, score=100.0),
        CheckResult(id="rfc4253.reject_null_in_id", team="red", passed=True, score=100.0),
    ]
    assert score_checks(checks) == 100.0
    suite = RFCSuiteResult(protocol="ssh", rfc="RFC 4253", checks=checks)
    assert suite.score == 100.0


def test_one_rfc_fail_still_drags_but_not_to_structural_floor() -> None:
    checks = [
        CheckResult(id="a", team="blue", passed=True, score=100.0),
        CheckResult(id="b", team="blue", passed=True, score=100.0),
        CheckResult(id="c", team="blue", passed=True, score=100.0),
        CheckResult(id="d", team="red", passed=False, score=0.0),
    ]
    result = score_checks(checks)
    # gmean with floor 0.5 → still low, but a perfect-minus-one suite is
    # distinguishable from the old structural ~25 ceiling on a *passing* suite.
    assert 0.0 < result < 40.0


def test_jsonl_content_in_json_extension_parses_events(tmp_path: Path) -> None:
    events = [
        {"eventid": "session.connect", "src_ip": "1.2.3.4"},
        {"eventid": "session.closed", "src_ip": "1.2.3.4"},
        {"eventid": "command.input", "input": "uname -a"},
    ]
    path = tmp_path / "honeypot.json"
    path.write_text("\n".join(json.dumps(e) for e in events) + "\n", encoding="utf-8")
    rows = _iter_records(path)
    malformed = sum(1 for r in rows if isinstance(r, dict) and "__malformed__" in r)
    assert malformed == 0
    assert len(rows) == 3
    assert rows[0]["eventid"] == "session.connect"


def test_true_single_json_object_still_loads(tmp_path: Path) -> None:
    path = tmp_path / "bundle.json"
    path.write_text(json.dumps({"type": "bundle", "objects": []}), encoding="utf-8")
    rows = _iter_records(path)
    assert len(rows) == 1
    assert rows[0]["type"] == "bundle"


def test_ssh_default_p95_is_multi_second_not_100ms() -> None:
    assert default_p95_latency_ms("Low-Interaction", "ssh") == 3000.0
    assert default_p95_latency_ms("POSIX-Shell", "ssh") == 3000.0
    tps = default_tps_for_class("Low-Interaction", "ssh")
    assert tps.expected_p95_latency_ms == 3000.0


def test_class_only_default_p95_uses_class_table() -> None:
    assert default_p95_latency_ms("Low-Interaction", None) == CLASS_DEFAULT_P95_MS[
        "Low-Interaction"
    ]
    assert default_p95_latency_ms("Web-API", None) == 150.0


def test_builtin_low_interaction_ssh_tps_has_realistic_p95() -> None:
    from uhbs_core.tps import PROFILES_DIR

    tps = load_tps(PROFILES_DIR / "low_interaction_ssh.yaml")
    assert tps.expected_p95_latency_ms >= 2000.0
