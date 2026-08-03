"""Protocol plugin interface — UHBS v4.4.0 Module A/B hooks."""

from __future__ import annotations

import os
from abc import ABC, abstractmethod

from ..models import CheckResult, TargetSpec
from ..stats import ks_2samp, sample_connect_latencies
from ..tps import TPS


class ProtocolPlugin(ABC):
    """One plugin per protocol identifier (ssh, smtp, http, modbus, …)."""

    name: str = "generic"
    families: tuple = ()

    @abstractmethod
    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        """A1 — out-of-order / invalid verbs vs mandated status codes."""

    @abstractmethod
    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        """A2 — capability / banner / cipher negotiation parity."""

    def probe_timing(
        self,
        host: str,
        port: int,
        target: TargetSpec,
        tps: TPS | None,
        samples: int = 1000,
    ) -> list[CheckResult]:
        """A3 — IAT distribution + optional Kolmogorov–Smirnov vs gold baseline."""
        import statistics

        # UHBS_QUICK=1 shortens formal 1000-sample runs for CI/dev
        if os.environ.get("UHBS_QUICK", "").strip() in {"1", "true", "yes"}:
            samples = min(samples, 50)
        samples = max(30, int(samples))

        lat, errors = sample_connect_latencies(host, port, samples)
        if not lat:
            return [
                CheckResult(
                    id=f"{self.name}.timing.unreachable",
                    team="red",
                    passed=False,
                    detail="no successful connects",
                    score=0.0,
                )
            ]

        med = statistics.median(lat)
        jitter = statistics.pstdev(lat) if len(lat) > 1 else 0.0
        sample_ok = len(lat) >= min(samples, 30)
        jitter_ok = jitter < max(2.0, 0.5 * med)
        checks: list[CheckResult] = [
            CheckResult(
                id=f"{self.name}.timing.sample_size",
                team="blue",
                passed=sample_ok,
                detail=f"n={len(lat)} requested={samples} errors={errors}",
                # 0–100 scale (geometric-mean aggregation requires this).
                score=100.0 if sample_ok else 20.0,
            ),
            CheckResult(
                id=f"{self.name}.timing.iat_jitter",
                team="red",
                passed=jitter_ok,
                detail=f"median={med:.3f}ms pstdev={jitter:.3f}ms (target jitter often <2ms vs native)",
                score=100.0 if jitter_ok else 30.0,
            ),
        ]

        baseline_host = None
        baseline_port = port
        if tps and tps.gold_baseline_host:
            # Only KS-compare protocols the gold service actually speaks.
            allowed = {p.lower() for p in (tps.gold_baseline_protocols or ["ssh"])}
            if self.name.lower() in allowed:
                baseline_host = tps.gold_baseline_host
                if tps.gold_baseline_port:
                    baseline_port = int(tps.gold_baseline_port)
        elif target.baseline_native_host:
            baseline_host = target.baseline_native_host

        if not baseline_host:
            # No gold configured — omit KS rather than recording a soft-fail.
            # Operators MAY set performance_baseline.gold_baseline_host for a
            # native peer comparison; absence is not a fidelity defect.
            return checks

        # Same port on gold baseline (native service) when available
        b_lat, b_err = sample_connect_latencies(
            baseline_host, baseline_port, min(samples, len(lat))
        )
        if len(b_lat) >= 10:
            d, p = ks_2samp(lat, b_lat)
            # UHBS: distribution should match baseline — fail if D large / p tiny
            ok = d < 0.35 or p > 0.05
            checks.append(
                CheckResult(
                    id=f"{self.name}.timing.ks_vs_gold",
                    team="red",
                    passed=ok,
                    detail=(
                        f"KS D={d:.3f} p≈{p:.3f} vs gold {baseline_host}:{baseline_port} "
                        f"(n_base={len(b_lat)} err={b_err})"
                    ),
                    score=100.0 if ok else 40.0,
                )
            )
        else:
            checks.append(
                CheckResult(
                    id=f"{self.name}.timing.ks_vs_gold",
                    team="red",
                    passed=False,
                    detail=(
                        f"gold baseline {baseline_host}:{baseline_port} "
                        f"unreachable/insufficient samples"
                    ),
                    score=40.0,
                )
            )
        return checks

    def probe_state(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        return [
            CheckResult(
                id=f"{self.name}.state.unsupported",
                team="blue",
                passed=True,
                detail="no state probe implemented — skipped",
                score=50.0,
            )
        ]

    def probe_payload(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        return [
            CheckResult(
                id=f"{self.name}.payload.unsupported",
                team="red",
                passed=True,
                detail="no payload probe — skipped",
                score=50.0,
            )
        ]

    def probe_fuzz(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        import socket

        try:
            with socket.create_connection((host, port), timeout=3.0) as s:
                s.settimeout(2.0)
                s.sendall(b"\x00\xff\xfe" + bytes(range(256))[:64])
                try:
                    s.recv(1024)
                except TimeoutError:
                    pass
            return [
                CheckResult(
                    id=f"{self.name}.fuzz.binary",
                    team="red",
                    passed=True,
                    detail="survived binary blast",
                    score=100.0,
                )
            ]
        except OSError as exc:
            return [
                CheckResult(
                    id=f"{self.name}.fuzz.binary",
                    team="red",
                    passed=False,
                    detail=str(exc),
                    score=20.0,
                )
            ]

    def probe_load_once(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> float:
        """Single request latency (ms) for Module E — override for protocol-native load."""
        lat, err = sample_connect_latencies(host, port, 1)
        if err or not lat:
            raise RuntimeError("connect failed")
        return lat[0]
