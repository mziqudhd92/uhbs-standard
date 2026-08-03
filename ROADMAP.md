# UHBS Maturity Roadmap

> **Lock document.** Execution must follow this roadmap. Do not invent parallel plans.
> Spec version: **4.4.0** · Status: **Beta / Experimental** · Last updated: 2026-08-01
>
> **What this is today:** an open-source **beta-status**, vendor-neutral
> **evaluation framework** (spec + schemas + harness + fixtures).
> It is **not** yet an industry or academic standard, a consortium, or a
> multi-party governed body.

This roadmap records how the project could mature toward something enterprise and
academic communities might adopt — without pretending those milestones are done.

**Vendor neutrality:** Normative text, templates, and marketing describe
**classes and protocols** only. Named products appear solely in
[conformance fixtures](conformance/index.md) as proof that the published tools
produce discriminating scores.

---

## North star

A mature UHBS would have all five pillars:

| # | Pillar | Current state |
| --- | --- | --- |
| 1 | Normative spec (RFC 2119, document status) | Done for v4.4.0 Beta |
| 2 | Machine-readable contracts (profile, scorecard, evidence) | Done |
| 3 | Reference implementation (runnable harness) | Done — `uhbs_core` / `uhbs[lab]` |
| 4 | Conformance suite (golden inputs → expected UHQS) | Done — public fixtures |
| 5 | Independent adoption (≥2 external evaluations / implementations) | **Not yet** |

**Critical insight:** Pillar 3 was proven in lab before extraction into this
repository. The public package is the vendor-neutral reference harness; private
lab inventory and product-specific signal overlays stay out of tree.

---

## Reference harness (do not reinvent)

### Public package (`src/uhbs_core/`)

| Component | Role |
| --- | --- |
| `run_benchmark.py` | UHBS v4.4.0 orchestrator (phases 1–5) |
| `test_stealth.py` | Module A — Protocol & Syntax Fidelity |
| `test_realism.py` | Module B — Behavioral & Stateful Realism |
| `test_telemetry.py` | Module C — Telemetry Quality |
| `test_safety.py` | Module D — Safety Gate (δ_C) |
| `test_scale.py` | Module E — Scalability & Latency |
| `test_static_code.py` | Module F — White-Box Static Audit |
| `models.py` | UHQS formula + profile weights + δ_C |
| `report.py` | Scorecard layout |
| `protocols/` | Protocol plugins (ssh, http, mcp, ftp, redis, modbus, smb, smtp, telnet, mysql, rdp, sip, snmp, ntp, tftp, vnc, git, generic) |
| `tps.py`, `profiles/tps/*.yaml` | Target Profile Specification |
| `manifest.py` | Per-run SHA-256 attestation digests |

### Spec alignment

| Spec | Implementation |
| --- | --- |
| TPS (`profile.yaml`) | `profiles/tps/*.yaml` |
| Modules A–F | `test_*` modules + protocol plugins |
| UHQS + δ_C | `models.compute_uhqs` |
| Profile weights (§5.3) | `PROFILE_WEIGHTS` |
| Phases 1–5 | `run_benchmark.py` |
| Scorecard layout | `report.py` |

### Published evaluation proof (named targets OK here)

Sanitized scorecards that prove the tools discriminate across classes. Full
artifacts: [docs/conformance/](conformance/index.md).

| Target (proof only) | Class | UHQS | Grade |
| --- | --- | --- | --- |
| Cowrie (OSS SSH baseline) | Low-Interaction | **61.37** | D |
| ESPot (HTTP Elasticsearch decoy) | Web-API | **49.82** | F |
| miniprint (PJL printer decoy) | Low-Interaction | **47.77** | F |
| Conpot (Modbus ICS) | ICS-SCADA | **55.51** | D |
| OpenCanary (HTTP canary) | Web-API | **50.12** | D |
| CyberHalluciNet (lab, post-hardening) | POSIX-Shell | **80.33** | B |

Live full-lab artifacts: [docs/conformance/reports/](conformance/reports/index.md).
An anonymous Low-Interaction **worked example** (A=23.5…F=69.0) still equals UHQS
**46.97** in unit tests — do not confuse that with the Cowrie fixture.

These runs show mature decoys near or below the production gate and one hardened
interactive decoy clearing UHQS > 80 — without endorsing any product as a UHBS
requirement.

**Public repo policy:** Framework docs, templates, and schemas MUST remain
class-/protocol-based. Named products belong in conformance fixtures and proof
tables only. Do not publish proprietary lab signal overlays or private host paths.

---

## Target topology

| Repo | Role |
| --- | --- |
| `uhbs-standard` (public, public GitHub repository today) | Spec, schemas, `uhbs_core`, conformance fixtures, docs, CLI |
| Private lab (optional) | Site inventory, product-specific signal overlays; consumes `uhbs[lab]` |

---

## Phases

### Phase 1 — Specification rigor ✅

- [x] Publish this `ROADMAP.md` as the lock document
- [x] RFC 2119 / BCP 14 keywords; Normative vs Informative markers
- [x] Document status: **Beta / Experimental**
- [x] Conformance levels: **UHBS-Core** vs **UHBS-Lab**
- [x] Align grade bands with harness `grade_for()` (A≥90, B≥80, C≥70, D≥50, F&lt;50)
- [x] Add **Database** + **GenAI-Shell** weight rows (match harness)
- [x] Demote "mandatory standard" marketing → **Production Baseline Profile (RECOMMENDED)**
- [x] Document reference harness + conformance proof in `docs/reference-implementation.md`

### Phase 2 — Contracts + conformance ✅

- [x] `schemas/evidence-pack.schema.json`
- [x] Extend scorecard schema for optional step-level checks (`PARTIAL` status)
- [x] CLI: enforce class→weights; **recompute** UHQS/δ_C/grade on validate
- [x] Round UHQS to **2 decimals**
- [x] Golden fixtures from sanitized lab scorecards (named only under conformance/)
- [x] Conformance tests in CI
- [ ] Pydantic v2 schema validation for `CheckResult`/`ModuleResult`/`ProtocolPlugin`
      (today: phase-1 advisory lint only — `uhbs_core.contract_validation`,
      see `docs/architecture/plugin-contracts.md`; not started as a real migration)

### Phase 3 — Reference implementation (`uhbs-core`) ✅

- [x] Extract vendor-neutral core (protocols, models, modules)
- [x] Leave proprietary signals / lab inventory private
- [x] Package as installable `uhbs[lab]` / `uhbs-lab`, version == spec `4.4.0`
- [x] Wire public docs to class-/protocol-based quickstart

### Phase 4 — Integrity (OpenSSF / SLSA)

- [x] Per-run `MANIFEST.json` SHA-256 digests (`uhbs_core.manifest`)
- [x] Release workflow with wheel/sdist + CycloneDX SBOM artifact
- [x] DCO required CI check; OpenSSF Scorecard action
- [ ] Sigstore/cosign keyless signing on PyPI Trusted Publishing (follow-up)

### Phase 5 — Interoperability mappings

- [x] ATT&CK / NIST CSF / IEC 62443 mappings under `docs/mappings/`
- [x] MITRE D3FEND (Deceive) + Engage goal mappings under `docs/mappings/`
- [x] Optional scorecard `framework_refs` (D3FEND / Engage; display-only)
- [x] Evidence-graded related-frameworks comparison (`docs/mappings/related-frameworks.md`)
- [x] Optional Advanced Evidence Profile (AEP) docs + offline `uhbs aep` analyzer
      (informative only — does **not** change UHQS / weights / δ_C)
- [x] Optional AEP SLM evaluator (**alpha**, opt-in, off by default) —
      `uhbs aep slm` + docs at `advanced-evidence/slm-alpha.md` (does **not**
      change UHQS; not MCP-exposed)
- [x] Citation metadata (`CITATION.cff`) + Zenodo DOI placeholder notes
- [x] Actual Zenodo DOI deposit (`10.5281/zenodo.21631156`, concept `10.5281/zenodo.21631155`)

### Phase 6 — Community maturity (aspirational — **not done**)

These items are **future goals**. The repo must **not** claim they are complete.

#### Multi-party governance

- [ ] Recruit **≥3 maintainers from different organizations** (not the same employer)
- [ ] Publish a real steward/maintainer roster (replace single-author `MAINTAINERS.md`)
- [ ] Define a lightweight decision process (who can accept RFCs; public notes)
- [ ] Keep public decision records (short meeting notes or Discussion posts)

#### Neutral hosting

- [x] Transfer the repository to a **neutral GitHub organization** (`uhbs/uhbs-standard`)
- [x] Update clone URLs, Pages, badges, and `CITATION.cff` after transfer
      (site: https://uhbs.github.io/uhbs-standard/)

#### Independent adopters & evaluations

- [ ] Publish an **ADOPTERS.md** (or similar) only when real external users consent
- [ ] At least **one independent reproduction** of a public fixture by someone other
      than the author
- [x] Expand the evaluation corpus (≥5 open-source deception targets across classes)
- [ ] Prioritize D3FEND Decoy Object types beyond network listeners (decoy files /
      credentials / personas — corpus is listener-heavy today)
- [ ] Optional: peer-reviewed or workshop paper / preprint with weight sensitivity notes
- [ ] Corpus validation of AEP metrics across ≥3 profile classes before any UHQS RFC
- [ ] Separate RFC only if informative AEP metrics justify normative scoring changes

#### Registry & distribution

- [ ] Working attested scorecard submission path (PR + CI recompute)
- [ ] PyPI Trusted Publishing + Sigstore signing
- [ ] Do **not** claim "industry-mandatory standard" until the above governance and
      adoption bars are met

---

## Exit criteria ("community-mature")

Technical scaffolding for a beta framework is largely in place. **Community
maturity** additionally requires:

- [ ] Multi-organization maintainers (≥3)
- [ ] Neutral GitHub org hosting
- [ ] ≥1 independent external evaluation or second implementation
- [ ] Published adopter list (with consent) **or** clear "no public adopters yet"
- [x] Zenodo DOI (v4.0.1 → `10.5281/zenodo.21631156`)
- [ ] Signed PyPI releases (Trusted Publishing + Sigstore)

Until then, describe UHBS as a **beta-status framework**, not as an adopted
industry or academic standard.

---

## Execution notes (anti-drift)

1. Prefer extracting/sanitizing the existing harness over rewriting Modules A–F.
2. **Naming:** normative docs and templates = classes/protocols only; named
   products only in `docs/conformance/` proof fixtures and explicit proof tables.
3. Keep UHQS math identical across `uhbs_cli.scoring` and `uhbs_core.models`.
4. Every phase PR must update the checkboxes in this file.
5. **Do not invent committees, stewards, or adopters in docs** — put those goals
   only in this ROADMAP until they are real.
6. Do not claim "production-mandatory industry standard" until Phase 6 exit criteria.
