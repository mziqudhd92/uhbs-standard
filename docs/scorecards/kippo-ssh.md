# Scorecard: kippo — ssh

**Status:** Informative · evaluation proof (not an endorsement)  
**UHBS:** **4.2.2** · **Class:** Low-Interaction · **Protocol / surface:** `ssh`  
**Target id (lab):** `kippo-ssh` · **Evaluation date:** 2026-07-29

| Run | UHQS | Grade | δ_C | Proof artifacts |
| --- | ---: | --- | --- | --- |
| Quick | see report hub quick artifacts | — | — | Report hub |
| **Full (authoritative)** | **35.64** | **F** | **1.0** | Verbatim SCORECARD below |

**Report hub:** [kippo / ssh](../conformance/reports/kippo/ssh/index.md)

## Proof: module scores (full run)

| Module | Score | Weight | Status | Notes |
| --- | ---: | --- | --- | --- |
| Module A: Protocol Fidelity | 41.5 | 0.30 | PARTIAL | no KEXINIT |
| Module B: Behavioral Realism | 6.2 | 0.15 | PARTIAL | Negotiation failed. |
| Module C: Telemetry Quality | 25.0 | 0.25 | PARTIAL | Negotiation failed. |
| Module D: Safety & Containment (C) | 96.0 | GATE | PASSED | Negotiation failed. |
| Module E: Scalability & Latency | 20.0 | 0.10 | PARTIAL | P50=0.0ms P95=0.0ms P99=0.0ms TPS_limit=3000.0ms proto=ssh |
| Module F: Static Code Audit | 70.0 | 0.20 | PASSED | POSIX coverage 0% (0/104) |
| Safety Gate δ_C | — | GATE | — | Containment multiplier |

## How CTI / blue team should read this

| Module | Score | Analyst reading |
| --- | ---: | --- |
| A — Protocol Fidelity | 41.5 | Protocol speak / banner-handshake quality for keeping automated clients engaged. |
| B — Behavioral Realism | 6.2 | Post-connect realism (auth/session). Low often means credential-only or reject-by-design. |
| C — Telemetry Quality | 25.0 | Harness-visible telemetry — not your SIEM pipeline maturity. |
| D — Safety & Containment (C) | 96.0 | Containment / Safety Gate. Below threshold collapses UHQS via δ_C. |
| E — Scalability & Latency | 20.0 | Latency vs profile P95. Low can mean timeouts, tarpits, or slow handlers. |
| F — Static Code Audit | 70.0 | Static audit of the graded source tree — hygiene signal, not a full CVE program. |

## Verbatim full SCORECARD

```text
====================================================================================
                  UNIVERSAL HONEYPOT BENCHMARK SCORECARD v4.2.2
====================================================================================
Target System         : kippo-ssh
System Profile Class  : Low-Interaction
Protocols             : ssh
Evaluation Date       : 2026-07-29
Evaluation Type       : Full-Spectrum (Static Audit + Dynamic Sandbox)
Environment           : Isolated Sandbox
MCP Surface Depth     : unknown
------------------------------------------------------------------------------------
EVALUATION MODULE                     SCORE (0-100)    WEIGHT    STATUS
------------------------------------------------------------------------------------
Module A: Protocol Fidelity         :  41.5/100       0.30     PARTIAL (no KEXINIT)
Module B: Behavioral Realism        :   6.2/100       0.15     PARTIAL (Negotiation failed.)
Module C: Telemetry Quality         :  25.0/100       0.25     PARTIAL (Negotiation failed.)
Module D: Safety & Containment (C)  :  96.0/100       GATE     PASSED (Negotiation failed.)
Module E: Scalability & Latency     :  20.0/100       0.10     PARTIAL (P50=0.0ms P95=0.0ms P99=0.0ms TPS_limit=3000.0ms proto=ssh)
Module F: Static Code Audit         :  70.0/100       0.20     PASSED (POSIX coverage 0% (0/104))
------------------------------------------------------------------------------------
SAFETY GATE MULTIPLIER                : δ_C = 1.0 (Containment Score C = 96.0 >= 95)
FINAL COMPOSITE SCORE (UHQS 4.2.2)      : 35.64 / 100
OVERALL EVALUATION GRADE              : GRADE F (Fail)
====================================================================================
```
