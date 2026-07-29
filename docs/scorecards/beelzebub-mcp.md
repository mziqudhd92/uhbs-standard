# Scorecard: Beelzebub — MCP :8000

**Status:** Informative · evaluation proof  
**Class:** Web-API (MCP v1) · **Protocol:** MCP `:8000`  
**Full UHQS:** **42.93** · Grade **F** · δ_C **0.56**  
**Quick UHQS:** 43.04 / F

Source report: [`../conformance/reports/beelzebub/mcp/`](../conformance/reports/beelzebub/mcp/index.md)  
Grading notes: [`../architecture/mcp-honeypot-grading.md`](../architecture/mcp-honeypot-grading.md)

> Product names appear only under conformance as evaluation proof — not UHBS requirements.

## How to read this scorecard (CTI / blue team)

| Module | Score | Analyst reading |
| --- | ---: | --- |
| A — Protocol Fidelity | 70.6 | Protocol speak / banner-handshake quality for keeping automated clients engaged. |
| B — Behavioral Realism | 94.3 | Post-connect realism (auth/session). Low often means credential-only or reject-by-design. |
| C — Telemetry Quality | 55.0 | How much useful telemetry the *graded lab* exposed to UHBS — not your SIEM maturity. |
| D — Safety & Containment (C) | 75.0 | Containment/Safety Gate. Below threshold collapses UHQS via δ_C. |
| E — Scalability & Latency | 100.0 | Latency vs profile P95. Low can mean timeouts, tarpits, or slow handlers. |
| F — Static Code Audit | 69.0 | Static audit of the lab source tree — hygiene signal, not a full CVE program. |
| δ_C | 0.5625 | Safety Gate multiplier applied to composite UHQS. |

- **CTI:** use module notes + verbatim SCORECARD to judge what attacker activity you can actually observe.
- **Blue team:** verify Safety Gate (δ_C / Module D) and plan log shipping before Internet exposure.
- **Guide:** [How to read UHBS lab proof](../conformance/reports/READING-UHQS.md)
