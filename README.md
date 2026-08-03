# Universal Honeypot Benchmarking Standard (UHBS)

<a href="https://github.com/uhbs/uhbs-standard/actions/workflows/ci-validate.yml"><img alt="CI" src="https://github.com/uhbs/uhbs-standard/actions/workflows/ci-validate.yml/badge.svg"></a>
<a href="https://uhbs.github.io/uhbs-standard/"><img alt="Docs" src="https://img.shields.io/badge/docs-uhbs.github.io-blue"></a>
<a href="https://pypi.org/project/uhbs/"><img alt="PyPI" src="https://img.shields.io/pypi/v/uhbs.svg"></a>
<a href="https://www.bestpractices.dev/projects/13853"><img alt="OpenSSF Best Practices" src="https://www.bestpractices.dev/projects/13853/badge"></a>
<a href="https://github.com/uhbs/uhbs-standard/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/badge/License-Apache%202.0-blue.svg"></a>
<a href="https://uhbs.github.io/uhbs-standard/mkdocs/specification/core-principles/"><img alt="Spec" src="https://img.shields.io/badge/Specification-v4.4.4-indigo.svg"></a>
<a href="https://uhbs.github.io/uhbs-standard/mkdocs/specification/scoring-formula/"><img alt="UHQS" src="https://img.shields.io/badge/UHQS-0--100-success.svg"></a>
<a href="https://doi.org/10.5281/zenodo.21631156"><img alt="DOI" src="https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21631156-blue"></a>

Open-source **beta** framework for **lab / sandbox** evaluation of honeypots and decoys — vendor-neutral **UHQS** scoring (0–100) with a non-linear Safety Gate.

**UHBS v4.4.4** measures deception realism, containment, scale, and telemetry quality by **class and protocol**. It is **not** an industry consortium standard or multi-party governed body. Source and docs: [github.com/uhbs/uhbs-standard](https://github.com/uhbs/uhbs-standard) · [uhbs.github.io/uhbs-standard](https://uhbs.github.io/uhbs-standard/) · [ROADMAP](https://github.com/uhbs/uhbs-standard/blob/main/ROADMAP.md).

| | Link |
| --- | --- |
| **Docs** | [Landing](https://uhbs.github.io/uhbs-standard/) · [MkDocs](https://uhbs.github.io/uhbs-standard/mkdocs/) |
| **Install** | `pip install uhbs` · extras: `lab`, `mcp`, `aep` |
| **Python** | ≥ 3.11 |
| **License** | [Apache-2.0](https://github.com/uhbs/uhbs-standard/blob/main/LICENSE) |

> **NOTICE:** UHBS/AEP are for **lab/sandbox evaluation of decoys**. Do **not** run them against production or unauthorized real services. CLI tools print this reminder on stderr when commands run.

## Table of contents

- [Project status](#project-status)
- [What you get](#what-you-get)
- [Install](#install)
- [Quickstart](#quickstart)
- [Demo](#demo)
- [Scoring (UHQS)](#scoring-uhqs)
- [Optional Advanced Evidence Profile (AEP)](#optional-advanced-evidence-profile-aep)
- [Documentation map](#documentation-map)
- [Repository layout](#repository-layout)
- [Contributing](#contributing)
- [Security](#security)
- [Citation](#citation)
- [License](#license)

## Project status

**Status:** Beta / Experimental — [specification status](https://uhbs.github.io/uhbs-standard/mkdocs/specification/status/)

| Topic | Reality today |
| --- | --- |
| Maintainer | [@mziqudhd92](https://github.com/mziqudhd92) — [MAINTAINERS.md](https://github.com/uhbs/uhbs-standard/blob/main/MAINTAINERS.md) |
| Governance | Single maintainer; no Steering Committee yet — [Phase 6 roadmap](https://github.com/uhbs/uhbs-standard/blob/main/ROADMAP.md#phase-6--community-maturity-aspirational--not-done) |
| Evaluation scope | **Laboratory / sandbox only** |
| Suggested internal gate | After lab grading, orgs **MAY** use **UHQS > 80** + passing Safety Gate before *they* deploy a decoy — not a standards-body mandate |

## What you get

| Capability | Package / surface |
| --- | --- |
| Spec + schemas (TPS, scorecard, evidence) | Repo `docs/` · `schemas/` |
| Validate profiles & scorecards; recompute UHQS | `pip install uhbs` → `uhbs` |
| Live Modules A–F lab harness (**36** protocols) | `pip install 'uhbs[lab]'` → `uhbs lab` / `uhbs-lab` |
| AI-host MCP tools (validate/score fixtures; no live probes) | `pip install 'uhbs[mcp]'` → `uhbs-mcp` |
| Offline Advanced Evidence Profile (optional; does not change UHQS) | `pip install 'uhbs[aep]'` → `uhbs aep` |
| AEP SLM trial generator (alpha; **off until you edit config**) | `pip install 'uhbs[aep-slm]'` → `uhbs aep slm` |
| Published lab grades / fixtures | [docs/conformance/](https://uhbs.github.io/uhbs-standard/mkdocs/conformance/) |

**Vendor neutrality:** normative docs use classes and protocols. Named products appear only under conformance as evaluation **proof**, not as UHBS requirements.

| Pillar | Detail |
| --- | --- |
| Protocol-agnostic | IT, OT/ICS, AI, and cloud decoy classes |
| Quantitative | UHQS 0–100 with Safety Gate \(\delta_C\) from Module D |
| Dual-plane | Static audit (F) + dynamic Modules A–E |
| Optional AEP | Lab decoy-vs-reference evidence (VoD, FSV, DTDR, EER) |

## Install

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Core CLI (validate / score)
pip install uhbs

# Common lab install
pip install 'uhbs[lab]'

# Optional extras (install only what you need)
pip install 'uhbs[mcp]'   # AI-host MCP server
pip install 'uhbs[aep]'       # offline Advanced Evidence Profile
pip install 'uhbs[aep-slm]'   # alpha SLM trial helper (still off until you edit config)
pip install 'uhbs[all]'       # lab + mcp + scapy (convenience; still not an attack runner)
```

| Extra | Purpose |
| --- | --- |
| *(none)* | Validators + UHQS math |
| `lab` | Controlled live Modules A–F harness |
| `mcp` | Local AI-host scorecard tools (stdio MCP) |
| `aep` | Offline advanced evidence analysis |
| `aep-slm` | Alpha AEP SLM trial generator (**disabled until you edit `aep-slm.yaml`**) |
| `scapy` | Optional protocol-encoding backend |
| `dev` | pytest, ruff, mypy (+ lab/mcp for contributors) |
| `all` | `lab` + `mcp` + `scapy` |

Development checkout:

```bash
git clone https://github.com/uhbs/uhbs-standard.git
cd uhbs-standard
pip install -e ".[lab,dev]"
# optional: pip install -e ".[aep,mcp]"
pytest -q
```

## Quickstart

### 1. Validate a profile or scorecard

```bash
# From a git checkout (templates ship in the repo)
cp templates/profile.yaml ./my-honeypot.profile.yaml
uhbs validate-profile my-honeypot.profile.yaml

uhbs validate-scorecard path/to/scorecard.json
uhbs score --class Low-Interaction --scores scores.json
```

### 2. Run the lab harness (isolated decoy only)

```bash
pip install 'uhbs[lab]'
uhbs lab --list-protocols
# Example shape — point only at a lab decoy you control:
# uhbs lab --tps low_interaction --protocol ssh \
#   --target 127.0.0.1 --port 2222 --out ./.local/bench-reports/my-target
```

### 3. Optional AEP (offline lab evidence)

```bash
pip install 'uhbs[aep]'
uhbs aep example beginner --out aep-beginner
uhbs aep validate aep-beginner/experiment.yaml
uhbs aep analyze --experiment aep-beginner/experiment.yaml \
  --trials aep-beginner/trials.jsonl \
  --scorecard aep-beginner/linked-scorecard.json \
  --out advanced-evidence.json
uhbs aep report advanced-evidence.json --format markdown --out ADVANCED-EVIDENCE.md
```

### 3b. Optional AEP SLM alpha (off by default)

Draft AEP trial JSONL with a deterministic mock or a loopback-only local model.
**Install does not enable it** — edit `aep-slm.yaml` first. Does not change UHQS.
Guide: [SLM evaluator (alpha)](https://uhbs.github.io/uhbs-standard/mkdocs/advanced-evidence/slm-alpha/).

```bash
pip install 'uhbs[aep-slm]'
uhbs aep slm init --out aep-slm.yaml
uhbs aep slm status aep-slm.yaml          # shows LOCKED until you edit the file
# Edit aep-slm.yaml: enabled + unlock phrase + attestations (see docs)
# uhbs aep slm generate aep-slm.yaml
```

### MCP for AI hosts (Cursor, Claude, VS Code, …)

```bash
pip install 'uhbs[mcp]'
# Configure the host — see docs/tooling/mcp.md
# uhbs-mcp   or:  python -m uhbs_mcp
```

Registry metadata: [`server.json`](https://github.com/uhbs/uhbs-standard/blob/main/server.json). Live lab probes stay on `uhbs lab`, not the AI-host MCP server.

Grade **MCP honeypot** surfaces (JSON-RPC over HTTP/SSE) with the in-tree `mcp` **protocol plugin** (`uhbs[lab]`) — different from the AI-host server above. See [MCP honeypot grading](https://github.com/uhbs/uhbs-standard/blob/main/docs/architecture/mcp-honeypot-grading.md).

### Docker

```bash
docker build -t uhbs:4.4.4 .
docker run --rm -v "$PWD:/work" -w /work uhbs:4.4.4 \
  validate-scorecard ./docs/conformance/fixtures/cowrie-low-interaction.scorecard.json
docker run --rm -v "$PWD:/work" -w /work uhbs:4.4.4 lab --list-protocols
```

Compose: `docker compose run --rm uhbs validate-profile ./my-honeypot.profile.yaml`.

## Demo

Terminal walkthrough: install UHBS + Cowrie/Conpot, start lab decoys, full UHQS
(Cowrie SSH · Conpot Modbus · HellPot HTTP).

![UHBS lab demo — install honeypots + full UHQS](https://github.com/uhbs/uhbs-standard/blob/main/docs/assets/uhbs-lab-demo.gif)

Replay: [`docs/assets/uhbs-lab-demo.cast`](https://github.com/uhbs/uhbs-standard/blob/main/docs/assets/uhbs-lab-demo.cast)
(`asciinema play docs/assets/uhbs-lab-demo.cast`).

## Scoring (UHQS)

The **Universal Honeypot Quality Score** is a normalized composite **0–100**:

\[
\mathrm{UHQS} = \delta_C \cdot (w_A S_A + w_B S_B + w_C S_C + w_E S_E + w_F S_F)
\]

| Symbol | Meaning |
| --- | --- |
| \(S_A \ldots S_F\) | Module scores 0–100 |
| \(w_A \ldots w_F\) | Profile-adaptive weights (sum to 1.00) |
| \(\delta_C\) | Safety Gate from Module D: \(1.0\) if \(C \ge 95\), else \((C/100)^2\) |

| Module | Focus |
| --- | --- |
| **A** | Protocol & syntax fidelity |
| **B** | Behavioral & stateful realism |
| **C** | Telemetry quality & pipeline resilience |
| **D** | Safety, containment & boundary controls (**Safety Gate**) |
| **E** | Scalability, latency & stress |
| **F** | White-box static code audit |

A decoy with strong deception scores can still fail lab evaluation if Module D is weak. Normative math: [`uhqs_math.py`](https://github.com/uhbs/uhbs-standard/blob/main/src/uhbs_core/uhqs_math.py) · [scoring formula](https://uhbs.github.io/uhbs-standard/mkdocs/specification/scoring-formula/).

### Lab audit workflow (5 phases)

```text
Profile & config → Static audit (F) → Sandbox provision → Dynamic A–E → Score & report
```

## Optional Advanced Evidence Profile (AEP)

UHQS remains the normative lab grade. **AEP** is an optional, informative layer for
controlled **lab** decoy-vs-reference experiments. **AEP does not change UHQS.**

| When | Use |
| --- | --- |
| Lab release / conformance | UHBS scorecard alone |
| Comparative lab study | Add AEP (`VoD`, `FSV`, `DTDR`, `EER` + uncertainty) |

- Offline analysis of local experiment/trial files only — no attack launch
- Status vocabulary: `valid | inconclusive | control_failed` (not letter grades)
- Packaged examples: `uhbs aep example beginner|advanced|template`

**Academic credit** (citation ≠ endorsement): Zhu (2019), Collins et al. (2024),
Ersok et al. (2022), Li et al. (2020) — full ledger:
[Research foundations & credits](https://uhbs.github.io/uhbs-standard/mkdocs/advanced-evidence/research-foundations/).

| Doc | URL |
| --- | --- |
| Overview | https://uhbs.github.io/uhbs-standard/mkdocs/advanced-evidence/ |
| Beginner tutorial | https://uhbs.github.io/uhbs-standard/mkdocs/advanced-evidence/tutorial-beginner/ |
| CLI | https://uhbs.github.io/uhbs-standard/mkdocs/advanced-evidence/cli/ |
| SLM evaluator (alpha, opt-in) | https://uhbs.github.io/uhbs-standard/mkdocs/advanced-evidence/slm-alpha/ |
| Landing hub (AEP section) | https://uhbs.github.io/uhbs-standard/#advanced-evidence |
| Related frameworks | https://uhbs.github.io/uhbs-standard/mkdocs/mappings/related-frameworks/ |

## Documentation map

| Resource | Link |
| --- | --- |
| Landing hub | https://uhbs.github.io/uhbs-standard/ |
| Specification | https://uhbs.github.io/uhbs-standard/mkdocs/specification/core-principles/ |
| Sitemap index (SEO) | https://uhbs.github.io/uhbs-standard/sitemap.xml |
| CLI guide | [docs/tooling/cli.md](https://uhbs.github.io/uhbs-standard/mkdocs/tooling/cli/) |
| MCP (AI hosts) | [docs/tooling/mcp.md](https://uhbs.github.io/uhbs-standard/mkdocs/tooling/mcp/) |
| AEP SLM (alpha) | https://uhbs.github.io/uhbs-standard/mkdocs/advanced-evidence/slm-alpha/ |
| Reference harness | [docs/reference-implementation.md](https://uhbs.github.io/uhbs-standard/mkdocs/reference-implementation/) |
| Conformance & lab reports | [docs/conformance/index.md](https://uhbs.github.io/uhbs-standard/mkdocs/conformance/) |
| Framework mappings | [docs/mappings/index.md](https://uhbs.github.io/uhbs-standard/mkdocs/mappings/) |
| Maturity roadmap | [ROADMAP.md](https://github.com/uhbs/uhbs-standard/blob/main/ROADMAP.md) |
| Agent / SEO / AEO index | [llms.txt](https://uhbs.github.io/uhbs-standard/llms.txt) · [AGENTS.md](https://github.com/uhbs/uhbs-standard/blob/main/AGENTS.md) · [humans.txt](https://uhbs.github.io/uhbs-standard/humans.txt) |

## Repository layout

```text
uhbs-standard/
├── docs/                      # MkDocs site + conformance proof
│   ├── advanced-evidence/     # Optional AEP docs
│   ├── conformance/           # Fixtures, lab reports, tutorials
│   ├── mappings/              # ATT&CK, D3FEND, Engage, related frameworks
│   └── specification/         # Normative prose
├── schemas/                   # JSON Schemas (scorecard, AEP, …)
├── templates/                 # Starter TPS + AEP templates
├── examples/advanced-evidence/# Synthetic AEP fixtures (also packaged in wheel)
├── src/uhbs_cli/              # `uhbs` CLI (+ packaged schemas / AEP data)
├── src/uhbs_core/             # UHBS-Lab harness + UHQS math
├── src/uhbs_mcp/              # AI-host MCP server
├── tests/                     # pytest suite
├── Dockerfile                 # Grading image
├── CONTRIBUTING.md · CODE_OF_CONDUCT.md · SECURITY.md · GOVERNANCE.md
└── CITATION.cff
```

## Embed a published grade

After you publish a scorecard (conformance / your own report), you can badge it:

```markdown
![UHBS v4.4.4](https://img.shields.io/badge/UHBS%20v4.4.4-Grade%20A-brightgreen)
```

## Contributing

Contributions are welcome under the project’s governance constraints.

1. Read [CONTRIBUTING.md](https://github.com/uhbs/uhbs-standard/blob/main/CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](https://github.com/uhbs/uhbs-standard/blob/main/CODE_OF_CONDUCT.md)
2. Follow [GOVERNANCE.md](https://github.com/uhbs/uhbs-standard/blob/main/GOVERNANCE.md) — specification changes use an **RFC** process
3. Sign off commits ([DCO](https://developercertificate.org/))
4. Run `pytest -q` and `ruff check` on touched Python before opening a PR

## Security

Please report vulnerabilities via [GitHub Security Advisories](https://github.com/uhbs/uhbs-standard/security/advisories/new)
per [SECURITY.md](https://github.com/uhbs/uhbs-standard/blob/main/SECURITY.md). Do not use UHBS tooling against systems you are
not authorized to test.

## Citation

```bibtex
@software{uhbs2026,
  author = {Zavdi, Moran},
  title = {Universal Honeypot Benchmarking Standard (UHBS)},
  year = {2026},
  version = {4.4.4},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.21631156},
  url = {https://doi.org/10.5281/zenodo.21631156}
}
```

Machine-readable: [`CITATION.cff`](https://github.com/uhbs/uhbs-standard/blob/main/CITATION.cff). Concept DOI (latest deposit):
[10.5281/zenodo.21631155](https://doi.org/10.5281/zenodo.21631155).

## License

Licensed under the [Apache License 2.0](https://github.com/uhbs/uhbs-standard/blob/main/LICENSE).
