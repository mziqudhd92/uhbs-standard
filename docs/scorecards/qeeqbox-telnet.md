# Scorecard: qeeqbox/honeypots — telnet

**Status:** Informative · evaluation proof  
**Class:** Low-Interaction · **Protocol:** `telnet`  
**Full UHQS:** **29.77** · Grade **F** · δ_C **0.5625**  
**Quick UHQS:** 29.88 / F  
**Evaluated:** 2026-07-29 · **UHBS:** 4.2.2

Source report: [`../conformance/reports/qeeqbox-honeypots/telnet/`](../conformance/reports/qeeqbox-honeypots/telnet/index.md)

## Module breakdown (full run)

| Module | Score | Weight | Status | Notes |
| --- | ---: | --- | --- | --- |
| Module A: Protocol Fidelity | 30.0 | 0.30 | PARTIAL | no IAC (0xFF) byte in response — not real Telnet: recv=b'' |
| Module B: Behavioral Realism | 42.5 | 0.15 | PARTIAL | no IAC / no prompt: b'' |
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
Target System         : qeeqbox-telnet
System Profile Class  : Low-Interaction
Protocols             : telnet
Evaluation Date       : 2026-07-29
Evaluation Type       : Full-Spectrum (Static Audit + Dynamic Sandbox)
Environment           : Isolated Sandbox
MCP Surface Depth     : unknown
------------------------------------------------------------------------------------
EVALUATION MODULE                     SCORE (0-100)    WEIGHT    STATUS
------------------------------------------------------------------------------------
Module A: Protocol Fidelity         :  30.0/100       0.30     PARTIAL (no IAC (0xFF) byte in response — not real Telnet: recv=b'')
Module B: Behavioral Realism        :  42.5/100       0.15     PARTIAL (no IAC / no prompt: b'')
Module C: Telemetry Quality         :  55.0/100       0.25     PARTIAL (no STIX objects found)
Module D: Safety & Containment (C)  :  75.0/100       GATE     PASSED (UHBS_AIRGAP_ATTESTED=1 (operator attestation; not a substitute for shell probes on SSH decoys))
Module E: Scalability & Latency     : 100.0/100       0.10     PASSED (service alive after load (connect 0.1ms))
Module F: Static Code Audit         :  69.0/100       0.20     PARTIAL (POSIX coverage 0% (0/104))
------------------------------------------------------------------------------------
SAFETY GATE MULTIPLIER                : δ_C = 0.5625 (C = 75.0 < 95 — exponential penalty)
FINAL COMPOSITE SCORE (UHQS 4.2.2)      : 29.77 / 100
OVERALL EVALUATION GRADE              : GRADE F (Fail)
====================================================================================
```


## Replication

See [tutorial](../conformance/reports/qeeqbox-honeypots/TUTORIAL.md) and [methodology](../conformance/reports/qeeqbox-honeypots/METHODOLOGY.md).
