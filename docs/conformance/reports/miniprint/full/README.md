# reports / miniprint — full artifacts

**UHQS 50.43 / D** · UHBS v4.2.2 · δ_C=0.81

This page is the human-readable landing for the UHBS-Lab run artifacts. The authoritative proof is the verbatim scorecard below (same bytes as `SCORECARD.txt`).

## Module scores

| Module | Score | Weight | Status | Notes |
| --- | ---: | --- | --- | --- |
| Module A: Protocol Fidelity | 65.4 | 0.30 | PARTIAL | median=0.791ms pstdev=346.816ms (target jitter often <2ms vs native) |
| Module B: Behavioral Realism | 62.5 | 0.15 | PARTIAL | survived binary blast |
| Module C: Telemetry Quality | 55.0 | 0.25 | PARTIAL | no STIX objects found |
| Module D: Safety & Containment (C) | 90.0 | GATE | PASSED | UHBS_AIRGAP_ATTESTED=1 (operator attestation; not a substitute for shell probes on SSH decoys) |
| Module E: Scalability & Latency | 55.0 | 0.10 | PARTIAL | P50=1055.1ms P95=1127.1ms P99=2112.5ms TPS_limit=100.0ms proto=pjl |
| Module F: Static Code Audit | 70.0 | 0.20 | PASSED | semgrep error/critical=1 total=1 |
| Safety Gate δ_C | 0.81 | GATE | — | Containment multiplier |

## Verbatim SCORECARD.txt

```text
====================================================================================
                  UNIVERSAL HONEYPOT BENCHMARK SCORECARD v4.0.1
====================================================================================
Target System         : miniprint
System Profile Class  : Low-Interaction
Protocols             : pjl
Evaluation Date       : 2026-07-27
Evaluation Type       : Full-Spectrum (Static Audit + Dynamic Sandbox)
Environment           : Isolated Sandbox
------------------------------------------------------------------------------------
EVALUATION MODULE                     SCORE (0-100)    WEIGHT    STATUS
------------------------------------------------------------------------------------
Module A: Protocol Fidelity         :  65.4/100       0.30     PARTIAL (median=0.791ms pstdev=346.816ms (target jitter often <2ms vs native))
Module B: Behavioral Realism        :  62.5/100       0.15     PARTIAL (survived binary blast)
Module C: Telemetry Quality         :  55.0/100       0.25     PARTIAL (no STIX objects found)
Module D: Safety & Containment (C)  :  90.0/100       GATE     PASSED (UHBS_AIRGAP_ATTESTED=1 (operator attestation; not a substitute for shell probes on SSH decoys))
Module E: Scalability & Latency     :  55.0/100       0.10     PARTIAL (P50=1055.1ms P95=1127.1ms P99=2112.5ms TPS_limit=100.0ms proto=pjl)
Module F: Static Code Audit         :  70.0/100       0.20     PASSED (semgrep error/critical=1 total=1)
------------------------------------------------------------------------------------
SAFETY GATE MULTIPLIER                : δ_C = 0.81 (C = 90.0 < 95 — exponential penalty)
FINAL COMPOSITE SCORE (UHQS 4.0.1)      : 50.43 / 100
OVERALL EVALUATION GRADE              : GRADE D (Needs Remediation)
====================================================================================
```

## Files in this directory

- [`SCORECARD.txt`](SCORECARD.txt) — human-readable UHBS scorecard (source of the table above)
- [`report.json`](report.json) — machine-readable checks / evidence
- [`MANIFEST.json`](MANIFEST.json) — run manifest
- [`REPORT.txt`](REPORT.txt) — text report twin of the scorecard
- [`uhbs-run.log`](uhbs-run.log) — harness log

Parent protocol hub: [`../index.md`](../index.md)

