---
title: UHBS — Universal Honeypot Benchmarking Standard
description: Open-source beta-status framework for vendor-neutral honeypot and deception evaluation (UHQS 0–100 with Safety Gate). Spec v4.3.0. Not a consortium standard.
---

# Universal Honeypot Benchmarking Standard

# UHBS v4.3.0 (2026)

An objective, repeatable, quantitative methodology for deception technology
evaluation — an open-source **beta-status** framework for comparing and grading
honeypots and decoy systems by class and protocol. Not a consortium standard;
see [ROADMAP](roadmap.md) for community-maturity goals.

!!! warning "Project posture"
    UHBS is maintained by one author today. There is no Steering Committee or
    independent adopter list yet.

!!! danger "Production Baseline Profile (RECOMMENDED)"
    Organizations **MAY** use UHBS as an *internal* gate. It is **RECOMMENDED**
    that active decoys meet **UHQS &gt; 80** with a passing Safety Gate before
    production deployment. See [Status](specification/status.md).

<div class="grid cards" markdown>

-   :material-lan: **Protocol-Agnostic**

    ---

    100% architecture-neutral testing across IT, OT/ICS, AI, and Cloud

-   :material-chart-box: **Quantitative Scoring**

    ---

    Normalized UHQS 0–100 composite with non-linear Safety Gate \(\delta_C\)

-   :material-view-module: **Six Evaluation Modules**

    ---

    Modules A–F covering fidelity, behavior, telemetry, safety, scale, and audit

-   :material-shield-check: **Production Baseline**

    ---

    UHQS &gt; 80 suggested as an internal beta recommendation

</div>

## Start here

1. Read [Core Principles](specification/core-principles.md) — dual-plane audit and isolation requirements  
2. Author a [Target Profile Specification](specification/target-profiles.md) (`profile.yaml`)  
3. Execute [Modules A–F](specification/modules.md) in the five-phase workflow  
4. Compute [UHQS](specification/scoring-formula.md) and publish a standard scorecard  

```bash
pip install -e .
uhbs validate-profile templates/profile.yaml
```

Specification version **4.3.0** · [GitHub repository](https://github.com/mziqudhd92/uhbs-standard) · [Site landing hub](https://mziqudhd92.github.io/uhbs-standard/) (this MkDocs tree is served under `/mkdocs/`)
