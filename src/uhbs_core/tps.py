"""Target Profile Specification (TPS) loader — UHBS v4.0 §3."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from .models import TargetSpec

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None

PROFILES_DIR = Path(__file__).resolve().parent / "profiles" / "tps"


@dataclass
class TPS:
    name: str
    profile_class: str = "POSIX-Shell"
    protocol: str = "ssh"
    protocols: List[str] = field(default_factory=list)
    expected_p95_latency_ms: float = 150.0
    strict_rfc_enforcement: bool = True
    allowed_outbound_traffic: bool = False
    allow_local_code_execution: bool = False
    timing_samples: int = 1000  # UHBS A3 formal default; UHBS_QUICK=1 shortens
    gold_baseline_host: Optional[str] = None
    gold_baseline_port: Optional[int] = None
    # Protocols that should KS/HASSH-compare against the gold host (default: ssh only).
    gold_baseline_protocols: List[str] = field(default_factory=lambda: ["ssh"])
    raw: Dict[str, Any] = field(default_factory=dict)

    def protocol_list(self) -> List[str]:
        if self.protocols:
            return [p.lower() for p in self.protocols]
        return [self.protocol.lower()]


def _load_yaml(path: Path) -> Dict[str, Any]:
    if yaml is None:
        raise RuntimeError("PyYAML required: pip install pyyaml")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"invalid TPS: {path}")
    return data


def load_tps(path: Path) -> TPS:
    data = _load_yaml(path)
    meta = data.get("target_metadata") or {}
    perf = data.get("performance_baseline") or {}
    safety = data.get("safety_boundary") or {}
    protocols = meta.get("protocols") or []
    if isinstance(protocols, str):
        protocols = [protocols]
    return TPS(
        name=str(meta.get("name") or path.stem),
        profile_class=str(meta.get("class") or meta.get("profile_class") or "POSIX-Shell"),
        protocol=str(meta.get("protocol") or "ssh"),
        protocols=[str(p) for p in protocols],
        expected_p95_latency_ms=float(perf.get("expected_p95_latency_ms", 150)),
        strict_rfc_enforcement=bool(perf.get("strict_rfc_enforcement", True)),
        allowed_outbound_traffic=bool(safety.get("allowed_outbound_traffic", False)),
        allow_local_code_execution=bool(safety.get("allow_local_code_execution", False)),
        timing_samples=int(perf.get("timing_samples", 1000)),
        gold_baseline_host=perf.get("gold_baseline_host") or meta.get("gold_baseline_host"),
        gold_baseline_port=(
            int(perf["gold_baseline_port"])
            if perf.get("gold_baseline_port") is not None
            else None
        ),
        gold_baseline_protocols=[
            str(p).lower()
            for p in (
                perf.get("gold_baseline_protocols")
                or meta.get("gold_baseline_protocols")
                or ["ssh"]
            )
        ],
        raw=data,
    )


def resolve_tps_path(name_or_path: Optional[str]) -> Optional[Path]:
    if not name_or_path:
        return None
    p = Path(name_or_path).expanduser()
    if p.is_file():
        return p
    cand = PROFILES_DIR / f"{name_or_path}.yaml"
    if cand.is_file():
        return cand
    cand2 = PROFILES_DIR / name_or_path
    if cand2.is_file():
        return cand2
    return None


def apply_tps(target: TargetSpec, tps: TPS) -> TargetSpec:
    """Mutate/enrich TargetSpec from TPS (non-destructive defaults)."""
    target.profile_class = tps.profile_class
    target.protocol = tps.protocol
    target.protocols = tps.protocol_list()
    if tps.gold_baseline_host and not target.baseline_native_host:
        target.baseline_native_host = tps.gold_baseline_host
    if not target.name or target.name == target.host:
        target.name = tps.name
    return target


def default_tps_for_class(profile_class: str, protocol: str = "ssh") -> TPS:
    return TPS(
        name=f"default-{profile_class}",
        profile_class=profile_class,
        protocol=protocol,
        protocols=[protocol],
    )
