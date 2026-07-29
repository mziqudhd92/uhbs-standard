# Scorecard: mysql-honeypotd — mysql

**Status:** Informative · evaluation proof  
**Class:** Low-Interaction · **Protocol:** `mysql`  
**Full UHQS:** **37.94** · Grade **F** · δ_C **0.5625**  
**Quick UHQS:** 40.35 / F  
**Evaluated:** 2026-07-29 · **UHBS:** 4.2.2

Source report: [`../conformance/reports/mysql-honeypotd/mysql/`](../conformance/reports/mysql-honeypotd/mysql/index.md)

## Module breakdown (full run)

| Module | Score | Weight | Status | Notes |
| --- | ---: | --- | --- | --- |
| Module A: Protocol Fidelity | 78.4 | 0.30 | PASSED | median=0.080ms pstdev=2.856ms (target jitter often <2ms vs native) |
| Module B: Behavioral Realism | 42.5 | 0.15 | PARTIAL |  |
| Module C: Telemetry Quality | 55.0 | 0.25 | PARTIAL | no STIX objects found |
| Module D: Safety & Containment (C) | 75.0 | GATE | PASSED | UHBS_AIRGAP_ATTESTED=1 (operator attestation; not a substitute for shell probes on SSH decoys) |
| Module E: Scalability & Latency | 100.0 | 0.10 | PASSED | service alive after load (connect 0.1ms) |
| Module F: Static Code Audit | 69.0 | 0.20 | PARTIAL | POSIX coverage 0% (0/104) |
| Safety Gate δ_C | 0.5625 | GATE | — | Containment multiplier |


## Verbatim full SCORECARD

```text
====================================================================================
                  UNIVERSAL HONEYPOT BENCHMARK SCORECARD v4.2.2
====================================================================================
Target System         : mysql-honeypotd
System Profile Class  : Low-Interaction
Protocols             : mysql
Evaluation Date       : 2026-07-29
Evaluation Type       : Full-Spectrum (Static Audit + Dynamic Sandbox)
Environment           : Isolated Sandbox
MCP Surface Depth     : unknown
------------------------------------------------------------------------------------
EVALUATION MODULE                     SCORE (0-100)    WEIGHT    STATUS
------------------------------------------------------------------------------------
Module A: Protocol Fidelity         :  78.4/100       0.30     PASSED (median=0.080ms pstdev=2.856ms (target jitter often <2ms vs native))
Module B: Behavioral Realism        :  42.5/100       0.15     PARTIAL (J
8.0.19�e68�pIf���!��V:������mysql_native_password!��#08S01Got packets out of order)
Module C: Telemetry Quality         :  55.0/100       0.25     PARTIAL (no STIX objects found)
Module D: Safety & Containment (C)  :  75.0/100       GATE     PASSED (UHBS_AIRGAP_ATTESTED=1 (operator attestation; not a substitute for shell probes on SSH decoys))
Module E: Scalability & Latency     : 100.0/100       0.10     PASSED (service alive after load (connect 0.1ms))
Module F: Static Code Audit         :  69.0/100       0.20     PARTIAL (POSIX coverage 0% (0/104))
------------------------------------------------------------------------------------
SAFETY GATE MULTIPLIER                : δ_C = 0.5625 (C = 75.0 < 95 — exponential penalty)
FINAL COMPOSITE SCORE (UHQS 4.2.2)      : 37.94 / 100
OVERALL EVALUATION GRADE              : GRADE F (Fail)
====================================================================================
```


## Replication

See the report [tutorial](../conformance/reports/mysql-honeypotd/TUTORIAL.md) and [methodology](../conformance/reports/mysql-honeypotd/METHODOLOGY.md).

> Product names appear only under conformance as evaluation proof — not UHBS requirements.
