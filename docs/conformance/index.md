# Conformance Suite

**Status:** Normative (fixtures) / Informative (narrative + lab reports)

This suite proves that UHQS math, weights, and grade bands match the reference
harness. Fixtures and **published lab reports** are the only place in the public
docs where specific deception products are named — as evaluation proof (not as
UHBS requirements).

## Lab reports (start here for real runs)

Published quick + full Docker grades, tutorials, and provenance:

**→ [reports/index.md](reports/index.md)**

| Honeypot | Quick | Full | Tutorial |
| --- | --- | --- | --- |
| [ESPot](reports/espot/index.md) | [39.95 / F](reports/espot/quick/) | [49.82 / F](reports/espot/full/) | [TUTORIAL](reports/espot/TUTORIAL.md) |
| [miniprint](reports/miniprint/index.md) | [39.99 / F](reports/miniprint/quick/) | [47.77 / F](reports/miniprint/full/) | [TUTORIAL](reports/miniprint/TUTORIAL.md) |
| [Conpot](reports/conpot/index.md) | [44.62 / F](reports/conpot/quick/) | [55.51 / D](reports/conpot/full/) | [TUTORIAL](reports/conpot/TUTORIAL.md) |

## Fixtures

| Fixture | Proof target | Expected UHQS | Grade |
| --- | --- | --- | --- |
| [`fixtures/cowrie-low-interaction.scorecard.json`](fixtures/cowrie-low-interaction.scorecard.json) | Cowrie (OSS low-interaction) | 46.97 | F |
| [`fixtures/posix-shell-lab.scorecard.json`](fixtures/posix-shell-lab.scorecard.json) | CyberHalluciNet (POSIX-Shell lab) | 80.33 | B |
| [`fixtures/espot-web-api.scorecard.json`](fixtures/espot-web-api.scorecard.json) | ESPot (Web-API, **full** lab) | 49.82 | F |
| [`fixtures/miniprint-low-interaction.scorecard.json`](fixtures/miniprint-low-interaction.scorecard.json) | miniprint (PJL / Low-Interaction, **full**) | 47.77 | F |
| [`fixtures/conpot-ics-scada.scorecard.json`](fixtures/conpot-ics-scada.scorecard.json) | Conpot (ICS-SCADA / Modbus, **full**) | 55.51 | D |
| [`fixtures/safety-gate-fail.scorecard.json`](fixtures/safety-gate-fail.scorecard.json) | Synthetic δ_C penalty case | 0.0 | F |

## How to run

```bash
pip install -e ".[dev]"
pytest tests/test_conformance.py -q
uhbs validate-scorecard docs/conformance/fixtures/cowrie-low-interaction.scorecard.json --strict
uhbs validate-scorecard docs/conformance/fixtures/espot-web-api.scorecard.json --strict
uhbs validate-scorecard docs/conformance/fixtures/miniprint-low-interaction.scorecard.json --strict
uhbs validate-scorecard docs/conformance/fixtures/conpot-ics-scada.scorecard.json --strict
```

## Relationship to the lab harness

Fixtures and reports were produced by `uhbs_core.run_benchmark` (Modules A–F)
and verified with `compute_uhqs`. See [reference-implementation.md](../reference-implementation.md)
and the per-honeypot [reports](reports/index.md).

**Naming policy:** Outside this conformance tree, docs and templates MUST use
decoy **classes** and **protocols** only (see repository `GOVERNANCE.md`).
