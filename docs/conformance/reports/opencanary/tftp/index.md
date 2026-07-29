# opencanary — TFTP

**Status:** Informative · evaluation proof  
**UHBS:** v4.2.2 · **Class:** Low-Interaction · **Protocol:** `tftp`  
**Target id:** `opencanary-tftp` · **Evaluated:** 2026-07-27

| Run | UHQS | Grade | δ_C | Artifacts |
| --- | ---: | --- | --- | --- |
| [Quick](quick/README.md) | **40.69** | F | 0.81 | [`SCORECARD.txt`](quick/SCORECARD.txt) · [`report.json`](quick/report.json) |
| [Full](full/README.md) | **47.42** | F | 0.81 | [`SCORECARD.txt`](full/SCORECARD.txt) · [`report.json`](full/report.json) |

## Full run — module breakdown (analyst view)

| Module | Score | Weight | Status | Notes |
| --- | ---: | --- | --- | --- |
| Module A: Protocol Fidelity | 55.7 | 0.30 | PARTIAL | fsm=60 nego=35 timing=71 |
| Module B: Behavioral Realism | 70.5 | 0.15 | PASSED | udp sent resp=b'' |
| Module C: Telemetry Quality | 55.0 | 0.25 | PARTIAL | no STIX objects found |
| Module D: Safety & Containment (C) | 90.0 | GATE | PASSED | UHBS_AIRGAP_ATTESTED=1 (operator attestation; not a substitute for shell probes on SSH decoys) |
| Module E: Scalability & Latency | 35.0 | 0.10 | PARTIAL | P50=1508.6ms P95=1514.6ms P99=1517.1ms TPS_limit=150.0ms proto=tftp |
| Module F: Static Code Audit | 70.0 | 0.20 | PASSED | bandit HIGH=21 |
| Safety Gate δ_C | 0.81 | GATE | — | Containment multiplier |

## Full scorecard (verbatim)

```text
====================================================================================
                  UNIVERSAL HONEYPOT BENCHMARK SCORECARD v4.0.1
====================================================================================
Target System         : opencanary-tftp
System Profile Class  : Low-Interaction
Protocols             : tftp
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
Module E: Scalability & Latency     :  35.0/100       0.10     PARTIAL (P50=1508.6ms P95=1514.6ms P99=1517.1ms TPS_limit=150.0ms proto=tftp)
Module F: Static Code Audit         :  70.0/100       0.20     PASSED (bandit HIGH=21)
------------------------------------------------------------------------------------
SAFETY GATE MULTIPLIER                : δ_C = 0.81 (C = 90.0 < 95 — exponential penalty)
FINAL COMPOSITE SCORE (UHQS 4.0.1)      : 47.42 / 100
OVERALL EVALUATION GRADE              : GRADE F (Fail)
====================================================================================
```

## CTI & blue-team reading

This page is the protocol-level proof hub for **opencanary** on **tftp**. Prefer the **full** run over quick for operational decisions. Numbers without the verbatim SCORECARD (or `report.json`) are not trustworthy citations.

### Module interpretation (this protocol)

| Module | Score | Analyst reading |
| --- | ---: | --- |
| A — Protocol Fidelity | 55.7 | Protocol speak / banner-handshake quality for keeping automated clients engaged. |
| B — Behavioral Realism | 70.5 | Post-connect realism (auth/session). Low often means credential-only or reject-by-design. **CTI:** treat primarily as auth/connection intelligence. |
| C — Telemetry Quality | 55.0 | How much useful telemetry the *graded lab* exposed to UHBS — not your SIEM maturity. **Blue team:** plan explicit log shipping; do not assume UHBS C equals production visibility. |
| D — Safety & Containment (C) | 90.0 | Containment/Safety Gate. Below threshold collapses UHQS via δ_C. Check δ_C carefully. |
| E — Scalability & Latency | 35.0 | Latency vs profile P95. Low can mean timeouts, tarpits, or slow handlers. |
| F — Static Code Audit | 70.0 | Static audit of the lab source tree — hygiene signal, not a full CVE program. |
| δ_C | 0.81 | Safety Gate multiplier applied to composite UHQS. |

- **CTI:** use Module A/B to judge engagement depth (scanner noise vs post-auth TTPs). Low B usually means credential/connection intelligence, not interactive malware staging.
- **Blue team:** verify Safety Gate (Module D / δ_C) before Internet exposure; wire SIEM shipping yourself — Module C is harness visibility, not your pipeline.
- **Replication:** commands live in the product tutorial; environment limits in the methodology.

## Guides

- Product hub: [`../`](../index.md)
- [Tutorial](../TUTORIAL.md)
- [Methodology](../METHODOLOGY.md)
- Published scorecard page: [`../../../../scorecards/opencanary-tftp.md`](../../../../scorecards/opencanary-tftp.md)
- How to read UHQS: [READING-UHQS.md](../../READING-UHQS.md)

> Named products appear only under conformance as evaluation proof — not UHBS requirements or endorsements.
