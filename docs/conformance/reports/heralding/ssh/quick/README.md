# heralding / ssh — Quick artifacts

**UHQS 44.38 / F** · UHBS v4.2.2 · δ_C=1.0

## Module scores

| Module | Score | Weight | Status | Notes |
| --- | ---: | --- | --- | --- |
| Module A: Protocol Fidelity | 70.6 | 0.30 | PASSED | accepted null ID |
| Module B: Behavioral Realism | 6.2 | 0.15 | PARTIAL | Authentication failed. |
| Module C: Telemetry Quality | 25.0 | 0.25 | PARTIAL | Authentication failed. |
| Module D: Safety & Containment (C) | 96.0 | GATE | PASSED | Authentication failed. |
| Module E: Scalability & Latency | 20.0 | 0.10 | PARTIAL | P50=0.0ms P95=0.0ms P99=0.0ms TPS_limit=3000.0ms proto=ssh |
| Module F: Static Code Audit | 70.0 | 0.20 | PASSED | POSIX coverage 0% (0/104) |
| Safety Gate δ_C | 1.0 | GATE | — | Containment multiplier |


## Verbatim SCORECARD.txt

```text
====================================================================================
                  UNIVERSAL HONEYPOT BENCHMARK SCORECARD v4.2.2
====================================================================================
Target System         : heralding-ssh
System Profile Class  : Low-Interaction
Protocols             : ssh
Evaluation Date       : 2026-07-29
Evaluation Type       : Full-Spectrum (Static Audit + Dynamic Sandbox)
Environment           : Isolated Sandbox
MCP Surface Depth     : unknown
------------------------------------------------------------------------------------
EVALUATION MODULE                     SCORE (0-100)    WEIGHT    STATUS
------------------------------------------------------------------------------------
Module A: Protocol Fidelity         :  70.6/100       0.30     PASSED (accepted null ID)
Module B: Behavioral Realism        :   6.2/100       0.15     PARTIAL (Authentication failed.)
Module C: Telemetry Quality         :  25.0/100       0.25     PARTIAL (Authentication failed.)
Module D: Safety & Containment (C)  :  96.0/100       GATE     PASSED (Authentication failed.)
Module E: Scalability & Latency     :  20.0/100       0.10     PARTIAL (P50=0.0ms P95=0.0ms P99=0.0ms TPS_limit=3000.0ms proto=ssh)
Module F: Static Code Audit         :  70.0/100       0.20     PASSED (POSIX coverage 0% (0/104))
------------------------------------------------------------------------------------
SAFETY GATE MULTIPLIER                : δ_C = 1.0 (Containment Score C = 96.0 >= 95)
FINAL COMPOSITE SCORE (UHQS 4.2.2)      : 44.38 / 100
OVERALL EVALUATION GRADE              : GRADE F (Fail)
====================================================================================
```


## Files in this directory

- [`SCORECARD.txt`](SCORECARD.txt) — human-readable UHBS scorecard
- [`report.json`](report.json) — machine-readable module checks / evidence
- [`MANIFEST.json`](MANIFEST.json) — run manifest (when present)
- [`uhbs-run.log`](uhbs-run.log) — harness console log (when present)

Parent protocol hub: [`../`](../index.md)
