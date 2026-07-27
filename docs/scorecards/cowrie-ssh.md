# Scorecard: Low-Interaction / SSH decoy (Cowrie proof)

**Status:** Informative · evaluation proof (not an endorsement)  
**Proof label:** [cowrie/cowrie](https://github.com/cowrie/cowrie) · report hub: [`../conformance/reports/cowrie/`](../conformance/reports/cowrie/index.md)

| Field | Value |
| --- | --- |
| Target | Low-Interaction SSH decoy |
| Class | Low-Interaction |
| Protocol | SSH `:2222` |
| Evaluated | 2026-07-27 (full Docker lab) |
| Spec | UHBS 4.0.0 |

## Module Results

| Evaluation Module | Score (0–100) | Weight | Status |
| --- | ---: | ---: | --- |
| Module A: Protocol Fidelity | 21.5/100 | 0.30 | PARTIAL |
| Module B: Behavioral Realism | 60.0/100 | 0.15 | PARTIAL |
| Module C: Telemetry Quality | 55.0/100 | 0.25 | PARTIAL |
| Module D: Safety & Containment (\(C\)) | 100.0/100 | GATE | GATE PASSED |
| Module E: Scalability & Latency | 55.0/100 | 0.10 | PARTIAL (P95: ~3100 ms) |
| Module F: Static Code Audit | 70.0/100 | 0.20 | PASSED (SAST gate capped) |

## Safety Gate & Composite

| Metric | Value |
| --- | --- |
| Safety Gate Multiplier \(\delta_C\) | 1.0 (\(C = 100 \ge 95\)) |
| **Final Composite Score (UHQS 4.0)** | **48.70 / 100** |
| Grade | **F (Fail)** |
| Production baseline (UHQS &gt; 80 + gate) | **NOT MET** (gate cleared; UHQS below 80) |

## Artifacts

- Fixture: [`../conformance/fixtures/cowrie-low-interaction.scorecard.json`](../conformance/fixtures/cowrie-low-interaction.scorecard.json)
- Full scorecard: [`../conformance/reports/cowrie/full/SCORECARD.txt`](../conformance/reports/cowrie/full/SCORECARD.txt)
- Quick scorecard: [`../conformance/reports/cowrie/quick/SCORECARD.txt`](../conformance/reports/cowrie/quick/SCORECARD.txt) (UHQS **63.52** / D)
- Tutorial: [`../conformance/reports/cowrie/TUTORIAL.md`](../conformance/reports/cowrie/TUTORIAL.md)
- Original project: [github.com/cowrie/cowrie](https://github.com/cowrie/cowrie)

```bash
uhbs validate-scorecard docs/conformance/fixtures/cowrie-low-interaction.scorecard.json --strict
```
