"""Lightweight terminal styling for human-facing UHBS CLI output.

Uses ANSI codes only (no extra pip dependency). Click already depends on
colorama-compatible behavior on Windows; we still honor ``NO_COLOR`` /
``FORCE_COLOR`` and disable color when the stream is not a TTY.

For richer tables/panels later, optional ``rich`` could be added — not required
for notices and OK/ERROR lines.
"""

from __future__ import annotations

import os
import sys
from typing import Any, TextIO


def colors_enabled(stream: TextIO | None = None) -> bool:
    """Return True when ANSI colors should be emitted on ``stream``."""
    if os.environ.get("NO_COLOR", "").strip() != "":
        return False
    force = os.environ.get("FORCE_COLOR", "").strip()
    if force not in ("", "0", "false", "False"):
        return True
    target = stream if stream is not None else sys.stderr
    try:
        return bool(target.isatty())
    except Exception:  # pragma: no cover
        return False


def style(
    text: str,
    *,
    fg: str | None = None,
    bold: bool = False,
    stream: TextIO | None = None,
) -> str:
    """Wrap ``text`` in ANSI SGR codes when colors are enabled for ``stream``."""
    if not colors_enabled(stream):
        return text
    codes: list[str] = []
    if bold:
        codes.append("1")
    fg_map = {
        "black": "30",
        "red": "31",
        "green": "32",
        "yellow": "33",
        "blue": "34",
        "magenta": "35",
        "cyan": "36",
        "white": "37",
        "bright_red": "91",
        "bright_green": "92",
        "bright_yellow": "93",
        "bright_cyan": "96",
    }
    if fg in fg_map:
        codes.append(fg_map[fg])
    if not codes:
        return text
    return f"\033[{';'.join(codes)}m{text}\033[0m"


def format_notice(message: str, *, stream: TextIO | None = None) -> str:
    label = style("NOTICE:", fg="bright_yellow", bold=True, stream=stream)
    body = style(message, fg="yellow", stream=stream)
    return f"{label} {body}"


def format_ok(message: str, *, stream: TextIO | None = None) -> str:
    return style(message, fg="bright_green", stream=stream)


def format_error(message: str, *, stream: TextIO | None = None) -> str:
    return style(message, fg="bright_red", bold=True, stream=stream)


def format_warn(message: str, *, stream: TextIO | None = None) -> str:
    return style(message, fg="bright_yellow", stream=stream)


def format_info(message: str, *, stream: TextIO | None = None) -> str:
    return style(message, fg="bright_cyan", stream=stream)


def echo(
    message: str,
    *,
    err: bool = False,
    nl: bool = True,
    **_kwargs: Any,
) -> None:
    """Print to stdout/stderr (Click-compatible ``err`` / ``nl`` kwargs)."""
    stream: TextIO = sys.stderr if err else sys.stdout
    end = "\n" if nl else ""
    print(message, file=stream, end=end)


def echo_ok(message: str, *, err: bool = False) -> None:
    stream: TextIO = sys.stderr if err else sys.stdout
    echo(format_ok(message, stream=stream), err=err)


def echo_error(message: str) -> None:
    echo(format_error(message, stream=sys.stderr), err=True)


def echo_warn(message: str, *, err: bool = False) -> None:
    stream: TextIO = sys.stderr if err else sys.stdout
    echo(format_warn(message, stream=stream), err=err)


def echo_info(message: str, *, err: bool = False) -> None:
    stream: TextIO = sys.stderr if err else sys.stdout
    echo(format_info(message, stream=stream), err=err)
