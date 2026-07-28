"""Per-run artifact digests for UHBS-Lab attestation."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_manifest(
    out_dir: Path,
    *,
    uhbs_version: str = "4.2.1",
    extra: dict[str, Any] | None = None,
) -> Path:
    """Write MANIFEST.json with SHA-256 digests of artifacts in out_dir."""
    artifacts = []
    for path in sorted(out_dir.rglob("*")):
        if not path.is_file():
            continue
        if path.name == "MANIFEST.json":
            continue
        rel = str(path.relative_to(out_dir))
        artifacts.append({"path": rel, "sha256": sha256_file(path)})

    payload: dict[str, Any] = {
        "uhbs_version": uhbs_version,
        "artifacts": artifacts,
    }
    if extra:
        payload["extra"] = extra

    dest = out_dir / "MANIFEST.json"
    dest.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return dest
