# datatrap / mysql — quick artifacts

**UHQS 40.35 / F** · UHBS v4.2.2 · δ_C=0.5625

This page is the human-readable landing for the UHBS-Lab run artifacts. The authoritative proof is the verbatim scorecard below (same bytes as `SCORECARD.txt`).

## Module scores

| Module | Score | Weight | Status | Notes |
| --- | ---: | --- | --- | --- |
| Safety Gate δ_C | 0.5625 | GATE | — | Containment multiplier |

## Verbatim SCORECARD.txt

```text
====================================================================================
                  UNIVERSAL HONEYPOT BENCHMARK SCORECARD v4.2.1
====================================================================================
Target System         : datatrap-mysql
System Profile Class  : Low-Interaction
Protocols             : mysql
Evaluation Date       : 2026-07-28
Evaluation Type       : Full-Spectrum (Static Audit + Dynamic Sandbox)
Environment           : Quick Docker lab: datatrap-mysql
------------------------------------------------------------------------------------
EVALUATION MODULE                     SCORE (0-100)    WEIGHT    STATUS
------------------------------------------------------------------------------------
Module A: Protocol Fidelity         :  92.0/100       0.30
Module B: Behavioral Realism        :  42.5/100       0.15
Module C: Telemetry Quality         :  55.0/100       0.25
Module D: Safety & Containment (C)  :  75.0/100       GATE
Module E: Scalability & Latency     :  100.0/100       0.10
Module F: Static Code Audit         :  70.0/100       0.20
------------------------------------------------------------------------------------
SAFETY GATE MULTIPLIER                : δ_C = 0.5625 (C = 75.0)
FINAL COMPOSITE SCORE (UHQS 4.2.1)      : 40.35 / 100
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

## Analyst note

This artifact folder is the **proof bundle** for one UHBS run (quick or full). Open `SCORECARD.txt` for the verbatim module table and UHQS; use `report.json` for automation. Prefer the sibling **full** folder when making operational comparisons. See the protocol hub and [READING-UHQS.md](../../../READING-UHQS.md) for CTI / blue-team interpretation. Do not cite the letter grade without the SCORECARD body.
