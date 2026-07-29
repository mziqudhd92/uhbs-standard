"""Packaged schema resolution for PyPI installs."""

from __future__ import annotations

from uhbs_cli.cli import _schema_dir


def test_packaged_schemas_include_scorecard() -> None:
    schema_dir = _schema_dir()
    assert (schema_dir / "scorecard.schema.json").is_file()
    assert (schema_dir / "profile.schema.json").is_file()
    assert (schema_dir / "evidence-pack.schema.json").is_file()
