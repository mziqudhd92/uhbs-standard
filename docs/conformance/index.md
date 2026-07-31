# Conformance Suite

**Status:** Normative (fixtures) / Informative (narrative + lab reports)

This suite proves that UHQS math, weights, and grade bands match the reference
harness. Fixtures and **published lab reports** are the only place in the public
docs where specific deception products are named — as evaluation proof (not as
UHBS requirements).

Optional controlled comparative evidence (VoD / FSV / DTDR / EER) lives in the
[Advanced Evidence Profile](../advanced-evidence/index.md) and does **not** alter
these UHQS fixtures.

## Lab reports (start here for real runs)

Published quick + full Docker grades, tutorials, and provenance:

**→ [reports/index.md](reports/index.md)**

| Honeypot | Quick | Full | Tutorial |
| --- | --- | --- | --- |
| [ESPot](reports/espot/index.md) | [49.34 / F](reports/espot/quick/) | [63.33 / D](reports/espot/full/) | [TUTORIAL](reports/espot/TUTORIAL.md) |
| [miniprint](reports/miniprint/index.md) | [41.83 / F](reports/miniprint/quick/) | [50.43 / D](reports/miniprint/full/) | [TUTORIAL](reports/miniprint/TUTORIAL.md) |
| [Conpot](reports/conpot/index.md) | [44.55 / F](reports/conpot/quick/) | [55.4 / D](reports/conpot/full/) | [TUTORIAL](reports/conpot/TUTORIAL.md) |
| [Cowrie](reports/cowrie/index.md) | [82.76 / B](reports/cowrie/ssh/quick/) | [61.37 / D](reports/cowrie/ssh/full/) | [TUTORIAL](reports/cowrie/TUTORIAL.md) |
| [Endlessh](reports/endlessh/index.md) | [46.55 / F](reports/endlessh/quick/) | [54.07 / D](reports/endlessh/full/) | [TUTORIAL](reports/endlessh/TUTORIAL.md) |
| [OpenCanary](reports/opencanary/index.md) | see hub | see hub | [TUTORIAL](reports/opencanary/TUTORIAL.md) |

## Fixtures

| Fixture | Proof target | Expected UHQS | Grade |
| --- | --- | --- | --- |
| [`fixtures/cowrie-low-interaction.scorecard.json`](fixtures/cowrie-low-interaction.scorecard.json) | Cowrie (SSH / Low-Interaction, **full** lab) | 61.37 | D |
| [`fixtures/posix-shell-lab.scorecard.json`](fixtures/posix-shell-lab.scorecard.json) | CyberHalluciNet (POSIX-Shell lab) | 80.33 | B |
| [`fixtures/espot-web-api.scorecard.json`](fixtures/espot-web-api.scorecard.json) | ESPot (Web-API, **full** lab) | 63.33 | D |
| [`fixtures/miniprint-low-interaction.scorecard.json`](fixtures/miniprint-low-interaction.scorecard.json) | miniprint (PJL / Low-Interaction, **full**) | 50.43 | D |
| [`fixtures/conpot-ics-scada.scorecard.json`](fixtures/conpot-ics-scada.scorecard.json) | Conpot (ICS-SCADA / Modbus, **full**) | 55.4 | D |
| [`fixtures/hellpot-web-api.scorecard.json`](fixtures/hellpot-web-api.scorecard.json) | HellPot (Web-API / HTTP, **full**) | 43.87 | F |
| [`fixtures/opencanary-web-api.scorecard.json`](fixtures/opencanary-web-api.scorecard.json) | OpenCanary (Web-API / HTTP, **full**) | 66.02 | D |
| [`fixtures/opencanary-ftp.scorecard.json`](fixtures/opencanary-ftp.scorecard.json) | OpenCanary (FTP, **full**) | 61.5 | D |
| [`fixtures/opencanary-ssh.scorecard.json`](fixtures/opencanary-ssh.scorecard.json) | OpenCanary (SSH, **full**) | 35.64 | F |
| [`fixtures/opencanary-telnet.scorecard.json`](fixtures/opencanary-telnet.scorecard.json) | OpenCanary (Telnet, **full**) | 64.9 | D |
| [`fixtures/opencanary-redis.scorecard.json`](fixtures/opencanary-redis.scorecard.json) | OpenCanary (Redis, **full**) | 53.72 | D |
| [`fixtures/endlessh-low-interaction.scorecard.json`](fixtures/endlessh-low-interaction.scorecard.json) | Endlessh (SSH tarpit / `ssh_tarpit`, **full**) | 54.07 | D |
| [`fixtures/safety-gate-fail.scorecard.json`](fixtures/safety-gate-fail.scorecard.json) | Synthetic δ_C penalty case | 0.0 | F |

## How to run

```bash
pip install -e ".[dev]"
pytest tests/test_conformance.py -q
uhbs validate-scorecard docs/conformance/fixtures/cowrie-low-interaction.scorecard.json --strict
uhbs validate-scorecard docs/conformance/fixtures/espot-web-api.scorecard.json --strict
uhbs validate-scorecard docs/conformance/fixtures/miniprint-low-interaction.scorecard.json --strict
uhbs validate-scorecard docs/conformance/fixtures/conpot-ics-scada.scorecard.json --strict
uhbs validate-scorecard docs/conformance/fixtures/opencanary-web-api.scorecard.json --strict
```

## Relationship to the lab harness

Fixtures and reports were produced by `uhbs_core.run_benchmark` (Modules A–F)
and verified with `compute_uhqs`. See [reference-implementation.md](../reference-implementation.md)
and the per-honeypot [reports](reports/index.md).

**Naming policy:** Outside this conformance tree, docs and templates MUST use
decoy **classes** and **protocols** only (see repository `GOVERNANCE.md`).
