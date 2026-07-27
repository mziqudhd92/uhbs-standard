# Changelog

All notable changes to the UHBS specification and tooling are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/). Spec and CLI
share version **4.0.0** (`uhbs_core` ships in-tree as `uhbs[lab]`; MCP as `uhbs[mcp]`).

## [Unreleased]

### Added
- **MCP server** (`uhbs[mcp]` / `uhbs-mcp`): local stdio tools for AI hosts
  (validate / UHQS / fixtures / schemas); `server.json` registry metadata;
  docs + landing `#mcp` section
- Published lab reports + landing Results: ESPot, miniprint, Conpot, Cowrie,
  OpenCanary (quick + full)
- Site-root AEO discovery: `llms-full.txt`, `humans.txt`, `.well-known/security.txt`,
  `server.json` (in addition to root `llms.txt`)
- Protocol plugins for git, mysql, ntp, rdp, sip, snmp, tftp, vnc; plugin SDK,
  check-scoring helpers, and OpenCanary multi-protocol lab TPS/inventory coverage
- Architecture notes: protocol-plugin audit, plugin contracts, CI baseline,
  supply-chain

### Changed
- GitHub Pages root is the React landing hub; MkDocs deploys under `/mkdocs/`
- Project maturity wording: **draft** → **beta**
- Cowrie live fixture regraded to UHQS **61.37** / D (SSH full); worked-example **46.97** kept in tests
- ROADMAP evaluation corpus ≥5 OSS targets marked complete
- **Module E P95 defaults** are class/protocol-aware when TPS omits
  `expected_p95_latency_ms` (e.g. SSH **3000 ms**, Telnet **500 ms**,
  Low-Interaction class **2000 ms**)
- Lab TPS for SSH/Telnet set realistic P95 baselines (Cowrie / OpenCanary /
  Beelzebub / Trapster)

### Fixed
- **Regraded Cowrie SSH/Telnet** after scoring-scale fixes: SSH quick **82.76 / B**,
  full **61.37 / D**; Telnet quick **53.41 / D**, full **64.90 / D**
- **Regraded OpenCanary** across HTTP/FTP/SSH/Telnet/Redis/MySQL/RDP/SIP/SNMP/
  NTP/TFTP/VNC/Git/SMB (quick+full) under the same scoring-scale fixes; HTTP full
  **50.12 → 66.02**, SSH full **28.44 → 35.64**
- **Regraded ESPot** (HTTP quick+full) under the same scoring-scale fixes; quick
  **39.95 → 49.34** / F, full **49.82 → 63.33** / D
- **Regraded miniprint** (PJL quick+full); quick **39.99 → 41.83** / F, full
  **47.77 → 50.43** / D
- **Regraded Conpot** (Modbus quick+full); quick **44.62 → 44.55** / F, full
  **55.51 → 55.4** / D
- **Protocol-agnostic lab binding:** TPS no longer silently overwrites inventory/CLI
  protocols; conflicting TPS vs `--protocol` raises `ProtocolConflictError`
- Builtin `low_interaction` is **class-only**; SSH/Telnet profile moved to
  `low_interaction_ssh`
- Module D never Paramikos the primary application port unless `ports.ssh` /
  `ssh_port` is explicit (HTTP/PJL/… decoys safe)
- Stale docs that labeled Cowrie / the Low-Interaction fixture as UHQS 46.97
- **RFC/timing CheckResult scores normalized to 0–100** so geometric-mean
  Module A aggregation no longer silently caps suites designed as sum-to-100
  partial points
- **Module C JSONL fallback:** telemetry loader accepts `.json` event files
  (one JSON object per line) in addition to `.jsonl`
- Omit KS timing check when `gold_baseline_host` is unset (no false fail)

## [4.0.0] — 2026-07-26

### Added
- `ROADMAP.md` — locked maturity plan incorporating the existing UHBS-Lab harness
- Document status, RFC 2119 keywords, UHBS-Core / UHBS-Lab conformance levels
- `schemas/evidence-pack.schema.json`
- Conformance fixtures (proof labels only), including an anonymous Low-Interaction
  worked example UHQS **46.97** and POSIX-Shell lab UHQS **80.33** — see
  `docs/conformance/` (live Cowrie full lab later published as **48.70**)
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
- Docs state clearly that UHBS is a **personal beta framework**, not a
  multi-party standards body; committee, neutral org, and adopters moved to
  ROADMAP Phase 6 as aspirational (unchecked) goals
- Unified UHQS math into `uhbs_core.uhqs_math` (CLI + harness); missing scores
  raise instead of silent 0.0; Actions pinned by SHA; CI uses `constraints.txt`;
  PEP 639 license metadata; expanded integrity/CLI tests
- SEO / AEO / GEO discovery: site `llms.txt`, `llms-full.txt`, `robots.txt`,
  `humans.txt`, `.well-known/security.txt`, JSON-LD; repo `llms.txt` + `AGENTS.md`

### Pending (manual / ops / community — see ROADMAP Phase 6)
- PyPI Trusted Publishing + Sigstore signing (blocks MCP Registry `uvx` path)
- Zenodo DOI deposit
- Neutral GitHub organization transfer
- Multi-organization maintainers and independent adopters
