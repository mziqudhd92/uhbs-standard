# Changelog

All notable changes to the UHBS specification and tooling are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/). Spec and CLI
share version **4.4.4** (`uhbs_core` ships in-tree as `uhbs[lab]`; MCP as `uhbs[mcp]`;
AEP as `uhbs[aep]`; AEP SLM alpha as `uhbs[aep-slm]`).

## [Unreleased]

### Fixed
- Restore `web/package-lock.json` `debug@4.4.3` after a bulk UHBS version bump
  rewrote it to nonexistent `debug@4.4.4` and broke Pages `npm ci`
- Restore OpenSSF Best Practices badge on the README / PyPI hero
- AEP SLM size-cap: treat mid-read connection reset after a large partial body
  as oversize; drop flaky chunked HTTP integration case (unit-tested via FakeResp)

### Changed
- CI Validate also runs `npm ci` in `web/` so lockfile breakage fails before
  (or with) docs deploy

## [4.4.4] — 2026-08-03

Patch release: clean up PyPI/README hero presentation. **UHQS math unchanged.**

### Changed
- README intro for PyPI: remove informal org-move note, fewer clearer HTML
  badges, tighter summary links and metadata table
- Spec/package/schema/`uhbs_version` fixtures aligned to **4.4.4**

## [4.4.3] — 2026-08-03

Patch release: PyPI-safe HTML badges for License / Spec / UHQS. **UHQS math unchanged.**

### Fixed
- README Spec / UHQS / License badges use raw HTML `<a href><img>` so Warehouse
  cannot mis-resolve nested Markdown badge links under `pypi.org/project/uhbs/…`

### Changed
- Spec/package/schema/`uhbs_version` fixtures aligned to **4.4.3**

## [4.4.2] — 2026-08-03

Patch release: make all README links PyPI-safe (absolute URLs). **UHQS math unchanged.**

### Fixed
- Remaining relative README links (docs, LICENSE, source paths, `server.json`)
  now use absolute GitHub / Docs URLs so PyPI does not resolve them under
  `pypi.org/project/uhbs/…`

### Changed
- Spec/package/schema/`uhbs_version` fixtures aligned to **4.4.2**

## [4.4.1] — 2026-08-03

Patch release: fix PyPI README badge links. **UHQS math unchanged.**

### Fixed
- README badge targets for License / Spec / UHQS use absolute URLs so they work
  on PyPI (relative `docs/...` links previously resolved under
  `pypi.org/project/uhbs/…`)
- Landing copy no longer claims Module F is “new in v4.4.0” (bulk version bump
  artifact); AEP SLM size-cap unit coverage for Content-Length and chunked bodies

### Changed
- Spec/package/schema/`uhbs_version` fixtures aligned to **4.4.1**

## [4.4.0] — 2026-08-03

Minor release: MCP Python SDK **2.x** migration for the AI-host server, Dependabot
CI action bumps, and org-host AEO/GEO discovery polish. **UHQS math, weights, and
δ_C are unchanged.**

### Changed
- AI-host MCP server (`uhbs[mcp]`) now requires **`mcp>=2,<3`** (pinned
  `mcp==2.0.0` in `constraints.txt`). Migrated from `FastMCP` to
  `MCPServer` (`from mcp.server import MCPServer`) per the official SDK v2
  migration guide. Decorator tools/resources/prompts and stdio transport are
  unchanged for hosts.
- GitHub Actions dependency updates (Dependabot #7–#12, applied on `main`):
  - `mcp` 1.28.1 → 2.0.0 (with code migration above)
  - `github/codeql-action` → **v4.37.4** (init / autobuild / analyze / upload-sarif)
  - `ossf/scorecard-action` → **v2.4.4**
  - `actions/upload-artifact` → **v7.0.1** and
    `actions/download-artifact` → **v8.0.0** (paired for release artifacts)
  - `softprops/action-gh-release` → **v3.0.2**
- Repository and GitHub Pages moved to the **uhbs** organization:
  https://github.com/uhbs/uhbs-standard ·
  https://uhbs.github.io/uhbs-standard/
  (old `mziqudhd92/uhbs-standard` GitHub URL redirects; user Pages URL does not)
- SEO / AEO / GEO discovery refreshed for the org hosts (`llms.txt` discovery
  section, richer landing sitemap, PyPI project URLs, agent footer links,
  `/.well-known/security.txt` publish fix)
- Spec/package/schema/`uhbs_version` fixtures aligned to **4.4.0**

### Fixed
- AEP SLM alpha oversized-response test: treat peer connection reset after the
  size-cap abort as an oversize refusal (avoids flaky CI
  `ConnectionResetError` on `tests/test_aep_slm.py`)

## [4.3.6] — 2026-08-01

Patch release: optional **AEP SLM evaluator (alpha)** plus SEO/AEO/GEO discovery
refresh. **UHQS math, weights, and δ_C are unchanged.**

### Added
- Optional **AEP SLM evaluator (alpha)** — opt-in helper that can synthesize
  local AEP trial JSONL for offline `uhbs aep analyze`. Commands:
  `uhbs aep slm init|validate|status|generate`. Schema
  [`aep-slm.schema.json`](schemas/aep-slm.schema.json); disabled-by-default
  templates under [`examples/advanced-evidence/slm/`](examples/advanced-evidence/slm/);
  marker extra `uhbs[aep-slm]`. **Off until you edit** `aep-slm.yaml`
  (`enabled`, unlock phrase `I_ENABLE_AEP_SLM_ALPHA`, activation attestations).
  Providers: offline `mock` (default), local `recorded`, or loopback-only
  `openai_compatible` (no HTTP redirects; size-capped responses; strict JSON
  types). Writes trials + `slm-run.json` provenance only; **does not** change
  UHQS; not exposed via AI-host MCP.
  - Docs (MkDocs / GitHub Pages):
    [SLM evaluator (alpha)](https://uhbs.github.io/uhbs-standard/mkdocs/advanced-evidence/slm-alpha/)
  - Repo guide: [docs/advanced-evidence/slm-alpha.md](docs/advanced-evidence/slm-alpha.md)
  - Landing hub (AEP section): https://uhbs.github.io/uhbs-standard/#advanced-evidence
  - CLI cross-links: [AEP CLI](docs/advanced-evidence/cli.md) ·
    [tooling CLI](docs/tooling/cli.md)

### Changed
- SEO / GEO / AEO discovery surfaces updated for v4.3.6 (landing meta + JSON-LD,
  root sitemap index, robots/humans/llms, MkDocs structured data)
- Spec/package/schema/`uhbs_version` fixtures aligned to **4.3.6**

## [4.3.5] — 2026-07-31

Patch release: optional Advanced Evidence Profile (AEP), related-frameworks
comparison, lab/sandbox scope notices, human-friendly colored CLI output, and
README refresh. **UHQS math, weights, and δ_C are unchanged.**

### Added
- HoneyWire (andreicscs) **HTTP** lab grades for official WebRouterDecoy
  (quick **45.84 / F**, full **45.84 / F**)
- README lab demo GIF (`docs/assets/uhbs-lab-demo.gif`) — install Cowrie/Conpot,
  start decoys, full UHQS for Cowrie · Conpot · HellPot
- HellPot sanitized scorecard fixture (`hellpot-web-api.scorecard.json`)
- Informative [MITRE D3FEND](docs/mappings/d3fend.md) and
  [MITRE Engage](docs/mappings/engage.md) mappings
- Optional scorecard `framework_refs` (ATT&CK technique IDs + D3FEND technique
  IDs + Engage goals; display-only, ignored by UHQS math) on Cowrie / Conpot /
  HellPot fixtures — formalizes the "scorecards MAY attach ATT&CK IDs" note in
  [docs/mappings/attack.md](docs/mappings/attack.md)
- Evidence-graded [related frameworks](docs/mappings/related-frameworks.md)
  comparison (14 framework/model families)
- Optional **Advanced Evidence Profile (AEP)** — offline `uhbs aep` CLI
  (`init` / `example` / `validate` / `validate-trials` / `analyze` / `report`),
  schemas (`aep-experiment`, `aep-trial`, `advanced-evidence`), templates,
  synthetic examples packaged in the wheel, MkDocs docs, and `uhbs[aep]` extra.
  Informative only; **does not** change UHQS, weights, δ_C, or letter grades.
  Trust boundary: local file analysis only (no sockets/HTTP/SSH/subprocess/lab
  launch); explicitly **lab/sandbox evaluation** (not real-world production
  testing). Academic credit ledger for Zhu (2019), Collins et al. (2024),
  Ersok et al. (2022), Li et al. (2020) on docs + landing page
- Lab/sandbox NOTICE on stderr for `uhbs`, `uhbs-lab`, `uhbs-uhqs`, and
  `uhbs-mcp` (stdio-safe)
- ANSI-colored human-facing CLI lines via `uhbs_core.termui` (`NO_COLOR` /
  `FORCE_COLOR` supported; no extra color dependency)

### Fixed
- Ship JSON Schemas inside the `uhbs` wheel (`uhbs_cli/schemas/`) so
  `pip install 'uhbs[lab]'` can `validate-scorecard` without a git checkout
- AEP analyze without `--scorecard` (null provenance fields)
- `uhbs aep init --trials 1` and packaged template example strict validation

### Changed
- README restructured for open-source clarity (lab scope, extras matrix, AEP,
  security / CoC / citation)
- Docs and landing page emphasize lab/sandbox-only evaluation vs real-world
  production testing

## [4.3.0] — 2026-07-29

Minor release: fifteen new built-in protocol plugins (registry **36** protocols),
awesome-honeypots survey grades/skips, analyst-facing report/scorecard pages,
LDAP/Bluetooth harness hardening, and beta-status project framing (no “personal
project” posture language).

### Added
- Built-in protocol plugins: **mongodb**, **imap**, **kubernetes**, **dns**,
  **bluetooth**, **dhcp**, **httpproxy**, **ipp**, **irc**, **ldap**,
  **memcache**, **mssql**, **oracle**, **pjl**, **socks5** (with aliases;
  Module E P95 defaults; deferred-protocol list updated)
- Built-in protocol count is now **36** via `uhbs lab --list-protocols`
  / `list_protocols()` (includes prior ssh/http/mcp/…/generic set)
- CTI/blue-team analyst sections on report hubs + scorecard reading tables;
  READING-UHQS guide
- Analyst-facing report/scorecard pages: module tables + verbatim SCORECARD;
  scorecards index lists all published proofs
- Awesome-honeypots survey triage + deferred/skipped lists under
  `docs/conformance/awesome-honeypots/`
- Batch lab grades (quick+full): sshesame, ssh-honeypotd, HellPot,
  express-honeypot, mailoney, pghoney, mysql-honeypotd, Log4Pot,
  node-ftp-honeypot, SentryPeer, wordpot, MockSSH, Heralding (SSH/FTP),
  HoneyHTTPD, SHIVA, and additional Batch A–D publishes / skip notes
- Results UI: name/repo search + paginated list view; GitHub last-push dates
- ssh-auth-logger full grade + droberson/ssh-honeypot skip note
- Built-in **`pop3`** protocol plugin (RFC 1939; aliases `pop`, `pop-3`) with
  Module E P95 default
- GenAIPot (ls1911) **SMTP** + **POP3** published lab grades
- Elastichoney **HTTP**, alexbredo/honeypot-ftp **FTP**, and
  qeeqbox/honeypots multi-protocol lab grades
- Evaluation notes for **Acra** and **Ensnare** (skipped — not standalone
  protocol honeypots)

### Fixed
- MkDocs `--strict` Pages deploy was failing on broken scorecard links /
  missing `uhbs-run.log` links; published pages embed verbatim SCORECARD proof
- CI Validate: ruff import/line-length in socks5 tests; tests no longer read
  gitignored `.local/plugin-patches/`
- LDAP BER reader caps message size (64 KiB); Bluetooth soft-skip no longer
  claims `passed=True` when the RFCOMM path is unavailable
- Removed HellPot-copied untracked `labs/lophiid` stubs that could mis-grade
  HTTP if used

### Changed
- Package / schemas / fixtures / docs / Docker tags advertise **4.3.0**
- Project posture language: open-source **beta-status** evaluation framework
  (removed “personal project” framing from docs, landing, MCP, discovery files)
- Plugin-authoring documents lab-target safety for proxy/DNS/DHCP/IMAP probes

## [4.2.2] — 2026-07-28

Minor release: new protocol plugins (`postgres`, `s7comm`), multi-honeypot lab
grades for GitHub Pages, and MCP client resilience under honeypot rate limits.

### Added
- Built-in **`postgres`** protocol plugin (StartupMessage / SSLRequest /
  Authentication* / auth-deny; alias `postgresql`) with Module E P95 default
- Built-in **`s7comm`** protocol plugin (ISO-on-TCP / COTP CC / S7 Setup
  Communication; aliases `s7`, `iso-tsap`, `isotp`, `iso_on_tcp`) with Module E
  P95 default
- HoneyMCP **MCP** published lab grades (quick **43.04 / F**, full **42.93 / F**)
  — Streamable HTTP `/mcp` (aws-admin); lab rate-limit override documented in
  `docs/conformance/reports/honeymcp/METHODOLOGY.md`
- LLM Honeypot (Palisade) **SSH** published lab grades (quick **67.94 / D**,
  full **61.17 / D**) — Cowrie overlays; Telnet disabled in shipped cfg
- HoneyAgents **SSH** published lab grades (quick **67.94 / D**, full **65.24 / D**)
  — stock Cowrie honeypot service; nginx/AutoGen out of UHQS decoy scope
- DataTrap (Thales dd-honeypot) multi-protocol lab grades (SSH / HTTP / MySQL /
  Redis / Telnet / PostgreSQL)
- LLMPot (momalab) Modbus + S7comm + HTTP lab grades
  — Modbus quick **38.48 / F**, full **55.24 / D** (HF CPU adapter);
  S7comm quick **45.53 / F**, full **65.41 / D** (Snap7 NoLogic gold);
  HTTP quick **45.84 / F**, full **63.11 / D**
- OpenSSF Best Practices **passing** badge
  ([project 13853](https://www.bestpractices.dev/projects/13853))
- Beelzebub **MCP** published lab grades (quick **43.04 / F**, full **42.93 / F**)
  (also reflected on Results hub)

### Fixed
- MCP client retries HTTP **429** with backoff (HoneyMCP-style Wait-for prose /
  `Retry-After`); Module A timing reuses one session for `tools/list` RTT samples
  so per-IP honeypot governors are not burned by full re-init storms

### Changed
- Package / schemas / fixtures / docs / Docker tags advertise **4.2.2**

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
