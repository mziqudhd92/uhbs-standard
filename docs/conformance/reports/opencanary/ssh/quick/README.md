# opencanary / ssh — quick artifacts

**UHQS 31.94 / F** · UHBS v4.2.2 · δ_C=1.0

This page is the human-readable landing for the UHBS-Lab run artifacts. The authoritative proof is the verbatim scorecard below (same bytes as `SCORECARD.txt`).

## Module scores

| Module | Score | Weight | Status | Notes |
| --- | ---: | --- | --- | --- |
| Module A: Protocol Fidelity | 41.5 | 0.30 | PARTIAL | no KEXINIT |
| Module B: Behavioral Realism | 6.2 | 0.15 | PARTIAL | Authentication failed. |
| Module C: Telemetry Quality | 0.0 | 0.25 | FAILED | Authentication failed. |
| Module D: Safety & Containment (C) | 96.0 | GATE | PASSED | Authentication failed. |
| Module E: Scalability & Latency | 20.0 | 0.10 | PARTIAL | P50=0.0ms P95=0.0ms P99=0.0ms TPS_limit=3000.0ms proto=ssh |
| Module F: Static Code Audit | 82.7 | 0.20 | PASSED | sleep/blocking markers in non-test code≈0 |
| Safety Gate δ_C | 1.0 | GATE | — | Containment multiplier |

## Verbatim SCORECARD.txt

```text
====================================================================================
                  UNIVERSAL HONEYPOT BENCHMARK SCORECARD v4.0.1
====================================================================================
Target System         : opencanary-ssh
System Profile Class  : Low-Interaction
Protocols             : ssh
Evaluation Date       : 2026-07-27
Evaluation Type       : Full-Spectrum (Static Audit + Dynamic Sandbox)
Environment           : Isolated Sandbox
------------------------------------------------------------------------------------
EVALUATION MODULE                     SCORE (0-100)    WEIGHT    STATUS
------------------------------------------------------------------------------------
Module A: Protocol Fidelity         :  41.5/100       0.30     PARTIAL (no KEXINIT)
Module B: Behavioral Realism        :   6.2/100       0.15     PARTIAL (Authentication failed.)
Module C: Telemetry Quality         :   0.0/100       0.25     FAILED (Authentication failed.)
Module D: Safety & Containment (C)  :  96.0/100       GATE     PASSED (Authentication failed.)
Module E: Scalability & Latency     :  20.0/100       0.10     PARTIAL (P50=0.0ms P95=0.0ms P99=0.0ms TPS_limit=3000.0ms proto=ssh)
Module F: Static Code Audit         :  82.7/100       0.20     PASSED (sleep/blocking markers in non-test code≈0)
------------------------------------------------------------------------------------
SAFETY GATE MULTIPLIER                : δ_C = 1.0 (Containment Score C = 96.0 >= 95)
FINAL COMPOSITE SCORE (UHQS 4.0.1)      : 31.94 / 100
OVERALL EVALUATION GRADE              : GRADE F (Fail)
====================================================================================
```

## Files in this directory

- [`SCORECARD.txt`](SCORECARD.txt) — human-readable UHBS scorecard (source of the table above)
- [`report.json`](report.json) — machine-readable checks / evidence
- [`MANIFEST.json`](MANIFEST.json) — run manifest
- [`REPORT.txt`](REPORT.txt) — text report twin of the scorecard
- [`uhbs-run.log`](uhbs-run.log) — harness log

Parent protocol hub: [`../index.md`](../index.md)

