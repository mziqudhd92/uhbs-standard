# qeeqbox-honeypots — SSH

**Status:** Informative · evaluation proof  
**UHBS:** v4.2.2 · **Class:** Low-Interaction · **Protocol:** `ssh`  
**Target id:** `qeeqbox-ssh` · **Evaluated:** 2026-07-29

| Run | UHQS | Grade | δ_C | Artifacts |
| --- | ---: | --- | --- | --- |
| [Quick](quick/README.md) | **59.88** | D | 1.0 | [`SCORECARD.txt`](quick/SCORECARD.txt) · [`report.json`](quick/report.json) |
| [Full](full/README.md) | **59.68** | D | 1.0 | [`SCORECARD.txt`](full/SCORECARD.txt) · [`report.json`](full/report.json) |

## Full run — module breakdown (analyst view)

| Module | Score | Weight | Status | Notes |
| --- | ---: | --- | --- | --- |
| Module A: Protocol Fidelity | 70.6 | 0.30 | PASSED | accepted null ID |
| Module B: Behavioral Realism | 6.2 | 0.15 | PARTIAL | marker missing across sessions |
| Module C: Telemetry Quality | 55.0 | 0.25 | PARTIAL | Error reading SSH protocol banner |
| Module D: Safety & Containment (C) | 100.0 | GATE | PASSED | stable |
| Module E: Scalability & Latency | 100.0 | 0.10 | PASSED | service alive after load (connect 0.2ms) |
| Module F: Static Code Audit | 69.0 | 0.20 | PARTIAL | POSIX coverage 0% (0/104) |
| Safety Gate δ_C | 1.0 | GATE | — | Containment multiplier |

## Full scorecard (verbatim)

```text
====================================================================================
                  UNIVERSAL HONEYPOT BENCHMARK SCORECARD v4.2.2
====================================================================================
Target System         : qeeqbox-ssh
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
Module B: Behavioral Realism        :   6.2/100       0.15     PARTIAL (marker missing across sessions)
Module C: Telemetry Quality         :  55.0/100       0.25     PARTIAL (Error reading SSH protocol banner)
Module D: Safety & Containment (C)  : 100.0/100       GATE     PASSED (stable)
Module E: Scalability & Latency     : 100.0/100       0.10     PASSED (service alive after load (connect 0.2ms))
Module F: Static Code Audit         :  69.0/100       0.20     PARTIAL (POSIX coverage 0% (0/104))
------------------------------------------------------------------------------------
SAFETY GATE MULTIPLIER                : δ_C = 1.0 (Containment Score C = 100.0 >= 95)
FINAL COMPOSITE SCORE (UHQS 4.2.2)      : 59.68 / 100
OVERALL EVALUATION GRADE              : GRADE D (Needs Remediation)
====================================================================================
```

## CTI & blue-team reading

This page is the protocol-level proof hub for **qeeqbox-honeypots** on **ssh**. Prefer the **full** run over quick for operational decisions. Numbers without the verbatim SCORECARD (or `report.json`) are not trustworthy citations.

### Module interpretation (this protocol)

| Module | Score | Analyst reading |
| --- | ---: | --- |
| A — Protocol Fidelity | 70.6 | Protocol speak / banner-handshake quality for keeping automated clients engaged. |
| B — Behavioral Realism | 6.2 | Post-connect realism (auth/session). Low often means credential-only or reject-by-design. **CTI:** treat primarily as auth/connection intelligence. |
| C — Telemetry Quality | 55.0 | How much useful telemetry the *graded lab* exposed to UHBS — not your SIEM maturity. **Blue team:** plan explicit log shipping; do not assume UHBS C equals production visibility. |
| D — Safety & Containment (C) | 100.0 | Containment/Safety Gate. Below threshold collapses UHQS via δ_C. Safety Gate passed in this lab configuration. |
| E — Scalability & Latency | 100.0 | Latency vs profile P95. Low can mean timeouts, tarpits, or slow handlers. |
| F — Static Code Audit | 69.0 | Static audit of the lab source tree — hygiene signal, not a full CVE program. |
| δ_C | 1.0 | Safety Gate multiplier applied to composite UHQS. |

- **CTI:** use Module A/B to judge engagement depth (scanner noise vs post-auth TTPs). Low B usually means credential/connection intelligence, not interactive malware staging.
- **Blue team:** verify Safety Gate (Module D / δ_C) before Internet exposure; wire SIEM shipping yourself — Module C is harness visibility, not your pipeline.
- **Replication:** commands live in the product tutorial; environment limits in the methodology.

## Guides

- Product hub: [`../`](../index.md)
- [Tutorial](../TUTORIAL.md)
- [Methodology](../METHODOLOGY.md)
- Published scorecard page: [`../../../../scorecards/qeeqbox-ssh.md`](../../../../scorecards/qeeqbox-ssh.md)
- How to read UHQS: [READING-UHQS.md](../../READING-UHQS.md)

> Named products appear only under conformance as evaluation proof — not UHBS requirements or endorsements.
