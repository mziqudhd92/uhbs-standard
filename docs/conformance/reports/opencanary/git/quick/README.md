# opencanary / git — quick artifacts

**UHQS 51.48 / D** · UHBS v4.2.2 · δ_C=0.5625

This page is the human-readable landing for the UHBS-Lab run artifacts. The authoritative proof is the verbatim scorecard below (same bytes as `SCORECARD.txt`).

## Module scores

| Module | Score | Weight | Status | Notes |
| --- | ---: | --- | --- | --- |
| Module A: Protocol Fidelity | 92.0 | 0.30 | PASSED | fsm=80 nego=100 timing=100 |
| Module B: Behavioral Realism | 82.5 | 0.15 | PASSED | survived binary blast |
| Module C: Telemetry Quality | 100.0 | 0.25 | PASSED | telemetry_dir missing — set TPS/inventory telemetry_dir for C1 schema gates |
| Module D: Safety & Containment (C) | 75.0 | GATE | PASSED | UHBS_AIRGAP_ATTESTED=1 (operator attestation; not a substitute for shell probes on SSH decoys) |
| Module E: Scalability & Latency | 100.0 | 0.10 | PASSED | service alive after load (connect 0.5ms) |
| Module F: Static Code Audit | 82.7 | 0.20 | PASSED | sleep/blocking markers in non-test code≈0 |
| Safety Gate δ_C | 0.5625 | GATE | — | Containment multiplier |

## Verbatim SCORECARD.txt

```text
====================================================================================
                  UNIVERSAL HONEYPOT BENCHMARK SCORECARD v4.0.1
====================================================================================
Target System         : opencanary-git
System Profile Class  : Low-Interaction
Protocols             : git
Evaluation Date       : 2026-07-27
Evaluation Type       : Full-Spectrum (Static Audit + Dynamic Sandbox)
Environment           : Isolated Sandbox
------------------------------------------------------------------------------------
EVALUATION MODULE                     SCORE (0-100)    WEIGHT    STATUS
------------------------------------------------------------------------------------
Module A: Protocol Fidelity         :  92.0/100       0.30     PASSED (fsm=80 nego=100 timing=100)
Module B: Behavioral Realism        :  82.5/100       0.15     PASSED (survived binary blast)
Module C: Telemetry Quality         : 100.0/100       0.25     PASSED (telemetry_dir missing — set TPS/inventory telemetry_dir for C1 schema gates)
Module D: Safety & Containment (C)  :  75.0/100       GATE     PASSED (UHBS_AIRGAP_ATTESTED=1 (operator attestation; not a substitute for shell probes on SSH decoys))
Module E: Scalability & Latency     : 100.0/100       0.10     PASSED (service alive after load (connect 0.5ms))
Module F: Static Code Audit         :  82.7/100       0.20     PASSED (sleep/blocking markers in non-test code≈0)
------------------------------------------------------------------------------------
SAFETY GATE MULTIPLIER                : δ_C = 0.5625 (C = 75.0 < 95 — exponential penalty)
FINAL COMPOSITE SCORE (UHQS 4.0.1)      : 51.48 / 100
OVERALL EVALUATION GRADE              : GRADE D (Needs Remediation)
====================================================================================
```

## Files in this directory

- [`SCORECARD.txt`](SCORECARD.txt) — human-readable UHBS scorecard (source of the table above)
- [`report.json`](report.json) — machine-readable checks / evidence
- [`MANIFEST.json`](MANIFEST.json) — run manifest
- [`REPORT.txt`](REPORT.txt) — text report twin of the scorecard

Parent protocol hub: [`../index.md`](../index.md)

