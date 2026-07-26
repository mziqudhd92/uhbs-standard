#!/usr/bin/env python3
"""UHBS v4.0 — Universal Honeypot Benchmarking Standard orchestrator (uhbs-core).

Phases (§6):
  1) profile  — load TPS
  2) static   — Module F (+ optional capability signals)
  3) sandbox  — air-gap / egress preflight
  4) dynamic  — Modules A–E via protocol plugins
  5) score    — UHQS 4.0 with profile-adaptive weights + δ_C gate

Examples:
  uhbs lab --tps posix_shell_ssh --target 127.0.0.1 --port 2222 \\
    --source-root . --phases profile,static,dynamic,score \\
    --out .local/bench-reports/uhbs-v4

  uhbs lab --inventory inventory.yaml --target cowrie-local --phases profile,static,dynamic
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from uhbs_core import test_realism  # noqa: E402
from uhbs_core import test_safety  # noqa: E402
from uhbs_core import test_scale  # noqa: E402
from uhbs_core import test_static_code  # noqa: E402
from uhbs_core import test_stealth  # noqa: E402
from uhbs_core import test_telemetry  # noqa: E402
from uhbs_core import sandbox_preflight  # noqa: E402
from uhbs_core.hqs import scores_from_modules  # noqa: E402
from uhbs_core.inventory import load_inventory, resolve_target  # noqa: E402
from uhbs_core.models import (  # noqa: E402
    DIM_A,
    DIM_B,
    DIM_C,
    DIM_D,
    DIM_E,
    ModuleResult,
    TargetSpec,
    compute_uhqs,
)
from uhbs_core.protocols import list_protocols  # noqa: E402
from uhbs_core.report import render_card, write_report  # noqa: E402
from uhbs_core.source_scan import scan_source  # noqa: E402
from uhbs_core.tps import TPS, apply_tps, default_tps_for_class, load_tps, resolve_tps_path  # noqa: E402
from uhbs_core.manifest import write_manifest  # noqa: E402

DYNAMIC_DIMS = (DIM_A, DIM_B, DIM_C, DIM_D, DIM_E)


def _normalize_phases(phases: Sequence[str]) -> List[str]:
    out: List[str] = []
    for raw in phases:
        p = raw.strip().lower()
        if p in {"1", "profile", "setup", "tps"}:
            out.append("profile")
        elif p in {"2", "source", "static", "whitebox", "white-box"}:
            out.append("static")
        elif p in {"3", "sandbox", "deploy", "preflight"}:
            out.append("sandbox")
        elif p in {"4", "exec", "execution", "dynamic", "runtime", "probe"}:
            out.append("dynamic")
        elif p in {"5", "score", "report"}:
            out.append("score")
        elif p:
            out.append(p)
    seen = set()
    ordered: List[str] = []
    for p in out:
        if p not in seen:
            seen.add(p)
            ordered.append(p)
    return ordered


def _want_module_f(modules: Sequence[str]) -> bool:
    if not modules:
        return True
    tokens = {m.upper() if len(m) == 1 else m.lower() for m in modules}
    if "all" in tokens or "static" in tokens or "F" in tokens:
        return True
    return not tokens.issubset(
        {
            "A",
            "B",
            "C",
            "D",
            "E",
            "stealth",
            "realism",
            "telemetry",
            "safety",
            "scale",
            "protocol",
            "behavior",
        }
    )


def _run_dynamic(
    target: TargetSpec,
    tps: TPS,
    modules: Sequence[str],
    scale_conc: int,
    scale_req: int,
) -> List[ModuleResult]:
    out: List[ModuleResult] = []
    mods = {m.upper() if len(m) == 1 else m.lower() for m in modules}
    if "A" in mods or "stealth" in mods or "protocol" in mods:
        out.append(test_stealth.run(target, tps=tps))
    if "B" in mods or "realism" in mods or "behavior" in mods:
        out.append(test_realism.run(target, tps=tps))
    if "C" in mods or "telemetry" in mods:
        out.append(test_telemetry.run(target, tps=tps))
    if "D" in mods or "safety" in mods:
        out.append(test_safety.run(target, tps=tps))
    if "E" in mods or "scale" in mods:
        out.append(
            test_scale.run(target, tps=tps, concurrency=scale_conc, requests=scale_req)
        )
    return out


def evaluate_one(
    target: TargetSpec,
    tps: TPS,
    phases: Sequence[str],
    modules: Sequence[str],
    scale_conc: int,
    scale_req: int,
    out_dir: Path,
    skip_sast_tools: bool,
) -> Tuple[List[ModuleResult], Dict[str, float]]:
    phases_n = _normalize_phases(phases)
    all_mods: List[ModuleResult] = []
    dyn_mods: List[ModuleResult] = []

    run_static = "static" in phases_n
    run_dynamic = "dynamic" in phases_n
    if "sandbox" in phases_n:
        all_mods.append(sandbox_preflight.run(target))

    mods_l = {m.upper() if len(m) == 1 else m.lower() for m in modules}
    if run_static and _want_module_f(modules):
        all_mods.append(
            test_static_code.run(
                target, out_dir=out_dir / "static", skip_sast_tools=skip_sast_tools
            )
        )
    # Capability signals fill A–E in static-only runs (skip when modules is F-only)
    f_only = bool(mods_l) and mods_l <= {"F", "static"}
    if run_static and not run_dynamic and not f_only:
        all_mods.extend(scan_source(target))

    if run_dynamic:
        dyn_mods = _run_dynamic(target, tps, modules, scale_conc, scale_req)
        all_mods.extend(dyn_mods)

    scores = scores_from_modules(
        [m for m in all_mods if m.module not in {"SANDBOX"}]
    )
    if dyn_mods:
        dyn_scores = scores_from_modules(dyn_mods)
        for d in DYNAMIC_DIMS:
            if any(m.dimension == d and m.status != "SKIPPED" for m in dyn_mods):
                scores[d] = dyn_scores[d]
    f_mods = [m for m in all_mods if m.module == "F" and m.status != "SKIPPED"]
    if f_mods:
        scores["static"] = f_mods[-1].score

    return all_mods, scores


def main() -> int:
    p = argparse.ArgumentParser(description="UHBS v4.0 Universal Honeypot Benchmark")
    p.add_argument("--inventory", type=Path)
    p.add_argument("--target", required=False, help="required unless --list-protocols")
    p.add_argument("--baseline")
    p.add_argument("--kind")
    p.add_argument("--baseline-kind")
    p.add_argument("--source-root")
    p.add_argument("--baseline-source")
    p.add_argument("--port", type=int)
    p.add_argument("--baseline-port", type=int)
    p.add_argument("--tps", help="TPS name or path (profiles/tps/*.yaml)")
    p.add_argument("--protocol", help="primary protocol id")
    p.add_argument("--class", dest="profile_class", help="POSIX-Shell|ICS-SCADA|Web-API|…")
    p.add_argument(
        "--phases",
        default="profile,static,dynamic,score",
        help="profile,static,sandbox,dynamic,score",
    )
    p.add_argument("--modules", default="A,B,C,D,E,F")
    p.add_argument("--concurrency", type=int, default=10)
    p.add_argument("--requests", type=int, default=30)
    p.add_argument("--out", type=Path, default=Path(".local/bench-reports/latest"))
    p.add_argument("--skip-sast-tools", action="store_true")
    p.add_argument(
        "--quick",
        action="store_true",
        help="set UHBS_QUICK=1 (fewer A3 samples / lighter Module E)",
    )
    p.add_argument("--list-protocols", action="store_true")
    p.add_argument(
        "--environment",
        default="Isolated Sandbox / air-gapped lab",
    )
    args = p.parse_args()

    if args.quick:
        import os

        os.environ["UHBS_QUICK"] = "1"

    if args.list_protocols:
        print("\n".join(list_protocols()))
        return 0

    inventory = load_inventory(args.inventory) if args.inventory else {}
    phases = [x.strip() for x in args.phases.split(",") if x.strip()]
    modules = [x.strip() for x in args.modules.split(",") if x.strip()]

    target = resolve_target(
        inventory,
        args.target,
        kind=args.kind,
        source_root=args.source_root,
        port=args.port,
        protocol=args.protocol,
        tps=args.tps,
        profile_class=args.profile_class,
    )

    tps_path = resolve_tps_path(args.tps or target.tps_path)
    if tps_path:
        tps = load_tps(tps_path)
        apply_tps(target, tps)
    else:
        tps = default_tps_for_class(
            args.profile_class or target.profile_class,
            args.protocol or target.protocol or "ssh",
        )
        apply_tps(target, tps)

    baseline: Optional[TargetSpec] = None
    baseline_tps = tps
    if args.baseline:
        baseline = resolve_target(
            inventory,
            args.baseline,
            kind=args.baseline_kind,
            source_root=args.baseline_source,
            port=args.baseline_port,
        )

    phases_n = _normalize_phases(phases)
    eval_type = "Full-Spectrum (Static Audit + Dynamic Sandbox)"
    if phases_n == ["static"] or set(phases_n) <= {"profile", "static", "score"}:
        eval_type = "Static Repo Audit (White-Box)"
    elif "dynamic" in phases_n and "static" not in phases_n:
        eval_type = "Dynamic Adversarial Probing"

    print(
        f"==> UHBS v4 target={target.label} class={target.profile_class} "
        f"protocols={target.protocol_list()} phases={phases_n}"
    )
    print(f"    plugins available: {', '.join(list_protocols())}")

    t_mods, t_scores = evaluate_one(
        target,
        tps,
        phases,
        modules,
        args.concurrency,
        args.requests,
        out_dir=args.out,
        skip_sast_tools=args.skip_sast_tools,
    )
    d_measured = any(
        m.module == "D" and m.status != "SKIPPED" for m in t_mods
    )
    t_uhqs = compute_uhqs(
        t_scores,
        target=target.label,
        profile_class=target.profile_class,
        phase="+".join(phases_n),
        containment_measured=d_measured,
    )

    extras = {
        "target_scores": t_scores,
        "uhqs_version": "4.0",
        "tps": {
            "name": tps.name,
            "class": tps.profile_class,
            "protocols": tps.protocol_list(),
            "expected_p95_latency_ms": tps.expected_p95_latency_ms,
        },
    }
    if baseline:
        print(f"==> baseline={baseline.label}")
        b_mods, b_scores = evaluate_one(
            baseline,
            baseline_tps,
            phases,
            modules,
            args.concurrency,
            args.requests,
            out_dir=args.out / "baseline",
            skip_sast_tools=args.skip_sast_tools,
        )
        b_d = any(m.module == "D" and m.status != "SKIPPED" for m in b_mods)
        b_uhqs = compute_uhqs(
            b_scores,
            target=baseline.label,
            profile_class=baseline.profile_class,
            phase="+".join(phases_n),
            containment_measured=b_d,
        )
        extras["baseline_scores"] = b_scores
        extras["baseline_uhqs"] = b_uhqs.to_dict()
        extras["delta_uhqs"] = round(t_uhqs.uhqs - b_uhqs.uhqs, 2)
        extras["baseline_modules"] = [m.to_dict() for m in b_mods]

    path = write_report(
        args.out,
        target,
        baseline,
        t_uhqs,
        t_mods,
        extras=extras,
        evaluation_type=eval_type,
    )
    print(
        render_card(
            target,
            baseline,
            t_uhqs,
            t_mods,
            environment=args.environment,
            evaluation_type=eval_type,
        )
    )
    if baseline and "baseline_uhqs" in extras:
        print(
            f"Baseline UHQS 4.0: {extras['baseline_uhqs']['uhqs']}  "
            f"Δ={extras['delta_uhqs']}"
        )
    print(f"Wrote {path}")
    manifest = write_manifest(
        args.out,
        extra={"target": target.label, "uhqs": t_uhqs.uhqs, "grade": t_uhqs.grade},
    )
    print(f"Wrote {manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
