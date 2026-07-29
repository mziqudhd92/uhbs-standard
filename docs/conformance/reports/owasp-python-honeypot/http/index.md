# OWASP Python-Honeypot — HTTP

**Status:** Informative · evaluation proof  
**UHBS:** v4.2.2 · **Class:** Web-API · **Protocol:** `http`  
**Target id:** `owasp-python-honeypot-http` · **Evaluated:** 2026-07-29

| Run | UHQS | Grade | δ_C | Artifacts |
| --- | ---: | --- | --- | --- |
| [Quick](quick/README.md) | **43.98** | F | 0.5625 | [`SCORECARD.txt`](quick/SCORECARD.txt) · [`report.json`](quick/report.json) |
| [Full](full/README.md) | **43.98** | F | 0.5625 | [`SCORECARD.txt`](full/SCORECARD.txt) · [`report.json`](full/report.json) |

## Full run — module breakdown (analyst view)

| Module | Score | Weight | Status | Notes |
| --- | ---: | --- | --- | --- |
| Module A: Protocol Fidelity | 86.8 | 0.25 | PASSED | status=401 (want 400/505 or close) |
| Module B: Behavioral Realism | 82.5 | 0.20 | PASSED | survived binary blast |
| Module C: Telemetry Quality | 55.0 | 0.20 | PARTIAL | no STIX objects found |
| Module D: Safety & Containment (C) | 75.0 | GATE | PASSED | UHBS_AIRGAP_ATTESTED=1 (operator attestation; not a substitute for shell probes on SSH decoys) |
| Module E: Scalability & Latency | 100.0 | 0.15 | PASSED | service alive after load (connect 0.1ms) |
| Module F: Static Code Audit | 70.0 | 0.20 | PASSED | POSIX coverage 0% (0/104) |
| Safety Gate δ_C | 0.5625 | GATE | — | Containment multiplier |

## Full scorecard (verbatim)

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

## CTI & blue-team reading

This page is the protocol-level proof hub for **OWASP Python-Honeypot** on **http**. Prefer the **full** run over quick for operational decisions. Numbers without the verbatim SCORECARD (or `report.json`) are not trustworthy citations.

### Module interpretation (this protocol)

| Module | Score | Analyst reading |
| --- | ---: | --- |
| A — Protocol Fidelity | 86.8 | HTTP basic-auth challenge (401) keeps scanners engaged; not a full app emulator. |
| B — Behavioral Realism | 82.5 | Survived binary blast; weak-password module is auth-gated, not multi-page CMS realism. |
| C — Telemetry Quality | 55.0 | Harness saw no STIX-shaped exports — wire Apache/access logs yourself for CTI. |
| D — Safety & Containment (C) | 75.0 | Air-gap attestation only; δ_C penalty applies (C < 95). |
| E — Scalability & Latency | 100.0 | Lightweight Apache container stayed responsive under lab load. |
| F — Static Code Audit | 70.0 | Static pass over upstream tree; POSIX shell coverage still 0% by design. |
| δ_C | 0.5625 | Safety Gate multiplier applied to composite UHQS. |

- **CTI:** use Module A/B to judge engagement depth (scanner noise vs post-auth TTPs). Low B usually means credential/connection intelligence, not interactive malware staging.
- **Blue team:** verify Safety Gate (Module D / δ_C) before Internet exposure; wire SIEM shipping yourself — Module C is harness visibility, not your pipeline.
- **Replication:** commands live in the product tutorial; environment limits in the methodology.

## Guides

- Product hub: [`../`](../index.md)
- [Tutorial](../TUTORIAL.md)
- [Methodology](../METHODOLOGY.md)
- Published scorecard page: [`../../../../scorecards/owasp-python-honeypot-http.md`](../../../../scorecards/owasp-python-honeypot-http.md)
- How to read UHQS: [READING-UHQS.md](../../READING-UHQS.md)

> Named products appear only under conformance as evaluation proof — not UHBS requirements or endorsements.
