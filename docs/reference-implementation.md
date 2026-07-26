# Reference Implementation & Lab Harness

**Status:** Informative  
**Related:** [ROADMAP.md](roadmap.md) · Spec modules A–F · Package: `src/uhbs_core/`

UHBS is not only a document. A full **UHBS-Lab** evaluation requires an executable
harness that implements Modules A–F, applies the UHQS formula with δ_C, and emits
a scorecard. That harness is now published in this repository as **`uhbs_core`**
(extracted from the lab `scripts/benchmarks/` tree).

## Install (public)

```bash
pip install -e ".[lab]"
uhbs-lab --list-protocols
# or:
uhbs lab --list-protocols
```

## Spec ↔ script map

| Spec | Implementation in `uhbs_core` |
| --- | --- |
| TPS (`profile.yaml`) | `tps.py` + `profiles/tps/*.yaml` |
| Module A | `test_stealth.py` + `protocols/*` |
| Module B | `test_realism.py` |
| Module C | `test_telemetry.py` |
| Module D (Safety Gate) | `test_safety.py` |
| Module E | `test_scale.py` |
| Module F | `test_static_code.py` |
| UHQS + δ_C | `models.py` → `compute_uhqs` (+ `calculate_uhqs_v4.py`) |
| Profile weights (§5.3) | `PROFILE_WEIGHTS` in `models.py` |
| Phases 1–5 | `run_benchmark.py` |
| Scorecard layout | `report.py` |
| Attestation | `manifest.py` → `MANIFEST.json` |
| Sandbox preflight | `sandbox_preflight.py` |

## Quick lab run

```bash
export UHBS_QUICK=1
export UHBS_AIRGAP_ATTESTED=1

uhbs lab \
  --tps low_interaction \
  --target 127.0.0.1 --port 2200 \
  --source-root /path/to/cowrie \
  --phases profile,static,sandbox,dynamic,score \
  --quick \
  --out .local/bench-reports/cowrie-local
```

Validate outputs:

```bash
uhbs validate-scorecard path/to/scorecard.json --strict
```

## Proven evaluations (sanitized fixtures)

| Target | Class | UHQS | Grade | Fixture |
| --- | --- | --- | --- | --- |
| Cowrie (OSS) | Low-Interaction | 46.97 | F | [`conformance/fixtures/cowrie-low-interaction.scorecard.json`](conformance/fixtures/cowrie-low-interaction.scorecard.json) |
| POSIX-Shell research decoy | POSIX-Shell | 80.33 | B | [`conformance/fixtures/posix-shell-lab.scorecard.json`](conformance/fixtures/posix-shell-lab.scorecard.json) |

## Private lab leftovers

Proprietary signal profiles and multi-site inventory remain in the private lab
repo (`deploy/benchmarking/`, `*_signals.yaml` for product-specific trees). The
public package ships OSS-oriented `cowrie_signals.yaml` only.

## Conformance levels

| Level | Requirements |
| --- | --- |
| **UHBS-Core** | Valid TPS + scorecard schemas; UHQS/δ_C/grade integrity |
| **UHBS-Lab** | UHBS-Core + `uhbs_core` Modules A–F + evidence/MANIFEST digests |

See [conformance/index.md](conformance/index.md) and [registry.md](registry.md).
