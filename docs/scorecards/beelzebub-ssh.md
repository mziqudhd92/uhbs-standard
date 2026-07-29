# Scorecard: Beelzebub — SSH :2222

**Status:** Informative · evaluation proof  
**Class:** Low-Interaction · **Protocol:** SSH `: 2222`  
**Full UHQS:** **59.88** · Grade **D** · δ_C **1.0**  
**Quick UHQS:** 74.45 / C

Source report: [`../conformance/reports/beelzebub/ssh/`](../conformance/reports/beelzebub/ssh/index.md)  
Fixture: [`../conformance/fixtures/beelzebub-ssh.scorecard.json`](../conformance/fixtures/beelzebub-ssh.scorecard.json)

> Product names appear only under conformance as evaluation proof — not UHBS requirements.

## How to read this scorecard (CTI / blue team)

| Module | Score | Analyst reading |
| --- | ---: | --- |
| A — Protocol Fidelity | 70.6 | Protocol speak / banner-handshake quality for keeping automated clients engaged. |
| B — Behavioral Realism | 6.2 | Post-connect realism (auth/session). Low often means credential-only or reject-by-design. **CTI:** treat primarily as auth/connection intelligence. |
| C — Telemetry Quality | 55.0 | How much useful telemetry the *graded lab* exposed to UHBS — not your SIEM maturity. |
| D — Safety & Containment (C) | 100.0 | Containment/Safety Gate. Below threshold collapses UHQS via δ_C. Safety Gate passed in this lab configuration. |
| E — Scalability & Latency | 100.0 | Latency vs profile P95. Low can mean timeouts, tarpits, or slow handlers. |
| F — Static Code Audit | 70.0 | Static audit of the lab source tree — hygiene signal, not a full CVE program. |
| δ_C | 1.0 | Safety Gate multiplier applied to composite UHQS. |

- **CTI:** use module notes + verbatim SCORECARD to judge what attacker activity you can actually observe.
- **Blue team:** verify Safety Gate (δ_C / Module D) and plan log shipping before Internet exposure.
- **Guide:** [How to read UHBS lab proof](../conformance/reports/READING-UHQS.md)
