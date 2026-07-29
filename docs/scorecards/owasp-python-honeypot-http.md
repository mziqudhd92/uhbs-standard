# Scorecard: OWASP Python-Honeypot — http

**Status:** Informative · evaluation proof (not an endorsement)  
**UHBS:** **4.2.2** · **Class:** Web-API · **Protocol / surface:** `http`  
**Target id (lab):** `owasp-python-honeypot-http` · **Evaluation date:** 2026-07-29

| Run | UHQS | Grade | δ_C | Proof artifacts |
| --- | ---: | --- | --- | --- |
| Quick | 43.98 | F | 0.5625 | See report hub quick artifacts |
| **Full (authoritative)** | **43.98** | **F** | **0.5625** | Verbatim SCORECARD below + `report.json` on the report hub |

**Report hub:** [OWASP Python-Honeypot / http](../conformance/reports/owasp-python-honeypot/http/index.md) · [Tutorial](../conformance/reports/owasp-python-honeypot/TUTORIAL.md) · [Methodology](../conformance/reports/owasp-python-honeypot/METHODOLOGY.md)  
**How to read UHQS:** [CTI / blue-team guide](../conformance/reports/READING-UHQS.md)

## Proof: module scores (full run)

| Module | Score | Weight | Status | Notes |
| --- | ---: | --- | --- | --- |
| Module A: Protocol Fidelity | 86.8 | 0.25 | PASSED | status=401 (want 400/505 or close) |
| Module B: Behavioral Realism | 82.5 | 0.20 | PASSED | survived binary blast |
| Module C: Telemetry Quality | 55.0 | 0.20 | PARTIAL | no STIX objects found |
| Module D: Safety & Containment (C) | 75.0 | GATE | PASSED | UHBS_AIRGAP_ATTESTED=1 |
| Module E: Scalability & Latency | 100.0 | 0.15 | PASSED | service alive after load |
| Module F: Static Code Audit | 70.0 | 0.20 | PASSED | POSIX coverage 0% (0/104) |
| Safety Gate δ_C | 0.5625 | GATE | — | Containment multiplier |

## Verbatim full SCORECARD

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

> Product names appear only under conformance as evaluation proof — not UHBS requirements.

## How CTI / blue team should read this

- Prefer the **full** SCORECARD over quick for operational decisions.
- Check **δ_C** carefully — values below 1.0 mean the Safety Gate reduced composite UHQS.
- Module C is harness visibility, not your SIEM pipeline; wire log shipping yourself.
- See [READING-UHQS.md](../conformance/reports/READING-UHQS.md) for module A–F interpretation.
