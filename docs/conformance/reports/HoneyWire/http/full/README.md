# HoneyWire / http — full artifacts

**UHQS 45.84 / F** · UHBS v4.4.1 · δ_C=0.5625

This page is the human-readable landing for the UHBS-Lab run artifacts. The authoritative proof is the verbatim scorecard below (same bytes as `SCORECARD.txt`).

## Module scores

| Module | Score | Weight | Status | Notes |
| --- | ---: | --- | --- | --- |
| Module A: Protocol Fidelity | 100.0 | 0.25 | PASSED | fsm=100 nego=100 timing=100 |
| Module B: Behavioral Realism | 82.5 | 0.20 | PASSED | survived binary blast |
| Module C: Telemetry Quality | 55.0 | 0.20 | PARTIAL | no STIX objects found |
| Module D: Safety & Containment (C) | 75.0 | GATE | PASSED | UHBS_AIRGAP_ATTESTED=1 (operator attestation; not a substitute for shell probes on SSH decoys) |
| Module E: Scalability & Latency | 100.0 | 0.15 | PASSED | service alive after load |
| Module F: Static Code Audit | 70.0 | 0.20 | PASSED | POSIX coverage 0% (0/104) |
| Safety Gate δ_C | 0.5625 | GATE | — | Containment multiplier |

## Verbatim SCORECARD.txt

```text
====================================================================================
                  UNIVERSAL HONEYPOT BENCHMARK SCORECARD v4.4.1
====================================================================================
Target System         : HoneyWire-http
System Profile Class  : Web-API
Protocols             : http
Evaluation Date       : 2026-07-29
Evaluation Type       : Full-Spectrum (Static Audit + Dynamic Sandbox)
Environment           : Isolated Sandbox
MCP Surface Depth     : unknown
------------------------------------------------------------------------------------
EVALUATION MODULE                     SCORE (0-100)    WEIGHT    STATUS
------------------------------------------------------------------------------------
Module A: Protocol Fidelity         : 100.0/100       0.25     PASSED (fsm=100 nego=100 timing=100)
Module B: Behavioral Realism        :  82.5/100       0.20     PASSED (survived binary blast)
Module C: Telemetry Quality         :  55.0/100       0.20     PARTIAL (no STIX objects found)
Module D: Safety & Containment (C)  :  75.0/100       GATE     PASSED (UHBS_AIRGAP_ATTESTED=1 (operator attestation; not a substitute for shell probes on SSH decoys))
Module E: Scalability & Latency     : 100.0/100       0.15     PASSED (service alive after load (connect 0.0ms))
Module F: Static Code Audit         :  70.0/100       0.20     PASSED (POSIX coverage 0% (0/104))
------------------------------------------------------------------------------------
SAFETY GATE MULTIPLIER                : δ_C = 0.5625 (C = 75.0 < 95 — exponential penalty)
FINAL COMPOSITE SCORE (UHQS 4.4.1)      : 45.84 / 100
OVERALL EVALUATION GRADE              : GRADE F (Fail)
====================================================================================
```

## Files in this directory

- [`SCORECARD.txt`](SCORECARD.txt) — human-readable UHBS scorecard (source of the table above)
- [`report.json`](report.json) — machine-readable checks / evidence
- [`MANIFEST.json`](MANIFEST.json) — run manifest
- [`REPORT.txt`](REPORT.txt) — text report twin of the scorecard
- [`uhbs-run.log`](uhbs-run.log) — harness log

Parent protocol hub: [`../index.md`](../index.md)

