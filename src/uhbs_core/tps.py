"""Target Profile Specification (TPS) loader — UHBS v4.0 §3.

Protocol-agnostic rules:
  - Class weights and performance baselines come from the TPS.
  - Explicit inventory / CLI protocols MUST NOT be silently overwritten by a TPS.
  - Conflicting TPS vs explicit protocols raise ``ProtocolConflictError``.
  - Builtin ``low_interaction`` is class-only; use ``low_interaction_ssh`` for SSH/Telnet.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .models import TargetSpec

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None

PROFILES_DIR = Path(__file__).resolve().parent / "profiles" / "tps"


class ProtocolConflictError(ValueError):
    """TPS protocol set conflicts with an explicitly configured target protocol."""


@dataclass
class TPS:
    name: str
    profile_class: str = "POSIX-Shell"
    protocol: str | None = None
    protocols: list[str] = field(default_factory=list)
    expected_p95_latency_ms: float = 150.0
    strict_rfc_enforcement: bool = True
    allowed_outbound_traffic: bool = False
    allow_local_code_execution: bool = False
    timing_samples: int = 1000  # UHBS A3 formal default; UHBS_QUICK=1 shortens
    gold_baseline_host: str | None = None
    gold_baseline_port: int | None = None
    # Protocols that should KS/HASSH-compare against the gold host (default: none).
    gold_baseline_protocols: list[str] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)

    def protocol_list(self) -> list[str]:
        if self.protocols:
            return [p.lower() for p in self.protocols if str(p).strip()]
        if self.protocol and str(self.protocol).strip():
            return [self.protocol.lower()]
        return []


def _load_yaml(path: Path) -> dict[str, Any]:
    if yaml is None:
        raise RuntimeError("PyYAML required: pip install pyyaml")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise TypeError(f"invalid TPS: {path}")
    return data


def load_tps(path: Path) -> TPS:
    data = _load_yaml(path)
    meta = data.get("target_metadata") or {}
    perf = data.get("performance_baseline") or {}
    safety = data.get("safety_boundary") or {}
    protocols = meta.get("protocols") or []
    if isinstance(protocols, str):
        protocols = [protocols]
    protocols = [str(p) for p in protocols if str(p).strip()]
    # Do not default missing protocol to "ssh" — class-only TPS is valid.
    protocol = meta.get("protocol")
    if protocol is not None:
        protocol = str(protocol).strip() or None
    if protocol is None and protocols:
        protocol = protocols[0]

    gold_protos = perf.get("gold_baseline_protocols") or meta.get("gold_baseline_protocols")
    if gold_protos is None:
        # Only default gold compare to SSH when the TPS itself is SSH-scoped.
        ssh_scoped = protocol == "ssh" or "ssh" in {p.lower() for p in protocols}
        gold_protos = ["ssh"] if ssh_scoped else []

    return TPS(
        name=str(meta.get("name") or path.stem),
        profile_class=str(meta.get("class") or meta.get("profile_class") or "POSIX-Shell"),
        protocol=protocol,
        protocols=protocols,
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
        gold_baseline_protocols=[str(p).lower() for p in gold_protos],
        raw=data,
    )


def resolve_tps_path(name_or_path: str | None) -> Path | None:
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


def _explicit_protocols(target: TargetSpec) -> list[str]:
    return [p.lower() for p in target.protocol_list() if p]


def apply_tps(
    target: TargetSpec,
    tps: TPS,
    *,
    preserve_explicit_protocols: bool = True,
) -> TargetSpec:
    """Enrich TargetSpec from TPS without silently hijacking protocols.

    - Always applies profile class (+ name / gold host defaults).
    - If the target already has explicit protocols (inventory / ``--protocol``)
      and the TPS also lists protocols with **no overlap**, raises
      ``ProtocolConflictError``.
    - If the target already has protocols, they are preserved when
      ``preserve_explicit_protocols`` is true (default).
    - Class-only TPS files (no protocol list) never invent SSH.
    """
    target.profile_class = tps.profile_class
    if tps.gold_baseline_host and not target.baseline_native_host:
        target.baseline_native_host = tps.gold_baseline_host
    if not target.name or target.name == target.host:
        target.name = tps.name

    tps_protos = tps.protocol_list()
    explicit = _explicit_protocols(target)

    if explicit and tps_protos and not set(explicit) & set(tps_protos):
        raise ProtocolConflictError(
            "TPS protocols "
            f"{tps_protos} conflict with target protocols {explicit}. "
            "Use a matching TPS (e.g. low_interaction_ssh for SSH/Telnet), "
            "a class-only TPS (low_interaction), or drop --protocol / "
            "inventory protocol so the TPS can define listeners."
        )

    if preserve_explicit_protocols and explicit:
        # Keep inventory/CLI protocol binding; TPS only contributed class/perf.
        return target

    if tps_protos:
        target.protocol = tps.protocol or tps_protos[0]
        target.protocols = list(tps_protos)
    # else: class-only TPS — leave target.protocol(s) unchanged
    return target


def default_tps_for_class(profile_class: str, protocol: str | None = None) -> TPS:
    proto = protocol.strip().lower() if protocol and protocol.strip() else None
    return TPS(
        name=f"default-{profile_class}",
        profile_class=profile_class,
        protocol=proto,
        protocols=[proto] if proto else [],
    )
