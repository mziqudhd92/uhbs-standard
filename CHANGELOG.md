# Changelog

All notable changes to the UHBS specification and tooling are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/). Spec and CLI
share version **4.0.0** until Phase 3 splits `uhbs-core`.

## [4.0.0] — 2026-07-26

### Added
- `ROADMAP.md` — locked maturity plan incorporating the existing UHBS-Lab harness
- Document status, RFC 2119 keywords, UHBS-Core / UHBS-Lab conformance levels
- `schemas/evidence-pack.schema.json`
- Conformance fixtures from real lab runs: **Cowrie** (UHQS 46.97) and POSIX-Shell
  research decoy (UHQS 80.33)
- Class→weight tables including `Database` and `GenAI-Shell`
- CLI `--strict` integrity checks (recompute UHQS / δ_C / grade)
- `docs/reference-implementation.md` mapping Modules A–F → harness scripts

### Changed
- Letter grade band D starts at **50** (aligned with reference harness)
- UHQS rounding to **two** decimal places (aligned with harness reports)
- Production gate language demoted to **RECOMMENDED** Production Baseline Profile

### Reference harness (external lab)
- Orchestrator: `run_benchmark.py`
- Modules: `test_stealth`, `test_realism`, `test_telemetry`, `test_safety`,
  `test_scale`, `test_static_code`
- Scoring: `lib/models.py`, `calculate_uhqs_v4.py`
- Scorecard layout: `lib/report.py`
- Proven targets: Cowrie (Low-Interaction), POSIX research decoy
