# Universal Honeypot Benchmarking Standard

# UHBS v4.0 (2026)

An objective, repeatable, quantitative methodology for deception technology evaluation — providing cybersecurity professionals with a non-biased baseline for comparing and grading honeypots and decoy systems.

!!! danger "Executive Mandate"
    This is the **mandatory** enterprise and academic standard before deploying any active decoys to production networks. Failure to meet baseline scores (**UHQS &gt; 80**) exposes internal networks to lateral movement risks from compromised containment shells.

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

    UHQS &gt; 80 required before any active decoy reaches production

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

[← Return to UHBS landing site](https://mziqudhd92.github.io/uhbs-standard/) · Specification version **4.0.0**

An objective, repeatable, quantitative methodology for deception technology evaluation — providing cybersecurity professionals with a non-biased baseline for comparing and grading honeypots and decoy systems.
