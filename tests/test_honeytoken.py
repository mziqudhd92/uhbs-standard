"""Offline unit tests for uhbs_core.honeytoken (architecture-review item 3).

All tests here are fully offline: FileTailLogSource uses a tmp_path file,
no network/daemon dependency.
"""

from __future__ import annotations

import pytest

from uhbs_core.honeytoken import (
    CallbackLogSource,
    FileTailLogSource,
    generate_honeytoken,
    inject_honeytoken,
    verify_oob_alert,
)


def test_generate_honeytoken_aws_access_key_shape() -> None:
    tok = generate_honeytoken("aws_access_key")
    assert tok.value.startswith("AKIA")
    assert len(tok.value) == 20
    assert tok.secondary_value  # secret key populated
    assert tok.token_id.startswith("uhbs-")


def test_generate_honeytoken_api_token_shape() -> None:
    tok = generate_honeytoken("api_token")
    assert tok.value.startswith("sk_live_")
    assert len(tok.value) > len("sk_live_")


def test_generate_honeytoken_bait_file_shape() -> None:
    tok = generate_honeytoken("bait_file")
    assert tok.value.startswith("/etc/shadow_bait_")
    assert tok.token_id in tok.value
    assert tok.token_id in tok.secondary_value


def test_generate_honeytoken_unknown_kind_raises() -> None:
    with pytest.raises(ValueError):
        generate_honeytoken("not_a_real_kind")


def test_generate_honeytoken_ids_are_unique() -> None:
    ids = {generate_honeytoken("api_token").token_id for _ in range(20)}
    assert len(ids) == 20


def test_inject_honeytoken_calls_send_fn_and_returns_token_id() -> None:
    sent: list[str] = []
    tok = generate_honeytoken("api_token")
    returned_id = inject_honeytoken(sent.append, tok)
    assert returned_id == tok.token_id
    assert sent == [tok.value]


def test_inject_honeytoken_custom_render() -> None:
    sent: list[str] = []
    tok = generate_honeytoken("bait_file")
    inject_honeytoken(sent.append, tok, render=lambda t: f"GET {t.value} HTTP/1.1")
    assert sent[0].startswith("GET /etc/shadow_bait_")


def test_file_tail_log_source_ignores_pre_existing_content(tmp_path) -> None:
    log_path = tmp_path / "alerts.log"
    log_path.write_text("old line mentioning uhbs-deadbeef00000000\n")

    # Constructed AFTER the stale line was written -> must not match it.
    source = FileTailLogSource(log_path)
    found, detail = source.check("uhbs-deadbeef00000000")
    assert found is False
    assert "not found" not in detail  # file exists; just no new match


def test_file_tail_log_source_detects_appended_alert(tmp_path) -> None:
    log_path = tmp_path / "alerts.log"
    log_path.write_text("startup\n")
    source = FileTailLogSource(log_path)

    with log_path.open("a") as f:
        f.write("ALERT token=uhbs-cafebabe00000000 severity=high\n")

    found, detail = source.check("uhbs-cafebabe00000000")
    assert found is True
    assert "uhbs-cafebabe00000000" in detail


def test_file_tail_log_source_missing_file_reports_not_found() -> None:
    source = FileTailLogSource("/nonexistent/path/does/not/exist.log")
    found, detail = source.check("uhbs-anything")
    assert found is False
    assert "not found" in detail


def test_verify_oob_alert_passes_when_alert_appears(tmp_path) -> None:
    log_path = tmp_path / "alerts.log"
    log_path.write_text("")
    source = FileTailLogSource(log_path)
    tok = generate_honeytoken("api_token")

    with log_path.open("a") as f:
        f.write(f"alert fired for {tok.token_id}\n")

    result = verify_oob_alert(source, tok.token_id, timeout_s=0.3)
    assert result.passed is True
    assert result.score == 100.0
    assert tok.token_id in result.evidence[0]


def test_verify_oob_alert_fails_honestly_when_nothing_ever_fires(tmp_path) -> None:
    log_path = tmp_path / "alerts.log"
    log_path.write_text("")
    source = FileTailLogSource(log_path)
    tok = generate_honeytoken("api_token")

    result = verify_oob_alert(source, tok.token_id, timeout_s=0.1)
    assert result.passed is False
    assert result.score == 0.0
    assert tok.token_id in result.detail


def test_verify_oob_alert_with_callback_log_source() -> None:
    calls: list[str] = []

    def _fn(token_id: str) -> tuple[bool, str]:
        calls.append(token_id)
        return True, f"webhook saw {token_id}"

    source = CallbackLogSource(_fn)
    result = verify_oob_alert(source, "uhbs-xyz", timeout_s=0.2)
    assert result.passed is True
    assert calls == ["uhbs-xyz"]
