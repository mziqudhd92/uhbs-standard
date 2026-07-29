# Scorecard: heralding — ssh

**Status:** Informative · evaluation proof (not an endorsement)  
**UHBS:** **4.2.2** · **Class:** Low-Interaction · **Protocol / surface:** `ssh`  
**Target id (lab):** `heralding-ssh` · **Evaluation date:** 2026-07-29

| Run | UHQS | Grade | δ_C | Proof artifacts |
| --- | ---: | --- | --- | --- |
| Quick | 44.38 | F | 1.0 | See report hub quick artifacts |
| **Full (authoritative)** | **44.18** | **F** | **1.0** | Verbatim SCORECARD below + `report.json` on the report hub |

**Report hub:** [heralding / ssh](../conformance/reports/heralding/ssh/index.md) · [Tutorial](../conformance/reports/heralding/TUTORIAL.md) · [Methodology](../conformance/reports/heralding/METHODOLOGY.md)  
**How to read UHQS:** [CTI / blue-team guide](../conformance/reports/READING-UHQS.md)

## Proof: module scores (full run)

These numbers are copied from the lab `SCORECARD.txt` produced by `uhbs-lab` — not hand-typed summaries.

| Module | Score | Weight | Status | Notes |
| --- | ---: | --- | --- | --- |
| Module A: Protocol Fidelity | 70.6 | 0.30 | PASSED | accepted null ID |
| Module B: Behavioral Realism | 6.2 | 0.15 | PARTIAL | Authentication failed. |
| Module C: Telemetry Quality | 25.0 | 0.25 | PARTIAL | Authentication failed. |
| Module D: Safety & Containment (C) | 96.0 | GATE | PASSED | Authentication failed. |
| Module E: Scalability & Latency | 20.0 | 0.10 | PARTIAL | P50=0.0ms P95=0.0ms P99=0.0ms TPS_limit=3000.0ms proto=ssh |
| Module F: Static Code Audit | 69.0 | 0.20 | PARTIAL | POSIX coverage 0% (0/104) |
| Safety Gate δ_C | 1.0 | GATE | — | Containment multiplier applied to UHQS |


## How CTI / blue team should read this

| Module | Score | Analyst reading |
| --- | ---: | --- |
| A — Protocol Fidelity | 70.6 | Protocol speak / banner-handshake quality for keeping automated clients engaged. |
| B — Behavioral Realism | 6.2 | Post-connect realism (auth/session). Low often means credential-only or reject-by-design. **CTI:** treat primarily as auth/connection intelligence. |
| C — Telemetry Quality | 25.0 | Telemetry visible to the UHBS lab harness — not a claim about your SIEM pipeline. **Blue team:** plan explicit log shipping. |
| D — Safety & Containment (C) | 96.0 | Containment / Safety Gate. Below threshold collapses UHQS via δ_C. Safety Gate passed in this lab configuration. |
| E — Scalability & Latency | 20.0 | Latency vs profile P95. Low can mean timeouts, tarpits, or slow handlers. |
| F — Static Code Audit | 69.0 | Static audit of the graded source tree — hygiene signal, not a full CVE program. |
| δ_C | 1.0 | Safety Gate multiplier applied to composite UHQS. |


- **CTI:** use module notes to judge what attacker activity you can actually observe (auth-only vs interactive vs tarpit).
- **Blue team:** verify Safety Gate (Module D / δ_C) and wire real log shipping before Internet exposure.
- **Do not** cite UHQS without the verbatim SCORECARD or `report.json` from the report hub.

## Verbatim full SCORECARD

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
Module F: Static Code Audit         :  69.0/100       0.20     PARTIAL (POSIX coverage 0% (0/104))
------------------------------------------------------------------------------------
SAFETY GATE MULTIPLIER                : δ_C = 1.0 (Containment Score C = 96.0 >= 95)
FINAL COMPOSITE SCORE (UHQS 4.2.2)      : 44.18 / 100
OVERALL EVALUATION GRADE              : GRADE F (Fail)
====================================================================================
```

## Replication

Re-run commands are in the [tutorial](../conformance/reports/heralding/TUTORIAL.md). Environment and limitations are in the [methodology](../conformance/reports/heralding/METHODOLOGY.md).

> Product names appear only under conformance as evaluation proof — not UHBS requirements.
