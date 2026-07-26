# UHBS Maturity Roadmap

> **Lock document.** Execution must follow this roadmap. Do not invent parallel plans.
> Spec version: **4.0.0** · Status: **Draft / Experimental** · Last updated: 2026-07-26

This roadmap turns UHBS from a scoring specification + schema validator into an
industry-credible **evaluation framework** (spec + contracts + reference
implementation + conformance suite), modeled on practices from IETF/W3C-style
standards work, OpenSSF, and NIST/MITRE-style frameworks.

---

## North star

A mature UHBS has all five pillars:

| # | Pillar | Current state |
| --- | --- | --- |
| 1 | Normative spec (RFC 2119, document status) | Partial — prose exists, keywords informal |
| 2 | Machine-readable contracts (profile, scorecard, evidence) | Partial — profile + scorecard schemas only |
| 3 | Reference implementation (runnable harness) | **Exists privately** — see [Existing harness](#existing-harness-do-not-reinvent) |
| 4 | Conformance suite (golden inputs → expected UHQS) | Missing in public repo |
| 5 | Independent adoption (≥2 implementations) | Not yet |

**Critical insight:** Pillar 3 is already built and battle-tested against **Cowrie**
(open-source low-interaction baseline) and a **POSIX/GenAI research decoy** (private
lab target). This roadmap **incorporates that harness**; it does not rebuild it.

---

## Existing harness (do not reinvent)

### Location (lab / private)

| Path | Role |
| --- | --- |
| `CyberHalluciNet/scripts/benchmarks/run_benchmark.py` | UHBS v4.0 orchestrator (phases 1–5) |
| `…/test_stealth.py` | Module A — Protocol & Syntax Fidelity |
| `…/test_realism.py` | Module B — Behavioral & Stateful Realism |
| `…/test_telemetry.py` | Module C — Telemetry Quality |
| `…/test_safety.py` | Module D — Safety Gate (δ_C) |
| `…/test_scale.py` | Module E — Scalability & Latency |
| `…/test_static_code.py` | Module F — White-Box Static Audit |
| `…/lib/models.py` | UHQS formula + profile weights + δ_C |
| `…/lib/report.py` | Scorecard layout (`SCORECARD.txt` / `report.json`) |
| `…/lib/protocols/` | Protocol plugins (ssh, http, ftp, redis, modbus, smb, smtp, telnet, generic) |
| `…/lib/tps.py`, `profiles/tps/*.yaml` | Target Profile Specification |
| `…/calculate_uhqs_v4.py` | Standalone UHQS recomputation helper |
| `…/sandbox_preflight.py` | Phase 3 air-gap / sandbox attestation |
| `CyberHalluciNet/deploy/benchmarking/FRAMEWORK.md` | Spec ↔ script compliance map |
| `…/docker-compose.yml` | Cowrie lab target |
| `…/inventory.example.yaml` | Multi-target inventory (Cowrie, ICS, research decoy) |

### Spec alignment (already proven)

| Spec (PDF / public docs) | Implementation |
| --- | --- |
| TPS (`profile.yaml`) | `profiles/tps/*.yaml` + inventory |
| Modules A–F objectives | `test_stealth` / plugins, `test_realism`, `test_telemetry`, `test_safety`, `test_scale`, `test_static_code` |
| UHQS + δ_C = 1 if C≥95 else (C/100)² | `lib/models.py` → `compute_uhqs` |
| Profile weights (§5.3) | Same numbers in `PROFILE_WEIGHTS` |
| Phases 1–5 | `run_benchmark.py` phases `profile,static,sandbox,dynamic,score` |
| Scorecard layout | `lib/report.py` |

### Produced lab artifacts (evidence of maturity)

| Target | Class | Artifact | UHQS (example) | Grade |
| --- | --- | --- | --- | --- |
| Cowrie (Docker loopback) | Low-Interaction | `.local/bench-reports/cowrie-local/full3/` | **46.97** | F |
| POSIX research decoy (lab) | POSIX-Shell | `.local/bench-reports/chn-live/modular4/final/` | **80.32** | B (production baseline) |
| Same decoy (earlier) | POSIX-Shell | `chn-live/modular3/final/` | 73.09 → improved to 80.32 | C → B |

These runs prove the framework is **executable and discriminating**: a mature
low-interaction baseline (Cowrie) scores below production gate; a hardened
interactive decoy can clear UHQS > 80.

**Public repo policy:** Vendor-neutral sanitized fixtures only. Do not publish
proprietary signal profiles (`chn_signals.yaml`) or private host paths. Cowrie
(OSS) may be named as an open-source baseline target.

---

## Target topology

| Repo | Role |
| --- | --- |
| `uhbs-standard` (this repo, public) | Spec, schemas, conformance fixtures, docs site, thin CLI validator |
| `uhbs-core` (public, extract later) | Vendor-neutral reference harness from `scripts/benchmarks/lib` + `test_*.py` |
| Lab repo (private) | Cowrie/compose inventory, proprietary signals, consumes `uhbs-core` |

---

## Phases

### Phase 1 — Specification rigor ✅ (this milestone)

- [x] Publish this `ROADMAP.md` as the lock document
- [x] RFC 2119 / BCP 14 keywords; Normative vs Informative markers
- [x] Document status: **Draft / Experimental**
- [x] Conformance levels: **UHBS-Core** vs **UHBS-Lab**
- [x] Align grade bands with harness `grade_for()` (A≥90, B≥80, C≥70, D≥50, F&lt;50)
- [x] Add **Database** + **GenAI-Shell** weight rows (match harness)
- [x] Demote "mandatory standard" marketing → **Production Baseline Profile (RECOMMENDED)** until adopters exist
- [x] Document existing harness + Cowrie/lab runs in `docs/reference-implementation.md`

### Phase 2 — Contracts + conformance ✅ (this milestone)

- [x] `schemas/evidence-pack.schema.json` (check-id, team, evidence digests)
- [x] Extend scorecard schema for optional step-level checks (`PARTIAL` status)
- [x] CLI: enforce class→weights; **recompute** UHQS/δ_C/grade on validate
- [x] Round UHQS to **2 decimals** (match harness reports)
- [x] Golden fixtures from sanitized Cowrie + lab decoy scorecards
- [x] Conformance tests in CI

### Phase 3 — Reference implementation (`uhbs-core`)

- [ ] Extract vendor-neutral core from `scripts/benchmarks/` (protocols, models, modules)
- [ ] Leave proprietary signals / lab inventory private
- [ ] PyPI package, version == spec `4.0.0`
- [ ] Wire public docs to `uhbs-core` quickstart; keep CHN/Cowrie lab recipes in private `deploy/benchmarking/`

### Phase 4 — Integrity (OpenSSF / SLSA)

- [ ] Per-run `MANIFEST.json` SHA-256 digests (reuse private `evidence/gates/` pattern)
- [ ] Signed releases, CycloneDX SBOM, Sigstore
- [ ] DCO required CI check; OpenSSF Scorecard action

### Phase 5 — Interoperability mappings

- [ ] ATT&CK / NIST CSF / IEC 62443 mappings under `docs/mappings/`
- [ ] Zenodo DOI + named editors in `CITATION.cff`

### Phase 6 — Governance

- [ ] Stewards roster (≥3); ≥1 accepted RFC; CHANGELOG SemVer policy
- [ ] Attested scorecard registry; badges only for digest-backed runs
- [ ] Neutral org transfer when ready

---

## Exit criteria ("mature")

- [ ] Spec uses RFC 2119; status + UHBS-Core / UHBS-Lab levels published
- [ ] Schemas for profile / scorecard / evidence; validator recomputes scores
- [ ] `uhbs-core` published; Cowrie + ≥1 other target pass documented conformance
- [ ] Signed releases + SBOM; DCO enforced
- [ ] Mappings + DOI; named stewards; ≥1 accepted RFC

---

## Execution notes (anti-drift)

1. Prefer extracting/sanitizing the existing harness over rewriting Modules A–F.
2. Public examples use **Cowrie** (OSS) and **vendor-neutral decoy labels** only.
3. Keep UHQS math identical to `lib/models.py` (`compute_uhqs`).
4. Every phase PR must update the checkboxes in this file.
5. Do not claim "production-mandatory industry standard" until Phase 6 exit criteria.
