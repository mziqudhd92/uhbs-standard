"""Path helpers for the UHBS MCP server."""

from __future__ import annotations

import os
from pathlib import Path


def repo_root() -> Path:
    """Resolve the UHBS checkout root (``UHBS_ROOT`` or editable layout)."""
    env = os.environ.get("UHBS_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    # src/uhbs_mcp/paths.py → repo root
    return Path(__file__).resolve().parents[2]


def schema_dir() -> Path:
    """Locate JSON Schemas for profile/scorecard/evidence validation."""
    env = os.environ.get("UHBS_SCHEMA_DIR")
    if env:
        return Path(env).expanduser().resolve()
    return repo_root() / "schemas"


def resolve_user_path(path: str) -> Path:
    """Resolve a tool path argument (absolute, or relative to ``UHBS_ROOT``)."""
    p = Path(path).expanduser()
    if not p.is_absolute():
        p = repo_root() / p
    return p.resolve()
