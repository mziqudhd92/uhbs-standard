# Universal Honeypot Benchmarking Standard

# UHBS v4.0 (2026)

An objective, repeatable, and quantitative methodology for benchmarking honeypots, decoys, and deception technology across enterprise and academic environments.

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

    Enterprise and academic standard before deploying decoys to production

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

---

Specification version **4.0.0** · Licensed under [Apache 2.0](https://github.com/mziqudhd92/uhbs-standard/blob/main/LICENSE)
