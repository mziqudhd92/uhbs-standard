# UHBS Maturity Roadmap

> **Lock document.** Execution must follow this roadmap. Do not invent parallel plans.
> Spec version: **4.0.0** · Status: **Draft / Experimental** · Last updated: 2026-07-26

This roadmap turns UHBS from a scoring specification + schema validator into an
industry-credible **evaluation framework** (spec + contracts + reference
implementation + conformance suite), modeled on practices from IETF/W3C-style
standards work, OpenSSF, and NIST/MITRE-style frameworks.

**Vendor neutrality:** UHBS is product- and brand-agnostic. Normative text,
templates, and marketing describe **classes and protocols** only. Named products
appear solely in [conformance fixtures](conformance/index.md) as proof that
the published tools produce discriminating scores.

---

## North star

A mature UHBS has all five pillars:

| # | Pillar | Current state |
| --- | --- | --- |
| 1 | Normative spec (RFC 2119, document status) | Done for v4.0.0 Draft |
| 2 | Machine-readable contracts (profile, scorecard, evidence) | Done |
| 3 | Reference implementation (runnable harness) | Done — `uhbs_core` / `uhbs[lab]` |
| 4 | Conformance suite (golden inputs → expected UHQS) | Done — public fixtures |
| 5 | Independent adoption (≥2 implementations) | Not yet |

**Critical insight:** Pillar 3 was proven in lab before extraction into this
repository. The public package is the vendor-neutral reference harness; private
lab inventory and product-specific signal overlays stay out of tree.

---

## Reference harness (do not reinvent)

### Public package (`src/uhbs_core/`)

| Component | Role |
| --- | --- |
| `run_benchmark.py` | UHBS v4.0 orchestrator (phases 1–5) |
| `test_stealth.py` | Module A — Protocol & Syntax Fidelity |
| `test_realism.py` | Module B — Behavioral & Stateful Realism |
| `test_telemetry.py` | Module C — Telemetry Quality |
| `test_safety.py` | Module D — Safety Gate (δ_C) |
| `test_scale.py` | Module E — Scalability & Latency |
| `test_static_code.py` | Module F — White-Box Static Audit |
| `models.py` | UHQS formula + profile weights + δ_C |
| `report.py` | Scorecard layout |
| `protocols/` | Protocol plugins (ssh, http, ftp, redis, modbus, smb, smtp, telnet, generic) |
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
| Cowrie (OSS low-interaction baseline) | Low-Interaction | **46.97** | F |
| CyberHalluciNet (lab, post-hardening) | POSIX-Shell | **80.33** | B |

These runs show a mature low-interaction baseline below the production gate and
a hardened interactive decoy clearing UHQS > 80 — without endorsing either
product as a UHBS requirement.

**Public repo policy:** Framework docs, templates, and schemas MUST remain
class-/protocol-based. Named products belong in conformance fixtures and proof
tables only. Do not publish proprietary lab signal overlays or private host paths.

---

## Target topology

| Repo | Role |
| --- | --- |
| `uhbs-standard` (public) | Spec, schemas, `uhbs_core`, conformance fixtures, docs, CLI |
| Private lab (optional) | Site inventory, product-specific signal overlays; consumes `uhbs[lab]` |

---

## Phases

### Phase 1 — Specification rigor ✅

- [x] Publish this `ROADMAP.md` as the lock document
- [x] RFC 2119 / BCP 14 keywords; Normative vs Informative markers
- [x] Document status: **Draft / Experimental**
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

### Phase 3 — Reference implementation (`uhbs-core`) ✅

- [x] Extract vendor-neutral core (protocols, models, modules)
- [x] Leave proprietary signals / lab inventory private
- [x] Package as installable `uhbs[lab]` / `uhbs-lab`, version == spec `4.0.0`
- [x] Wire public docs to class-/protocol-based quickstart

### Phase 4 — Integrity (OpenSSF / SLSA)

- [x] Per-run `MANIFEST.json` SHA-256 digests (`uhbs_core.manifest`)
- [x] Release workflow with wheel/sdist + CycloneDX SBOM artifact
- [x] DCO required CI check; OpenSSF Scorecard action
- [ ] Sigstore/cosign keyless signing on PyPI Trusted Publishing (follow-up)

### Phase 5 — Interoperability mappings

- [x] ATT&CK / NIST CSF / IEC 62443 mappings under `docs/mappings/`
- [x] Named editors in `CITATION.cff` + Zenodo DOI placeholder notes
- [ ] Actual Zenodo DOI deposit (manual maintainer step)

### Phase 6 — Governance

- [x] Stewards roster (`MAINTAINERS.md`); accepted RFC-0001 baseline; `VERSIONING.md`
- [x] Attested scorecard registry rules (`docs/registry.md`)
- [ ] Neutral org transfer when ready (manual)

---

## Exit criteria ("mature")

- [x] Spec uses RFC 2119; status + UHBS-Core / UHBS-Lab levels published
- [x] Schemas for profile / scorecard / evidence; validator recomputes scores
- [x] `uhbs_core` in-repo (`uhbs[lab]`); class-based fixtures document conformance
- [x] Release SBOM workflow + DCO + OpenSSF Scorecard (Sigstore/PyPI publish pending)
- [x] Mappings + named stewards + accepted RFC-0001 (Zenodo DOI + org transfer pending)

---

## Execution notes (anti-drift)

1. Prefer extracting/sanitizing the existing harness over rewriting Modules A–F.
2. **Naming:** normative docs and templates = classes/protocols only; named
   products only in `docs/conformance/` proof fixtures and explicit proof tables.
3. Keep UHQS math identical across `uhbs_cli.scoring` and `uhbs_core.models`.
4. Every phase PR must update the checkboxes in this file.
5. Do not claim "production-mandatory industry standard" until Phase 6 exit criteria.
