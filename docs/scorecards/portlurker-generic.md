# Scorecard: portlurker — generic

**Status:** Informative · evaluation proof (not an endorsement)  
**UHBS:** **4.2.2** · **Class:** Low-Interaction · **Protocol / surface:** `generic`  
**Target id (lab):** `portlurker-generic` · **Evaluation date:** 2026-07-29

| Run | UHQS | Grade | δ_C | Proof artifacts |
| --- | ---: | --- | --- | --- |
| Quick | 39.84 | F | 0.5625 | See report hub quick artifacts |
| **Full (authoritative)** | **39.84** | **F** | **0.5625** | Verbatim SCORECARD below + `report.json` on the report hub |

**Report hub:** [portlurker / generic](../conformance/reports/portlurker/generic/index.md) · [Tutorial](../conformance/reports/portlurker/TUTORIAL.md) · [Methodology](../conformance/reports/portlurker/METHODOLOGY.md)  
**How to read UHQS:** [CTI / blue-team guide](../conformance/reports/READING-UHQS.md)

## Proof: module scores (full run)

| Module | Score | Weight | Status | Notes |
| --- | ---: | --- | --- | --- |
| Module A: Protocol Fidelity | 79.0 | 0.30 | PASSED |  |
| Module B: Behavioral Realism | 62.5 | 0.15 | PARTIAL |  |
| Module C: Telemetry Quality | 55.0 | 0.25 | PARTIAL |  |
| Module D: Safety & Containment (C) | 75.0 | GATE | PASSED |  |
| Module E: Scalability & Latency | 100.0 | 0.10 | PASSED |  |
| Module F: Static Code Audit | 70.0 | 0.20 | PASSED |  |

## Verbatim full SCORECARD

```text
====================================================================================
                  UNIVERSAL HONEYPOT BENCHMARK SCORECARD v4.2.2
====================================================================================
Target System         : portlurker-generic
System Profile Class  : Low-Interaction
Protocols             : generic
Evaluation Date       : 2026-07-29
Evaluation Type       : Full-Spectrum (Static Audit + Dynamic Sandbox)
Environment           : Isolated Sandbox
MCP Surface Depth     : unknown
------------------------------------------------------------------------------------
EVALUATION MODULE                     SCORE (0-100)    WEIGHT    STATUS
------------------------------------------------------------------------------------
Module A: Protocol Fidelity         :  79.0/100       0.30     PASSED (fsm=70 nego=70 timing=100)
Module B: Behavioral Realism        :  62.5/100       0.15     PARTIAL (survived binary blast)
Module C: Telemetry Quality         :  55.0/100       0.25     PARTIAL (no STIX objects found)
Module D: Safety & Containment (C)  :  75.0/100       GATE     PASSED (UHBS_AIRGAP_ATTESTED=1 (operator attestation; not a substitute for shell probes on SSH decoys))
Module E: Scalability & Latency     : 100.0/100       0.10     PASSED (service alive after load (connect 0.9ms))
Module F: Static Code Audit         :  70.0/100       0.20     PASSED (POSIX coverage 0% (0/104))
------------------------------------------------------------------------------------
SAFETY GATE MULTIPLIER                : δ_C = 0.5625 (C = 75.0 < 95 — exponential penalty)
FINAL COMPOSITE SCORE (UHQS 4.2.2)      : 39.84 / 100
OVERALL EVALUATION GRADE              : GRADE F (Fail)
====================================================================================
```

## How CTI / blue team should read this

Prefer the **full** SCORECARD. Check **δ_C** (below 1.0 reduces UHQS). Module C is harness visibility, not SIEM. See [READING-UHQS.md](../conformance/reports/READING-UHQS.md). Do not cite UHQS without verbatim SCORECARD or `report.json`.
