# Universal Honeypot Benchmarking Standard (UHBS)

[![CI](https://github.com/mziqudhd92/uhbs-standard/actions/workflows/ci-validate.yml/badge.svg)](https://github.com/mziqudhd92/uhbs-standard/actions/workflows/ci-validate.yml)
[![Docs](https://github.com/mziqudhd92/uhbs-standard/actions/workflows/deploy-docs.yml/badge.svg)](https://mziqudhd92.github.io/uhbs-standard/)
[![CodeQL](https://github.com/mziqudhd92/uhbs-standard/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/mziqudhd92/uhbs-standard/actions/workflows/codeql-analysis.yml)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Spec](https://img.shields.io/badge/Specification-v4.0.0-indigo.svg)](docs/specification/core-principles.md)
[![UHQS](https://img.shields.io/badge/UHQS-0%E2%80%93100-success.svg)](docs/specification/scoring-formula.md)

> An objective, repeatable, quantitative methodology for deception technology evaluation — a **personal open-source draft framework** for comparing and grading honeypots and decoy systems by class and protocol.

**UHBS v4.0** is a protocol-agnostic, **vendor-neutral** evaluation framework for measuring deception realism, safety containment, operational scale, and telemetry quality. It is **not** an industry consortium standard or multi-party governed body — see [ROADMAP.md](ROADMAP.md) for what maturity would require.

## Project status

**Status:** Draft / Experimental · personal project ([specification status](docs/specification/status.md)).

- **Author / maintainer:** [@mziqudhd92](https://github.com/mziqudhd92) — see [MAINTAINERS.md](MAINTAINERS.md)
- **Governance claims:** no Steering Committee, no independent adopter list yet — those are [roadmap goals](ROADMAP.md#phase-6--community-maturity-aspirational--not-done)
- **Suggested use:** organizations **MAY** use the Production Baseline Profile (**UHQS > 80** + passing Safety Gate) as an *internal* evaluation gate; that is a recommendation in the draft, not a mandate from any standards body

## Why UHBS?

| Pillar | What it delivers |
| --- | --- |
| **Protocol-Agnostic** | Architecture-neutral testing across IT, OT/ICS, AI, and Cloud |
| **Vendor-Neutral** | Class- and protocol-based evaluation — no product or brand endorsements |
| **Quantitative Scoring** | Normalized **UHQS 0–100** composite with a non-linear Safety Gate |
| **Six Evaluation Modules** | Modules A–F covering fidelity, behavior, telemetry, safety, scale, and audit |
| **Production Baseline** | **UHQS > 80** suggested as an internal gate (RECOMMENDED in the draft) |

> **Vendor-neutral** draft framework: compare any deception by class and protocol.
> UHBS-Lab harness: `pip install -e '.[lab]'` → `uhbs-lab` / `uhbs lab`.
> Named product proof lives only under [conformance fixtures](docs/conformance/index.md).
> Maturity goals (committee, adopters, neutral org): [ROADMAP.md](ROADMAP.md).

## Quickstart

Validate a honeypot against a Target Profile Specification (`profile.yaml`) in three steps:

```bash
# 1. Install the CLI (add [lab] for the Modules A–F harness)
pip install -e ".[lab]"

# 2. Create or adapt a target profile
cp templates/profile.yaml ./my-honeypot.profile.yaml

# 3. Validate the profile against the official schema
uhbs validate-profile my-honeypot.profile.yaml
```

Run a full scorecard validation once your audit harness produces results:

```bash
uhbs validate-scorecard path/to/scorecard.json
uhbs score --profile my-honeypot.profile.yaml --scores scores.json
```

Documentation site: **[https://mziqudhd92.github.io/uhbs-standard/](https://mziqudhd92.github.io/uhbs-standard/)** (MkDocs)  
Maturity roadmap: **[ROADMAP.md](ROADMAP.md)** · Reference harness: **[docs/reference-implementation.md](docs/reference-implementation.md)**

### Discovery for search & AI agents (SEO / AEO / GEO)

| File | Purpose |
| --- | --- |
| [llms.txt](llms.txt) (repo) · [site llms.txt](https://mziqudhd92.github.io/uhbs-standard/llms.txt) | Curated index for coding / answer agents |
| [AGENTS.md](AGENTS.md) | Rules for assistants editing this repo |
| [CITATION.cff](CITATION.cff) | Formal citation metadata |
| Site [robots.txt](https://mziqudhd92.github.io/uhbs-standard/robots.txt) · [sitemap.xml](https://mziqudhd92.github.io/uhbs-standard/sitemap.xml) | Crawler hints |

## Scoring Summary (UHQS 4.0)

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
├── schemas/              # JSON Schemas for profiles & scorecards
├── templates/            # Starter profile.yaml for framework users
├── src/uhbs_cli/         # Validation CLI
├── src/uhbs_core/        # UHBS-Lab reference harness
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
![UHBS v4.0](https://img.shields.io/badge/UHBS%20v4.0-Grade%20A-brightgreen)
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) and [GOVERNANCE.md](GOVERNANCE.md). Specification changes go through an **RFC** process. By contributing, you agree to the [Developer Certificate of Origin (DCO)](https://developercertificate.org/) (sign-off required on commits).

## Citation

```bibtex
@software{uhbs2026,
  title = {Universal Honeypot Benchmarking Standard (UHBS) v4.0},
  year = {2026},
  url = {https://github.com/mziqudhd92/uhbs-standard}
}
```

Or use the machine-readable [`CITATION.cff`](CITATION.cff).

## License

Licensed under the [Apache License 2.0](LICENSE).

---

An objective, repeatable, quantitative methodology for deception technology evaluation — providing cybersecurity professionals with a non-biased baseline for comparing and grading honeypots and decoy systems.
