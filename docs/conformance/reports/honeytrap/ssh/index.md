# Honeytrap (DutchSec) — SSH

**Status:** Informative · evaluation proof  
**UHBS:** v4.2.2 · **Class:** Low-Interaction · **Protocol:** `ssh`  
**Target id:** `honeytrap-ssh` · **Evaluated:** 2026-07-29

| Run | UHQS | Grade | δ_C | Artifacts |
| --- | ---: | --- | --- | --- |
| [Quick](quick/README.md) | **44.38** | F | 1.0 | [`SCORECARD.txt`](quick/SCORECARD.txt) · [`report.json`](quick/report.json) |
| [Full](full/README.md) | **44.38** | F | 1.0 | [`SCORECARD.txt`](full/SCORECARD.txt) · [`report.json`](full/report.json) |

## Full run — module breakdown (analyst view)

| Module | Score | Weight | Status | Notes |
| --- | ---: | --- | --- | --- |
| Module A: Protocol Fidelity | 70.6 | 0.30 | PASSED |  |
| Module B: Behavioral Realism | 6.2 | 0.15 | PARTIAL |  |
| Module C: Telemetry Quality | 25.0 | 0.25 | PARTIAL |  |
| Module D: Safety & Containment (C) | 96.0 | GATE | PASSED |  |
| Module E: Scalability & Latency | 20.0 | 0.10 | PARTIAL |  |
| Module F: Static Code Audit | 70.0 | 0.20 | PASSED |  |

## Full scorecard (verbatim)

```text
====================================================================================
                  UNIVERSAL HONEYPOT BENCHMARK SCORECARD v4.2.2
====================================================================================
Target System         : honeytrap-ssh
System Profile Class  : Low-Interaction
Protocols             : ssh
Evaluation Date       : 2026-07-29
Evaluation Type       : Full-Spectrum (Static Audit + Dynamic Sandbox)
Environment           : Isolated Sandbox
MCP Surface Depth     : unknown
------------------------------------------------------------------------------------
EVALUATION MODULE                     SCORE (0-100)    WEIGHT    STATUS
------------------------------------------------------------------------------------
Module A: Protocol Fidelity         :  70.6/100       0.30     PASSED (accepted null ID)
Module B: Behavioral Realism        :   6.2/100       0.15     PARTIAL (Incompatible ssh peer (no acceptable host key))
Module C: Telemetry Quality         :  25.0/100       0.25     PARTIAL (Incompatible ssh peer (no acceptable host key))
Module D: Safety & Containment (C)  :  96.0/100       GATE     PASSED (Incompatible ssh peer (no acceptable host key))
Module E: Scalability & Latency     :  20.0/100       0.10     PARTIAL (P50=0.0ms P95=0.0ms P99=0.0ms TPS_limit=3000.0ms proto=ssh)
Module F: Static Code Audit         :  70.0/100       0.20     PASSED (POSIX coverage 0% (0/104))
------------------------------------------------------------------------------------
SAFETY GATE MULTIPLIER                : δ_C = 1.0 (Containment Score C = 96.0 >= 95)
FINAL COMPOSITE SCORE (UHQS 4.2.2)      : 44.38 / 100
OVERALL EVALUATION GRADE              : GRADE F (Fail)
====================================================================================
```

## CTI & blue-team reading

This page is the protocol-level proof hub for **Honeytrap (DutchSec)** on **ssh**. Prefer the **full** run over quick for operational decisions. Numbers without the verbatim SCORECARD (or `report.json`) are not trustworthy citations.

- Honeytrap’s standalone agent exposes an SSH simulator on container port **8022** in this lab; UHBS Module B reflects credential-style interaction rather than a full Cowrie-class shell.
- **CTI:** treat captures as auth and banner intelligence unless you enable higher-interaction directors yourself.
- **Blue team:** stdout logging in this config is harness-visible only — wire Elasticsearch/Kafka yourself for production.

## Guides

- Product hub: [`../`](../index.md)
- [Tutorial](../TUTORIAL.md)
- [Methodology](../METHODOLOGY.md)
- Published scorecard page: [`../../../../scorecards/honeytrap-ssh.md`](../../../../scorecards/honeytrap-ssh.md)
- How to read UHQS: [READING-UHQS.md](../../READING-UHQS.md)

> Named products appear only under conformance as evaluation proof — not UHBS requirements or endorsements.
