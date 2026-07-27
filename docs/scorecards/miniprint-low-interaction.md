# Scorecard: Low-Interaction / PJL decoy (miniprint proof)

**Status:** Informative · evaluation proof (not an endorsement)  
**Proof label:** [sa7mon/miniprint](https://github.com/sa7mon/miniprint) · report hub: [`../conformance/reports/miniprint/`](../conformance/reports/miniprint/index.md)

| Field | Value |
| --- | --- |
| Target | Low-Interaction printer decoy (PJL / raw TCP) |
| Class | Low-Interaction |
| Protocol | PJL `:9100` |
| Evaluated | 2026-07-27 (full Docker lab) |
| Spec | UHBS 4.0.1 |

## Module Results

| Evaluation Module | Score (0–100) | Weight | Status |
| --- | ---: | ---: | --- |
| Module A: Protocol Fidelity | 65.4/100 | 0.30 | PARTIAL |
| Module B: Behavioral Realism | 62.5/100 | 0.15 | PARTIAL |
| Module C: Telemetry Quality | 55.0/100 | 0.25 | PARTIAL |
| Module D: Safety & Containment (\(C\)) | 90.0/100 | GATE | GATE FAILED (C &lt; 95) |
| Module E: Scalability & Latency | 55.0/100 | 0.10 | PARTIAL (P95: ~1127 ms) |
| Module F: Static Code Audit | 70.0/100 | 0.20 | PASSED (SAST gate capped) |

## Safety Gate & Composite

| Metric | Value |
| --- | --- |
| Safety Gate Multiplier \(\delta_C\) | 0.81 (\(C = 90 &lt; 95\)) |
| **Final Composite Score (UHQS 4.0.1)** | **50.43 / 100** |
| Grade | **D (Needs Remediation)** |
| Production baseline (UHQS &gt; 80 + gate) | **NOT MET** |

## Artifacts

- Fixture: [`../conformance/fixtures/miniprint-low-interaction.scorecard.json`](../conformance/fixtures/miniprint-low-interaction.scorecard.json)
- Full scorecard: [`../conformance/reports/miniprint/full/SCORECARD.txt`](../conformance/reports/miniprint/full/SCORECARD.txt)
- Quick scorecard: [`../conformance/reports/miniprint/quick/SCORECARD.txt`](../conformance/reports/miniprint/quick/SCORECARD.txt) (UHQS **41.83** / F)
- Tutorial: [`../conformance/reports/miniprint/TUTORIAL.md`](../conformance/reports/miniprint/TUTORIAL.md)

```bash
uhbs validate-scorecard docs/conformance/fixtures/miniprint-low-interaction.scorecard.json --strict
```
