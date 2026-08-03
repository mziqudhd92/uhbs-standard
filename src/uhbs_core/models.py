"""UHBS v4.4.0 — Universal Honeypot Benchmarking Standard shared types."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from uhbs_core.uhqs_math import (
    PROFILE_WEIGHTS as _LETTER_WEIGHTS,
)
from uhbs_core.uhqs_math import (
    compute_uhqs as _shared_compute_uhqs,
)
from uhbs_core.uhqs_math import (
    grade_for,
    weights_for_class_dims,
)

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

WEIGHTS_POSIX = weights_for_class_dims("POSIX-Shell")
PROFILE_WEIGHTS: dict[str, dict[str, float]] = {
    name: weights_for_class_dims(name) for name in _LETTER_WEIGHTS
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
    evidence: list[str] = field(default_factory=list)
    # Circuit-breaker gate (2026-07-27 architecture review): a critical=True
    # check that fails hard-caps the whole check-list aggregate to 0.0 via
    # uhbs_core.check_scoring.score_checks, instead of being diluted by an
    # arithmetic/geometric mean with unrelated passing checks. Reserve this
    # for genuine security gatekeepers (auth rejection, protocol header
    # validation, data-plane integrity) — not every check should be critical.
    critical: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ModuleResult:
    module: str  # A|B|C|D|E|F|SOURCE
    dimension: str
    score: float
    status: str
    checks: list[CheckResult] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
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
    source_root: str | None = None
    host: str | None = None
    port: int = 2222
    user: str = "root"
    password: str = "root"
    telemetry_dir: str | None = None
    profile: str | None = None  # signals profile stem OR path to TPS
    baseline_native_host: str | None = None
    container_image: str | None = None
    smtp_port: int | None = None
    http_port: int | None = None
    ssh_port: int | None = None
    # UHBS v4
    tps_path: str | None = None
    protocol: str | None = None  # primary protocol id
    protocols: list[str] = field(default_factory=list)  # multi-protocol
    profile_class: str = "POSIX-Shell"
    ports_map: dict[str, int] = field(default_factory=dict)
    # Lab inventory annotations (mcp_path, mcp_transport, mcp_custom_allowlist_tools, …)
    annotations: dict[str, Any] = field(default_factory=dict)

    @property
    def label(self) -> str:
        return self.name or self.host or self.source_root or "unknown"

    def effective_ssh_port(self) -> int:
        """Legacy helper — prefer ``shell_exec_port()`` for Module D.

        Only returns an explicit SSH listener. Does **not** invent SSH on the
        primary application port (e.g. PJL :9100 or HTTP :9200).
        """
        port = self.shell_exec_port()
        if port is not None:
            return port
        raise ValueError(
            "no explicit SSH listener configured "
            "(set ports.ssh / ssh_port, or --protocol ssh --port …)"
        )

    def shell_exec_port(self) -> int | None:
        """Port for remote shell / containment probes (Module D).

        Protocol-agnostic rule: shell probes run **only** when SSH is
        explicitly configured. Never treat the primary decoy port as SSH
        just because a TPS mentioned ssh elsewhere.
        """
        if "ssh" in self.ports_map:
            return int(self.ports_map["ssh"])
        if self.ssh_port is not None:
            return int(self.ssh_port)
        return None

    def port_for(self, protocol: str) -> int | None:
        p = protocol.lower()
        if p in self.ports_map:
            return int(self.ports_map[p])
        if p == "ssh":
            return self.shell_exec_port()
        if p == "smtp":
            if self.smtp_port is not None:
                return self.smtp_port
            if self.protocol and self.protocol.lower() == "smtp":
                return int(self.port)
            return None
        if p in {"http", "https"}:
            if self.http_port is not None:
                return self.http_port
            if self.protocol and self.protocol.lower() in {"http", "https"}:
                return int(self.port)
            return None
        # Unknown / custom protocols (pjl, redis, …): map primary port when it matches
        if self.protocol and self.protocol.lower() == p:
            return int(self.port)
        return None

    def protocol_list(self) -> list[str]:
        if self.protocols:
            return [x.lower() for x in self.protocols if x]
        if self.protocol:
            return [self.protocol.lower()]
        # Infer from configured ports — never invent SSH by default
        found: list[str] = []
        for key in sorted(self.ports_map.keys()):
            found.append(key.lower())
        if not found and self.shell_exec_port() is not None:
            found.append("ssh")
        if not found and self.http_port is not None:
            found.append("http")
        if not found and self.smtp_port is not None:
            found.append("smtp")
        return found


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
    weights: dict[str, float]
    profile_class: str
    grade: str
    phase: str = "combined"
    version: str = "4.4.0"
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

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def weights_for_class(profile_class: str) -> dict[str, float]:
    return weights_for_class_dims(profile_class)


def compute_uhqs(
    scores: dict[str, float],
    target: str,
    profile_class: str = "POSIX-Shell",
    phase: str = "combined",
    *,
    containment_measured: bool = True,
) -> UHQSResult:
    """UHQS = δ_C · (w_A·S_A + w_B·S_B + w_C·S_C + w_E·S_E + w_F·S_F).

    Missing module scores raise ``KeyError`` (never silently default to 0.0).
    Math is delegated to ``uhbs_core.uhqs_math`` (shared with the CLI).
    """
    result = _shared_compute_uhqs(
        scores,
        profile_class=profile_class,
        containment_measured=containment_measured,
    )
    s = result.scores
    return UHQSResult(
        target=target,
        S_A=round(s["A"], 2),
        S_B=round(s["B"], 2),
        S_C=round(s["C"], 2),
        C=round(s["D"], 2),
        S_E=round(s["E"], 2),
        S_F=round(s["F"], 2),
        delta_c=round(result.delta_c, 4),
        uhqs=result.uhqs,
        weights=weights_for_class(profile_class),
        profile_class=profile_class,
        grade=grade_for(result.uhqs),
        phase=phase,
        version="4.4.0",
        containment_measured=containment_measured,
    )


# Backward-compatible name
HQSResult = UHQSResult


def compute_hqs(
    scores: dict[str, float],
    target: str,
    phase: str = "combined",
    profile_class: str = "POSIX-Shell",
) -> UHQSResult:
    return compute_uhqs(scores, target=target, profile_class=profile_class, phase=phase)


def average_scores(*score_maps: dict[str, float]) -> dict[str, float]:
    out: dict[str, float] = {}
    for dim in DIMS:
        vals = [m[dim] for m in score_maps if dim in m]
        out[dim] = round(sum(vals) / len(vals), 2) if vals else 0.0
    return out
