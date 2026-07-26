# Universal Honeypot Benchmarking Standard (UHBS)

[![CI](https://github.com/mziqudhd92/uhbs-standard/actions/workflows/ci-validate.yml/badge.svg)](https://github.com/mziqudhd92/uhbs-standard/actions/workflows/ci-validate.yml)
[![Docs](https://github.com/mziqudhd92/uhbs-standard/actions/workflows/deploy-docs.yml/badge.svg)](https://mziqudhd92.github.io/uhbs-standard/)
[![CodeQL](https://github.com/mziqudhd92/uhbs-standard/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/mziqudhd92/uhbs-standard/actions/workflows/codeql-analysis.yml)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Spec](https://img.shields.io/badge/Specification-v4.0.0-indigo.svg)](docs/specification/core-principles.md)
[![UHQS](https://img.shields.io/badge/UHQS-0%E2%80%93100-success.svg)](docs/specification/scoring-formula.md)

> An objective, repeatable, and quantitative methodology for benchmarking honeypots, decoys, and deception technology across enterprise and academic environments.

**UHBS v4.0** is a protocol-agnostic production baseline for measuring deception realism, safety containment, operational scale, and telemetry quality **before** decoys are deployed to production.

## Why UHBS?

| Pillar | What it delivers |
| --- | --- |
| **Protocol-Agnostic** | Architecture-neutral testing across IT, OT/ICS, AI, and Cloud |
| **Quantitative Scoring** | Normalized **UHQS 0–100** composite with a non-linear Safety Gate |
| **Six Evaluation Modules** | Modules A–F covering fidelity, behavior, telemetry, safety, scale, and audit |
| **Production Baseline** | Enterprise and academic standard prior to production deployment |

## Quickstart

Validate a honeypot against a Target Profile Specification (`profile.yaml`) in three steps:

```bash
# 1. Install the CLI
pip install -e .

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

Documentation site: **[https://mziqudhd92.github.io/uhbs-standard/](https://mziqudhd92.github.io/uhbs-standard/)**

## Scoring Summary (UHQS 4.0)

The **Universal Honeypot Quality Score (UHQS)** is a normalized composite from **0 to 100**:

\[
\mathrm{UHQS} = \delta_C \cdot (w_A S_A + w_B S_B + w_C S_C + w_E S_E + w_F S_F)
\]

- \(S_A \ldots S_F\) — normalized module scores (0–100)
- \(w_A \ldots w_F\) — profile-adaptive weights (sum to 1.00)
- \(\delta_C\) — **Safety Gate** from Module D (Containment):  
  \(\delta_C = 1.0\) if \(C \ge 95\); otherwise \(\delta_C = (C/100)^2\)

A decoy with excellent deception scores can still fail evaluation if Module D falls below the gate. See [Scoring Formula](docs/specification/scoring-formula.md).

## Audit Workflow (5 Phases)

```text
┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│  Phase 1    │──▶│  Phase 2    │──▶│  Phase 3    │──▶│  Phase 4    │──▶│  Phase 5    │
│  Profile &  │   │  Static     │   │  Sandbox    │   │  Dynamic    │   │  Score &    │
│  Config     │   │  Audit (F)  │   │  Provision  │   │  Modules A–E│   │  Report     │
└─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘
```

1. **Configuration & Profile Setup** — Define `profile.yaml`, protocol expectations, baselines  
2. **Static Audit Execution** — Analyze repository, Dockerfiles, and system prompts  
3. **Sandbox Environment Provisioning** — Isolated runtime with egress monitors  
4. **Dynamic Adversarial Execution** — Modules A–E via automated harnesses  
5. **Score Computation & Reporting** — Apply \(\delta_C\) and emit the standard scorecard  

## Repository Layout

```text
uhbs-standard/
├── docs/                 # Docs-as-Code (GitHub Pages / MkDocs Material)
├── schemas/              # JSON Schemas for profiles & scorecards
├── templates/            # Starter profile.yaml for adopters
├── src/uhbs_cli/         # Official validation CLI
├── GOVERNANCE.md         # RFC process & steering committee
├── SECURITY.md           # Vulnerability disclosure policy
└── CITATION.cff          # Academic / enterprise citation metadata
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

After publishing an official scorecard, honeypot maintainers can embed:

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
