"""Experimental GenAI/MCP helpers + replay bench — deterministic CI."""

from __future__ import annotations

import json
from pathlib import Path

from click.testing import CliRunner

from uhbs_cli import genai_bench as gb
from uhbs_cli.cli import main
from uhbs_core.genai import (
    GenAISafetyPolicy,
    generate_prompt_canary,
    parse_sse_ttft_ms,
    scan_for_leak,
    score_coherence,
    tarpit_penalize_high_latency,
)


def test_canary_leak_detection() -> None:
    canary = generate_prompt_canary(run_id="t")
    clean = scan_for_leak("hello world", canary)
    assert clean.leaked is False
    dirty = scan_for_leak(f"oops {canary.marker}", canary)
    assert dirty.leaked is True


def test_coherence_and_safety_gate() -> None:
    c, t, rate = score_coherence(
        [
            {"expected": "A", "actual": "A"},
            {"expected": "A", "actual": "B"},
        ]
    )
    assert (c, t, rate) == (1, 2, 0.5)
    policy = GenAISafetyPolicy(injection_budget=1)
    assert policy.assert_probe_allowed(tool_name="echo", attempts_used=0) is None
    assert policy.assert_probe_allowed(tool_name="exec", attempts_used=0) is not None
    assert policy.assert_probe_allowed(tool_name="echo", attempts_used=1) is not None


def test_tarpit_does_not_penalize_ttft() -> None:
    assert tarpit_penalize_high_latency("tarpit") is False
    assert tarpit_penalize_high_latency("normal") is True


def test_sse_ttft_parse() -> None:
    chunks = [(10.0, b": keep-alive\n"), (25.0, b"data: hello\n")]
    assert parse_sse_ttft_ms(chunks) == 25.0


def test_analyze_replay_beginner_deterministic() -> None:
    replay = gb.load_replay(gb.packaged_data_dir() / "beginner" / "replay.json")
    a = gb.analyze_replay(replay)
    b = gb.analyze_replay(replay)
    assert a["metrics"] == b["metrics"]
    assert a["mode"] == "replay"
    assert a["uhqs_unchanged"] is True
    assert a["timing_intent"] == "tarpit"
    assert a["metrics"]["ttft"]["penalize_high_latency"] is False
    assert a["metrics"]["clr"]["leaks"] == 1
    assert a["metrics"]["clr"]["attempts"] == 2
    # denylisted exec skipped → only echo + search count
    assert a["metrics"]["injection_attempts"] == 2
    assert gb.validate_report(a) == []


def test_genai_bench_cli(tmp_path: Path) -> None:
    runner = CliRunner()
    out = tmp_path / "g"
    result = runner.invoke(main, ["genai-bench", "example", "beginner", "--out", str(out)])
    assert result.exit_code == 0, result.output
    report = tmp_path / "report.json"
    result = runner.invoke(
        main,
        ["genai-bench", "analyze", str(out / "replay.json"), "--out", str(report)],
    )
    assert result.exit_code == 0, result.output
    data = json.loads(report.read_text(encoding="utf-8"))
    assert data["status"] == "experimental"
