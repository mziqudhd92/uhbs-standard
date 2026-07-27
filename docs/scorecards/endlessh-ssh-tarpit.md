# Scorecard: Low-Interaction / SSH tarpit (Endlessh proof)

**Status:** Informative · evaluation proof (not an endorsement)  
**Proof label:** [skeeto/endlessh](https://github.com/skeeto/endlessh) · report hub: [`../conformance/reports/endlessh/`](../conformance/reports/endlessh/index.md)

| Field | Value |
| --- | --- |
| Target | Low-Interaction SSH tarpit (generic `ssh_tarpit`) |
| Class | Low-Interaction |
| Protocol | `ssh_tarpit` · TCP `:2222` |
| Evaluated | 2026-07-27 (full Docker lab) |
| Spec | UHBS 4.0.1 |

## Module Results

| Evaluation Module | Score (0–100) | Weight | Status |
| --- | ---: | ---: | --- |
| Module A: Protocol Fidelity | 65.43/100 | 0.30 | PARTIAL (generic TCP) |
| Module B: Behavioral Realism | 62.5/100 | 0.15 | PARTIAL |
| Module C: Telemetry Quality | 55.0/100 | 0.25 | PARTIAL |
| Module D: Safety & Containment (\(C\)) | 90.0/100 | GATE | GATE FAILED (C &lt; 95) |
| Module E: Scalability & Latency | 100.0/100 | 0.10 | PASSED |
| Module F: Static Code Audit | 70.0/100 | 0.20 | PASSED (SAST gate capped) |

## Safety Gate & Composite

| Metric | Value |
| --- | --- |
| Safety Gate Multiplier \(\delta_C\) | 0.81 (\(C = 90 &lt; 95\)) |
| **Final Composite Score (UHQS 4.0.1)** | **54.07 / 100** |
| Grade | **D (Needs Remediation)** |
| Production baseline (UHQS &gt; 80 + gate) | **NOT MET** |

## Artifacts

- Fixture: [`../conformance/fixtures/endlessh-low-interaction.scorecard.json`](../conformance/fixtures/endlessh-low-interaction.scorecard.json)
- Full scorecard: [`../conformance/reports/endlessh/full/SCORECARD.txt`](../conformance/reports/endlessh/full/SCORECARD.txt)
- Quick scorecard: [`../conformance/reports/endlessh/quick/SCORECARD.txt`](../conformance/reports/endlessh/quick/SCORECARD.txt) (UHQS **46.55** / F)
- Tutorial: [`../conformance/reports/endlessh/TUTORIAL.md`](../conformance/reports/endlessh/TUTORIAL.md)

```bash
uhbs validate-scorecard docs/conformance/fixtures/endlessh-low-interaction.scorecard.json --strict
```
