# Conformance Suite

**Status:** Normative (fixtures) / Informative (narrative)

This suite proves that UHQS math, weights, and grade bands match the reference
harness. Fixtures are **sanitized** from real lab runs against Cowrie (OSS) and a
vendor-neutral POSIX-Shell research decoy.

## Fixtures

| Fixture | Source | Expected UHQS | Grade |
| --- | --- | --- | --- |
| [`fixtures/cowrie-low-interaction.scorecard.json`](fixtures/cowrie-low-interaction.scorecard.json) | Cowrie Docker lab | 46.97 | F |
| [`fixtures/posix-shell-lab.scorecard.json`](fixtures/posix-shell-lab.scorecard.json) | POSIX research decoy (post-hardening) | 80.33 | B |
| [`fixtures/safety-gate-fail.scorecard.json`](fixtures/safety-gate-fail.scorecard.json) | Synthetic δ_C penalty case | 0.0 | F |

## How to run

```bash
pip install -e ".[dev]"
pytest tests/test_conformance.py -q
uhbs validate-scorecard docs/conformance/fixtures/cowrie-low-interaction.scorecard.json --strict
```

## Relationship to the lab harness

Fixtures were produced by `run_benchmark.py` (Modules A–F) and verified with
`calculate_uhqs_v4.py` / `lib/models.py` `compute_uhqs`. See
[reference-implementation.md](../reference-implementation.md).
