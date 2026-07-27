# Scorecard: Low-Interaction / SSH tarpit (Endlessh proof)

**Status:** Informative · evaluation proof (not an endorsement)  
**Proof label:** [skeeto/endlessh](https://github.com/skeeto/endlessh) · report hub: [`../conformance/reports/endlessh/`](../conformance/reports/endlessh/index.md)

| Field | Value |
| --- | --- |
| Target | Low-Interaction SSH tarpit |
| Class | Low-Interaction |
| Protocol | SSH `:2223` (lab) |
| Evaluated | 2026-07-27 (loopback lab) |
| Spec | UHBS 4.0.0 |

## Module Results

| Evaluation Module | Score (0–100) | Weight | Status |
| --- | ---: | ---: | --- |
| Module A: Protocol Fidelity | 12.5/100 | 0.30 | PARTIAL |
| Module B: Behavioral Realism | 6.2/100 | 0.15 | PARTIAL |
| Module C: Telemetry Quality | 25.0/100 | 0.25 | PARTIAL |
| Module D: Safety & Containment (\(C\)) | 96.0/100 | GATE | GATE PASSED |
| Module E: Scalability & Latency | 20.0/100 | 0.10 | PARTIAL |
| Module F: Static Code Audit | 70.0/100 | 0.20 | PASSED |

## Safety Gate & Composite

| Metric | Value |
| --- | --- |
| Safety Gate Multiplier \(\delta_C\) | 1.0 (\(C = 96 \ge 95\)) |
| **Final Composite Score (UHQS 4.0)** | **26.94 / 100** |
| Grade | **F (Fail)** |
| Production baseline (UHQS &gt; 80 + gate) | **NOT MET** |

## Artifacts

- Fixture: [`../conformance/fixtures/endlessh-low-interaction.scorecard.json`](../conformance/fixtures/endlessh-low-interaction.scorecard.json)
- Full scorecard: [`../conformance/reports/endlessh/full/SCORECARD.txt`](../conformance/reports/endlessh/full/SCORECARD.txt)
- Quick scorecard: [`../conformance/reports/endlessh/quick/SCORECARD.txt`](../conformance/reports/endlessh/quick/SCORECARD.txt) (UHQS **26.94** / F)
- Tutorial: [`../conformance/reports/endlessh/TUTORIAL.md`](../conformance/reports/endlessh/TUTORIAL.md)
- Original project: [github.com/skeeto/endlessh](https://github.com/skeeto/endlessh)

```bash
uhbs validate-scorecard docs/conformance/fixtures/endlessh-low-interaction.scorecard.json --strict
```
