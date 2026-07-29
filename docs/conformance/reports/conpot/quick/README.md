# reports / conpot — quick artifacts

**UHQS 44.55 / F** · UHBS v4.2.2 · δ_C=0.5625

This page is the human-readable landing for the UHBS-Lab run artifacts. The authoritative proof is the verbatim scorecard below (same bytes as `SCORECARD.txt`).

## Module scores

| Module | Score | Weight | Status | Notes |
| --- | ---: | --- | --- | --- |
| Module A: Protocol Fidelity | 79.0 | 0.35 | PASSED | resp=000100000003018302 |
| Module B: Behavioral Realism | 42.5 | 0.20 | PARTIAL | write step (FC 0x06) failed/unacknowledged: resp=000200000003018602 |
| Module C: Telemetry Quality | 100.0 | 0.15 | PASSED | telemetry_dir missing — set TPS/inventory telemetry_dir for C1 schema gates |
| Module D: Safety & Containment (C) | 75.0 | GATE | PASSED | UHBS_AIRGAP_ATTESTED=1 (operator attestation; not a substitute for shell probes on SSH decoys) |
| Module E: Scalability & Latency | 100.0 | 0.10 | PASSED | service alive after load (connect 12.1ms) |
| Module F: Static Code Audit | 90.3 | 0.20 | PASSED | 2 static private keys: conpot/templates/default/ssl/ssl.key, conpot/templates/kamstrup_382/ssl/ssl.key |
| Safety Gate δ_C | 0.5625 | GATE | — | Containment multiplier |

## Verbatim SCORECARD.txt

```text
====================================================================================
                  UNIVERSAL HONEYPOT BENCHMARK SCORECARD v4.0.1
====================================================================================
Target System         : ICS-Modbus-Decoy
System Profile Class  : ICS-SCADA
Protocols             : modbus
Evaluation Date       : 2026-07-27
Evaluation Type       : Full-Spectrum (Static Audit + Dynamic Sandbox)
Environment           : Isolated Sandbox
------------------------------------------------------------------------------------
EVALUATION MODULE                     SCORE (0-100)    WEIGHT    STATUS
------------------------------------------------------------------------------------
Module A: Protocol Fidelity         :  79.0/100       0.35     PASSED (resp=000100000003018302)
Module B: Behavioral Realism        :  42.5/100       0.20     PARTIAL (write step (FC 0x06) failed/unacknowledged: resp=000200000003018602)
Module C: Telemetry Quality         : 100.0/100       0.15     PASSED (telemetry_dir missing — set TPS/inventory telemetry_dir for C1 schema gates)
Module D: Safety & Containment (C)  :  75.0/100       GATE     PASSED (UHBS_AIRGAP_ATTESTED=1 (operator attestation; not a substitute for shell probes on SSH decoys))
Module E: Scalability & Latency     : 100.0/100       0.10     PASSED (service alive after load (connect 12.1ms))
Module F: Static Code Audit         :  90.3/100       0.20     PASSED (2 static private keys: conpot/templates/default/ssl/ssl.key, conpot/templates/kamstrup_382/ssl/ssl.key)
------------------------------------------------------------------------------------
SAFETY GATE MULTIPLIER                : δ_C = 0.5625 (C = 75.0 < 95 — exponential penalty)
FINAL COMPOSITE SCORE (UHQS 4.0.1)      : 44.55 / 100
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

