# Scorecard: Cowrie — SSH :2222

**Status:** Informative · evaluation proof  
**Class:** Low-Interaction · **Protocol:** SSH `:2222`  
**Full UHQS:** **61.37** · Grade **D** · δ_C **1.0**  
**Quick UHQS:** 82.76 / B

Source report: [`../conformance/reports/cowrie/ssh/`](../conformance/reports/cowrie/ssh/index.md)  
Fixture: [`../conformance/fixtures/cowrie-ssh.scorecard.json`](../conformance/fixtures/cowrie-ssh.scorecard.json)

> SFTP uploads are supported by Cowrie as an **SSH subsystem** (`sftp_enabled = true`). UHBS has no separate `sftp` protocol plugin; SFTP was smoke-verified during this lab under the SSH target.

## How to read this scorecard (CTI / blue team)

| Module | Score | Analyst reading |
| --- | ---: | --- |
| A — Protocol Fidelity | 57.1 | Protocol speak / banner-handshake quality for keeping automated clients engaged. |
| B — Behavioral Realism | 60.0 | Post-connect realism (auth/session). Low often means credential-only or reject-by-design. |
| C — Telemetry Quality | 55.0 | How much useful telemetry the *graded lab* exposed to UHBS — not your SIEM maturity. |
| D — Safety & Containment (C) | 100.0 | Containment/Safety Gate. Below threshold collapses UHQS via δ_C. Safety Gate passed in this lab configuration. |
| E — Scalability & Latency | 75.0 | Latency vs profile P95. Low can mean timeouts, tarpits, or slow handlers. |
| F — Static Code Audit | 70.0 | Static audit of the lab source tree — hygiene signal, not a full CVE program. |
| δ_C | 1.0 | Safety Gate multiplier applied to composite UHQS. |

- **CTI:** use module notes + verbatim SCORECARD to judge what attacker activity you can actually observe.
- **Blue team:** verify Safety Gate (δ_C / Module D) and plan log shipping before Internet exposure.
- **Guide:** [How to read UHBS lab proof](../conformance/reports/READING-UHQS.md)
