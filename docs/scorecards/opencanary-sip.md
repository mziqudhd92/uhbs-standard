# OpenCanary — SIP

**Status:** Informative · evaluation proof  
**Full UHQS:** **46.44** · Grade **F** · δ_C **0.81**  
**Quick UHQS:** 40.01 / F

Fixture: [`../conformance/fixtures/opencanary-sip.scorecard.json`](../conformance/fixtures/opencanary-sip.scorecard.json)  
Reports: [`../conformance/reports/opencanary/sip/`](../conformance/reports/opencanary/sip/)

## How to read this scorecard (CTI / blue team)

| Module | Score | Analyst reading |
| --- | ---: | --- |
| A — Protocol Fidelity | 55.7 | Protocol speak / banner-handshake quality for keeping automated clients engaged. |
| B — Behavioral Realism | 62.5 | Post-connect realism (auth/session). Low often means credential-only or reject-by-design. |
| C — Telemetry Quality | 55.0 | How much useful telemetry the *graded lab* exposed to UHBS — not your SIEM maturity. |
| D — Safety & Containment (C) | 90.0 | Containment/Safety Gate. Below threshold collapses UHQS via δ_C. |
| E — Scalability & Latency | 35.0 | Latency vs profile P95. Low can mean timeouts, tarpits, or slow handlers. Expect timeouts or slow responses under probe load. |
| F — Static Code Audit | 70.0 | Static audit of the lab source tree — hygiene signal, not a full CVE program. |
| δ_C | 0.81 | Safety Gate multiplier applied to composite UHQS. |

- **CTI:** use module notes + verbatim SCORECARD to judge what attacker activity you can actually observe.
- **Blue team:** verify Safety Gate (δ_C / Module D) and plan log shipping before Internet exposure.
- **Guide:** [How to read UHBS lab proof](../conformance/reports/READING-UHQS.md)
