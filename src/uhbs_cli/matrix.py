"""UHBS experimental five-dimension matrix — offline informative analysis.

Does not change UHQS, weights, or δ_C. Missing dimensions stay missing
(never silently scored as 0 or 50).
"""

from __future__ import annotations

import json
import os
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from uhbs_cli import __version__

MATRIX_SCHEMA_VERSION = "1.0.0"
DIMENSION_KEYS = (
    "fingerprinting_resistance",
    "interaction_depth",
    "artifact_protocol_fidelity",
    "data_quality_actionability",
    "resource_overhead",
)
EXAMPLE_BUNDLES = ("beginner", "advanced", "template")


class MatrixError(Exception):
    """User-facing matrix validation or analysis error."""


def _schema_dir() -> Path:
    env = os.environ.get("UHBS_SCHEMA_DIR")
    if env:
        return Path(env)
    packaged = Path(__file__).resolve().parent / "schemas"
    if (packaged / "experimental-matrix.schema.json").is_file():
        return packaged
    return Path(__file__).resolve().parents[2] / "schemas"


def packaged_data_dir() -> Path:
    return Path(__file__).resolve().parent / "data" / "experimental" / "matrix"


def load_schema(name: str = "experimental-matrix.schema.json") -> dict[str, Any]:
    path = _schema_dir() / name
    if not path.is_file():
        raise MatrixError(f"matrix schema not found: {path}")
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as fh:
        data = json.load(fh)
    if data is None:
        raise MatrixError(f"{path}: JSON null root is not allowed")
    return data


def validate_input(data: dict[str, Any]) -> list[str]:
    """Validate a matrix *input* document (dimensions may be partial)."""
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["root must be an object"]
    dims = data.get("dimensions")
    if dims is None:
        return ["missing dimensions object"]
    if not isinstance(dims, dict):
        return ["dimensions must be an object"]
    for key, val in dims.items():
        if key not in DIMENSION_KEYS:
            errors.append(f"unknown dimension: {key}")
            continue
        if not isinstance(val, dict):
            errors.append(f"{key}: must be an object")
            continue
        status = val.get("status")
        if status not in {"scored", "missing", "not_applicable"}:
            errors.append(f"{key}: status must be scored|missing|not_applicable")
        if status == "scored":
            score = val.get("score")
            if not isinstance(score, (int, float)) or score < 0 or score > 100:
                errors.append(f"{key}: scored dimension requires score in 0..100")
        elif "score" in val and val["score"] is not None:
            errors.append(f"{key}: non-scored dimension must not set a numeric score")
    return errors


def validate_report(report: dict[str, Any]) -> list[str]:
    schema = load_schema()
    validator = Draft202012Validator(schema)
    return [
        f"{'/'.join(str(p) for p in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(report), key=lambda e: list(e.path))
    ]


def _normalize_dimension(raw: dict[str, Any] | None) -> dict[str, Any]:
    if not raw:
        return {"status": "missing", "score": None, "notes": "not provided"}
    status = str(raw.get("status", "missing"))
    if status == "scored":
        return {
            "status": "scored",
            "score": float(raw["score"]),
            "confidence": float(raw.get("confidence", 1.0)),
            "sample_count": int(raw.get("sample_count", 0)),
            "source": str(raw.get("source", "operator")),
            "notes": str(raw.get("notes", "")),
        }
    if status == "not_applicable":
        return {
            "status": "not_applicable",
            "score": None,
            "notes": str(raw.get("notes", "")),
        }
    return {
        "status": "missing",
        "score": None,
        "notes": str(raw.get("notes", "missing")),
    }


def analyze(data: dict[str, Any]) -> dict[str, Any]:
    """Compute equal-weight composite over present scored dimensions only."""
    errors = validate_input(data)
    if errors:
        raise MatrixError("; ".join(errors))

    dims_in = data.get("dimensions") or {}
    dimensions: dict[str, Any] = {}
    present_scores: list[float] = []
    missing: list[str] = []

    for key in DIMENSION_KEYS:
        dim = _normalize_dimension(dims_in.get(key))
        dimensions[key] = dim
        if dim["status"] == "scored":
            present_scores.append(float(dim["score"]))
        elif dim["status"] == "missing":
            missing.append(key)

    if present_scores:
        composite_score: float | None = round(
            sum(present_scores) / len(present_scores), 2
        )
    else:
        composite_score = None

    leave_one_out: dict[str, float | None] = {}
    for key in DIMENSION_KEYS:
        others = [
            float(dimensions[k]["score"])
            for k in DIMENSION_KEYS
            if k != key and dimensions[k]["status"] == "scored"
        ]
        leave_one_out[key] = (
            round(sum(others) / len(others), 2) if others else None
        )

    status = "experimental" if present_scores else "incomplete"
    report = {
        "schema_version": MATRIX_SCHEMA_VERSION,
        "uhbs_version": __version__,
        "status": status,
        "uhqs_unchanged": True,
        "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "scorecard_ref": data.get("scorecard_ref"),
        "notes": data.get(
            "notes",
            "Experimental equal-weight composite over present dimensions only.",
        ),
        "dimensions": dimensions,
        "composite": {
            "method": "equal_weight_present_only",
            "score": composite_score,
            "present_count": len(present_scores),
            "missing": missing,
        },
        "sensitivity": {
            "leave_one_out": leave_one_out,
            "notes": "Leave-one-out recomputes equal-weight mean without each dimension.",
        },
    }
    # Drop null optional scorecard_ref for cleaner JSON
    if report["scorecard_ref"] is None:
        del report["scorecard_ref"]

    schema_errors = validate_report(report)
    if schema_errors:
        raise MatrixError("report failed schema: " + "; ".join(schema_errors[:5]))
    return report


def export_example_bundle(name: str, out_dir: Path, *, force: bool = False) -> Path:
    if name not in EXAMPLE_BUNDLES:
        raise MatrixError(
            f"Unknown matrix example {name!r}. Choose one of: {', '.join(EXAMPLE_BUNDLES)}"
        )
    src = packaged_data_dir() / name
    if not src.is_dir():
        raise MatrixError(f"Packaged matrix example missing: {src}")
    out_dir = Path(out_dir)
    if out_dir.exists() and any(out_dir.iterdir()) and not force:
        raise MatrixError(
            f"Output directory {out_dir} is not empty. Choose an empty path or use --force."
        )
    out_dir.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        dest = out_dir / item.name
        if item.is_dir():
            if dest.exists() and force:
                shutil.rmtree(dest)
            shutil.copytree(item, dest, dirs_exist_ok=force)
        else:
            if dest.exists() and not force:
                raise MatrixError(f"Refusing to overwrite {dest}. Use --force.")
            shutil.copy2(item, dest)
    return out_dir


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Experimental Five-Dimension Matrix",
        "",
        f"- Status: `{report['status']}`",
        f"- UHQS unchanged: `{report['uhqs_unchanged']}`",
        f"- Composite ({report['composite']['method']}): "
        f"**{report['composite']['score']}** "
        f"({report['composite']['present_count']}/5 present)",
        "",
        "## Dimensions",
        "",
    ]
    for key in DIMENSION_KEYS:
        dim = report["dimensions"][key]
        score = dim.get("score")
        lines.append(
            f"- `{key}`: status={dim['status']}"
            + (f", score={score}" if score is not None else "")
        )
    missing = report["composite"].get("missing") or []
    if missing:
        lines.extend(["", f"Missing: {', '.join(missing)}"])
    lines.append("")
    return "\n".join(lines)
