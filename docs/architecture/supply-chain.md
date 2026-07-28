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

---

## Checklist: PyPI Trusted Publishing + Sigstore (not done yet)

Trusted Publishing removes long-lived PyPI API tokens. Modern
`pypa/gh-action-pypi-publish` also attaches **PEP 740 provenance** (Sigstore-
backed attestations) when publishing via OIDC — that is the usual “Sigstore
signing” path for PyPI wheels, not a separate cosign step (optional extra).

### Maintainer actions (PyPI + GitHub)

1. Create a PyPI account and reserve the project name `uhbs` (or confirm ownership).
2. On PyPI → project **Publishing** settings, add a **Trusted Publisher**:
   - Owner: `mziqudhd92`
   - Repository: `uhbs-standard`
   - Workflow filename: `release.yml` (exact name under `.github/workflows/`)
   - Environment: `pypi` (recommended)
3. If the project does not exist yet, use a **pending** trusted publisher so the
   first tag publish can create the project.
4. In GitHub → **Settings → Environments**, create environment `pypi` with:
   - Deployment branch restriction: only tags / `main` (as appropriate)
   - Optional: required reviewers for production publishes
5. Extend `.github/workflows/release.yml` with a **publish** job that:
   - `needs: build`
   - `environment: pypi`
   - `permissions: { id-token: write, contents: read }`
   - downloads the `python-dist` artifact
   - runs `pypa/gh-action-pypi-publish` **pinned to a commit SHA** (no password)
6. Tag a release (`v4.2.2`), verify the PyPI project page shows the files **and**
   provenance attestations.
7. Document install as `pip install uhbs` / `pip install 'uhbs[lab]'` and update
   MCP `uvx` docs once the package exists.
8. (Optional) Add an explicit `cosign`/`sigstore-python` attest step for GitHub
   Release assets — separate from PyPI provenance.

### Do not

- Commit PyPI API tokens or use `TWINE_PASSWORD` long-lived secrets when OIDC works.
- Grant `id-token: write` on unrelated jobs that restore caches or run untrusted code.
- Claim SLSA Level 3 solely because Trusted Publishing succeeded.

---

## Checklist: OpenSSF Best Practices (passing badge)

Submit at [https://www.bestpractices.dev/](https://www.bestpractices.dev/) for
this GitHub repo. Passing is a **questionnaire + evidence URLs**, not an automatic
CI pass. Scorecard (already in-repo) is related but separate.

### Already in good shape for many “passing” criteria

- Public git history, Apache-2.0, `LICENSE`
- `SECURITY.md` + private vulnerability reporting
- CI (tests + lint), CodeQL, Dependabot, DCO
- `CONTRIBUTING.md`, CoC, issue/PR templates
- `CHANGELOG.md` / release notes via GitHub Releases
- Docs site + README quickstart

### Likely work before claiming “passing”

1. Create the badge project entry and answer every required criterion with a URL.
2. Confirm **branch protection** on `main` (required reviews and/or status checks) —
   Scorecard and Best Practices both care about this; it is a GitHub setting, not a file.
3. Ensure a clear **“how to run tests”** statement (README or CONTRIBUTING) matching CI.
4. Document **known security risks** of the lab harness (network probes against lab
   targets only; Safety Gate notes) if asked under security documentation criteria.
5. After first PyPI release: link distributed packages and prefer HTTPS-only install.
6. Silver/gold need multi-person bus factor — **out of scope** until Phase 6 maintainers.

### After acceptance

- Add the Best Practices badge to `README.md`.
- Keep the entry updated when version/support policy changes (`SECURITY.md` 4.2.x).
