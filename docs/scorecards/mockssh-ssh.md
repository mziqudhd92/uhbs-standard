# Scorecard: mockssh — ssh

**Status:** Informative · evaluation proof  
**Class:** Low-Interaction · **Protocol:** `ssh`  
**Full UHQS:** **59.0** · Grade **D** · δ_C **1.0**  
**Quick UHQS:** 59.2 / D  
**Evaluated:** 2026-07-29 · **UHBS:** 4.2.2

Source report: [`../conformance/reports/mockssh/ssh/`](../conformance/reports/mockssh/ssh/index.md)

## Module breakdown (full run)

| Module | Score | Weight | Status | Notes |
| --- | ---: | --- | --- | --- |
| Module A: Protocol Fidelity | 41.5 | 0.30 | PARTIAL | no KEXINIT |
| Module B: Behavioral Realism | 60.0 | 0.15 | PARTIAL | marker missing across sessions |
| Module C: Telemetry Quality | 55.0 | 0.25 | PARTIAL | no STIX objects found |
| Module D: Safety & Containment (C) | 100.0 | GATE | PASSED | stable |
| Module E: Scalability & Latency | 100.0 | 0.10 | PASSED | service alive after load (connect 0.2ms) |
| Module F: Static Code Audit | 69.0 | 0.20 | PARTIAL | POSIX coverage 0% (0/104) |
| Safety Gate δ_C | 1.0 | GATE | — | Containment multiplier |



## How to read this scorecard (CTI / blue team)

| Module | Score | Analyst reading |
| --- | ---: | --- |
| A — Protocol Fidelity | 41.5 | Protocol speak / banner-handshake quality for keeping automated clients engaged. |
| B — Behavioral Realism | 60.0 | Post-connect realism (auth/session). Low often means credential-only or reject-by-design. |
| C — Telemetry Quality | 55.0 | How much useful telemetry the *graded lab* exposed to UHBS — not your SIEM maturity. |
| D — Safety & Containment (C) | 100.0 | Containment/Safety Gate. Below threshold collapses UHQS via δ_C. Safety Gate passed in this lab configuration. |
| E — Scalability & Latency | 100.0 | Latency vs profile P95. Low can mean timeouts, tarpits, or slow handlers. |
| F — Static Code Audit | 69.0 | Static audit of the lab source tree — hygiene signal, not a full CVE program. |
| δ_C | 1.0 | Safety Gate multiplier applied to composite UHQS. |

- **CTI:** use module notes + verbatim SCORECARD to judge what attacker activity you can actually observe.
- **Blue team:** verify Safety Gate (δ_C / Module D) and plan log shipping before Internet exposure.
- **Guide:** [How to read UHBS lab proof](../conformance/reports/READING-UHQS.md)

## Verbatim full SCORECARD

```text
====================================================================================
                  UNIVERSAL HONEYPOT BENCHMARK SCORECARD v4.2.2
====================================================================================
Target System         : mockssh-ssh
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
Module B: Behavioral Realism        :  60.0/100       0.15     PARTIAL (marker missing across sessions)
Module C: Telemetry Quality         :  55.0/100       0.25     PARTIAL (no STIX objects found)
Module D: Safety & Containment (C)  : 100.0/100       GATE     PASSED (stable)
Module E: Scalability & Latency     : 100.0/100       0.10     PASSED (service alive after load (connect 0.2ms))
Module F: Static Code Audit         :  69.0/100       0.20     PARTIAL (POSIX coverage 0% (0/104))
------------------------------------------------------------------------------------
SAFETY GATE MULTIPLIER                : δ_C = 1.0 (Containment Score C = 100.0 >= 95)
FINAL COMPOSITE SCORE (UHQS 4.2.2)      : 59.0 / 100
OVERALL EVALUATION GRADE              : GRADE D (Needs Remediation)
====================================================================================
```


## Replication

See the report [tutorial](../conformance/reports/mockssh/TUTORIAL.md) and [methodology](../conformance/reports/mockssh/METHODOLOGY.md).

> Product names appear only under conformance as evaluation proof — not UHBS requirements.
