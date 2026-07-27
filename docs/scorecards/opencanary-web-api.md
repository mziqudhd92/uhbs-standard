# Scorecard: Web-API / HTTP decoy (OpenCanary proof)

**Status:** Informative · evaluation proof (not an endorsement)  
**Proof label:** [thinkst/opencanary](https://github.com/thinkst/opencanary) · report hub: [`../conformance/reports/opencanary/`](../conformance/reports/opencanary/index.md)

| Field | Value |
| --- | --- |
| Target | Web-API / HTTP decoy (multi-protocol canary; HTTP graded) |
| Class | Web-API |
| Protocol | HTTP `:80` |
| Evaluated | 2026-07-27 (full Docker lab) |
| Spec | UHBS 4.0.0 |

## Module Results

| Evaluation Module | Score (0–100) | Weight | Status |
| --- | ---: | ---: | --- |
| Module A: Protocol Fidelity | 21.5/100 | 0.25 | PARTIAL |
| Module B: Behavioral Realism | 82.5/100 | 0.20 | PASSED |
| Module C: Telemetry Quality | 55.0/100 | 0.20 | PARTIAL |
| Module D: Safety & Containment (\(C\)) | 90.0/100 | GATE | GATE FAILED (C &lt; 95) |
| Module E: Scalability & Latency | 100.0/100 | 0.15 | PASSED (P95: 7.5 ms) |
| Module F: Static Code Audit | 70.0/100 | 0.20 | PASSED (SAST gate capped) |

## Safety Gate & Composite

| Metric | Value |
| --- | --- |
| Safety Gate Multiplier \(\delta_C\) | 0.81 (\(C = 90 &lt; 95\)) |
| **Final Composite Score (UHQS 4.0)** | **50.12 / 100** |
| Grade | **D (Needs Remediation)** |
| Production baseline (UHQS &gt; 80 + gate) | **NOT MET** |

## Artifacts

- Fixture: [`../conformance/fixtures/opencanary-web-api.scorecard.json`](../conformance/fixtures/opencanary-web-api.scorecard.json)
- Full scorecard: [`../conformance/reports/opencanary/full/SCORECARD.txt`](../conformance/reports/opencanary/full/SCORECARD.txt)
- Quick scorecard: [`../conformance/reports/opencanary/quick/SCORECARD.txt`](../conformance/reports/opencanary/quick/SCORECARD.txt) (UHQS **41.30** / F)
- Tutorial: [`../conformance/reports/opencanary/TUTORIAL.md`](../conformance/reports/opencanary/TUTORIAL.md)

```bash
uhbs validate-scorecard docs/conformance/fixtures/opencanary-web-api.scorecard.json --strict
```
