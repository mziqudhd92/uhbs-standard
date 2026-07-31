"""Terminal styling helpers (NO_COLOR / TTY aware)."""

from __future__ import annotations

from uhbs_core import termui
from uhbs_core.notices import LAB_SANDBOX_NOTICE
from uhbs_core.termui import format_error, format_notice, format_ok


def test_no_color_disables_ansi(monkeypatch) -> None:
    monkeypatch.setenv("NO_COLOR", "1")
    monkeypatch.delenv("FORCE_COLOR", raising=False)
    assert "\033[" not in format_ok("OK hello")
    assert "\033[" not in format_error("ERROR boom")
    assert "\033[" not in format_notice(LAB_SANDBOX_NOTICE)


def test_force_color_enables_ansi(monkeypatch) -> None:
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.setenv("FORCE_COLOR", "1")
    assert "\033[" in format_ok("OK hello")
    assert "\033[" in format_error("ERROR boom")
    assert "\033[" in format_notice(LAB_SANDBOX_NOTICE)


def test_colors_enabled_respects_no_color(monkeypatch) -> None:
    monkeypatch.setenv("NO_COLOR", "1")
    assert termui.colors_enabled() is False
