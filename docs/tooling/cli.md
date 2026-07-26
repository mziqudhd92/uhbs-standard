# CLI & Validator Guide

**Status:** Normative (CLI behavior for UHBS-Core)

The `uhbs` CLI validates Target Profile Specifications and scorecards against the
official JSON Schemas, enforces class→weight tables, and recomputes UHQS.

For the full executable Modules A–F harness, see
[Reference Implementation](../reference-implementation.md).

## Install

```bash
git clone https://github.com/mziqudhd92/uhbs-standard.git
cd uhbs-standard
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uhbs --help
```

### UHBS-Lab harness

```bash
pip install -e ".[lab]"
uhbs lab --list-protocols
uhbs-lab --help
```

## Commands

### Validate a profile

```bash
uhbs validate-profile templates/profile.yaml
uhbs validate-profile templates/profiles/low-interaction.yaml
```

Checks:

- JSON Schema conformance (`schemas/profile.schema.json`)
- Module weights sum to \(1.00 \pm 0.001\)
- Class→weight table match (strict mode, default on)

### Validate a scorecard (with integrity)

```bash
uhbs validate-scorecard docs/conformance/fixtures/cowrie-low-interaction.scorecard.json
uhbs validate-scorecard docs/conformance/fixtures/posix-shell-lab.scorecard.json
```

Strict mode (default) **recomputes** UHQS, δ_C, and letter grade and **MUST** fail
if declared values diverge from the normative formula.

Conformance fixtures may name specific products as **evaluation proof** only;
see [Conformance](../conformance/index.md).

### Validate an evidence pack

```bash
uhbs validate-evidence path/to/evidence-pack.json
```

### Compute UHQS

```bash
uhbs score --class Low-Interaction --scores scores.json
uhbs score --profile templates/profile.yaml --scores scores.json
```

Where `scores.json` contains module scores:

```json
{
  "A": 23.5,
  "B": 42.5,
  "C": 57.0,
  "D": 100,
  "E": 55.0,
  "F": 69.0
}
```

Expected for the Low-Interaction conformance fixture weights: **UHQS = 46.97** (Grade F).

## CI Integration

`.github/workflows/ci-validate.yml` runs schema validation and conformance
fixtures on every push and pull request.
