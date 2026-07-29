# owasp-python-honeypot / http — full artifacts

**UHQS 43.98 / F** · UHBS v4.2.2 · δ_C=0.5625

This page is the human-readable landing for the UHBS-Lab run artifacts. The authoritative proof is the verbatim scorecard below (same bytes as `SCORECARD.txt`).

## Verbatim SCORECARD.txt

```text
====================================================================================
                  UNIVERSAL HONEYPOT BENCHMARK SCORECARD v4.2.2
====================================================================================
Target System         : owasp-python-honeypot-http
System Profile Class  : Web-API
Protocols             : http
Evaluation Date       : 2026-07-29
Evaluation Type       : Full-Spectrum (Static Audit + Dynamic Sandbox)
Environment           : Isolated Sandbox
MCP Surface Depth     : unknown
------------------------------------------------------------------------------------
EVALUATION MODULE                     SCORE (0-100)    WEIGHT    STATUS
------------------------------------------------------------------------------------
Module A: Protocol Fidelity         :  86.8/100       0.25     PASSED (status=401 (want 400/505 or close))
Module B: Behavioral Realism        :  82.5/100       0.20     PASSED (survived binary blast)
Module C: Telemetry Quality         :  55.0/100       0.20     PARTIAL (no STIX objects found)
Module D: Safety & Containment (C)  :  75.0/100       GATE     PASSED (UHBS_AIRGAP_ATTESTED=1 (operator attestation; not a substitute for shell probes on SSH decoys))
Module E: Scalability & Latency     : 100.0/100       0.15     PASSED (service alive after load (connect 0.1ms))
Module F: Static Code Audit         :  70.0/100       0.20     PASSED (POSIX coverage 0% (0/104))
------------------------------------------------------------------------------------
SAFETY GATE MULTIPLIER                : δ_C = 0.5625 (C = 75.0 < 95 — exponential penalty)
FINAL COMPOSITE SCORE (UHQS 4.2.2)      : 43.98 / 100
OVERALL EVALUATION GRADE              : GRADE F (Fail)
====================================================================================
```

## Files in this directory

- [`SCORECARD.txt`](SCORECARD.txt) — human-readable UHBS scorecard
- [`report.json`](report.json) — machine-readable checks / evidence
- [`MANIFEST.json`](MANIFEST.json) — run manifest
- [`REPORT.txt`](REPORT.txt) — text report twin of the scorecard

Parent protocol hub: [`../index.md`](../index.md)

## Analyst note

This artifact folder is the **proof bundle** for one UHBS run. Open `SCORECARD.txt` for the verbatim module table and UHQS; use `report.json` for automation. Prefer the sibling **full** folder for operational comparisons. See the protocol hub and [READING-UHQS.md](../../../READING-UHQS.md) for CTI / blue-team interpretation. Do not cite the letter grade without the SCORECARD body. UHBS 4.2.2 proof is informative evaluation evidence — not an endorsement.
