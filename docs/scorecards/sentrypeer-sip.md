# Scorecard: sentrypeer — sip

**Status:** Informative · evaluation proof  
**Class:** Low-Interaction · **Protocol:** `sip`  
**Full UHQS:** **43.38** · Grade **F** · δ_C **0.5625**  
**Quick UHQS:** 43.38 / F  
**Evaluated:** 2026-07-29 · **UHBS:** 4.2.2

Source report: [`../conformance/reports/sentrypeer/sip/`](../conformance/reports/sentrypeer/sip/index.md)

## Module breakdown (full run)

| Module | Score | Weight | Status | Notes |
| --- | ---: | --- | --- | --- |
| Module A: Protocol Fidelity | 100.0 | 0.30 | PASSED | fsm=100 nego=100 timing=100 |
| Module B: Behavioral Realism | 62.5 | 0.15 | PARTIAL | udp sent resp=b'' |
| Module C: Telemetry Quality | 55.0 | 0.25 | PARTIAL | no STIX objects found |
| Module D: Safety & Containment (C) | 75.0 | GATE | PASSED | UHBS_AIRGAP_ATTESTED=1 (operator attestation; not a substitute for shell probes on SSH decoys) |
| Module E: Scalability & Latency | 100.0 | 0.10 | PASSED | service alive after load (connect 3.2ms) |
| Module F: Static Code Audit | 70.0 | 0.20 | PASSED | POSIX coverage 0% (0/104) |
| Safety Gate δ_C | 0.5625 | GATE | — | Containment multiplier |


## Verbatim full SCORECARD

```text
====================================================================================
                  UNIVERSAL HONEYPOT BENCHMARK SCORECARD v4.2.2
====================================================================================
Target System         : sentrypeer-sip
System Profile Class  : Low-Interaction
Protocols             : sip
Evaluation Date       : 2026-07-29
Evaluation Type       : Full-Spectrum (Static Audit + Dynamic Sandbox)
Environment           : Isolated Sandbox
MCP Surface Depth     : unknown
------------------------------------------------------------------------------------
EVALUATION MODULE                     SCORE (0-100)    WEIGHT    STATUS
------------------------------------------------------------------------------------
Module A: Protocol Fidelity         : 100.0/100       0.30     PASSED (fsm=100 nego=100 timing=100)
Module B: Behavioral Realism        :  62.5/100       0.15     PARTIAL (udp sent resp=b'')
Module C: Telemetry Quality         :  55.0/100       0.25     PARTIAL (no STIX objects found)
Module D: Safety & Containment (C)  :  75.0/100       GATE     PASSED (UHBS_AIRGAP_ATTESTED=1 (operator attestation; not a substitute for shell probes on SSH decoys))
Module E: Scalability & Latency     : 100.0/100       0.10     PASSED (service alive after load (connect 3.2ms))
Module F: Static Code Audit         :  70.0/100       0.20     PASSED (POSIX coverage 0% (0/104))
------------------------------------------------------------------------------------
SAFETY GATE MULTIPLIER                : δ_C = 0.5625 (C = 75.0 < 95 — exponential penalty)
FINAL COMPOSITE SCORE (UHQS 4.2.2)      : 43.38 / 100
OVERALL EVALUATION GRADE              : GRADE F (Fail)
====================================================================================
```


## Replication

See the report [tutorial](../conformance/reports/sentrypeer/TUTORIAL.md) and [methodology](../conformance/reports/sentrypeer/METHODOLOGY.md).

> Product names appear only under conformance as evaluation proof — not UHBS requirements.
