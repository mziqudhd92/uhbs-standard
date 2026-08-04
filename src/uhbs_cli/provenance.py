"""UHBS experimental host provenance — collector-neutral offline validation.

Ingests JSONL event exports, applies rate limits / aggregation BEFORE hashing,
and emits an informative summary. Does not change UHQS. Does not load eBPF.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from uhbs_cli import __version__

PROVENANCE_SCHEMA_VERSION = "1.0.0"
DEFAULT_MAX_EVENTS = 5000
DEFAULT_MAX_BYTES = 2_000_000
EXAMPLE_BUNDLES = ("beginner", "advanced", "template")
EVENT_TYPES = frozenset(
    {"exec", "connect", "mount", "namespace", "privilege", "file_mutation", "other"}
)


class ProvenanceError(Exception):
    """User-facing provenance validation error."""


def _schema_dir() -> Path:
    env = os.environ.get("UHBS_SCHEMA_DIR")
    if env:
        return Path(env)
    packaged = Path(__file__).resolve().parent / "schemas"
    if (packaged / "experimental-provenance.schema.json").is_file():
        return packaged
    return Path(__file__).resolve().parents[2] / "schemas"


def packaged_data_dir() -> Path:
    return Path(__file__).resolve().parent / "data" / "experimental" / "provenance"


def load_schema(name: str = "experimental-provenance.schema.json") -> dict[str, Any]:
    path = _schema_dir() / name
    if not path.is_file():
        raise ProvenanceError(f"provenance schema not found: {path}")
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def validate_report(report: dict[str, Any]) -> list[str]:
    schema = load_schema()
    validator = Draft202012Validator(schema)
    return [
        f"{'/'.join(str(p) for p in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(report), key=lambda e: list(e.path))
    ]


def load_events_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as fh:
        for i, line in enumerate(fh, start=1):
            text = line.strip()
            if not text:
                continue
            try:
                obj = json.loads(text)
            except json.JSONDecodeError as exc:
                raise ProvenanceError(f"{path}:{i}: invalid JSON: {exc}") from exc
            if not isinstance(obj, dict):
                raise ProvenanceError(f"{path}:{i}: event must be an object")
            rows.append(obj)
    return rows


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonicalize_event(event: dict[str, Any]) -> dict[str, Any]:
    etype = str(event.get("type", "other")).lower()
    if etype not in EVENT_TYPES:
        etype = "other"
    return {
        "type": etype,
        "ts": event.get("ts"),
        "pid": event.get("pid"),
        "cgroup": event.get("cgroup"),
        "container_id": event.get("container_id"),
        "probe_id": event.get("probe_id"),
        "redacted": bool(event.get("redacted", False)),
    }


def summarize_events(
    events: list[dict[str, Any]],
    *,
    collector: dict[str, Any] | None = None,
    max_events: int = DEFAULT_MAX_EVENTS,
    max_bytes: int = DEFAULT_MAX_BYTES,
    aggregation: str = "by_type",
    platform: str | None = None,
) -> dict[str, Any]:
    """Rate-limit and aggregate events, then hash the filtered view."""
    if platform and platform.lower() not in {"linux", "linux-x86_64", "linux-aarch64"}:
        return {
            "schema_version": PROVENANCE_SCHEMA_VERSION,
            "uhbs_version": __version__,
            "status": "not_applicable",
            "uhqs_unchanged": True,
            "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
            "collector": {
                "name": (collector or {}).get("name", "none"),
                "placement": (collector or {}).get("placement", "unknown"),
                "platform": platform,
                "threat_model": (collector or {}).get("threat_model", "unspecified"),
            },
            "summary": {
                "event_counts": {},
                "accepted": 0,
                "dropped": 0,
                "overflow": False,
                "correlated_probe_ids": [],
            },
            "digest": {
                "algorithm": "sha256",
                "value": _sha256_hex(b"not_applicable"),
                "chain_root": _sha256_hex(b"not_applicable"),
            },
            "notes": "Host provenance is Linux-oriented; platform marked not_applicable.",
        }

    accepted: list[dict[str, Any]] = []
    dropped = 0
    overflow = False
    running_bytes = 0
    chain = hashlib.sha256()

    for raw in events:
        if len(accepted) >= max_events:
            dropped += 1
            overflow = True
            continue
        canon = _canonicalize_event(raw)
        encoded = json.dumps(canon, sort_keys=True, separators=(",", ":")).encode()
        if running_bytes + len(encoded) > max_bytes:
            dropped += 1
            overflow = True
            continue
        running_bytes += len(encoded)
        accepted.append(canon)
        chain.update(encoded)
        chain.update(b"\n")

    counts = Counter(e["type"] for e in accepted)
    if aggregation == "by_type":
        digest_payload = json.dumps(
            {"counts": dict(sorted(counts.items())), "accepted": len(accepted), "dropped": dropped},
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    else:
        digest_payload = json.dumps(accepted, sort_keys=True, separators=(",", ":")).encode()

    probe_ids = sorted(
        {str(e["probe_id"]) for e in accepted if e.get("probe_id")}
    )

    col = collector or {
        "name": "synthetic",
        "placement": "sandbox_host",
        "threat_model": "container_root",
    }
    report = {
        "schema_version": PROVENANCE_SCHEMA_VERSION,
        "uhbs_version": __version__,
        "status": "experimental",
        "uhqs_unchanged": True,
        "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "collector": {
            "name": str(col.get("name", "synthetic")),
            "version": col.get("version"),
            "placement": str(col.get("placement", "sandbox_host")),
            "platform": platform or col.get("platform", "linux"),
            "threat_model": str(col.get("threat_model", "container_root")),
        },
        "limits": {
            "max_events": max_events,
            "max_bytes": max_bytes,
            "aggregation": aggregation,
        },
        "summary": {
            "event_counts": dict(sorted(counts.items())),
            "accepted": len(accepted),
            "dropped": dropped,
            "overflow": overflow,
            "correlated_probe_ids": probe_ids,
        },
        "digest": {
            "algorithm": "sha256",
            "value": _sha256_hex(digest_payload),
            "chain_root": chain.hexdigest(),
        },
        "notes": (
            "Filtered/aggregated events hashed before attach. "
            "Optional signed envelopes (in-toto/COSE/DSSE) are a follow-up."
        ),
    }
    # Drop null version
    if report["collector"].get("version") is None:
        del report["collector"]["version"]

    errors = validate_report(report)
    if errors:
        raise ProvenanceError("report failed schema: " + "; ".join(errors[:5]))
    return report


def attach_digest_to_manifest(
    manifest_path: Path,
    report: dict[str, Any],
    *,
    artifact_name: str = "provenance-summary.json",
) -> dict[str, Any]:
    """Attach provenance digest reference into an existing MANIFEST.json-like object."""
    if manifest_path.is_file():
        with manifest_path.open(encoding="utf-8") as fh:
            manifest = json.load(fh)
    else:
        manifest = {"artifacts": []}
    if not isinstance(manifest, dict):
        raise ProvenanceError("manifest root must be an object")
    artifacts = manifest.setdefault("artifacts", [])
    if not isinstance(artifacts, list):
        raise ProvenanceError("manifest.artifacts must be a list")
    digest = report["digest"]["value"]
    entry = {
        "path": artifact_name,
        "sha256": digest,
        "kind": "experimental_provenance",
        "uhqs_unchanged": True,
    }
    # Replace existing provenance artifact if present
    artifacts[:] = [
        a
        for a in artifacts
        if not (isinstance(a, dict) and a.get("kind") == "experimental_provenance")
    ]
    artifacts.append(entry)
    manifest["experimental_provenance"] = {
        "digest": digest,
        "chain_root": report["digest"]["chain_root"],
        "accepted": report["summary"]["accepted"],
        "dropped": report["summary"]["dropped"],
        "overflow": report["summary"].get("overflow", False),
    }
    return manifest


def export_example_bundle(name: str, out_dir: Path, *, force: bool = False) -> Path:
    if name not in EXAMPLE_BUNDLES:
        raise ProvenanceError(
            f"Unknown provenance example {name!r}. Choose one of: {', '.join(EXAMPLE_BUNDLES)}"
        )
    src = packaged_data_dir() / name
    if not src.is_dir():
        raise ProvenanceError(f"Packaged provenance example missing: {src}")
    out_dir = Path(out_dir)
    if out_dir.exists() and any(out_dir.iterdir()) and not force:
        raise ProvenanceError(
            f"Output directory {out_dir} is not empty. Choose an empty path or use --force."
        )
    out_dir.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        dest = out_dir / item.name
        if item.is_file():
            if dest.exists() and not force:
                raise ProvenanceError(f"Refusing to overwrite {dest}. Use --force.")
            shutil.copy2(item, dest)
    return out_dir
