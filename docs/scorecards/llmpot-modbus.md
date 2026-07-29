# Scorecard: llmpot — modbus

**Status:** Informative · evaluation proof (not an endorsement)  
**UHBS:** **4.2.2** · **Class:** ICS-SCADA · **Protocol / surface:** `modbus`  
**Target id (lab):** `llmpot-modbus` · **Evaluation date:** 2026-07-28

| Run | UHQS | Grade | δ_C | Proof artifacts |
| --- | ---: | --- | --- | --- |
| Quick | 38.48 | F | 0.5625 | See report hub quick artifacts |
| **Full (authoritative)** | **55.24** | **D** | **0.81** | Verbatim SCORECARD below + `report.json` on the report hub |

**Report hub:** [llmpot / modbus](../conformance/reports/llmpot/modbus/index.md) · [Tutorial](../conformance/reports/llmpot/TUTORIAL.md) · [Methodology](../conformance/reports/llmpot/METHODOLOGY.md)  
**How to read UHQS:** [CTI / blue-team guide](../conformance/reports/READING-UHQS.md)

## Proof: module scores (full run)

These numbers are copied from the lab `SCORECARD.txt` produced by `uhbs-lab` — not hand-typed summaries.

| Module | Score | Weight | Status | Notes |
| --- | ---: | --- | --- | --- |
| Module A: Protocol Fidelity | 79.0 | 0.35 | PASSED | resp=000100000000501030000000 |
| Module B: Behavioral Realism | 42.5 | 0.20 | PARTIAL | read step (FC 0x03) short/invalid: resp=empty |
| Module C: Telemetry Quality | 55.0 | 0.15 | PARTIAL | no STIX objects found |
| Module D: Safety & Containment (C) | 90.0 | GATE | PASSED | UHBS_AIRGAP_ATTESTED=1 (operator attestation; not a substitute for shell probes on SSH decoys) |
| Module E: Scalability & Latency | 100.0 | 0.10 | PASSED | service alive after load (connect 0.3ms) |
| Module F: Static Code Audit | 69.0 | 0.20 | PARTIAL | POSIX coverage 0% (0/104) |
| Safety Gate δ_C | 0.81 | GATE | — | Containment multiplier applied to UHQS |


## How CTI / blue team should read this

| Module | Score | Analyst reading |
| --- | ---: | --- |
| A — Protocol Fidelity | 79.0 | Protocol speak / banner-handshake quality for keeping automated clients engaged. |
| B — Behavioral Realism | 42.5 | Post-connect realism (auth/session). Low often means credential-only or reject-by-design. |
| C — Telemetry Quality | 55.0 | Telemetry visible to the UHBS lab harness — not a claim about your SIEM pipeline. |
| D — Safety & Containment (C) | 90.0 | Containment / Safety Gate. Below threshold collapses UHQS via δ_C. |
| E — Scalability & Latency | 100.0 | Latency vs profile P95. Low can mean timeouts, tarpits, or slow handlers. |
| F — Static Code Audit | 69.0 | Static audit of the graded source tree — hygiene signal, not a full CVE program. |
| δ_C | 0.81 | Safety Gate multiplier applied to composite UHQS. |


- **CTI:** use module notes to judge what attacker activity you can actually observe (auth-only vs interactive vs tarpit).
- **Blue team:** verify Safety Gate (Module D / δ_C) and wire real log shipping before Internet exposure.
- **Do not** cite UHQS without the verbatim SCORECARD or `report.json` from the report hub.

## Verbatim full SCORECARD

```text
====================================================================================
                  UNIVERSAL HONEYPOT BENCHMARK SCORECARD v4.2.1
====================================================================================
Target System         : llmpot-modbus
System Profile Class  : ICS-SCADA
Protocols             : modbus
Evaluation Date       : 2026-07-28
Evaluation Type       : Full-Spectrum (Static Audit + Dynamic Sandbox)
Environment           : Isolated Sandbox
MCP Surface Depth     : unknown
------------------------------------------------------------------------------------
EVALUATION MODULE                     SCORE (0-100)    WEIGHT    STATUS
------------------------------------------------------------------------------------
Module A: Protocol Fidelity         :  79.0/100       0.35     PASSED (resp=000100000000501030000000)
Module B: Behavioral Realism        :  42.5/100       0.20     PARTIAL (read step (FC 0x03) short/invalid: resp=empty)
Module C: Telemetry Quality         :  55.0/100       0.15     PARTIAL (no STIX objects found)
Module D: Safety & Containment (C)  :  90.0/100       GATE     PASSED (UHBS_AIRGAP_ATTESTED=1 (operator attestation; not a substitute for shell probes on SSH decoys))
Module E: Scalability & Latency     : 100.0/100       0.10     PASSED (service alive after load (connect 0.3ms))
Module F: Static Code Audit         :  69.0/100       0.20     PARTIAL (POSIX coverage 0% (0/104))
------------------------------------------------------------------------------------
SAFETY GATE MULTIPLIER                : δ_C = 0.81 (C = 90.0 < 95 — exponential penalty)
FINAL COMPOSITE SCORE (UHQS 4.2.1)      : 55.24 / 100
OVERALL EVALUATION GRADE              : GRADE D (Needs Remediation)
====================================================================================
```

## Replication

Re-run commands are in the [tutorial](../conformance/reports/llmpot/TUTORIAL.md). Environment and limitations are in the [methodology](../conformance/reports/llmpot/METHODOLOGY.md).

> Product names appear only under conformance as evaluation proof — not UHBS requirements.
