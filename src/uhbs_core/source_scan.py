"""Phase 0 — Source examination of source-available honeypot trees.

Maps static capability signals → D1–D5 so source and execution phases share
the same scoring dimensions before HQS 2.0 fusion.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from uhbs_core.hqs import pass_status
from uhbs_core.models import (
    DIM_CONTAINMENT,
    DIM_EFFICIENCY,
    DIM_REALISM,
    DIM_STEALTH,
    DIM_TELEMETRY,
    CheckResult,
    ModuleResult,
    TargetSpec,
)

# YAML profile keys → UHBS v4 dimension ids
YAML_TO_DIM = {
    "stealth": DIM_STEALTH,  # protocol
    "realism": DIM_REALISM,  # behavior
    "telemetry": DIM_TELEMETRY,
    "containment": DIM_CONTAINMENT,
    "efficiency": DIM_EFFICIENCY,  # scale
    "protocol": DIM_STEALTH,
    "behavior": DIM_REALISM,
    "scale": DIM_EFFICIENCY,
}
CAPABILITY_DIMS = (
    DIM_STEALTH,
    DIM_REALISM,
    DIM_TELEMETRY,
    DIM_CONTAINMENT,
    DIM_EFFICIENCY,
)
YAML_DIM_KEYS = ("stealth", "realism", "telemetry", "containment", "efficiency")

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None

PROFILES_DIR = Path(__file__).resolve().parent / "profiles"


def _load_yaml(path: Path) -> Dict[str, Any]:
    if yaml is None:
        raise RuntimeError("PyYAML required: pip install pyyaml")
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError(f"invalid signals profile: {path}")
    return data


def resolve_profile(kind: str, override: Optional[str] = None) -> Path:
    stem = override or kind
    path = PROFILES_DIR / f"{stem}_signals.yaml"
    if path.is_file():
        return path
    # Class-oriented default for OSS low-interaction SSH decoy source trees.
    if kind in {"generic", "cowrie", "low_interaction", "low-interaction"}:
        alt = PROFILES_DIR / "low_interaction_ssh_signals.yaml"
        if alt.is_file():
            return alt
    raise FileNotFoundError(f"no signals profile for kind={kind!r}: expected {path}")


_SKIP_PARTS = {".git", "node_modules", ".venv", "venv", "dist", "build", ".local"}


def _match_paths(root: Path, patterns: List[str], limit: int = 40) -> List[str]:
    hits: List[str] = []
    for pattern in patterns:
        for p in root.glob(pattern):
            if any(part in _SKIP_PARTS for part in p.parts):
                continue
            if p.is_file() or (p.is_dir() and any(p.iterdir())):
                hits.append(str(p.relative_to(root)))
                if len(hits) >= limit:
                    return hits
    return hits


def _content_matches(root: Path, rel_paths: List[str], regex: str, max_files: int = 25) -> bool:
    cre = re.compile(regex, re.IGNORECASE | re.MULTILINE)
    checked = 0
    for rel in rel_paths:
        path = root / rel
        files: List[Path]
        if path.is_dir():
            files = [p for p in path.rglob("*") if p.is_file()][:10]
        elif path.is_file():
            files = [path]
        else:
            continue
        for fp in files:
            checked += 1
            if checked > max_files:
                return False
            try:
                text = fp.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if cre.search(text):
                return True
    return False


def _score_dimension(root: Path, name: str, dim: Dict[str, Any]) -> ModuleResult:
    signals = dim.get("signals") or []
    earned = 0
    max_pts = 0
    checks: List[CheckResult] = []

    for sig in signals:
        sid = str(sig.get("id", "unnamed"))
        points = int(sig.get("points", 0))
        max_pts += points
        patterns = list(sig.get("paths") or ["**/*"])
        matched = _match_paths(root, patterns)
        content_re = sig.get("content")
        content_ok = True
        if content_re:
            content_ok = bool(matched) and _content_matches(root, matched, str(content_re))
        ok = bool(matched) and content_ok
        if ok:
            earned += points
        checks.append(
            CheckResult(
                id=f"source.{sid}",
                team="blue",
                passed=ok,
                detail=("hit: " + ", ".join(matched[:3])) if ok else "missing signal",
                score=float(points if ok else 0),
                evidence=matched[:8],
            )
        )

    score = 0.0 if max_pts == 0 else 100.0 * earned / max_pts
    return ModuleResult(
        module="SOURCE",
        dimension=name,
        score=round(score, 2),
        status=pass_status(score),
        checks=checks,
        metrics={"earned_points": earned, "max_points": max_pts},
        notes=[f"source_root={root}"],
    )


def scan_source(target: TargetSpec) -> List[ModuleResult]:
    """Return one ModuleResult per dimension from static source signals."""
    if not target.source_root:
        return [
            ModuleResult(
                module="SOURCE",
                dimension=d,
                score=0.0,
                status="SKIPPED",
                notes=["no source_root configured"],
            )
            for d in CAPABILITY_DIMS
        ]

    root = Path(target.source_root).expanduser().resolve()
    if not root.is_dir():
        return [
            ModuleResult(
                module="SOURCE",
                dimension=d,
                score=0.0,
                status="FAILED",
                error=f"source_root not found: {root}",
            )
            for d in CAPABILITY_DIMS
        ]

    try:
        profile_path = resolve_profile(target.kind, target.profile)
        profile = _load_yaml(profile_path)
    except Exception as exc:  # noqa: BLE001
        return [
            ModuleResult(
                module="SOURCE",
                dimension=d,
                score=0.0,
                status="FAILED",
                error=str(exc),
            )
            for d in CAPABILITY_DIMS
        ]

    dims = profile.get("dimensions") or {}
    results: List[ModuleResult] = []
    for yaml_key in YAML_DIM_KEYS:
        dim_id = YAML_TO_DIM[yaml_key]
        if yaml_key not in dims and dim_id not in dims:
            results.append(
                ModuleResult(
                    module="SOURCE",
                    dimension=dim_id,
                    score=0.0,
                    status="SKIPPED",
                    notes=[f"missing dimension in profile {profile_path.name}"],
                )
            )
            continue
        block = dims.get(yaml_key) or dims.get(dim_id) or {}
        m = _score_dimension(root, dim_id, block)
        m.notes.append(f"profile={profile_path.name}")
        results.append(m)
    return results
