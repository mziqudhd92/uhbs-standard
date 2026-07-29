# Scorecard: node-ftp-honeypot — ftp

**Status:** Informative · evaluation proof  
**Class:** Low-Interaction · **Protocol:** `ftp`  
**Full UHQS:** **35.85** · Grade **F** · δ_C **0.5625**  
**Quick UHQS:** 35.96 / F  
**Evaluated:** 2026-07-29 · **UHBS:** 4.2.2

Source report: [`../conformance/reports/node-ftp-honeypot/ftp/`](../conformance/reports/node-ftp-honeypot/ftp/index.md)

## Module breakdown (full run)

| Module | Score | Weight | Status | Notes |
| --- | ---: | --- | --- | --- |
| Module A: Protocol Fidelity | 60.0 | 0.30 | PARTIAL |  |
| Module B: Behavioral Realism | 54.5 | 0.15 | PARTIAL |  |
| Module C: Telemetry Quality | 55.0 | 0.25 | PARTIAL | no STIX objects found |
| Module D: Safety & Containment (C) | 75.0 | GATE | PASSED | UHBS_AIRGAP_ATTESTED=1 (operator attestation; not a substitute for shell probes on SSH decoys) |
| Module E: Scalability & Latency | 100.0 | 0.10 | PASSED | service alive after load (connect 0.3ms) |
| Module F: Static Code Audit | 69.0 | 0.20 | PARTIAL | POSIX coverage 0% (0/104) |
| Safety Gate δ_C | 0.5625 | GATE | — | Containment multiplier |



## How to read this scorecard (CTI / blue team)

| Module | Score | Analyst reading |
| --- | ---: | --- |
| A — Protocol Fidelity | 60.0 | Protocol speak / banner-handshake quality for keeping automated clients engaged. |
| B — Behavioral Realism | 54.5 | Post-connect realism (auth/session). Low often means credential-only or reject-by-design. |
| C — Telemetry Quality | 55.0 | How much useful telemetry the *graded lab* exposed to UHBS — not your SIEM maturity. |
| D — Safety & Containment (C) | 75.0 | Containment/Safety Gate. Below threshold collapses UHQS via δ_C. |
| E — Scalability & Latency | 100.0 | Latency vs profile P95. Low can mean timeouts, tarpits, or slow handlers. |
| F — Static Code Audit | 69.0 | Static audit of the lab source tree — hygiene signal, not a full CVE program. |
| δ_C | 0.5625 | Safety Gate multiplier applied to composite UHQS. |

- **CTI:** use module notes + verbatim SCORECARD to judge what attacker activity you can actually observe.
- **Blue team:** verify Safety Gate (δ_C / Module D) and plan log shipping before Internet exposure.
- **Guide:** [How to read UHBS lab proof](../conformance/reports/READING-UHQS.md)

## Verbatim full SCORECARD

```text
====================================================================================
                  UNIVERSAL HONEYPOT BENCHMARK SCORECARD v4.2.2
====================================================================================
Target System         : node-ftp-honeypot
System Profile Class  : Low-Interaction
Protocols             : ftp
Evaluation Date       : 2026-07-29
Evaluation Type       : Full-Spectrum (Static Audit + Dynamic Sandbox)
Environment           : Isolated Sandbox
MCP Surface Depth     : unknown
------------------------------------------------------------------------------------
EVALUATION MODULE                     SCORE (0-100)    WEIGHT    STATUS
------------------------------------------------------------------------------------
Module A: Protocol Fidelity         :  60.0/100       0.30     PARTIAL (220-Welcome to VOFTP a very open FTP Server.
220 Ready
502 Command not whitelisted: RETR
502 Command not whitelisted:)
Module B: Behavioral Realism        :  54.5/100       0.15     PARTIAL (USER step failed: 220 Ready
)
Module C: Telemetry Quality         :  55.0/100       0.25     PARTIAL (no STIX objects found)
Module D: Safety & Containment (C)  :  75.0/100       GATE     PASSED (UHBS_AIRGAP_ATTESTED=1 (operator attestation; not a substitute for shell probes on SSH decoys))
Module E: Scalability & Latency     : 100.0/100       0.10     PASSED (service alive after load (connect 0.3ms))
Module F: Static Code Audit         :  69.0/100       0.20     PARTIAL (POSIX coverage 0% (0/104))
------------------------------------------------------------------------------------
SAFETY GATE MULTIPLIER                : δ_C = 0.5625 (C = 75.0 < 95 — exponential penalty)
FINAL COMPOSITE SCORE (UHQS 4.2.2)      : 35.85 / 100
OVERALL EVALUATION GRADE              : GRADE F (Fail)
====================================================================================
```


## Replication

See the report [tutorial](../conformance/reports/node-ftp-honeypot/TUTORIAL.md) and [methodology](../conformance/reports/node-ftp-honeypot/METHODOLOGY.md).

> Product names appear only under conformance as evaluation proof — not UHBS requirements.
