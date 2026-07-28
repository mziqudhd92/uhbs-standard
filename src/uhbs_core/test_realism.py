#!/usr/bin/env python3
"""Module B — Behavioral & Stateful Realism (UHBS v4.2.1).

Class/protocol-aware via plugins: B1 state · B2 payload · B3 fuzz.
"""

from __future__ import annotations

import argparse
import base64
import sys
from pathlib import Path
from typing import List, Optional

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from uhbs_core.check_scoring import score_checks as _mean  # noqa: E402
from uhbs_core.hqs import pass_status  # noqa: E402
from uhbs_core.models import CheckResult, ModuleResult, TargetSpec  # noqa: E402
from uhbs_core.protocols import get_plugin  # noqa: E402
from uhbs_core.ssh_session import run_ssh_command  # noqa: E402
from uhbs_core.tps import TPS, apply_tps, default_tps_for_class, load_tps, resolve_tps_path  # noqa: E402

PAYLOAD = ROOT / "payloads" / "math_logic_probe"

W_STATE = 0.40
W_PAYLOAD = 0.35
W_FUZZ = 0.25

# NOTE: _mean now delegates to uhbs_core.check_scoring.score_checks (circuit
# breaker for critical=True gate failures + geometric mean otherwise).


def run(target: TargetSpec, tps: Optional[TPS] = None) -> ModuleResult:
    if not target.host:
        return ModuleResult(
            module="B",
            dimension="behavior",
            score=0.0,
            status="SKIPPED",
            notes=["no exec host"],
        )

    if tps is None:
        tps = default_tps_for_class(target.profile_class, (target.protocol_list() or ["ssh"])[0])
        apply_tps(target, tps)

    all_checks: List[CheckResult] = []
    per_proto = {}

    for proto in target.protocol_list():
        port = target.port_for(proto)
        if port is None:
            continue
        plugin = get_plugin(proto)
        state = plugin.probe_state(target.host, port, target, tps)
        payload = plugin.probe_payload(target.host, port, target, tps)
        fuzz = plugin.probe_fuzz(target.host, port, target, tps)

        # Extra ELF math probe for POSIX/SSH shells when binary present
        if proto == "ssh" and PAYLOAD.is_file():
            blob = base64.b64encode(PAYLOAD.read_bytes()).decode("ascii")
            drop = (
                f"echo {blob} | base64 -d > /tmp/math_logic_probe && "
                "chmod +x /tmp/math_logic_probe && /tmp/math_logic_probe 7 3"
            )
            elf = run_ssh_command(
                target.host, port, target.user, target.password, drop, timeout=30
            )
            elf_ok = elf.ok and "22" in elf.stdout
            payload.append(
                CheckResult(
                    id="ssh.payload.elf_math",
                    team="red",
                    passed=elf_ok,
                    detail=(elf.stdout.strip() or elf.error or "no output")[:160],
                    score=100.0 if elf_ok else 0.0,
                )
            )

        s = W_STATE * _mean(state) + W_PAYLOAD * _mean(payload) + W_FUZZ * _mean(fuzz)
        per_proto[proto] = round(s, 2)
        all_checks.extend(state)
        all_checks.extend(payload)
        all_checks.extend(fuzz)

    if not per_proto:
        return ModuleResult(
            module="B",
            dimension="behavior",
            score=0.0,
            status="FAILED",
            notes=["no protocol ports available"],
        )

    score = sum(per_proto.values()) / len(per_proto)
    notes = [f"UHBS Module B class={tps.profile_class}"]
    # MCP honeypot honesty: zero-tool / high-risk-only surfaces cannot inflate B
    surface = (target.annotations or {}).get("mcp_surface_depth")
    reason = (target.annotations or {}).get("mcp_surface_reason")
    if surface == "metadata_only" or any(
        "NEUTRAL_NO_SURFACE" in (c.detail or "")
        or "SKIPPED_HIGH_RISK_TOOL" in (c.detail or "")
        or "SKIPPED_UNSATISFIABLE_SCHEMA" in (c.detail or "")
        for c in all_checks
    ):
        score = min(score, 50.0)
        notes.append("surface_depth=metadata_only (Module B ceiling 50)")
        if reason:
            notes.append(str(reason)[:240])
    elif surface == "interactive":
        notes.append("surface_depth=interactive")

    return ModuleResult(
        module="B",
        dimension="behavior",
        score=round(score, 2),
        status=pass_status(score),
        checks=all_checks,
        metrics={
            "per_protocol": per_proto,
            "class": tps.profile_class,
            "surface_depth": surface or "unknown",
        },
        notes=notes,
    )


def main() -> int:
    p = argparse.ArgumentParser(description="UHBS Module B: Behavioral Realism")
    p.add_argument("--target", required=True)
    p.add_argument("--port", type=int, default=2222)
    p.add_argument("--protocol", default="ssh")
    p.add_argument("--tps", default=None)
    p.add_argument("--user", default="root")
    p.add_argument("--password", default="root")
    args = p.parse_args()
    tps = load_tps(resolve_tps_path(args.tps)) if resolve_tps_path(args.tps) else None
    t = TargetSpec(
        name=args.target,
        kind="generic",
        host=args.target,
        port=args.port,
        protocol=args.protocol,
        protocols=[args.protocol],
        ports_map={args.protocol: args.port},
        user=args.user,
        password=args.password,
    )
    if tps:
        apply_tps(t, tps)
    result = run(t, tps=tps)
    print(f"Module B behavior score={result.score} status={result.status}")
    for c in result.checks:
        print(f"  [{c.team}] {c.id}: {'PASS' if c.passed else 'FAIL'} — {c.detail}")
    return 0 if result.status != "FAILED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
