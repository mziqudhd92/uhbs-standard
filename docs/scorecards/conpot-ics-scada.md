# Scorecard: ICS-SCADA / Modbus decoy (Conpot proof)

**Status:** Informative · evaluation proof (not an endorsement)  
**Proof label:** [mushorg/conpot](https://github.com/mushorg/conpot) · report hub: [`../conformance/reports/conpot/`](../conformance/reports/conpot/index.md)

| Field | Value |
| --- | --- |
| Target | ICS-SCADA Modbus decoy |
| Class | ICS-SCADA |
| Protocol | Modbus TCP `:5020` |
| Evaluated | 2026-07-27 (full Docker lab) |
| Spec | UHBS 4.0.1 |

## Module Results

| Evaluation Module | Score (0–100) | Weight | Status |
| --- | ---: | ---: | --- |
| Module A: Protocol Fidelity | 79.0/100 | 0.35 | PASSED |
| Module B: Behavioral Realism | 42.5/100 | 0.20 | PARTIAL |
| Module C: Telemetry Quality | 55.0/100 | 0.15 | PARTIAL |
| Module D: Safety & Containment (\(C\)) | 90.0/100 | GATE | GATE FAILED (C &lt; 95) |
| Module E: Scalability & Latency | 100.0/100 | 0.10 | PASSED |
| Module F: Static Code Audit | 70.0/100 | 0.20 | PASSED (SAST gate capped) |

## Safety Gate & Composite

| Metric | Value |
| --- | --- |
| Safety Gate Multiplier \(\delta_C\) | 0.81 (\(C = 90 &lt; 95\)) |
| **Final Composite Score (UHQS 4.0.1)** | **55.4 / 100** |
| Grade | **D (Needs Remediation)** |
| Production baseline (UHQS &gt; 80 + gate) | **NOT MET** |

## Artifacts

- Fixture: [`../conformance/fixtures/conpot-ics-scada.scorecard.json`](../conformance/fixtures/conpot-ics-scada.scorecard.json)
- Full scorecard: [`../conformance/reports/conpot/full/SCORECARD.txt`](../conformance/reports/conpot/full/SCORECARD.txt)
- Quick scorecard: [`../conformance/reports/conpot/quick/SCORECARD.txt`](../conformance/reports/conpot/quick/SCORECARD.txt) (UHQS **44.55** / F)
- Tutorial: [`../conformance/reports/conpot/TUTORIAL.md`](../conformance/reports/conpot/TUTORIAL.md)

```bash
uhbs validate-scorecard docs/conformance/fixtures/conpot-ics-scada.scorecard.json --strict
```

## How to read this scorecard (CTI / blue team)

_Module interpretation unavailable (missing full SCORECARD)._

- **CTI:** use module notes + verbatim SCORECARD to judge what attacker activity you can actually observe.
- **Blue team:** verify Safety Gate (δ_C / Module D) and plan log shipping before Internet exposure.
- **Guide:** [How to read UHBS lab proof](../conformance/reports/READING-UHQS.md)
