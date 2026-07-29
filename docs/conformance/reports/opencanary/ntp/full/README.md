# opencanary / ntp — full artifacts

**UHQS 47.42 / F** · UHBS v4.2.2 · δ_C=0.81

This page is the human-readable landing for the UHBS-Lab run artifacts. The authoritative proof is the verbatim scorecard below (same bytes as `SCORECARD.txt`).

## Module scores

| Module | Score | Weight | Status | Notes |
| --- | ---: | --- | --- | --- |
| Module A: Protocol Fidelity | 55.7 | 0.30 | PARTIAL | fsm=60 nego=35 timing=71 |
| Module B: Behavioral Realism | 70.5 | 0.15 | PASSED | udp sent resp=b'' |
| Module C: Telemetry Quality | 55.0 | 0.25 | PARTIAL | no STIX objects found |
| Module D: Safety & Containment (C) | 90.0 | GATE | PASSED | UHBS_AIRGAP_ATTESTED=1 (operator attestation; not a substitute for shell probes on SSH decoys) |
| Module E: Scalability & Latency | 35.0 | 0.10 | PARTIAL | P50=1504.2ms P95=1509.0ms P99=1510.3ms TPS_limit=150.0ms proto=ntp |
| Module F: Static Code Audit | 70.0 | 0.20 | PASSED | bandit HIGH=21 |
| Safety Gate δ_C | 0.81 | GATE | — | Containment multiplier |

## Verbatim SCORECARD.txt

```text
====================================================================================
                  UNIVERSAL HONEYPOT BENCHMARK SCORECARD v4.0.1
====================================================================================
Target System         : opencanary-ntp
System Profile Class  : Low-Interaction
Protocols             : ntp
Evaluation Date       : 2026-07-27
Evaluation Type       : Full-Spectrum (Static Audit + Dynamic Sandbox)
Environment           : Isolated Sandbox
------------------------------------------------------------------------------------
EVALUATION MODULE                     SCORE (0-100)    WEIGHT    STATUS
------------------------------------------------------------------------------------
Module A: Protocol Fidelity         :  55.7/100       0.30     PARTIAL (fsm=60 nego=35 timing=71)
Module B: Behavioral Realism        :  70.5/100       0.15     PASSED (udp sent resp=b'')
Module C: Telemetry Quality         :  55.0/100       0.25     PARTIAL (no STIX objects found)
Module D: Safety & Containment (C)  :  90.0/100       GATE     PASSED (UHBS_AIRGAP_ATTESTED=1 (operator attestation; not a substitute for shell probes on SSH decoys))
Module E: Scalability & Latency     :  35.0/100       0.10     PARTIAL (P50=1504.2ms P95=1509.0ms P99=1510.3ms TPS_limit=150.0ms proto=ntp)
Module F: Static Code Audit         :  70.0/100       0.20     PASSED (bandit HIGH=21)
------------------------------------------------------------------------------------
SAFETY GATE MULTIPLIER                : δ_C = 0.81 (C = 90.0 < 95 — exponential penalty)
FINAL COMPOSITE SCORE (UHQS 4.0.1)      : 47.42 / 100
OVERALL EVALUATION GRADE              : GRADE F (Fail)
====================================================================================
```

## Files in this directory

- [`SCORECARD.txt`](SCORECARD.txt) — human-readable UHBS scorecard (source of the table above)
- [`report.json`](report.json) — machine-readable checks / evidence
- [`MANIFEST.json`](MANIFEST.json) — run manifest
- [`REPORT.txt`](REPORT.txt) — text report twin of the scorecard

Parent protocol hub: [`../index.md`](../index.md)

