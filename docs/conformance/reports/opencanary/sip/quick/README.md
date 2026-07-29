# opencanary / sip — quick artifacts

**UHQS 40.01 / F** · UHBS v4.2.2 · δ_C=0.5625

This page is the human-readable landing for the UHBS-Lab run artifacts. The authoritative proof is the verbatim scorecard below (same bytes as `SCORECARD.txt`).

## Module scores

| Module | Score | Weight | Status | Notes |
| --- | ---: | --- | --- | --- |
| Module A: Protocol Fidelity | 55.7 | 0.30 | PARTIAL | fsm=60 nego=35 timing=71 |
| Module B: Behavioral Realism | 62.5 | 0.15 | PARTIAL | udp sent resp=b'' |
| Module C: Telemetry Quality | 100.0 | 0.25 | PASSED | telemetry_dir missing — set TPS/inventory telemetry_dir for C1 schema gates |
| Module D: Safety & Containment (C) | 75.0 | GATE | PASSED | UHBS_AIRGAP_ATTESTED=1 (operator attestation; not a substitute for shell probes on SSH decoys) |
| Module E: Scalability & Latency | 35.0 | 0.10 | PARTIAL | P50=1510.2ms P95=1517.8ms P99=1519.3ms TPS_limit=150.0ms proto=sip |
| Module F: Static Code Audit | 82.7 | 0.20 | PASSED | sleep/blocking markers in non-test code≈0 |
| Safety Gate δ_C | 0.5625 | GATE | — | Containment multiplier |

## Verbatim SCORECARD.txt

```text
====================================================================================
                  UNIVERSAL HONEYPOT BENCHMARK SCORECARD v4.0.1
====================================================================================
Target System         : opencanary-sip
System Profile Class  : Low-Interaction
Protocols             : sip
Evaluation Date       : 2026-07-27
Evaluation Type       : Full-Spectrum (Static Audit + Dynamic Sandbox)
Environment           : Isolated Sandbox
------------------------------------------------------------------------------------
EVALUATION MODULE                     SCORE (0-100)    WEIGHT    STATUS
------------------------------------------------------------------------------------
Module A: Protocol Fidelity         :  55.7/100       0.30     PARTIAL (fsm=60 nego=35 timing=71)
Module B: Behavioral Realism        :  62.5/100       0.15     PARTIAL (udp sent resp=b'')
Module C: Telemetry Quality         : 100.0/100       0.25     PASSED (telemetry_dir missing — set TPS/inventory telemetry_dir for C1 schema gates)
Module D: Safety & Containment (C)  :  75.0/100       GATE     PASSED (UHBS_AIRGAP_ATTESTED=1 (operator attestation; not a substitute for shell probes on SSH decoys))
Module E: Scalability & Latency     :  35.0/100       0.10     PARTIAL (P50=1510.2ms P95=1517.8ms P99=1519.3ms TPS_limit=150.0ms proto=sip)
Module F: Static Code Audit         :  82.7/100       0.20     PASSED (sleep/blocking markers in non-test code≈0)
------------------------------------------------------------------------------------
SAFETY GATE MULTIPLIER                : δ_C = 0.5625 (C = 75.0 < 95 — exponential penalty)
FINAL COMPOSITE SCORE (UHQS 4.0.1)      : 40.01 / 100
OVERALL EVALUATION GRADE              : GRADE F (Fail)
====================================================================================
```

## Files in this directory

- [`SCORECARD.txt`](SCORECARD.txt) — human-readable UHBS scorecard (source of the table above)
- [`report.json`](report.json) — machine-readable checks / evidence
- [`MANIFEST.json`](MANIFEST.json) — run manifest
- [`REPORT.txt`](REPORT.txt) — text report twin of the scorecard

Parent protocol hub: [`../index.md`](../index.md)

