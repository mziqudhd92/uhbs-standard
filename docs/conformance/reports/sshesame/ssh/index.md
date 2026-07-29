# sshesame — SSH

**Status:** Informative · evaluation proof  
**UHBS:** v4.2.2 · **Class:** Low-Interaction · **Protocol:** `ssh`  
**Target id:** `sshesame-ssh` · **Evaluated:** 2026-07-29

| Run | UHQS | Grade | δ_C | Artifacts |
| --- | ---: | --- | --- | --- |
| [Quick](quick/) | **65.13** | D | 1.0 | [`SCORECARD.txt`](quick/SCORECARD.txt) · [`report.json`](quick/report.json) |
| [Full](full/) | **61.06** | D | 1.0 | [`SCORECARD.txt`](full/SCORECARD.txt) · [`report.json`](full/report.json) |

## Full run — module breakdown (analyst view)

| Module | Score | Weight | Status | Notes |
| --- | ---: | --- | --- | --- |
| Module A: Protocol Fidelity | 57.1 | 0.30 | PARTIAL | accepted null ID |
| Module B: Behavioral Realism | 41.2 | 0.15 | PARTIAL | marker missing across sessions |
| Module C: Telemetry Quality | 55.0 | 0.25 | PARTIAL | no STIX objects found |
| Module D: Safety & Containment (C) | 100.0 | GATE | PASSED | stable |
| Module E: Scalability & Latency | 100.0 | 0.10 | PASSED | service alive after load (connect 0.1ms) |
| Module F: Static Code Audit | 70.0 | 0.20 | PASSED | POSIX coverage 0% (0/104) |
| Safety Gate δ_C | 1.0 | GATE | — | Containment multiplier |


## Full scorecard (verbatim)

```text
====================================================================================
                  UNIVERSAL HONEYPOT BENCHMARK SCORECARD v4.2.2
====================================================================================
Target System         : sshesame-ssh
System Profile Class  : Low-Interaction
Protocols             : ssh
Evaluation Date       : 2026-07-29
Evaluation Type       : Full-Spectrum (Static Audit + Dynamic Sandbox)
Environment           : Isolated Sandbox
MCP Surface Depth     : unknown
------------------------------------------------------------------------------------
EVALUATION MODULE                     SCORE (0-100)    WEIGHT    STATUS
------------------------------------------------------------------------------------
Module A: Protocol Fidelity         :  57.1/100       0.30     PARTIAL (accepted null ID)
Module B: Behavioral Realism        :  41.2/100       0.15     PARTIAL (marker missing across sessions)
Module C: Telemetry Quality         :  55.0/100       0.25     PARTIAL (no STIX objects found)
Module D: Safety & Containment (C)  : 100.0/100       GATE     PASSED (stable)
Module E: Scalability & Latency     : 100.0/100       0.10     PASSED (service alive after load (connect 0.1ms))
Module F: Static Code Audit         :  70.0/100       0.20     PASSED (POSIX coverage 0% (0/104))
------------------------------------------------------------------------------------
SAFETY GATE MULTIPLIER                : δ_C = 1.0 (Containment Score C = 100.0 >= 95)
FINAL COMPOSITE SCORE (UHQS 4.2.2)      : 61.06 / 100
OVERALL EVALUATION GRADE              : GRADE D (Needs Remediation)
====================================================================================
```



## CTI & blue-team reading

Low-interaction SSH decoy that accepts sessions and logs activity without executing host commands.

### Module interpretation (this protocol)

| Module | Score | Analyst reading |
| --- | ---: | --- |
| A — Protocol Fidelity | 57.1 | Protocol speak / banner-handshake quality for keeping automated clients engaged. |
| B — Behavioral Realism | 41.2 | Post-connect realism (auth/session). Low often means credential-only or reject-by-design. |
| C — Telemetry Quality | 55.0 | How much useful telemetry the *graded lab* exposed to UHBS — not your SIEM maturity. |
| D — Safety & Containment (C) | 100.0 | Containment/Safety Gate. Below threshold collapses UHQS via δ_C. Safety Gate passed in this lab configuration. |
| E — Scalability & Latency | 100.0 | Latency vs profile P95. Low can mean timeouts, tarpits, or slow handlers. |
| F — Static Code Audit | 70.0 | Static audit of the lab source tree — hygiene signal, not a full CVE program. |
| δ_C | 1.0 | Safety Gate multiplier applied to composite UHQS. |

- Useful for collecting SSH brute-force / credential-stuffing attempts and client banners from opportunistic Internet noise.
- Expect session metadata and command attempts as logged by the decoy — not a full high-interaction filesystem for malware drop analysis unless you add other tooling.

- Deploy only on isolated decoy segments; treat accepted credentials as poisoned (never reuse on real assets).
- Forward decoy logs to SIEM with clear `honeypot=sshesame` labels to avoid false-positive incident escalations.

**Signals:** SSH auth attempts, channel/request activity, client versions — as emitted by sshesame logging.

See product hub for full analyst notes and [READING-UHQS.md](../../READING-UHQS.md).

## Guides

- Product hub: [`../`](../index.md)
- [Tutorial](../TUTORIAL.md)
- [Methodology](../METHODOLOGY.md)
- Published scorecard page: [`../../../scorecards/sshesame-ssh.md`](../../../scorecards/sshesame-ssh.md)

> Named products appear only under conformance as evaluation proof — not UHBS requirements or endorsements.
