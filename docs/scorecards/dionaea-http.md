# Scorecard: Dionaea — HTTP :80

**Status:** Informative · evaluation proof  
**Class:** Web-API · **Protocol:** HTTP `: 80`  
**Full UHQS:** **51.14** · Grade **D** · δ_C **0.81**  
**Quick UHQS:** 46.21 / F

Source report: [`../conformance/reports/dionaea/http/`](../conformance/reports/dionaea/http/index.md)  
Fixture: [`../conformance/fixtures/dionaea-http.scorecard.json`](../conformance/fixtures/dionaea-http.scorecard.json)

> Product names appear only under conformance as evaluation proof — not UHBS requirements.

## How to read this scorecard (CTI / blue team)

| Module | Score | Analyst reading |
| --- | ---: | --- |
| A — Protocol Fidelity | 53.5 | Protocol speak / banner-handshake quality for keeping automated clients engaged. |
| B — Behavioral Realism | 82.5 | Post-connect realism (auth/session). Low often means credential-only or reject-by-design. |
| C — Telemetry Quality | 55.0 | How much useful telemetry the *graded lab* exposed to UHBS — not your SIEM maturity. |
| D — Safety & Containment (C) | 90.0 | Containment/Safety Gate. Below threshold collapses UHQS via δ_C. |
| E — Scalability & Latency | 55.0 | Latency vs profile P95. Low can mean timeouts, tarpits, or slow handlers. |
| F — Static Code Audit | 70.0 | Static audit of the lab source tree — hygiene signal, not a full CVE program. |
| δ_C | 0.81 | Safety Gate multiplier applied to composite UHQS. |

- **CTI:** use module notes + verbatim SCORECARD to judge what attacker activity you can actually observe.
- **Blue team:** verify Safety Gate (δ_C / Module D) and plan log shipping before Internet exposure.
- **Guide:** [How to read UHBS lab proof](../conformance/reports/READING-UHQS.md)
