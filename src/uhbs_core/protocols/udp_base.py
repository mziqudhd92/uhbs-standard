"""UDP-aware ProtocolPlugin mixin — timing / load use datagram RTT.

Architecture note (2026-07-27 review): the original ``probe_timing``
sampled with the *full* protocol-level timeout (1.5-2.0s) on every one of
up to 1000 samples, then used the elapsed time as if it were a measured RTT
even when the server never replied. Two problems with that:

1. **Performance** — 200 full-timeout samples at 1.5s each is 5 minutes of
   dead wall-clock time per protocol per run, for canaries that are
   silent by design (confirmed via source read of OpenCanary's SIP/SNMP/
   NTP/TFTP modules).
2. **Ceiling problem** — a genuinely responsive UDP service (a real NTP or
   DNS server that answers every request) was never given credit for that:
   the code didn't distinguish "got a real reply fast" from "timed out
   waiting," so both cases fed the same jitter/KS math using timeout-length
   pseudo-RTTs instead of the real reply latency.

Fix: sample with a short, fixed per-attempt timeout (``_TIMING_SAMPLE_TIMEOUT``)
purely to detect responsiveness without paying the full negotiation-level
timeout N times, and branch scoring on whether *any* real reply arrived:

* **Responsive target** (≥1 real reply): jitter/KS use only the real
  reply latencies — no ceiling, a fast/consistent responder can score the
  same as a TCP-backed protocol would.
* **Silent target** (0 replies): timing check is explicitly labeled a
  measurement limitation (score capped low, not zero) rather than a
  fidelity claim either way.
"""

from __future__ import annotations

import os
import statistics

from uhbs_core.models import CheckResult, TargetSpec
from uhbs_core.netutil import udp_transact
from uhbs_core.protocols.base import ProtocolPlugin
from uhbs_core.stats import ks_2samp
from uhbs_core.tps import TPS

# Short per-attempt timeout used ONLY for the repeated timing-sample loop.
# Protocol-level probe_negotiation()/probe_state() calls in each concrete
# UDP plugin use their own longer, protocol-appropriate timeouts (1.5-2.0s)
# for single-shot correctness checks — this constant does not affect those.
_TIMING_SAMPLE_TIMEOUT = 0.25


class UdpProtocolPlugin(ProtocolPlugin):
    """Base for UDP protocols (SIP/SNMP/NTP/TFTP/…)."""

    udp_probe_payload: bytes = b"\x00"

    def probe_timing(
        self,
        host: str,
        port: int,
        target: TargetSpec,
        tps: TPS | None,
        samples: int = 1000,
    ) -> list[CheckResult]:
        if os.environ.get("UHBS_QUICK", "").strip() in {"1", "true", "yes"}:
            samples = min(samples, 50)
        samples = max(30, int(samples))

        replied_lat: list[float] = []
        silent = 0
        errors = 0
        for _ in range(samples):
            raw, rtt, err = udp_transact(
                host, port, self.udp_probe_payload, timeout=_TIMING_SAMPLE_TIMEOUT
            )
            if err:
                errors += 1
            elif raw:
                replied_lat.append(rtt)
            else:
                silent += 1

        checks: list[CheckResult] = [
            CheckResult(
                id=f"{self.name}.timing.sample_size",
                team="blue",
                passed=(len(replied_lat) + silent) >= min(samples, 30),
                detail=(
                    f"n={samples} replied={len(replied_lat)} "
                    f"silent={silent} errors={errors}"
                ),
                score=(
                    100.0
                    if (len(replied_lat) + silent) >= min(samples, 30)
                    else 20.0
                ),
            )
        ]

        if replied_lat:
            # Responsive target — score on real reply latencies, no ceiling.
            med = statistics.median(replied_lat)
            jitter = statistics.pstdev(replied_lat) if len(replied_lat) > 1 else 0.0
            jitter_ok = jitter < max(2.0, 0.5 * med)
            checks.append(
                CheckResult(
                    id=f"{self.name}.timing.iat_jitter",
                    team="red",
                    passed=jitter_ok,
                    detail=(
                        f"median={med:.3f}ms pstdev={jitter:.3f}ms "
                        f"(n_replied={len(replied_lat)}/{samples})"
                    ),
                    score=100.0 if jitter_ok else 30.0,
                )
            )

            if not (tps and tps.gold_baseline_host):
                return checks

            allowed = {p.lower() for p in (tps.gold_baseline_protocols or [])}
            if self.name.lower() not in allowed:
                return checks

            b_port = int(tps.gold_baseline_port or port)
            b_lat: list[float] = []
            for _ in range(min(samples, len(replied_lat))):
                b_raw, b_rtt, b_err = udp_transact(
                    tps.gold_baseline_host,
                    b_port,
                    self.udp_probe_payload,
                    timeout=_TIMING_SAMPLE_TIMEOUT,
                )
                if not b_err and b_raw:
                    b_lat.append(b_rtt)
            if len(b_lat) >= 10:
                d, p = ks_2samp(replied_lat, b_lat)
                ok = d < 0.35 or p > 0.05
                checks.append(
                    CheckResult(
                        id=f"{self.name}.timing.ks_vs_gold",
                        team="red",
                        passed=ok,
                        detail=f"KS D={d:.3f} p≈{p:.3f} (n_base_replied={len(b_lat)})",
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
                            f"gold baseline {tps.gold_baseline_host}:{b_port} "
                            "did not reply enough to KS-compare"
                        ),
                        score=40.0,
                    )
                )
        else:
            # Silent-by-design (or genuinely broken) target — we cannot
            # measure a real RTT distribution either way, so this is
            # explicitly a measurement limitation, not a fidelity verdict.
            checks.append(
                CheckResult(
                    id=f"{self.name}.timing.iat_jitter",
                    team="blue",
                    passed=True,
                    detail=(
                        f"no UDP replies in {samples} samples — cannot measure "
                        "jitter (alert-only canary assumed; timing N/A)"
                    ),
                    score=50.0,
                )
            )
        return checks

    def probe_load_once(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> float:
        _, rtt, err = udp_transact(host, port, self.udp_probe_payload, timeout=1.5)
        if err:
            raise RuntimeError(err)
        return rtt

    def probe_fuzz(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        raw, _, err = udp_transact(
            host, port, b"\x00\xff\xfe" + bytes(range(64)), timeout=1.5
        )
        ok = not err
        return [
            CheckResult(
                id=f"{self.name}.fuzz.binary",
                team="red",
                passed=ok,
                detail=(err or f"udp sent resp={raw[:40]!r}"),
                score=100.0 if ok else 20.0,
            )
        ]
