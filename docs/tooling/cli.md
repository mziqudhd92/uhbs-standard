# CLI & Validator Guide

The `uhbs` CLI validates Target Profile Specifications and scorecards against the official JSON Schemas, and computes UHQS from module scores.

## Install

```bash
git clone https://github.com/mziqudhd92/uhbs-standard.git
cd uhbs-standard
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uhbs --help
```

## Commands

### Validate a profile

```bash
uhbs validate-profile templates/profile.yaml
```

Checks:

- JSON Schema conformance (`schemas/profile.schema.json`)
- Module weights sum to \(1.00 \pm 0.001\)

### Validate a scorecard

```bash
uhbs validate-scorecard docs/scorecards/examples/illustrative-posix-genai.scorecard.json
```

### Compute UHQS

```bash
uhbs score --profile templates/profile.yaml --scores scores.json
```

Where `scores.json` contains module scores:

```json
{
  "A": 88,
  "B": 94,
  "C": 98,
  "D": 97,
  "E": 88,
  "F": 91
}
```

The CLI applies the Safety Gate:

\[
\delta_C = 1.0 \text{ if } C \ge 95,\quad \text{else } (C/100)^2
\]

…and prints the composite UHQS plus recommended letter grade.

## CI Integration

The repository workflow `.github/workflows/ci-validate.yml` runs schema validation on every push and pull request. Adopters can vendor the schemas or call `uhbs` from their own pipelines.
