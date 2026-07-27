#!/usr/bin/env python3
"""Module E — Scalability, Latency & Stress (UHBS v4.0.1).

E1: connection saturation — P50/P95/P99 vs TPS expected_p95_latency_ms
E2: resource exhaustion + circuit-breaker liveness
"""

from __future__ import annotations

import argparse
import concurrent.futures
import os
import sys
import time
from pathlib import Path
from typing import List, Optional

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from uhbs_core.hqs import pass_status  # noqa: E402
from uhbs_core.models import CheckResult, ModuleResult, TargetSpec  # noqa: E402
from uhbs_core.protocols import get_plugin  # noqa: E402
from uhbs_core.ssh_session import tcp_connect  # noqa: E402
from uhbs_core.tps import TPS  # noqa: E402


def _percentile(vals: List[float], p: float) -> float:
    if not vals:
        return 0.0
    s = sorted(vals)
    k = (len(s) - 1) * (p / 100.0)
    f = int(k)
    c = min(f + 1, len(s) - 1)
    if f == c:
        return s[f]
    return s[f] + (s[c] - s[f]) * (k - f)


def run(
    target: TargetSpec,
    tps: Optional[TPS] = None,
    concurrency: int = 10,
    requests: int = 30,
) -> ModuleResult:
    if not target.host:
        return ModuleResult(
            module="E",
            dimension="scale",
            score=0.0,
            status="SKIPPED",
            notes=["no exec host"],
        )

    if os.environ.get("UHBS_QUICK", "").strip() in {"1", "true", "yes"}:
        concurrency = min(concurrency, 5)
        requests = min(requests, 15)

    p95_limit = float(tps.expected_p95_latency_ms) if tps else 150.0
    proto = (target.protocol_list() or ["ssh"])[0]
    port = target.port_for(proto) or target.port
    plugin = get_plugin(proto)

    checks: List[CheckResult] = []
    latencies: List[float] = []
    errors = 0

    def one(_i: int) -> float:
        return plugin.probe_load_once(target.host, port, target, tps)

    t0 = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as pool:
        futs = [pool.submit(one, i) for i in range(requests)]
        for fut in concurrent.futures.as_completed(futs):
            try:
                latencies.append(fut.result())
            except Exception:  # noqa: BLE001
                errors += 1
    elapsed = time.perf_counter() - t0

    p50 = _percentile(latencies, 50)
    p95 = _percentile(latencies, 95)
    p99 = _percentile(latencies, 99)

    checks.append(
        CheckResult(
            id="e1.p95_vs_tps",
            team="blue",
            passed=bool(latencies) and p95 < p95_limit,
            detail=(
                f"P50={p50:.1f}ms P95={p95:.1f}ms P99={p99:.1f}ms "
                f"TPS_limit={p95_limit:.1f}ms proto={proto}"
            ),
            score=(
                45.0
                if latencies and p95 < p95_limit
                else (20.0 if latencies and p95 < p95_limit * 2 else 0.0)
            ),
        )
    )
    err_rate = errors / max(requests, 1)
    checks.append(
        CheckResult(
            id="e1.error_rate",
            team="blue",
            passed=err_rate < 0.2,
            detail=f"errors={errors}/{requests} rate={err_rate:.2%}",
            score=20.0 if err_rate < 0.2 else 5.0,
        )
    )

    # E2 — memory/context stuffing then liveness (circuit breaker)
    try:
        plugin.probe_fuzz(target.host, port, target, tps)
        stuffed = True
        stuff_err = ""
    except Exception as exc:  # noqa: BLE001
        stuffed = False
        stuff_err = str(exc)
    checks.append(
        CheckResult(
            id="e2.exhaustion_input",
            team="red",
            passed=stuffed,
            detail="completed exhaustion/fuzz blast" if stuffed else stuff_err,
            score=15.0 if stuffed else 0.0,
        )
    )

    ok, ms, err = tcp_connect(target.host, port)
    try:
        _ = plugin.probe_load_once(target.host, port, target, tps)
        alive = ok
        alive_detail = f"service alive after load (connect {ms:.1f}ms)"
    except Exception as exc:  # noqa: BLE001
        alive = False
        alive_detail = str(exc) or err or "down"
    checks.append(
        CheckResult(
            id="e2.circuit_breaker_alive",
            team="blue",
            passed=alive,
            detail=alive_detail,
            score=20.0 if alive else 0.0,
        )
    )

    score = min(100.0, sum(c.score for c in checks))
    return ModuleResult(
        module="E",
        dimension="scale",
        score=round(score, 2),
        status=pass_status(score),
        checks=checks,
        metrics={
            "p50_ms": round(p50, 2),
            "p95_ms": round(p95, 2),
            "p99_ms": round(p99, 2),
            "p95_limit_ms": p95_limit,
            "errors": errors,
            "concurrency": concurrency,
            "requests": requests,
            "wall_s": round(elapsed, 2),
            "protocol": proto,
        },
    )


def main() -> int:
    p = argparse.ArgumentParser(description="UHBS Module E: Scale & Latency")
    p.add_argument("--target", required=True)
    p.add_argument("--port", type=int, default=2222)
    p.add_argument("--protocol", default="ssh")
    p.add_argument("--user", default="root")
    p.add_argument("--password", default="root")
    p.add_argument("--concurrency", type=int, default=10)
    p.add_argument("--requests", type=int, default=30)
    p.add_argument("--p95-limit", type=float, default=150.0)
    args = p.parse_args()
    t = TargetSpec(
        name=args.target,
        kind="generic",
        host=args.target,
        port=args.port,
        user=args.user,
        password=args.password,
        protocol=args.protocol,
        protocols=[args.protocol],
        ports_map={args.protocol: args.port},
    )
    tps = TPS(
        name="cli",
        profile_class="POSIX-Shell",
        protocol=args.protocol,
        expected_p95_latency_ms=args.p95_limit,
    )
    result = run(t, tps=tps, concurrency=args.concurrency, requests=args.requests)
    print(f"Module E scale score={result.score} status={result.status}")
    print(f"  metrics={result.metrics}")
    for c in result.checks:
        print(f"  [{c.team}] {c.id}: {'PASS' if c.passed else 'FAIL'} — {c.detail}")
    return 0 if result.status != "FAILED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
