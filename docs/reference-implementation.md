# Reference Implementation & Lab Harness

**Status:** Informative  
**Related:** [ROADMAP.md](roadmap.md) · Spec modules A–F · Package: `src/uhbs_core/`

UHBS is not only a document. A full **UHBS-Lab** evaluation requires an executable
harness that implements Modules A–F, applies the UHQS formula with δ_C, and emits
a scorecard. That harness ships in this repository as **`uhbs_core`** — a
**vendor-neutral** reference anyone can run against any deception target.

Named products appear only under [Conformance](conformance/index.md) as proof
artifacts, not as requirements of the standard.

## Install

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

Point the harness at **any** reachable target and optional source tree:

```bash
export UHBS_QUICK=1
export UHBS_AIRGAP_ATTESTED=1

uhbs lab \
  --tps low_interaction \
  --protocol ssh \
  --target 127.0.0.1 --port 2200 \
  --source-root /path/to/your-decoy-sources \
  --phases profile,static,sandbox,dynamic,score \
  --quick \
  --out .local/bench-reports/my-target
```

For SSH/Telnet decoys you may also use `--tps low_interaction_ssh` (declares those protocols).  
For HTTP / PJL / other non-shell decoys, pass `--protocol http` / `--protocol pjl` (or inventory) with a **class-only** TPS such as `low_interaction` / `web_api` — never silently reuse an SSH profile.

Validate outputs:

```bash
uhbs validate-scorecard path/to/scorecard.json --strict
```

## Published evaluation proof

Sanitized fixtures that prove the tools discriminate across classes. Product
names are **proof labels only** — UHBS does not require or endorse them.

| Target (proof) | Class | UHQS | Grade | Fixture |
| --- | --- | --- | --- | --- |
| Cowrie | Low-Interaction · SSH | **48.70** | F | [`cowrie-low-interaction.scorecard.json`](conformance/fixtures/cowrie-low-interaction.scorecard.json) |
| ESPot | Web-API · HTTP | **49.82** | F | [`espot-web-api.scorecard.json`](conformance/fixtures/espot-web-api.scorecard.json) |
| miniprint | Low-Interaction · PJL | **47.77** | F | [`miniprint-low-interaction.scorecard.json`](conformance/fixtures/miniprint-low-interaction.scorecard.json) |
| Conpot | ICS-SCADA · Modbus | **55.51** | D | [`conpot-ics-scada.scorecard.json`](conformance/fixtures/conpot-ics-scada.scorecard.json) |
| OpenCanary | Web-API · HTTP | **50.12** | D | [`opencanary-web-api.scorecard.json`](conformance/fixtures/opencanary-web-api.scorecard.json) |
| CyberHalluciNet | POSIX-Shell | **80.33** | B | [`posix-shell-lab.scorecard.json`](conformance/fixtures/posix-shell-lab.scorecard.json) |

A separate **worked example** (anonymous module scores A=23.5…F=69.0 under Low-Interaction
weights) yields UHQS **46.97** — that number is **not** the live Cowrie fixture.

## Signal profiles

Module F uses **class-oriented** signal YAML under `uhbs_core/profiles/` (for
example `low_interaction_ssh_signals.yaml`). Product-specific overlays and
multi-site inventory stay in private lab repos.

## Conformance levels

| Level | Requirements |
| --- | --- |
| **UHBS-Core** | Valid TPS + scorecard schemas; UHQS/δ_C/grade integrity |
| **UHBS-Lab** | UHBS-Core + `uhbs_core` Modules A–F + evidence/MANIFEST digests |

See [conformance/index.md](conformance/index.md) and [registry.md](registry.md).
