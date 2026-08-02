# AEP Research Foundations & Credits

**Status:** Informative · citation ledger for the optional Advanced Evidence Profile  
**Scope:** Lab / sandbox evaluation only — not real-world production testing

AEP’s experimental vocabulary and metric *discipline* draw on published research.
UHBS **credits these authors and venues**. Citing them does **not** mean those
works adopt UHBS, endorse this project, or that UHBS implements their full models.

> **Credit statement.** The Advanced Evidence Profile is an optional, informative
> layer maintained by the UHBS project. Where AEP borrows threat-model language,
> experimental controls, or measurement caution from prior work, that debt is
> acknowledged below with DOIs / arXiv identifiers so readers can verify sources.

## How to read these citations

| Label | Meaning |
| --- | --- |
| Peer-reviewed / DOI | Prefer for normative-sounding claims; still informative in UHBS |
| Preprint (arXiv) | Research in progress — maturity labeled; do not over-claim consensus |
| Role in AEP | What UHBS takes from the paper (vocabulary / design / threat model) |
| What AEP does **not** claim | Explicit non-claims to avoid false endorsement |

## Primary references (AEP design)

### 1. Zhu (2019) — game-theoretic deception tutorial

**Quanyan Zhu.** *Game Theory for Cyber Deception: A Tutorial.* HotSoS 2019.
DOI: [10.1145/3314058.3314067](https://doi.org/10.1145/3314058.3314067)

| | |
| --- | --- |
| **Credit / role in AEP** | Signaling and dynamic games as a **threat-model vocabulary** (players, information sets, actions, utilities, priors). |
| **AEP does not claim** | That UHBS computes an equilibrium score, or that VoD is Zhu’s utility without an experiment-declared \(U_D\). |

### 2. Collins, Xu & Brown (2024) — game-theoretic cybersecurity critique

**Andrew Collins, Jing Xu, and Michael Brown.** *Game-Theoretic Cybersecurity: the Good, the Bad and the Ugly.* arXiv preprint
[arXiv:2401.13815](https://arxiv.org/abs/2401.13815) (2024).

| | |
| --- | --- |
| **Credit / role in AEP** | Require every model to state **uncertainty**, data availability, model efficacy, and solution practicality; ground parameters in observables. |
| **Maturity** | Preprint — labeled as such. |
| **AEP does not claim** | That AEP solves the open problems surveyed in that paper. |

### 3. Ersok et al. (2022) — measuring honeypots via CTF

**Ersok et al.** *Measuring Honeypots based on CTF game.* IEEE ICCC 2022.
DOI: [10.1109/ICCC202255925.2022.9922853](https://doi.org/10.1109/ICCC202255925.2022.9922853)

| | |
| --- | --- |
| **Credit / role in AEP** | Controlled CTF / red-team **log validation patterns** and human-in-the-loop measurement caution. |
| **AEP does not claim** | That every CTF indicator in the paper is reproduced as a UHQS module. |

### 4. Li et al. (2020) — anti-honeypot attacker strategies (ICS)

**Li et al.** *Anti-Honeypot Enabled Optimal Attack Strategy for Industrial Cyber-Physical Systems.* IEEE Open Journal of the Computer Society, 2020.
DOI: [10.1109/OJCS.2020.3030825](https://doi.org/10.1109/OJCS.2020.3030825)

| | |
| --- | --- |
| **Credit / role in AEP** | **Attacker** sophistication / incomplete-information tiers for lab anti-honeypot probe design. |
| **AEP does not claim** | That this paper is a defender evaluation standard or that UHQS grades “anti-honeypot resistance” as a letter grade. |

## Related research families (comparison context)

These families inform the [related-frameworks](../mappings/related-frameworks.md)
comparison. They are credited there with maturity labels; AEP does not absorb
them into UHQS.

| Family / example source | Credit note |
| --- | --- |
| Dynamic Honeypot Mixture-of-Experts — Pittman et al., arXiv [2005.12969](https://arxiv.org/abs/2005.12969) | Engagement / sojourn-style metrics (informative) |
| Honeyval — Google Research, arXiv [2605.29963](https://arxiv.org/abs/2605.29963) | Paired controls / agent evaluation patterns (preprint) |
| CLOUDBURST / CAS — arXiv [2605.12976](https://arxiv.org/abs/2605.12976) | Cloud honeytoken taxonomy (preprint; coverage map only) |
| Heckman et al., *Cyber Denial, Deception and Counter Deception* (Springer) | Cyber-Deception Chain campaign lifecycle (map only) |

## Lab-only evaluation scope

UHBS (including UHBS-Lab and AEP) is an **evaluation framework for laboratory /
sandbox use**:

- Run Modules A–F and AEP trials against **isolated lab decoys and lab references**
- Do **not** use UHBS or AEP to probe production systems, customer environments,
  or unauthorized third-party infrastructure
- The optional “UHQS > 80 production baseline” language means: *after lab grading,
  your organization may use that score as an internal gate before you choose to
  deploy a decoy* — it does **not** authorize real-world attack testing

## Suggested citation of UHBS when using AEP

When publishing an AEP addendum, cite UHBS (see root [`CITATION.cff`](https://github.com/uhbs/uhbs-standard/blob/main/CITATION.cff))
**and** cite the primary papers above that your study relies on. Do not imply
those authors endorse your results.
