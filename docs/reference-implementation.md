# Reference Implementation & Lab Harness

**Status:** Informative  
**Related:** [ROADMAP.md](roadmap.md) · Spec modules A–F

UHBS is not only a document. A full **UHBS-Lab** evaluation requires an executable
harness that implements Modules A–F, applies the UHQS formula with δ_C, and emits
a scorecard. That harness already exists and has been run against real targets.

## Spec ↔ script map

| Spec | Scripts (lab harness) |
| --- | --- |
| TPS (`profile.yaml`) | `profiles/tps/*.yaml` + inventory |
| Module A | `test_stealth.py` + `lib/protocols/*` |
| Module B | `test_realism.py` |
| Module C | `test_telemetry.py` |
| Module D (Safety Gate) | `test_safety.py` |
| Module E | `test_scale.py` |
| Module F | `test_static_code.py` |
| UHQS + δ_C | `lib/models.py` → `compute_uhqs` |
| Profile weights (§5.3) | `PROFILE_WEIGHTS` in `lib/models.py` |
| Phases 1–5 | `run_benchmark.py` (`profile,static,sandbox,dynamic,score`) |
| Scorecard layout | `lib/report.py` |
| Standalone UHQS helper | `calculate_uhqs_v4.py` |
| Sandbox preflight | `sandbox_preflight.py` |

Entry point:

```text
run_benchmark.py
```

Shared libraries: TPS loader, scoring, SSH/HASSH helpers, protocol plugin registry
under `lib/protocols/` (ssh, http, ftp, redis, modbus, smb, smtp, telnet, generic).

Lab packaging: compose file for an open-source low-interaction SSH decoy (Cowrie),
inventory example, and `FRAMEWORK.md` compliance map.

## Upstream destination

Per [ROADMAP.md](roadmap.md) Phase 3, the vendor-neutral core of this harness
becomes the public **`uhbs-core`** package. Proprietary signal profiles and private
lab inventory stay out of `uhbs-standard`.

Until Phase 3 lands, this repository ships:

- Normative schemas + UHQS validator (`uhbs` CLI)
- Conformance fixtures derived from sanitized lab scorecards
- This document as the authoritative pointer to the reference harness

## Produced evaluations (sanitized)

The following runs demonstrate that the framework **discriminates** between decoy classes.

### Open-source baseline — Cowrie (Low-Interaction)

| Field | Value |
| --- | --- |
| Target class | `Low-Interaction` |
| Protocol | SSH |
| Environment | Local Docker (loopback) |
| Module scores (example run) | A 23.5 · B 42.5 · C 57.0 · D 100 · E 55.0 · F 69.0 |
| δ_C | 1.0 (C ≥ 95) |
| **UHQS 4.0** | **46.97** |
| Grade | **F** |

Machine fixture: [`conformance/fixtures/cowrie-low-interaction.scorecard.json`](conformance/fixtures/cowrie-low-interaction.scorecard.json)

Interpretation: a widely deployed low-interaction emulator can pass containment
while still failing protocol fidelity, behavioral realism, and latency gates —
exactly what UHBS is designed to surface.

### Interactive research decoy — POSIX-Shell (lab)

| Field | Value |
| --- | --- |
| Target class | `POSIX-Shell` |
| Protocols | SSH (+ additional services in lab) |
| Progression | 62.61 → 73.09 → **80.33** (post hardening; normative recompute) |
| **UHQS 4.0 (latest)** | **80.33** |
| Grade | **B** (meets production baseline UHQS > 80) |

Machine fixture: [`conformance/fixtures/posix-shell-lab.scorecard.json`](conformance/fixtures/posix-shell-lab.scorecard.json)

Interpretation: iterative hardening against Modules A–F moves a decoy across the
**Production Baseline Profile** threshold while Module A (protocol fingerprinting)
remains the primary drag — a useful engineering signal.

## Quick lab invocation (informative)

```bash
# From the lab repo that vendors the harness:
export UHBS_QUICK=1
export UHBS_AIRGAP_ATTESTED=1

python3 scripts/benchmarks/run_benchmark.py \
  --tps low_interaction \
  --target 127.0.0.1 --port 2200 \
  --source-root /path/to/cowrie \
  --phases profile,static,sandbox,dynamic,score \
  --quick \
  --out .local/bench-reports/cowrie-local
```

Validate the emitted scorecard with the public CLI:

```bash
uhbs validate-scorecard path/to/scorecard.json --strict
uhbs score --profile templates/profile.yaml --scores scores.json
```

## Conformance levels

| Level | Requirements |
| --- | --- |
| **UHBS-Core** | Valid TPS + scorecard schemas; UHQS/δ_C/grade integrity |
| **UHBS-Lab** | UHBS-Core + executable Modules A–F + evidence pack digests |

See [conformance/index.md](conformance/index.md).
