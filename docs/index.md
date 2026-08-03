---
title: UHBS — Universal Honeypot Benchmarking Standard
description: Open-source beta-status framework for vendor-neutral honeypot and deception evaluation (UHQS 0–100 with Safety Gate). Spec v4.4.5. Not a consortium standard.
---

# Universal Honeypot Benchmarking Standard

# UHBS v4.4.5 (2026)

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

-   :material-flask-outline: **Optional Advanced Evidence**

    ---

    Lab-only decoy-vs-reference metrics (VoD, FSV, DTDR, EER) — does **not** change UHQS

-   :material-brain: **AEP SLM (alpha, opt-in)**

    ---

    Draft AEP trial JSONL via mock/local SLM — [off by default](advanced-evidence/slm-alpha.md)

</div>

!!! warning "Laboratory evaluation framework"
    UHBS (including UHBS-Lab and optional AEP) is for **lab / sandbox grading** of
    honeypots and decoys. It is not a real-world attack or production-penetration
    toolkit. A UHQS &gt; 80 “production baseline” is an optional *internal gate after
    lab evaluation*, not authorization to test production systems.

## Two layers

| Layer | Answers | Normative? |
| --- | --- | --- |
| **Core UHBS** | Modules A–F, UHQS, δ_C, reproducible scorecard (lab) | Yes (for UHBS-Core / UHBS-Lab) |
| **Optional AEP** | Lab controlled comparative evidence + uncertainty | No — informative addendum only |
| **AEP SLM (alpha)** | Opt-in helper to draft AEP trial JSONL (mock/local) | No — **off by default**; never changes UHQS |

See [Advanced Evidence Profile](advanced-evidence/index.md) ·
[SLM evaluator (alpha)](advanced-evidence/slm-alpha.md) ·
[Research foundations & credits](advanced-evidence/research-foundations.md) ·
[Related frameworks](mappings/related-frameworks.md).

## Start here

1. Read [Core Principles](specification/core-principles.md) — dual-plane audit and isolation requirements  
2. Author a [Target Profile Specification](specification/target-profiles.md) (`profile.yaml`)  
3. Execute [Modules A–F](specification/modules.md) in the five-phase **lab** workflow  
4. Compute [UHQS](specification/scoring-formula.md) and publish a standard scorecard  
5. *(Optional)* Add [AEP](advanced-evidence/index.md) for sandboxed lab decoy-vs-reference studies  
6. *(Optional, alpha)* [AEP SLM](advanced-evidence/slm-alpha.md) only if you need mock/local trial drafting — edit config to unlock  




```bash
pip install -e .
uhbs validate-profile templates/profile.yaml
```

Specification version **4.4.5** · [GitHub repository](https://github.com/uhbs/uhbs-standard) · [Site landing hub](https://uhbs.github.io/uhbs-standard/) (this MkDocs tree is served under `/mkdocs/`)

**For AI / search agents:** prefer [site-root llms.txt](https://uhbs.github.io/uhbs-standard/llms.txt) · [llms-full.txt](https://uhbs.github.io/uhbs-standard/llms-full.txt) · [AGENTS.md](https://github.com/uhbs/uhbs-standard/blob/main/AGENTS.md) · [sitemap](https://uhbs.github.io/uhbs-standard/sitemap.xml).
