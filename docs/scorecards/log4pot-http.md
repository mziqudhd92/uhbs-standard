# Scorecard: Log4Pot — http

**Status:** Informative · evaluation proof (not an endorsement)  
**UHBS:** **4.2.2** · **Class:** Web-API · **Protocol / surface:** `http`  
**Target id (lab):** `Log4Pot-http` · **Evaluation date:** 2026-07-29

| Run | UHQS | Grade | δ_C | Proof artifacts |
| --- | ---: | --- | --- | --- |
| Quick | 41.71 | F | 0.5625 | See report hub quick artifacts |
| **Full (authoritative)** | **38.0** | **F** | **0.5625** | Verbatim SCORECARD below + `report.json` on the report hub |

**Report hub:** [Log4Pot / http](../conformance/reports/Log4Pot/http/index.md) · [Tutorial](../conformance/reports/Log4Pot/TUTORIAL.md) · [Methodology](../conformance/reports/Log4Pot/METHODOLOGY.md)  
**How to read UHQS:** [CTI / blue-team guide](../conformance/reports/READING-UHQS.md)

## Proof: module scores (full run)

These numbers are copied from the lab `SCORECARD.txt` produced by `uhbs-lab` — not hand-typed summaries.

| Module | Score | Weight | Status | Notes |
| --- | ---: | --- | --- | --- |
| Module A: Protocol Fidelity | 70.6 | 0.25 | PASSED | status=200 |
| Module B: Behavioral Realism | 50.5 | 0.20 | PARTIAL | inconsistent/no HTTP |
| Module C: Telemetry Quality | 55.0 | 0.20 | PARTIAL | no STIX objects found |
| Module D: Safety & Containment (C) | 75.0 | GATE | PASSED | UHBS_AIRGAP_ATTESTED=1 (operator attestation; not a substitute for shell probes on SSH decoys) |
| Module E: Scalability & Latency | 100.0 | 0.15 | PASSED | service alive after load (connect 0.2ms) |
| Module F: Static Code Audit | 69.0 | 0.20 | PARTIAL | POSIX coverage 0% (0/104) |
| Safety Gate δ_C | 0.5625 | GATE | — | Containment multiplier applied to UHQS |


## How CTI / blue team should read this

| Module | Score | Analyst reading |
| --- | ---: | --- |
| A — Protocol Fidelity | 70.6 | Protocol speak / banner-handshake quality for keeping automated clients engaged. |
| B — Behavioral Realism | 50.5 | Post-connect realism (auth/session). Low often means credential-only or reject-by-design. |
| C — Telemetry Quality | 55.0 | Telemetry visible to the UHBS lab harness — not a claim about your SIEM pipeline. |
| D — Safety & Containment (C) | 75.0 | Containment / Safety Gate. Below threshold collapses UHQS via δ_C. |
| E — Scalability & Latency | 100.0 | Latency vs profile P95. Low can mean timeouts, tarpits, or slow handlers. |
| F — Static Code Audit | 69.0 | Static audit of the graded source tree — hygiene signal, not a full CVE program. |
| δ_C | 0.5625 | Safety Gate multiplier applied to composite UHQS. |


- **CTI:** use module notes to judge what attacker activity you can actually observe (auth-only vs interactive vs tarpit).
- **Blue team:** verify Safety Gate (Module D / δ_C) and wire real log shipping before Internet exposure.
- **Do not** cite UHQS without the verbatim SCORECARD or `report.json` from the report hub.

## Verbatim full SCORECARD

```text
====================================================================================
                  UNIVERSAL HONEYPOT BENCHMARK SCORECARD v4.2.2
====================================================================================
Target System         : Log4Pot-http
System Profile Class  : Web-API
Protocols             : http
Evaluation Date       : 2026-07-29
Evaluation Type       : Full-Spectrum (Static Audit + Dynamic Sandbox)
Environment           : Isolated Sandbox
MCP Surface Depth     : unknown
------------------------------------------------------------------------------------
EVALUATION MODULE                     SCORE (0-100)    WEIGHT    STATUS
------------------------------------------------------------------------------------
Module A: Protocol Fidelity         :  70.6/100       0.25     PASSED (status=200)
Module B: Behavioral Realism        :  50.5/100       0.20     PARTIAL (inconsistent/no HTTP)
Module C: Telemetry Quality         :  55.0/100       0.20     PARTIAL (no STIX objects found)
Module D: Safety & Containment (C)  :  75.0/100       GATE     PASSED (UHBS_AIRGAP_ATTESTED=1 (operator attestation; not a substitute for shell probes on SSH decoys))
Module E: Scalability & Latency     : 100.0/100       0.15     PASSED (service alive after load (connect 0.2ms))
Module F: Static Code Audit         :  69.0/100       0.20     PARTIAL (POSIX coverage 0% (0/104))
------------------------------------------------------------------------------------
SAFETY GATE MULTIPLIER                : δ_C = 0.5625 (C = 75.0 < 95 — exponential penalty)
FINAL COMPOSITE SCORE (UHQS 4.2.2)      : 38.0 / 100
OVERALL EVALUATION GRADE              : GRADE F (Fail)
====================================================================================
```

## Replication

Re-run commands are in the [tutorial](../conformance/reports/Log4Pot/TUTORIAL.md). Environment and limitations are in the [methodology](../conformance/reports/Log4Pot/METHODOLOGY.md).

> Product names appear only under conformance as evaluation proof — not UHBS requirements.
