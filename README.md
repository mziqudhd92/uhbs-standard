# Universal Honeypot Benchmarking Standard (UHBS)

[![CI](https://github.com/mziqudhd92/uhbs-standard/actions/workflows/ci-validate.yml/badge.svg)](https://github.com/mziqudhd92/uhbs-standard/actions/workflows/ci-validate.yml)
[![Docs](https://github.com/mziqudhd92/uhbs-standard/actions/workflows/deploy-docs.yml/badge.svg)](https://mziqudhd92.github.io/uhbs-standard/)
[![CodeQL](https://github.com/mziqudhd92/uhbs-standard/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/mziqudhd92/uhbs-standard/actions/workflows/codeql-analysis.yml)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/13853/badge)](https://www.bestpractices.dev/projects/13853)
[![PyPI](https://img.shields.io/pypi/v/uhbs.svg)](https://pypi.org/project/uhbs/)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21631156-blue)](https://doi.org/10.5281/zenodo.21631156)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Spec](https://img.shields.io/badge/Specification-v4.2.2-indigo.svg)](docs/specification/core-principles.md)
[![UHQS](https://img.shields.io/badge/UHQS-0%E2%80%93100-success.svg)](docs/specification/scoring-formula.md)

> An objective, repeatable, quantitative methodology for deception technology evaluation — a **personal open-source beta framework** for comparing and grading honeypots and decoy systems by class and protocol.

**UHBS v4.2.2** is a protocol-agnostic, **vendor-neutral** evaluation framework for measuring deception realism, safety containment, operational scale, and telemetry quality. It is **not** an industry consortium standard or multi-party governed body — see [ROADMAP.md](ROADMAP.md) for what maturity would require.

## Project status

**Status:** Beta / Experimental · personal project ([specification status](docs/specification/status.md)).

- **Author / maintainer:** [@mziqudhd92](https://github.com/mziqudhd92) — see [MAINTAINERS.md](MAINTAINERS.md)
- **Governance claims:** no Steering Committee, no independent adopter list yet — those are [roadmap goals](ROADMAP.md#phase-6--community-maturity-aspirational--not-done)
- **Suggested use:** organizations **MAY** use the Production Baseline Profile (**UHQS > 80** + passing Safety Gate) as an *internal* evaluation gate; that is a recommendation in the beta, not a mandate from any standards body

## Why UHBS?

| Pillar | What it delivers |
| --- | --- |
| **Protocol-Agnostic** | Architecture-neutral testing across IT, OT/ICS, AI, and Cloud |
| **Vendor-Neutral** | Class- and protocol-based evaluation — no product or brand endorsements |
| **Quantitative Scoring** | Normalized **UHQS 0–100** composite with a non-linear Safety Gate |
| **Six Evaluation Modules** | Modules A–F covering fidelity, behavior, telemetry, safety, scale, and audit |
| **Production Baseline** | **UHQS > 80** suggested as an internal gate (RECOMMENDED in the beta) |

> **Vendor-neutral** beta framework: compare any deception by class and protocol.
> Install from PyPI: `pip install 'uhbs[lab]'` → `uhbs-lab` / `uhbs lab`.
> Named product proof lives only under [conformance fixtures](docs/conformance/index.md).
> Maturity goals (committee, adopters, neutral org): [ROADMAP.md](ROADMAP.md).

## Quickstart

```bash
# Official PyPI install (CLI + lab harness)
pip install 'uhbs[lab]'

# Optional: AI-host MCP tools (validate/score fixtures — no live lab probes)
pip install 'uhbs[mcp]'
```

Validate a honeypot against a Target Profile Specification (`profile.yaml`):

```bash
# From a checkout (templates live in the repo) or your own profile file
cp templates/profile.yaml ./my-honeypot.profile.yaml   # if you cloned the repo
uhbs validate-profile my-honeypot.profile.yaml
```

From a git checkout (editable / development):

```bash
pip install -e ".[lab,dev]"
```

Run a full scorecard validation once your audit harness produces results:

```bash
uhbs validate-scorecard path/to/scorecard.json
uhbs score --profile my-honeypot.profile.yaml --scores scores.json
```

### MCP (AI hosts — Cursor, Claude, VS Code, …)

Install the optional MCP extra so agents can call validators / UHQS scoring over
the [Model Context Protocol](https://modelcontextprotocol.io/) (local stdio):

```bash
pip install 'uhbs[mcp]'
# Configure your host — see docs/tooling/mcp.md
# Cursor / Claude example uses: uhbs-mcp  or  python -m uhbs_mcp
# Set UHBS_ROOT to a checkout if you need fixtures/docs from the repo
```

Registry metadata: [`server.json`](server.json). Live Docker lab probes stay on the CLI (`uhbs lab`), not MCP.

### MCP honeypot grading (`uhbs[lab]`)

Grade network-facing MCP decoys (JSON-RPC over HTTP/SSE) with the in-tree `mcp` protocol plugin — distinct from the AI-host MCP server above:

```bash
pip install 'uhbs[lab]'
uhbs-lab --list-protocols   # includes mcp
# Lab inventories/TPS live in the git repo (or your own paths):
uhbs-lab \
  --inventory docs/conformance/labs/beelzebub/inventory.yaml \
  --target beelzebub-mcp \
  --tps docs/conformance/labs/beelzebub/web_api_mcp_quick.yaml \
  --protocol mcp \
  --out ./reports/mcp
```

Details: [docs/architecture/mcp-honeypot-grading.md](docs/architecture/mcp-honeypot-grading.md). PyPI: https://pypi.org/project/uhbs/

### Docker (grade without a local Python install)

Build the grading image (CLI + UHBS-Lab harness):

```bash
docker build -t uhbs:4.2.2 .
# or: docker compose build
```

Mount your working directory at `/work` and pass the same `uhbs` commands:

```bash
# Validate a scorecard on disk
docker run --rm -v "$PWD:/work" -w /work uhbs:4.2.2 \
  validate-scorecard ./docs/conformance/fixtures/cowrie-low-interaction.scorecard.json

# Compute UHQS from module scores
docker run --rm -v "$PWD:/work" -w /work uhbs:4.2.2 \
  score --class Low-Interaction --scores ./scores.json

# List protocol plugins / run a lab probe against a reachable honeypot
docker run --rm -v "$PWD:/work" -w /work uhbs:4.2.2 lab --list-protocols
docker run --rm -v "$PWD:/work" -w /work \
  -e UHBS_QUICK=1 -e UHBS_AIRGAP_ATTESTED=1 \
  uhbs:4.2.2 lab \
    --tps low_interaction \
    --protocol ssh \
    --target host.docker.internal --port 2222 \
    --source-root /work \
    --phases profile,static,dynamic,score \
    --quick \
    --out /work/.local/bench-reports/my-target
```

Compose shorthand: `docker compose run --rm uhbs validate-profile ./my-honeypot.profile.yaml`.

Documentation site: **[https://mziqudhd92.github.io/uhbs-standard/](https://mziqudhd92.github.io/uhbs-standard/)** (landing hub) · **[docs / MkDocs](https://mziqudhd92.github.io/uhbs-standard/mkdocs/)**  
Maturity roadmap: **[ROADMAP.md](ROADMAP.md)** · Reference harness: **[docs/reference-implementation.md](docs/reference-implementation.md)** · CLI guide: **[docs/tooling/cli.md](docs/tooling/cli.md)**

### Discovery for search & AI agents (SEO / AEO / GEO)

| File | Purpose |
| --- | --- |
| [llms.txt](llms.txt) (repo) · [site llms.txt](https://mziqudhd92.github.io/uhbs-standard/llms.txt) | Curated index for coding / answer agents |
| [AGENTS.md](AGENTS.md) | Rules for assistants editing this repo |
| [CITATION.cff](CITATION.cff) | Formal citation metadata |
| Site [robots.txt](https://mziqudhd92.github.io/uhbs-standard/robots.txt) · [sitemap.xml](https://mziqudhd92.github.io/uhbs-standard/mkdocs/sitemap.xml) | Crawler hints |

## Scoring Summary (UHQS 4.2.2)

The **Universal Honeypot Quality Score (UHQS)** is a normalized composite from **0 to 100**:

\[
\mathrm{UHQS} = \delta_C \cdot (w_A S_A + w_B S_B + w_C S_C + w_E S_E + w_F S_F)
\]

- \(S_A \ldots S_F\) — normalized module scores (0–100)
- \(w_A \ldots w_F\) — profile-adaptive weights (sum to 1.00)
- \(\delta_C\) — **Safety Gate** from Module D (Containment):  
  \(\delta_C = 1.0\) if \(C \ge 95\); otherwise \(\delta_C = (C/100)^2\)

Production deployment requires **UHQS > 80** and a passing Safety Gate. A decoy with excellent deception scores can still fail evaluation if Module D falls below the gate. See [Scoring Formula](docs/specification/scoring-formula.md).

## Audit Workflow (5 Phases)

```text
┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│  Phase 1    │──▶│  Phase 2    │──▶│  Phase 3    │──▶│  Phase 4    │──▶│  Phase 5    │
│  Profile &  │   │  Static     │   │  Sandbox    │   │  Dynamic    │   │  Score &    │
│  Config     │   │  Audit (F)  │   │  Provision  │   │  Modules A–E│   │  Report     │
└─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘
```

1. **Configuration & Profile Setup** — Define `profile.yaml`, protocol expectations, baselines  
2. **Static Audit Execution** — Analyze repository, container build manifests, and system prompts  
3. **Sandbox Environment Provisioning** — Isolated runtime with egress monitors  
4. **Dynamic Adversarial Execution** — Modules A–E via automated harnesses  
5. **Score Computation & Reporting** — Apply \(\delta_C\) and emit the standard scorecard  

## Repository Layout

```text
uhbs-standard/
├── docs/                 # Website + Docs-as-Code (MkDocs → GitHub Pages)
│   └── conformance/
│       ├── fixtures/     # Sanitized scorecard JSON
│       └── reports/      # Quick + full lab artifacts + tutorials (named proof)
├── schemas/              # JSON Schemas for profiles & scorecards
├── templates/            # Starter profile.yaml for framework users
├── src/uhbs_cli/         # Validation CLI
├── src/uhbs_core/        # UHBS-Lab reference harness
├── Dockerfile            # Grading image (uhbs CLI + lab)
├── Dockerfile.full       # Grading image + Module F SAST tools
├── docker-compose.yml    # Mount-cwd helper for the grading image
├── GOVERNANCE.md         # Project notes (personal maintainer; not a committee)
├── SECURITY.md           # Vulnerability disclosure policy
└── CITATION.cff          # Citation metadata
```

## Modules at a Glance

| Module | Focus |
| --- | --- |
| **A** | Protocol & Syntax Fidelity |
| **B** | Behavioral & Stateful Realism |
| **C** | Telemetry Quality & Pipeline Resilience |
| **D** | Safety, Containment & Boundary Controls (**Safety Gate**) |
| **E** | Scalability, Latency & Stress Performance |
| **F** | White-Box Static Code Audit |

## Embed Your Grade

After publishing an official scorecard, maintainers can embed:

```markdown
![UHBS v4.2.2](https://img.shields.io/badge/UHBS%20v4.2.2-Grade%20A-brightgreen)
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) and [GOVERNANCE.md](GOVERNANCE.md). Specification changes go through an **RFC** process. By contributing, you agree to the [Developer Certificate of Origin (DCO)](https://developercertificate.org/) (sign-off required on commits).

## Citation

```bibtex
@software{uhbs2026,
  author = {Zavdi, Moran},
  title = {Universal Honeypot Benchmarking Standard (UHBS)},
  year = {2026},
  version = {4.2.2},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.21631156},
  url = {https://doi.org/10.5281/zenodo.21631156}
}
```

Or use the machine-readable [`CITATION.cff`](CITATION.cff). Concept DOI (always resolves to the latest deposit): [10.5281/zenodo.21631155](https://doi.org/10.5281/zenodo.21631155).

## License

Licensed under the [Apache License 2.0](LICENSE).

---

An objective, repeatable, quantitative methodology for deception technology evaluation — providing cybersecurity professionals with a non-biased baseline for comparing and grading honeypots and decoy systems.
