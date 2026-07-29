# Scorecard: beelzebub — ssh

**Status:** Informative · evaluation proof (not an endorsement)  
**UHBS:** **4.2.2** · **Class:** Low-Interaction · **Protocol / surface:** `ssh`  
**Target id (lab):** `beelzebub-ssh` · **Evaluation date:** 2026-07-27

| Run | UHQS | Grade | δ_C | Proof artifacts |
| --- | ---: | --- | --- | --- |
| Quick | 74.45 | C | 1.0 | See report hub quick artifacts |
| **Full (authoritative)** | **59.88** | **D** | **1.0** | Verbatim SCORECARD below + `report.json` on the report hub |

**Report hub:** [beelzebub / ssh](../conformance/reports/beelzebub/ssh/index.md) · [Tutorial](../conformance/reports/beelzebub/TUTORIAL.md) · [Methodology](../conformance/reports/beelzebub/METHODOLOGY.md)  
**How to read UHQS:** [CTI / blue-team guide](../conformance/reports/READING-UHQS.md)

## Proof: module scores (full run)

These numbers are copied from the lab `SCORECARD.txt` produced by `uhbs-lab` — not hand-typed summaries.

| Module | Score | Weight | Status | Notes |
| --- | ---: | --- | --- | --- |
| Module A: Protocol Fidelity | 70.6 | 0.30 | PASSED | accepted null ID |
| Module B: Behavioral Realism | 6.2 | 0.15 | PARTIAL | marker missing across sessions |
| Module C: Telemetry Quality | 55.0 | 0.25 | PARTIAL | no STIX objects found |
| Module D: Safety & Containment (C) | 100.0 | GATE | PASSED | stable |
| Module E: Scalability & Latency | 100.0 | 0.10 | PASSED | service alive after load (connect 0.8ms) |
| Module F: Static Code Audit | 70.0 | 0.20 | PASSED | semgrep error/critical=7 total=36 |
| Safety Gate δ_C | 1.0 | GATE | — | Containment multiplier applied to UHQS |


## How CTI / blue team should read this

| Module | Score | Analyst reading |
| --- | ---: | --- |
| A — Protocol Fidelity | 70.6 | Protocol speak / banner-handshake quality for keeping automated clients engaged. |
| B — Behavioral Realism | 6.2 | Post-connect realism (auth/session). Low often means credential-only or reject-by-design. **CTI:** treat primarily as auth/connection intelligence. |
| C — Telemetry Quality | 55.0 | Telemetry visible to the UHBS lab harness — not a claim about your SIEM pipeline. |
| D — Safety & Containment (C) | 100.0 | Containment / Safety Gate. Below threshold collapses UHQS via δ_C. Safety Gate passed in this lab configuration. |
| E — Scalability & Latency | 100.0 | Latency vs profile P95. Low can mean timeouts, tarpits, or slow handlers. |
| F — Static Code Audit | 70.0 | Static audit of the graded source tree — hygiene signal, not a full CVE program. |
| δ_C | 1.0 | Safety Gate multiplier applied to composite UHQS. |


- **CTI:** use module notes to judge what attacker activity you can actually observe (auth-only vs interactive vs tarpit).
- **Blue team:** verify Safety Gate (Module D / δ_C) and wire real log shipping before Internet exposure.
- **Do not** cite UHQS without the verbatim SCORECARD or `report.json` from the report hub.

## Verbatim full SCORECARD

```text
====================================================================================
                  UNIVERSAL HONEYPOT BENCHMARK SCORECARD v4.0.1
====================================================================================
Target System         : beelzebub-ssh
System Profile Class  : Low-Interaction
Protocols             : ssh
Evaluation Date       : 2026-07-27
Evaluation Type       : Full-Spectrum (Static Audit + Dynamic Sandbox)
Environment           : Isolated Sandbox
------------------------------------------------------------------------------------
EVALUATION MODULE                     SCORE (0-100)    WEIGHT    STATUS
------------------------------------------------------------------------------------
Module A: Protocol Fidelity         :  70.6/100       0.30     PASSED (accepted null ID)
Module B: Behavioral Realism        :   6.2/100       0.15     PARTIAL (marker missing across sessions)
Module C: Telemetry Quality         :  55.0/100       0.25     PARTIAL (no STIX objects found)
Module D: Safety & Containment (C)  : 100.0/100       GATE     PASSED (stable)
Module E: Scalability & Latency     : 100.0/100       0.10     PASSED (service alive after load (connect 0.8ms))
Module F: Static Code Audit         :  70.0/100       0.20     PASSED (semgrep error/critical=7 total=36)
------------------------------------------------------------------------------------
SAFETY GATE MULTIPLIER                : δ_C = 1.0 (Containment Score C = 100.0 >= 95)
FINAL COMPOSITE SCORE (UHQS 4.0.1)      : 59.88 / 100
OVERALL EVALUATION GRADE              : GRADE D (Needs Remediation)
====================================================================================
```

## Replication

Re-run commands are in the [tutorial](../conformance/reports/beelzebub/TUTORIAL.md). Environment and limitations are in the [methodology](../conformance/reports/beelzebub/METHODOLOGY.md).

> Product names appear only under conformance as evaluation proof — not UHBS requirements.
