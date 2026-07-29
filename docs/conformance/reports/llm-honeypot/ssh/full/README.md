# llm-honeypot / ssh — full artifacts

**UHQS 61.17 / D** · UHBS v4.2.2 · δ_C=1.0

This page is the human-readable landing for the UHBS-Lab run artifacts. The authoritative proof is the verbatim scorecard below (same bytes as `SCORECARD.txt`).

## Module scores

| Module | Score | Weight | Status | Notes |
| --- | ---: | --- | --- | --- |
| Module A: Protocol Fidelity | 57.1 | 0.30 | PARTIAL | accepted null ID |
| Module B: Behavioral Realism | 60.0 | 0.15 | PARTIAL | marker missing across sessions |
| Module C: Telemetry Quality | 55.0 | 0.25 | PARTIAL | no STIX objects found |
| Module D: Safety & Containment (C) | 100.0 | GATE | PASSED | stable |
| Module E: Scalability & Latency | 75.0 | 0.10 | PASSED | P50=3160.3ms P95=3902.6ms P99=4831.2ms TPS_limit=3000.0ms proto=ssh |
| Module F: Static Code Audit | 69.0 | 0.20 | PARTIAL | POSIX coverage 0% (0/104) |
| Safety Gate δ_C | 1.0 | GATE | — | Containment multiplier |

## Verbatim SCORECARD.txt

```text
====================================================================================
                  UNIVERSAL HONEYPOT BENCHMARK SCORECARD v4.2.1
====================================================================================
Target System         : llm-honeypot-ssh
System Profile Class  : Low-Interaction
Protocols             : ssh
Evaluation Date       : 2026-07-28
Evaluation Type       : Full-Spectrum (Static Audit + Dynamic Sandbox)
Environment           : Isolated Sandbox
MCP Surface Depth     : unknown
------------------------------------------------------------------------------------
EVALUATION MODULE                     SCORE (0-100)    WEIGHT    STATUS
------------------------------------------------------------------------------------
Module A: Protocol Fidelity         :  57.1/100       0.30     PARTIAL (accepted null ID)
Module B: Behavioral Realism        :  60.0/100       0.15     PARTIAL (marker missing across sessions)
Module C: Telemetry Quality         :  55.0/100       0.25     PARTIAL (no STIX objects found)
Module D: Safety & Containment (C)  : 100.0/100       GATE     PASSED (stable)
Module E: Scalability & Latency     :  75.0/100       0.10     PASSED (P50=3160.3ms P95=3902.6ms P99=4831.2ms TPS_limit=3000.0ms proto=ssh)
Module F: Static Code Audit         :  69.0/100       0.20     PARTIAL (POSIX coverage 0% (0/104))
------------------------------------------------------------------------------------
SAFETY GATE MULTIPLIER                : δ_C = 1.0 (Containment Score C = 100.0 >= 95)
FINAL COMPOSITE SCORE (UHQS 4.2.1)      : 61.17 / 100
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

