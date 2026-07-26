# Conformance Suite

**Status:** Normative (fixtures) / Informative (narrative)

This suite proves that UHQS math, weights, and grade bands match the reference
harness. Fixtures are **sanitized scorecards from real lab runs** — the only
place in the public docs where specific deception products are named, as
evaluation proof (not as UHBS requirements).

## Fixtures

| Fixture | Proof target | Expected UHQS | Grade |
| --- | --- | --- | --- |
| [`fixtures/cowrie-low-interaction.scorecard.json`](fixtures/cowrie-low-interaction.scorecard.json) | Cowrie (OSS low-interaction) | 46.97 | F |
| [`fixtures/posix-shell-lab.scorecard.json`](fixtures/posix-shell-lab.scorecard.json) | CyberHalluciNet (POSIX-Shell lab) | 80.33 | B |
| [`fixtures/safety-gate-fail.scorecard.json`](fixtures/safety-gate-fail.scorecard.json) | Synthetic δ_C penalty case | 0.0 | F |

## How to run

```bash
pip install -e ".[dev]"
pytest tests/test_conformance.py -q
uhbs validate-scorecard docs/conformance/fixtures/cowrie-low-interaction.scorecard.json --strict
uhbs validate-scorecard docs/conformance/fixtures/posix-shell-lab.scorecard.json --strict
```

## Relationship to the lab harness

Fixtures were produced by `uhbs_core.run_benchmark` (Modules A–F) and verified
with `compute_uhqs`. See [reference-implementation.md](../reference-implementation.md).

**Naming policy:** Outside this conformance tree, docs and templates MUST use
decoy **classes** and **protocols** only (see repository `GOVERNANCE.md`).
