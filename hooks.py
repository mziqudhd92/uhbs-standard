"""MkDocs hooks — copy discovery files GitHub Pages needs (dotdirs, etc.)."""

from __future__ import annotations

import shutil
from pathlib import Path


def on_post_build(config, **kwargs) -> None:
    """Ensure .well-known/security.txt is published (MkDocs skips dotdirs)."""
    docs_dir = Path(config["docs_dir"])
    site_dir = Path(config["site_dir"])
    src = docs_dir / ".well-known" / "security.txt"
    if not src.is_file():
        return
    dest_dir = site_dir / ".well-known"
    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest_dir / "security.txt")
