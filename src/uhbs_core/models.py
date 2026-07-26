"""UHBS v4.0 — Universal Honeypot Benchmarking Standard shared types."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional

# Module letter ↔ dimension keys (stable internal IDs)
DIM_A = "protocol"  # Module A — Protocol & Syntax Fidelity
DIM_B = "behavior"  # Module B — Behavioral & Stateful Realism
DIM_C = "telemetry"  # Module C — Telemetry Quality
DIM_D = "containment"  # Module D — Safety gate (δ_C)
DIM_E = "scale"  # Module E — Scalability & Latency
DIM_F = "static"  # Module F — White-Box Static Audit

# Backward-compatible aliases used by older module code
DIM_STEALTH = DIM_A
DIM_REALISM = DIM_B
DIM_TELEMETRY = DIM_C
DIM_CONTAINMENT = DIM_D
DIM_EFFICIENCY = DIM_E
DIM_STATIC = DIM_F

DIMS = (DIM_A, DIM_B, DIM_C, DIM_D, DIM_E, DIM_F)

# Default POSIX / Interactive Shells weights (UHBS §5.3)
WEIGHTS_POSIX = {
    DIM_A: 0.20,
    DIM_B: 0.25,
    DIM_C: 0.20,
    DIM_E: 0.15,
    DIM_F: 0.20,
}

PROFILE_WEIGHTS: Dict[str, Dict[str, float]] = {
    "POSIX-Shell": WEIGHTS_POSIX,
    "GenAI-Shell": WEIGHTS_POSIX,
    "Low-Interaction": {
        DIM_A: 0.30,
        DIM_B: 0.15,
        DIM_C: 0.25,
        DIM_E: 0.10,
        DIM_F: 0.20,
    },
    "ICS-SCADA": {
        DIM_A: 0.35,
        DIM_B: 0.20,
        DIM_C: 0.15,
        DIM_E: 0.10,
        DIM_F: 0.20,
    },
    "Web-API": {
        DIM_A: 0.25,
        DIM_B: 0.20,
        DIM_C: 0.20,
        DIM_E: 0.15,
        DIM_F: 0.20,
    },
    "Database": {
        DIM_A: 0.25,
        DIM_B: 0.25,
        DIM_C: 0.20,
        DIM_E: 0.10,
        DIM_F: 0.20,
    },
}

DIM_LABELS = {
    DIM_A: "Module A: Protocol Fidelity",
    DIM_B: "Module B: Behavioral Realism",
    DIM_C: "Module C: Telemetry Quality",
    DIM_D: "Module D: Safety & Containment (C)",
    DIM_E: "Module E: Scalability & Latency",
    DIM_F: "Module F: Static Code Audit",
}

# Scorecard attribute names
UHQS_ATTR = {
    DIM_A: "S_A",
    DIM_B: "S_B",
    DIM_C: "S_C",
    DIM_D: "C",
    DIM_E: "S_E",
    DIM_F: "S_F",
}


@dataclass
class CheckResult:
    id: str
    team: str  # blue | red | white
    passed: bool
    detail: str = ""
    score: float = 0.0
    evidence: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ModuleResult:
    module: str  # A|B|C|D|E|F|SOURCE
    dimension: str
    score: float
    status: str
    checks: List[CheckResult] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    notes: List[str] = field(default_factory=list)
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "module": self.module,
            "dimension": self.dimension,
            "score": self.score,
            "status": self.status,
            "checks": [c.to_dict() for c in self.checks],
            "metrics": self.metrics,
            "notes": self.notes,
            "error": self.error,
        }


@dataclass
class TargetSpec:
    """Runtime binding of a decoy instance (+ optional TPS)."""

    name: str
    kind: str = "generic"
    source_root: Optional[str] = None
    host: Optional[str] = None
    port: int = 2222
    user: str = "root"
    password: str = "root"
    telemetry_dir: Optional[str] = None
    profile: Optional[str] = None  # signals profile stem OR path to TPS
    baseline_native_host: Optional[str] = None
    container_image: Optional[str] = None
    smtp_port: Optional[int] = None
    http_port: Optional[int] = None
    ssh_port: Optional[int] = None
    # UHBS v4
    tps_path: Optional[str] = None
    protocol: Optional[str] = None  # primary protocol id
    protocols: List[str] = field(default_factory=list)  # multi-protocol
    profile_class: str = "POSIX-Shell"
    ports_map: Dict[str, int] = field(default_factory=dict)

    @property
    def label(self) -> str:
        return self.name or self.host or self.source_root or "unknown"

    def effective_ssh_port(self) -> int:
        if "ssh" in self.ports_map:
            return int(self.ports_map["ssh"])
        return int(self.ssh_port or self.port or 2222)

    def port_for(self, protocol: str) -> Optional[int]:
        p = protocol.lower()
        if p in self.ports_map:
            return int(self.ports_map[p])
        if p == "ssh":
            return self.effective_ssh_port()
        if p == "smtp":
            return self.smtp_port
        if p in {"http", "https"}:
            return self.http_port
        return self.port if self.protocol and self.protocol.lower() == p else None

    def protocol_list(self) -> List[str]:
        if self.protocols:
            return [x.lower() for x in self.protocols]
        if self.protocol:
            return [self.protocol.lower()]
        # Infer from configured ports
        found: List[str] = []
        if self.port_for("ssh"):
            found.append("ssh")
        if self.port_for("smtp"):
            found.append("smtp")
        if self.port_for("http"):
            found.append("http")
        return found or ["ssh"]


@dataclass
class UHQSResult:
    target: str
    S_A: float
    S_B: float
    S_C: float
    C: float
    S_E: float
    S_F: float
    delta_c: float
    uhqs: float
    weights: Dict[str, float]
    profile_class: str
    grade: str
    phase: str = "combined"
    version: str = "4.0"
    containment_measured: bool = True

    # Compat with older report code expecting .hqs / .S/.R/...
    @property
    def hqs(self) -> float:
        return self.uhqs

    @property
    def S(self) -> float:
        return self.S_A

    @property
    def R(self) -> float:
        return self.S_B

    @property
    def Q(self) -> float:
        return self.S_C

    @property
    def E(self) -> float:
        return self.S_E

    @property
    def F(self) -> float:
        return self.S_F

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def grade_for(uhqs: float) -> str:
    if uhqs >= 90:
        return "GRADE A (Enterprise Grade)"
    if uhqs >= 80:
        return "GRADE B (Production Candidate)"
    if uhqs >= 70:
        return "GRADE C (Lab / Limited)"
    if uhqs >= 50:
        return "GRADE D (Needs Remediation)"
    return "GRADE F (Fail)"


def weights_for_class(profile_class: str) -> Dict[str, float]:
    return dict(PROFILE_WEIGHTS.get(profile_class, WEIGHTS_POSIX))


def compute_uhqs(
    scores: Dict[str, float],
    target: str,
    profile_class: str = "POSIX-Shell",
    phase: str = "combined",
    *,
    containment_measured: bool = True,
) -> UHQSResult:
    """UHQS = δ_C · (w_A·S_A + w_B·S_B + w_C·S_C + w_E·S_E + w_F·S_F)."""
    # Accept both new and legacy dimension keys
    def g(*keys: str) -> float:
        for k in keys:
            if k in scores:
                return float(scores[k])
        return 0.0

    S_A = g(DIM_A, "stealth", "protocol")
    S_B = g(DIM_B, "realism", "behavior")
    S_C = g(DIM_C, "telemetry")
    C = g(DIM_D, "containment")
    S_E = g(DIM_E, "efficiency", "scale")
    S_F = g(DIM_F, "static")
    weights = weights_for_class(profile_class)
    # If Module D was not executed, do not apply a false δ_C=0 penalty
    if not containment_measured:
        delta_c = 1.0
    else:
        delta_c = 1.0 if C >= 95.0 else (C / 100.0) ** 2
    weighted = (
        weights[DIM_A] * S_A
        + weights[DIM_B] * S_B
        + weights[DIM_C] * S_C
        + weights[DIM_E] * S_E
        + weights[DIM_F] * S_F
    )
    uhqs = round(delta_c * weighted, 2)
    return UHQSResult(
        target=target,
        S_A=round(S_A, 2),
        S_B=round(S_B, 2),
        S_C=round(S_C, 2),
        C=round(C, 2),
        S_E=round(S_E, 2),
        S_F=round(S_F, 2),
        delta_c=round(delta_c, 4),
        uhqs=uhqs,
        weights={k: weights[k] for k in (DIM_A, DIM_B, DIM_C, DIM_E, DIM_F)},
        profile_class=profile_class,
        grade=grade_for(uhqs),
        phase=phase,
        version="4.0",
        containment_measured=containment_measured,
    )


# Backward-compatible name
HQSResult = UHQSResult


def compute_hqs(
    scores: Dict[str, float],
    target: str,
    phase: str = "combined",
    profile_class: str = "POSIX-Shell",
) -> UHQSResult:
    return compute_uhqs(scores, target=target, profile_class=profile_class, phase=phase)


def average_scores(*score_maps: Dict[str, float]) -> Dict[str, float]:
    out: Dict[str, float] = {}
    for dim in DIMS:
        vals = [m[dim] for m in score_maps if dim in m]
        out[dim] = round(sum(vals) / len(vals), 2) if vals else 0.0
    return out
