#!/usr/bin/env python3
"""Module A — Protocol & Syntax Fidelity (UHBS v4.4.2).

Protocol-agnostic via plugins (ssh/smtp/http/telnet/modbus/generic/…).
Steps: A1 FSM · A2 negotiation · A3 timing/IAT.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from uhbs_core.check_scoring import score_checks as _score_checks  # noqa: E402
from uhbs_core.hqs import pass_status  # noqa: E402
from uhbs_core.models import CheckResult, ModuleResult, TargetSpec  # noqa: E402
from uhbs_core.protocols import get_plugin, list_protocols  # noqa: E402
from uhbs_core.tps import TPS, apply_tps, default_tps_for_class, load_tps, resolve_tps_path  # noqa: E402

W_FSM = 0.40
W_NEGO = 0.30
W_TIMING = 0.30

# NOTE: _score_checks now delegates to uhbs_core.check_scoring.score_checks
# (circuit breaker for critical=True gate failures + geometric mean for the
# rest — see that module's docstring). Kept as a local alias so the rest of
# this file, and any external callers, don't need to change.


def run(
    target: TargetSpec,
    tps: Optional[TPS] = None,
    native_baseline_ms: Optional[float] = None,
) -> ModuleResult:
    if not target.host:
        return ModuleResult(
            module="A",
            dimension="protocol",
            score=0.0,
            status="SKIPPED",
            notes=["no exec host"],
        )

    if tps is None:
        tps = default_tps_for_class(target.profile_class, target.protocol or "ssh")
        apply_tps(target, tps)

    protocols = target.protocol_list()
    samples = int(tps.timing_samples if tps else 50)
    all_checks: List[CheckResult] = []
    per_proto = {}

    for proto in protocols:
        port = target.port_for(proto)
        if port is None:
            all_checks.append(
                CheckResult(
                    id=f"{proto}.port.missing",
                    team="blue",
                    passed=False,
                    detail="no port mapped for protocol",
                    score=0.0,
                )
            )
            continue
        plugin = get_plugin(proto)
        fsm = plugin.probe_fsm(target.host, port, target, tps)
        nego = plugin.probe_negotiation(target.host, port, target, tps)
        timing = plugin.probe_timing(target.host, port, target, tps, samples=samples)
        s_fsm = _score_checks(fsm)
        s_nego = _score_checks(nego)
        s_timing = _score_checks(timing)
        proto_score = W_FSM * s_fsm + W_NEGO * s_nego + W_TIMING * s_timing
        per_proto[proto] = round(proto_score, 2)
        all_checks.extend(fsm)
        all_checks.extend(nego)
        all_checks.extend(timing)
        all_checks.append(
            CheckResult(
                id=f"{proto}.module_a.composite",
                team="blue",
                passed=proto_score >= 70,
                detail=f"fsm={s_fsm:.0f} nego={s_nego:.0f} timing={s_timing:.0f}",
                score=proto_score,
            )
        )

    if not per_proto:
        return ModuleResult(
            module="A",
            dimension="protocol",
            score=0.0,
            status="FAILED",
            checks=all_checks,
            notes=["no protocols probed — set protocol/ports in TPS or inventory"],
        )

    score = sum(per_proto.values()) / len(per_proto)
    _ = native_baseline_ms  # reserved for gold-baseline KS compare
    return ModuleResult(
        module="A",
        dimension="protocol",
        score=round(score, 2),
        status=pass_status(score),
        checks=all_checks,
        metrics={
            "per_protocol": per_proto,
            "protocols": protocols,
            "timing_samples": samples,
            "available_plugins": list_protocols(),
        },
        notes=[
            f"UHBS Module A — plugins={list(per_proto)}",
            f"class={tps.profile_class} strict_rfc={tps.strict_rfc_enforcement}",
        ],
    )


def main() -> int:
    p = argparse.ArgumentParser(description="UHBS Module A: Protocol & Syntax Fidelity")
    p.add_argument("--target", required=True, help="host")
    p.add_argument("--port", type=int, default=2222)
    p.add_argument("--protocol", default=None, help="ssh|smtp|http|modbus|telnet|…")
    p.add_argument("--protocols", default=None, help="comma-separated protocol list")
    p.add_argument("--smtp-port", type=int, default=None)
    p.add_argument("--http-port", type=int, default=None)
    p.add_argument("--tps", default=None, help="path or name of TPS yaml")
    p.add_argument("--class", dest="profile_class", default="POSIX-Shell")
    p.add_argument("--user", default="root")
    p.add_argument("--password", default="root")
    p.add_argument("--list-protocols", action="store_true")
    args = p.parse_args()
    if args.list_protocols:
        print("\n".join(list_protocols()))
        return 0

    tps = None
    tps_path = resolve_tps_path(args.tps)
    if tps_path:
        tps = load_tps(tps_path)

    protos = []
    if args.protocols:
        protos = [x.strip() for x in args.protocols.split(",") if x.strip()]
    elif args.protocol:
        protos = [args.protocol]
    elif tps:
        protos = tps.protocol_list()
    else:
        protos = ["ssh"]

    ports_map = {"ssh": args.port}
    if args.smtp_port:
        ports_map["smtp"] = args.smtp_port
    if args.http_port:
        ports_map["http"] = args.http_port

    t = TargetSpec(
        name=args.target,
        kind="generic",
        host=args.target,
        port=args.port,
        ssh_port=args.port,
        smtp_port=args.smtp_port,
        http_port=args.http_port,
        user=args.user,
        password=args.password,
        protocol=protos[0],
        protocols=protos,
        profile_class=args.profile_class if not tps else tps.profile_class,
        ports_map=ports_map,
    )
    if tps:
        apply_tps(t, tps)
        t.ports_map.update(ports_map)

    result = run(t, tps=tps)
    print(f"Module A protocol score={result.score} status={result.status}")
    print(f"  metrics={result.metrics}")
    for c in result.checks:
        print(f"  [{c.team}] {c.id}: {'PASS' if c.passed else 'FAIL'} — {c.detail}")
    return 0 if result.status != "FAILED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
