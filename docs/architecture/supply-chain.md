# Supply-chain hygiene — concrete steps taken vs. aspirational target

> Companion to [`GOVERNANCE.md`](https://github.com/mziqudhd92/uhbs-standard/blob/main/GOVERNANCE.md) §7 and
> [`ROADMAP.md`](https://github.com/mziqudhd92/uhbs-standard/blob/main/ROADMAP.md) Phase 4 (Integrity / OpenSSF / SLSA).
> Written for a **personal open-source beta project**, not a certified
> supply-chain program — see [`AGENTS.md`](https://github.com/mziqudhd92/uhbs-standard/blob/main/AGENTS.md).

## Aspirational target (not achieved)

A commonly cited bar for open-source supply-chain maturity is an
[SLSA](https://slsa.dev/) build level (e.g. Level 3: hermetic, verifiable
build provenance) plus fully typed, statically-verified source. **UHBS does
not claim SLSA Level 3, or any other specific SLSA level, today.** This
page exists to say plainly what has actually been done and what's missing,
rather than assert a level that hasn't been evaluated.

## Concrete steps taken so far

| Step | Status | Where |
| --- | --- | --- |
| GitHub Actions pinned to a commit SHA (not a mutable version tag) | Done in `ci-validate.yml`, `openssf-scorecard.yml`, `dco.yml`, `release.yml`, and the new `golden-baseline.yml` | `.github/workflows/*.yml` (`# vN` comment kept alongside each SHA for human readability) |
| Per-run SHA-256 manifest of harness output | Done | `uhbs_core.manifest` |
| CycloneDX SBOM published on release | Done | `.github/workflows/release.yml` |
| DCO (signed-off commits) required on PRs | Done | `.github/workflows/dco.yml` |
| OpenSSF Scorecard action (public score, not a pass/fail gate) | Done | `.github/workflows/openssf-scorecard.yml` |
| Lint (`ruff`) on shared/core surfaces | Done, pre-existing | `[tool.ruff]` in `pyproject.toml` |
| Static typing (`mypy`) — **scoped to brand-new files only** | Done for `contract_validation.py` and `plugin_sdk.py` (`mypy --strict` clean) | `[tool.mypy]` in `pyproject.toml` |

## What's still missing (be honest about the gaps)

- **No SLSA provenance attestation** on release artifacts (e.g. no
  `slsa-github-generator` build). The release workflow builds sdist/wheel
  and an SBOM, but does not produce or attach signed provenance.
- **No Sigstore/cosign keyless signing** yet — already tracked as a
  Phase 4 follow-up in `ROADMAP.md`; unchanged by this pass.
- **`mypy` does not cover the existing ~17-plugin codebase.** Retrofitting
  `mypy --strict` (or even non-strict) across `src/uhbs_core/protocols/*`,
  `models.py`, `run_benchmark.py`, etc. is a separate, larger effort with
  its own review — not attempted here. The `[tool.mypy]` `files` list in
  `pyproject.toml` is intentionally short; widening it is future work.
- **No dependency-update automation verification** beyond Dependabot
  defaults (not audited as part of this pass).
- **No reproducible/hermetic build** verification (e.g. bit-for-bit
  rebuild comparison).

## Why "informational-only" extends to this list

Consistent with `docs/architecture/ci-baseline.md`'s golden-baseline CI job
and `docs/architecture/plugin-contracts.md`'s advisory contract validator,
none of the above becomes a required/blocking gate in this pass. This
document exists so a reader can tell the difference between "we pinned
Actions by SHA" (true, verifiable in the workflow files) and "we are
SLSA Level 3" (not true, not claimed).
