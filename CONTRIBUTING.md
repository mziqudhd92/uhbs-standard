# Contributing to UHBS

Thank you for helping establish the Universal Honeypot Benchmarking Standard as a trusted,
vendor-neutral, production-grade open-source project.

## Vendor neutrality

- Spec, templates, and scorecard *examples* use **classes and protocols** only.
- Named products belong only in `docs/conformance/` as evaluation **proof**.
- Do not add product endorsements to README, normative docs, or marketing copy.

## Ways to Contribute

- **Specification clarifications** — docs under `docs/specification/`
- **Schema improvements** — `schemas/*.schema.json`
- **CLI / validator tooling** — `src/uhbs_cli/`
- **Scorecard examples** — `docs/scorecards/`
- **Bug reports & profile submissions** — use the GitHub issue templates

## Development Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uhbs --help
pytest
```

## Pull Request Workflow

1. Fork the repository and create a topic branch from `main`.
2. Keep changes focused (one concern per PR).
3. Ensure CI passes: schema validation, lint, and unit tests.
4. Fill out the pull request template completely.
5. Request review from CODEOWNERS.

### Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` new capability
- `fix:` bug fix
- `docs:` documentation only
- `chore:` maintenance
- `test:` tests
- `refactor:` non-behavioral refactor

### Developer Certificate of Origin (DCO)

All commits must be signed off:

```bash
git commit -s -m "feat: add profile weight validation"
```

By signing off, you certify the [Developer Certificate of Origin](https://developercertificate.org/).

## Specification Changes (RFC)

Normative changes to Modules A–F, UHQS formula, Safety Gate \(\delta_C\), or TPS semantics **require an RFC**. See [GOVERNANCE.md](GOVERNANCE.md).

Non-normative docs, examples, and tooling fixes may proceed via ordinary PRs.

## Code Style

- Python 3.11+
- Format with `ruff format`; lint with `ruff check`
- Prefer clear, typed public APIs
- Do not add exploit PoCs to the repository; defensive tests only

## Security

Report vulnerabilities per [SECURITY.md](SECURITY.md). Do not open public issues for security findings.

## Conduct

Participation is governed by our [Code of Conduct](CODE_OF_CONDUCT.md).
