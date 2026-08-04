"""Strict schema parity: root schemas/ vs packaged uhbs_cli/schemas/."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROOT_SCHEMAS = ROOT / "schemas"
PKG_SCHEMAS = ROOT / "src" / "uhbs_cli" / "schemas"


def _canonical(data: object) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


def test_mirrored_schemas_deep_equal() -> None:
    """Every schema present in both trees must deep-diff equal."""
    root_files = {p.name for p in ROOT_SCHEMAS.glob("*.schema.json")}
    pkg_files = {p.name for p in PKG_SCHEMAS.glob("*.schema.json")}
    shared = sorted(root_files & pkg_files)
    assert shared, "expected mirrored schemas"
    mismatches: list[str] = []
    for name in shared:
        root_data = json.loads((ROOT_SCHEMAS / name).read_text(encoding="utf-8"))
        pkg_data = json.loads((PKG_SCHEMAS / name).read_text(encoding="utf-8"))
        if _canonical(root_data) != _canonical(pkg_data):
            mismatches.append(name)
    assert mismatches == [], f"schema drift between schemas/ and uhbs_cli/schemas/: {mismatches}"


def test_experimental_schemas_packaged() -> None:
    for name in (
        "experimental-matrix.schema.json",
        "experimental-provenance.schema.json",
        "genai-benchmark-report.schema.json",
    ):
        assert (ROOT_SCHEMAS / name).is_file()
        assert (PKG_SCHEMAS / name).is_file()
