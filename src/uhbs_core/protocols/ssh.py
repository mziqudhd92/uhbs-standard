from __future__ import annotations

from typing import List, Optional

from ..hassh import parse_server_hassh
from ..models import CheckResult, TargetSpec
from ..rfc_probes import probe_ssh_rfc4253
from ..ssh_session import run_ssh_command
from ..tps import TPS
from uhbs_core.protocols.base import ProtocolPlugin


class SSHPlugin(ProtocolPlugin):
    name = "ssh"
    families = ("it", "posix", "genai")

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: Optional[TPS]
    ) -> List[CheckResult]:
        suite = probe_ssh_rfc4253(host, port)
        if suite.skipped:
            return [
                CheckResult(
                    id="ssh.fsm.skipped",
                    team="blue",
                    passed=False,
                    detail=suite.skip_reason,
                    score=0.0,
                )
            ]
        return [c for c in suite.checks if c.id.startswith("rfc4253.")]

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: Optional[TPS]
    ) -> List[CheckResult]:
        checks: List[CheckResult] = []
        suite = probe_ssh_rfc4253(host, port)
        checks.extend([c for c in suite.checks if "kex" in c.id or "identification" in c.id])

        hassh, algo, banner = parse_server_hassh(host, port)
        checks.append(
            CheckResult(
                id="ssh.nego.hassh",
                team="blue",
                passed=bool(hassh),
                detail=(f"HASSH={hassh} banner={banner}" if hassh else "HASSH parse failed"),
                score=40.0 if hassh else 0.0,
                evidence=[algo[:200]] if algo else [],
            )
        )
        # Optional gold baseline HASSH compare
        gold = (tps.gold_baseline_host if tps else None) or target.baseline_native_host
        if gold and hassh:
            gport = port
            if tps and tps.gold_baseline_port:
                gport = int(tps.gold_baseline_port)
            g_hassh, _, g_ban = parse_server_hassh(gold, gport)
            match = bool(g_hassh) and g_hassh == hassh
            checks.append(
                CheckResult(
                    id="ssh.nego.hassh_vs_gold",
                    team="blue",
                    passed=match,
                    detail=(
                        f"decoy={hassh} gold={g_hassh} banner_gold={g_ban}"
                        if g_hassh
                        else f"gold {gold}:{gport} HASSH unavailable"
                    ),
                    # Algo-offer match is informative; decoy may intentionally differ.
                    score=40.0 if match else (20.0 if g_hassh else 10.0),
                )
            )
        return checks

    def probe_state(
        self, host: str, port: int, target: TargetSpec, tps: Optional[TPS]
    ) -> List[CheckResult]:
        # B1: cross-session persistence — write in session 1, read in session 2
        marker = "UHBS_CROSS_SESSION_OK"
        path = "/tmp/uhbs_cross_session_marker"
        s1 = run_ssh_command(
            host,
            port,
            target.user,
            target.password,
            f"mkdir -p /tmp && echo {marker} > {path} && cat {path}",
        )
        s2 = run_ssh_command(
            host,
            port,
            target.user,
            target.password,
            f"cat {path}",
        )
        ok = s1.ok and s2.ok and marker in s2.stdout
        return [
            CheckResult(
                id="ssh.state.cross_session",
                team="blue",
                passed=ok,
                detail=(
                    "state persisted across independent SSH sessions"
                    if ok
                    else (s2.error or s1.error or "marker missing across sessions")
                ),
                score=100.0 if ok else 0.0,
                evidence=[(s1.stdout or "")[:80], (s2.stdout or "")[:80]],
            )
        ]

    def probe_payload(
        self, host: str, port: int, target: TargetSpec, tps: Optional[TPS]
    ) -> List[CheckResult]:
        out = run_ssh_command(host, port, target.user, target.password, "echo PAYLOAD_OK")
        ok = out.ok and "PAYLOAD_OK" in out.stdout
        return [
            CheckResult(
                id="ssh.payload.echo",
                team="red",
                passed=ok,
                detail="echo path ok" if ok else (out.error or "failed"),
                score=100.0 if ok else 0.0,
            )
        ]

    def probe_fuzz(
        self, host: str, port: int, target: TargetSpec, tps: Optional[TPS]
    ) -> List[CheckResult]:
        out = run_ssh_command(
            host, port, target.user, target.password, "head -c 1000 /dev/urandom | wc -c"
        )
        ok = out.ok and any(ch.isdigit() for ch in out.stdout)
        return [
            CheckResult(
                id="ssh.fuzz.non_utf8",
                team="red",
                passed=ok,
                detail=(out.stdout.strip() or out.error or "failed")[:160],
                score=100.0 if ok else 25.0,
            )
        ]

    def probe_load_once(
        self, host: str, port: int, target: TargetSpec, tps: Optional[TPS]
    ) -> float:
        out = run_ssh_command(host, port, target.user, target.password, "true", timeout=20)
        if not out.ok:
            raise RuntimeError(out.error or "ssh failed")
        return out.latency_ms
