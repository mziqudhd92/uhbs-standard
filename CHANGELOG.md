# Changelog

All notable changes to the UHBS specification and tooling are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/). Spec and CLI
share version **4.0.0** (`uhbs_core` ships in-tree as `uhbs[lab]`).

## [4.0.0] — 2026-07-26

### Added
- `ROADMAP.md` — locked maturity plan incorporating the existing UHBS-Lab harness
- Document status, RFC 2119 keywords, UHBS-Core / UHBS-Lab conformance levels
- `schemas/evidence-pack.schema.json`
- Conformance fixtures (proof labels only): Low-Interaction UHQS 46.97,
  POSIX-Shell UHQS 80.33 — see `docs/conformance/`
- Class→weight tables including `Database` and `GenAI-Shell`
- CLI `--strict` integrity checks (recompute UHQS / δ_C / grade)
- **`uhbs_core`** reference harness (Modules A–F, protocol plugins, `uhbs-lab`)
- Per-run `MANIFEST.json` digests; Release workflow + CycloneDX SBOM artifact
- DCO check + OpenSSF Scorecard workflows
- ATT&CK / NIST / IEC 62443 mappings; RFC-0001 baseline; `MAINTAINERS.md`;
  `VERSIONING.md`; scorecard registry rules

### Changed
- Letter grade band D starts at **50** (aligned with reference harness)
- UHQS rounding to **two** decimal places (aligned with harness reports)
- Production gate language demoted to **RECOMMENDED** Production Baseline Profile
- Vendor-neutrality pass: product names confined to conformance proof fixtures;
  Module F signals profile renamed to `low_interaction_ssh_signals.yaml`

### Changed (honesty / posture)
- Docs state clearly that UHBS is a **personal draft framework**, not a
  multi-party standards body; committee, neutral org, and adopters moved to
  ROADMAP Phase 6 as aspirational (unchecked) goals

### Pending (manual / ops / community — see ROADMAP Phase 6)
- PyPI Trusted Publishing + Sigstore signing
- Zenodo DOI deposit
- Neutral GitHub organization transfer
- Multi-organization maintainers and independent adopters
