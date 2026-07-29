# Scorecard: Honeytrap (DutchSec) — ssh

**Status:** Informative · evaluation proof (not an endorsement)  
**UHBS:** **4.2.2** · **Class:** Low-Interaction · **Protocol / surface:** `ssh`  
**Target id (lab):** `honeytrap-ssh` · **Evaluation date:** 2026-07-29

| Run | UHQS | Grade | δ_C | Proof artifacts |
| --- | ---: | --- | --- | --- |
| Quick | 44.38 | F | 1.0 | See report hub quick artifacts |
| **Full (authoritative)** | **44.38** | **F** | **1.0** | Verbatim SCORECARD below + `report.json` on the report hub |

**Report hub:** [Honeytrap (DutchSec) / ssh](../conformance/reports/honeytrap/ssh/index.md) · [Tutorial](../conformance/reports/honeytrap/TUTORIAL.md) · [Methodology](../conformance/reports/honeytrap/METHODOLOGY.md)  
**How to read UHQS:** [CTI / blue-team guide](../conformance/reports/READING-UHQS.md)

## Proof: module scores (full run)

| Module | Score | Weight | Status | Notes |
| --- | ---: | --- | --- | --- |
| Module A: Protocol Fidelity | 70.6 | 0.30 | PASSED |  |
| Module B: Behavioral Realism | 6.2 | 0.15 | PARTIAL |  |
| Module C: Telemetry Quality | 25.0 | 0.25 | PARTIAL |  |
| Module D: Safety & Containment (C) | 96.0 | GATE | PASSED |  |
| Module E: Scalability & Latency | 20.0 | 0.10 | PARTIAL |  |
| Module F: Static Code Audit | 70.0 | 0.20 | PASSED |  |

## Verbatim full SCORECARD

```text
====================================================================================
                  UNIVERSAL HONEYPOT BENCHMARK SCORECARD v4.2.2
====================================================================================
Target System         : honeytrap-ssh
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
Module B: Behavioral Realism        :   6.2/100       0.15     PARTIAL (Incompatible ssh peer (no acceptable host key))
Module C: Telemetry Quality         :  25.0/100       0.25     PARTIAL (Incompatible ssh peer (no acceptable host key))
Module D: Safety & Containment (C)  :  96.0/100       GATE     PASSED (Incompatible ssh peer (no acceptable host key))
Module E: Scalability & Latency     :  20.0/100       0.10     PARTIAL (P50=0.0ms P95=0.0ms P99=0.0ms TPS_limit=3000.0ms proto=ssh)
Module F: Static Code Audit         :  70.0/100       0.20     PASSED (POSIX coverage 0% (0/104))
------------------------------------------------------------------------------------
SAFETY GATE MULTIPLIER                : δ_C = 1.0 (Containment Score C = 96.0 >= 95)
FINAL COMPOSITE SCORE (UHQS 4.2.2)      : 44.38 / 100
OVERALL EVALUATION GRADE              : GRADE F (Fail)
====================================================================================
```

## How CTI / blue team should read this

Prefer the **full** SCORECARD. Check **δ_C** (below 1.0 reduces UHQS). Module C is harness visibility, not SIEM. See [READING-UHQS.md](../conformance/reports/READING-UHQS.md). Do not cite UHQS without verbatim SCORECARD or `report.json`.
