"""UHBS v4.0 scorecard + JSON report writer."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from .models import DIM_LABELS, DIMS, UHQS_ATTR, ModuleResult, TargetSpec, UHQSResult


def _status_line(mod: Optional[ModuleResult], score: float) -> str:
    if mod is None:
        return "N/A"
    if mod.status == "SKIPPED":
        return f"SKIPPED ({'; '.join(mod.notes[:1]) or 'not run'})"
    detail = ""
    failed = [c for c in mod.checks if not c.passed]
    passed = [c for c in mod.checks if c.passed]
    if failed:
        detail = failed[0].detail or failed[0].id
    elif passed:
        detail = passed[-1].detail or passed[-1].id
    st = mod.status if score < 70 or mod.status == "FAILED" else "PASSED"
    return f"{st}" + (f" ({detail})" if detail else "")


def render_card(
    target: TargetSpec,
    baseline: Optional[TargetSpec],
    uhqs: UHQSResult,
    modules: List[ModuleResult],
    environment: str = "Isolated Sandbox",
    evaluation_type: str = "Full-Spectrum (Static Audit + Dynamic Sandbox)",
) -> str:
    by_dim: Dict[str, ModuleResult] = {}
    for m in modules:
        if m.module == "SOURCE":
            by_dim.setdefault(m.dimension, m)
        else:
            by_dim[m.dimension] = m

    weights = uhqs.weights
    lines = [
        "====================================================================================",
        "                  UNIVERSAL HONEYPOT BENCHMARK SCORECARD v4.0",
        "====================================================================================",
        f"Target System         : {target.label}",
        f"System Profile Class  : {uhqs.profile_class}",
        f"Protocols             : {', '.join(target.protocol_list())}",
        f"Evaluation Date       : {datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
        f"Evaluation Type       : {evaluation_type}",
        f"Environment           : {environment}",
        "------------------------------------------------------------------------------------",
        "EVALUATION MODULE                     SCORE (0-100)    WEIGHT    STATUS",
        "------------------------------------------------------------------------------------",
    ]
    for dim in DIMS:
        label = DIM_LABELS[dim]
        score = getattr(uhqs, UHQS_ATTR[dim])
        if dim == "containment":
            wtxt = "GATE"
        else:
            wtxt = f"{weights.get(dim, 0):.2f}"
        status = _status_line(by_dim.get(dim), score)
        lines.append(f"{label:<36}: {score:>5.1f}/100       {wtxt:<6}   {status}")
    if not uhqs.containment_measured:
        gate = f"δ_C = {uhqs.delta_c} (Module D not run — gate not applied)"
    elif uhqs.delta_c >= 1.0:
        gate = f"δ_C = {uhqs.delta_c} (Containment Score C = {uhqs.C} >= 95)"
    else:
        gate = f"δ_C = {uhqs.delta_c} (C = {uhqs.C} < 95 — exponential penalty)"
    lines += [
        "------------------------------------------------------------------------------------",
        f"SAFETY GATE MULTIPLIER                : {gate}",
        f"FINAL COMPOSITE SCORE (UHQS 4.0)      : {uhqs.uhqs} / 100",
        f"OVERALL EVALUATION GRADE              : {uhqs.grade}",
        "====================================================================================",
    ]
    if baseline:
        lines.insert(6, f"Baseline System       : {baseline.label}")
    return "\n".join(lines) + "\n"


def write_report(
    out_dir: Path,
    target: TargetSpec,
    baseline: Optional[TargetSpec],
    uhqs: UHQSResult,
    modules: List[ModuleResult],
    extras: Optional[Dict[str, Any]] = None,
    evaluation_type: str = "Full-Spectrum (Static Audit + Dynamic Sandbox)",
) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    card = render_card(
        target, baseline, uhqs, modules, evaluation_type=evaluation_type
    )
    (out_dir / "REPORT.txt").write_text(card, encoding="utf-8")
    (out_dir / "SCORECARD.txt").write_text(card, encoding="utf-8")
    payload = {
        "framework": "Universal Honeypot Benchmarking Standard (UHBS) v4.0",
        "evaluation_type": evaluation_type,
        "target": {
            "name": target.name,
            "kind": target.kind,
            "host": target.host,
            "port": target.port,
            "source_root": target.source_root,
            "profile_class": target.profile_class,
            "protocols": target.protocol_list(),
            "ports_map": target.ports_map,
        },
        "baseline": (
            {
                "name": baseline.name,
                "kind": baseline.kind,
                "host": baseline.host,
                "protocols": baseline.protocol_list(),
            }
            if baseline
            else None
        ),
        "uhqs": uhqs.to_dict(),
        "hqs": uhqs.to_dict(),  # compat
        "modules": [m.to_dict() for m in modules],
        "extras": extras or {},
    }
    path = out_dir / "report.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path
