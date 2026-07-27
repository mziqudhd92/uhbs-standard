# Endlessh — published UHBS lab reports

**Proof label:** [skeeto/endlessh](https://github.com/skeeto/endlessh)  
**Class / protocol:** `Low-Interaction` · **ssh_tarpit** (generic TCP) · container port `2222`  
**UHBS:** v4.0.0 · evaluation proof only (not an endorsement)

Endlessh is an **SSH tarpit**: it accepts TCP and slowly drips random banner lines,
but **never** emits a valid `SSH-2.0-…` identification string. This grade uses the
**generic** plugin under protocol id `ssh_tarpit` — **not** the SSH/Paramiko plugin
(which hangs waiting for a handshake that never comes).

## Results at a glance

| Mode | UHQS | Grade | δ_C | Safety Gate | Folder |
| --- | --- | --- | --- | --- | --- |
| **Quick** | **46.55** | F | 0.5625 | not cleared (C=75) | [`quick/`](quick/) |
| **Full** | **54.07** | D | 0.81 | not cleared (C=90) | [`full/`](full/) |

Sanitized fixture (full): [`../../fixtures/endlessh-low-interaction.scorecard.json`](../../fixtures/endlessh-low-interaction.scorecard.json)

### Why full &gt; quick

Quick skips telemetry schema gates (optimistic C=100) and has weaker Module D
(airgap only → C=75, δ_C=0.5625). Full measures telemetry honestly (C=55), runs
SAST (F capped at 70), and records a clean gateway canary (D=90, δ_C=0.81).

**Takeaway:** prefer **full/**; do **not** grade Endlessh with `--protocol ssh`.

## Contents

| Document | Purpose |
| --- | --- |
| [TUTORIAL.md](TUTORIAL.md) | Step-by-step Docker replication |
| [METHODOLOGY.md](METHODOLOGY.md) | Digests, tarpit limits, verification |
| [`quick/SCORECARD.txt`](quick/SCORECARD.txt) | Human scorecard (quick) |
| [`full/SCORECARD.txt`](full/SCORECARD.txt) | Human scorecard (full) |
| [`full/static/`](full/static/) | Bandit / Semgrep (full) |

## Module snapshot (full)

| Module | Score | Evidence highlight |
| --- | --- | --- |
| A Protocol | 65.43 | Generic connect/banner/timing (n=1000); no SSH RFC suite |
| B Behavior | 62.5 | Survived binary blast |
| C Telemetry | 55.0 | Docker/log text — no STIX/OTel/ECS (capped) |
| D Containment | 90.0 | No `ports.ssh` → shell probes skipped; airgap + gateway |
| E Scale | 100.0 | 200 TCP connects @ concurrency 25; P95 ≪ 150 ms |
| F Static | 70.0 | Semgrep findings; SAST gate cap |

## Start here

1. [METHODOLOGY.md](METHODOLOGY.md)  
2. [TUTORIAL.md](TUTORIAL.md)  
3. [`full/SCORECARD.txt`](full/SCORECARD.txt)  

Back to the [reports index](../index.md).
