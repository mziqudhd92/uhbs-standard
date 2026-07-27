# Endlessh — published UHBS lab reports

**Proof label:** [skeeto/endlessh](https://github.com/skeeto/endlessh)  
**Class / protocol:** `Low-Interaction` · SSH tarpit · lab port `2223`  
**UHBS:** v4.0.0 · evaluation proof only (not an endorsement)

Endlessh is an **SSH tarpit**: it accepts TCP connections and slowly drips random
banner bytes, but **never** completes an RFC4253 identification / handshake.
This grade uses the SSH plugin and Low-Interaction weights as a **negative
control** — low UHQS is expected when the product goal is delay, not emulation.

## Results at a glance

| Mode | UHQS | Grade | δ_C | Safety Gate | Folder |
| --- | --- | --- | --- | --- | --- |
| **Quick** | **26.94** | F | 1.0 | cleared (C=96) | [`quick/`](quick/) |
| **Full** | **26.94** | F | 1.0 | cleared (C=96) | [`full/`](full/) |

Sanitized fixture (full): [`../../fixtures/endlessh-low-interaction.scorecard.json`](../../fixtures/endlessh-low-interaction.scorecard.json)

## Contents

| Document | Purpose |
| --- | --- |
| [TUTORIAL.md](TUTORIAL.md) | Step-by-step replication (local build) |
| [METHODOLOGY.md](METHODOLOGY.md) | Digests, tarpit limits, verification |
| [`quick/SCORECARD.txt`](quick/SCORECARD.txt) | Human scorecard (quick) |
| [`full/SCORECARD.txt`](full/SCORECARD.txt) | Human scorecard (full-lab) |

## Module snapshot (full / quick — same composite)

| Module | Score | Highlight |
| --- | --- | --- |
| A Protocol | 12.5 | No valid SSH banner / KEXINIT |
| B Behavior | 6.2 | No SSH session |
| C Telemetry | 25.0 | No session inject / CTI pipeline |
| D Containment | 96.0 | No shell breakout surface; gate cleared |
| E Scale | 20.0 | 100% SSH client errors under load |
| F Static | 70.0 | Small C tree; POSIX VFS coverage N/A |

## Start here

1. [METHODOLOGY.md](METHODOLOGY.md)  
2. [TUTORIAL.md](TUTORIAL.md)  
3. [`full/SCORECARD.txt`](full/SCORECARD.txt) / [`full/report.json`](full/report.json)  

Back to the [reports index](../index.md).
