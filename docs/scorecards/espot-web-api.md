# Scorecard: Web-API / HTTP decoy (ESPot proof)

**Status:** Informative · evaluation proof (not an endorsement)  
**Proof label:** [mycert/ESPot](https://github.com/mycert/ESPot) · report hub: [`../conformance/reports/espot/`](../conformance/reports/espot/index.md)

| Field | Value |
| --- | --- |
| Target | Web-API / HTTP decoy (Elasticsearch-style) |
| Class | Web-API |
| Protocol | HTTP `:9200` |
| Evaluated | 2026-07-27 (full Docker lab) |
| Spec | UHBS 4.0.1 |

## Module Results

| Evaluation Module | Score (0–100) | Weight | Status |
| --- | ---: | ---: | --- |
| Module A: Protocol Fidelity | 86.75/100 | 0.25 | PASSED |
| Module B: Behavioral Realism | 82.5/100 | 0.20 | PASSED |
| Module C: Telemetry Quality | 55.0/100 | 0.20 | PARTIAL |
| Module D: Safety & Containment (\(C\)) | 90.0/100 | GATE | GATE FAILED (C &lt; 95) |
| Module E: Scalability & Latency | 100.0/100 | 0.15 | PASSED (P95: 8.28 ms) |
| Module F: Static Code Audit | 70.0/100 | 0.20 | PASSED (SAST gate capped) |

## Safety Gate & Composite

| Metric | Value |
| --- | --- |
| Safety Gate Multiplier \(\delta_C\) | 0.81 (\(C = 90 &lt; 95\)) |
| **Final Composite Score (UHQS 4.0.1)** | **63.33 / 100** |
| Grade | **D (Needs Remediation)** |
| Production baseline (UHQS &gt; 80 + gate) | **NOT MET** |

## Artifacts

- Fixture: [`../conformance/fixtures/espot-web-api.scorecard.json`](../conformance/fixtures/espot-web-api.scorecard.json)
- Full scorecard: [`../conformance/reports/espot/full/SCORECARD.txt`](../conformance/reports/espot/full/SCORECARD.txt)
- Quick scorecard: [`../conformance/reports/espot/quick/SCORECARD.txt`](../conformance/reports/espot/quick/SCORECARD.txt) (UHQS **49.34** / F)
- Tutorial: [`../conformance/reports/espot/TUTORIAL.md`](../conformance/reports/espot/TUTORIAL.md)

```bash
uhbs validate-scorecard docs/conformance/fixtures/espot-web-api.scorecard.json --strict
```

## How to read this scorecard (CTI / blue team)

_Module interpretation unavailable (missing full SCORECARD)._

- **CTI:** use module notes + verbatim SCORECARD to judge what attacker activity you can actually observe.
- **Blue team:** verify Safety Gate (δ_C / Module D) and plan log shipping before Internet exposure.
- **Guide:** [How to read UHBS lab proof](../conformance/reports/READING-UHQS.md)
