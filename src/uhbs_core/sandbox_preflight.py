#!/usr/bin/env python3
"""UHBS Phase 3 — Sandbox preflight (air-gap / reachability checklist)."""

from __future__ import annotations

import argparse
import os
import socket
import sys
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from uhbs_core.hqs import pass_status  # noqa: E402
from uhbs_core.models import CheckResult, ModuleResult, TargetSpec  # noqa: E402


def run(target: TargetSpec) -> ModuleResult:
    checks: List[CheckResult] = []
    if not target.host:
        return ModuleResult(
            module="SANDBOX",
            dimension="sandbox",
            score=0.0,
            status="SKIPPED",
            notes=["no host"],
        )

    # Reachability for each protocol port
    reachable = 0
    for proto in target.protocol_list():
        port = target.port_for(proto)
        if port is None:
            continue
        try:
            with socket.create_connection((target.host, port), timeout=3.0):
                ok = True
        except OSError as exc:
            ok = False
            detail = str(exc)
        else:
            detail = f"{target.host}:{port} open"
        reachable += int(ok)
        checks.append(
            CheckResult(
                id=f"sandbox.reach.{proto}",
                team="blue",
                passed=ok,
                detail=detail,
                score=25.0 if ok else 0.0,
            )
        )

    # Air-gap attestation: operator must set UHBS_AIRGAP_ATTESTED=1
    attested = os.environ.get("UHBS_AIRGAP_ATTESTED", "").strip() in {"1", "true", "yes"}
    checks.append(
        CheckResult(
            id="sandbox.airgap_attested",
            team="blue",
            passed=attested,
            detail=(
                "operator attested air-gapped sandbox (UHBS_AIRGAP_ATTESTED=1)"
                if attested
                else "set UHBS_AIRGAP_ATTESTED=1 after isolating VLAN/container egress"
            ),
            score=25.0 if attested else 0.0,
        )
    )

    # Optional host egress deny script presence (lab environment)
    egress_script = Path(__file__).resolve().parents[2] / "deploy" / "rootless" / "scripts" / "host-egress-deny.sh"
    checks.append(
        CheckResult(
            id="sandbox.egress_deny_tooling",
            team="blue",
            passed=egress_script.is_file(),
            detail=str(egress_script) if egress_script.is_file() else "host-egress-deny.sh not found",
            score=25.0 if egress_script.is_file() else 10.0,
        )
    )

    gw = os.environ.get("UHBS_EGRESS_GATEWAY_LOG", "").strip()
    checks.append(
        CheckResult(
            id="sandbox.gateway_log_configured",
            team="blue",
            passed=bool(gw),
            detail=f"UHBS_EGRESS_GATEWAY_LOG={gw}" if gw else "gateway log path not set",
            score=25.0 if gw else 10.0,
        )
    )

    score = min(100.0, sum(c.score for c in checks))
    # Normalize roughly
    score = min(100.0, score)
    return ModuleResult(
        module="SANDBOX",
        dimension="sandbox",
        score=round(score, 2),
        status=pass_status(score, threshold=50.0),
        checks=checks,
        metrics={"reachable_protocols": reachable},
        notes=["Phase 3 preflight — does not replace real air-gap deployment"],
    )


def main() -> int:
    p = argparse.ArgumentParser(description="UHBS Phase 3 sandbox preflight")
    p.add_argument("--target", required=True)
    p.add_argument("--port", type=int, default=2222)
    p.add_argument("--protocol", default="ssh")
    args = p.parse_args()
    t = TargetSpec(
        name=args.target,
        kind="generic",
        host=args.target,
        port=args.port,
        protocol=args.protocol,
        protocols=[args.protocol],
        ports_map={args.protocol: args.port},
    )
    r = run(t)
    print(f"Sandbox preflight score={r.score} status={r.status}")
    for c in r.checks:
        print(f"  {c.id}: {'PASS' if c.passed else 'FAIL'} — {c.detail}")
    return 0 if r.status != "FAILED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
