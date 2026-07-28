# Changelog

All notable changes to the UHBS specification and tooling are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/). Spec and CLI
share version **4.2.1** (`uhbs_core` ships in-tree as `uhbs[lab]`; MCP as `uhbs[mcp]`).

## [Unreleased]

### Added
- OpenSSF Best Practices **passing** badge
  ([project 13853](https://www.bestpractices.dev/projects/13853))
- Beelzebub **MCP** published lab grades (quick **43.04 / F**, full **42.93 / F**)
## [4.2.1] — 2026-07-28

Patch release after the first PyPI upload of `uhbs`.

### Changed
- README quickstart prefers official PyPI installs (`pip install 'uhbs[lab]'` /
  `'uhbs[mcp]'`); adds PyPI version badge; keeps editable install for
  development checkouts
- Package / schemas / fixtures / docs / Docker tags advertise **4.2.1**

### Fixed
- MkDocs `--strict` Deploy Documentation: Beelzebub MCP hub link to
  `architecture/mcp-honeypot-grading.md` (wrong relative depth)

## [4.2.0] — 2026-07-28

First **PyPI** release of `uhbs` (Trusted Publishing / OIDC + PEP 740 provenance).

### Added
- **MCP honeypot grading** (`mcp` protocol plugin): JSON-RPC lifecycle, tool
  allowlist + inputSchema denylist, schema-aware `tools/call`, SSE handshake
  hygiene, `surface_depth` / reason strings, TPS `mcp_server.yaml`, Beelzebub
  MCP lab inventory + docs (`docs/architecture/mcp-honeypot-grading.md`)
- SCORECARD / report extras: `MCP Surface Depth` and `MCP Surface Reason` when
  Module B sets metadata-only / interactive surface annotations
- Release workflow **PyPI Trusted Publishing** job (`publish-pypi`, environment
  `pypi`) for OIDC upload + PEP 740 provenance on `v*` tags
- Supply-chain checklists for PyPI Trusted Publishing and OpenSSF Best Practices
  passing submission (`docs/architecture/supply-chain.md`)
- Zenodo DOI badge + citation metadata (`10.5281/zenodo.21631156`; concept
  `10.5281/zenodo.21631155`)

### Changed
- Spec / package / schemas / fixtures / Docker tags advertise **4.2.0**
- `SECURITY.md` supported line: **4.2.x** (4.0.x security-fixes only)
- Core registry/TPS tests assert `mcp` plugin and packaged `mcp_server` profile

### Fixed
- Release `publish-pypi` staging finds wheel/sdist under nested
  `actions/download-artifact` paths

## [4.0.1] — 2026-07-27

Patch release for Zenodo DOI deposit and post-`v4.0.0` harness/docs work.
Published fixtures, reports, Docker tags, and docs now advertise `4.0.1`.

### Added
- **MCP server** (`uhbs[mcp]` / `uhbs-mcp`): local stdio tools for AI hosts
  (validate / UHQS / fixtures / schemas); `server.json` registry metadata;
  docs + landing `#mcp` section
- Published lab reports + landing Results: ESPot, miniprint, Conpot, Cowrie,
  OpenCanary, Beelzebub, Trapster, Dionaea, Endlessh (quick + full where applicable)
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
- **CI fix:** sync `tests/test_conformance.py` / `tests/test_mcp.py` fixture
  expectations to regraded UHQS values; add MkDocs `{#proto}` anchors on lab
  TUTORIALs; retarget architecture/plugin-authoring docs links to absolute
  GitHub URLs so `mkdocs build --strict` (Deploy Documentation) passes
- **Regraded** Cowrie, OpenCanary, ESPot, miniprint, Conpot, Endlessh, Beelzebub,
  Trapster, Dionaea under scoring-scale fixes (see prior Unreleased notes)
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
- GitHub Actions CI for schema validation and unit tests
- Templates for profiles (POSIX, Low-Interaction, ICS-SCADA)
- Initial RFCs under `docs/rfcs/`
- Mapping notes (ATT&CK / NIST / IEC 62443) as informative

### Changed
- Spec and package version aligned at **4.0.0**
- UHQS formula and Safety Gate documented as normative in
  `docs/specification/scoring-formula.md`

### Fixed
- N/A (initial public baseline cut)
