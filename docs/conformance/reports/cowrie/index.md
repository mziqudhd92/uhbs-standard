# Cowrie — published UHBS lab reports

**Proof label:** [cowrie/cowrie](https://github.com/cowrie/cowrie)  
**Class / protocol:** `Low-Interaction` · SSH · container port `2222`  
**UHBS:** v4.0.0 · evaluation proof only (not an endorsement)

Cowrie is a medium-interaction SSH (and Telnet) honeypot. This published grade evaluates the **SSH** listener with the first-class SSH plugin and Low-Interaction class weights. Auth for the lab used `root` / `admin` (default `root`/`root` is rejected by the current Docker image).

## Results at a glance

| Mode | UHQS | Grade | δ_C | Safety Gate | Folder |
| --- | --- | --- | --- | --- | --- |
| **Quick** | **63.52** | D | 1.0 | cleared (C=100) | [`quick/`](quick/) |
| **Full** | **48.70** | F | 1.0 | cleared (C=100) | [`full/`](full/) |

Sanitized fixture (full): [`../../fixtures/cowrie-low-interaction.scorecard.json`](../../fixtures/cowrie-low-interaction.scorecard.json)

## Contents

| Document | Purpose |
| --- | --- |
| [TUTORIAL.md](TUTORIAL.md) | Step-by-step replication (Docker) |
| [METHODOLOGY.md](METHODOLOGY.md) | Digests, plugin limits, verification |
| [`quick/SCORECARD.txt`](quick/SCORECARD.txt) | Human scorecard (quick) |
| [`full/SCORECARD.txt`](full/SCORECARD.txt) | Human scorecard (full) |
| [`full/static/semgrep-report.json`](full/static/semgrep-report.json) | Module F Semgrep |
| [`full/static/bandit-report.json`](full/static/bandit-report.json) | Module F Bandit |

## Module snapshot (full)

| Module | Score | Highlight |
| --- | --- | --- |
| A Protocol | 21.5 | SSH RFC4253; null-in-ID still accepted; **n=1000** timing |
| B Behavior | 60.0 | Echo path OK; cross-session marker missing |
| C Telemetry | 55.0 | `cowrie.json` present — schema/injection gates limited (capped) |
| D Containment | 100.0 | Shell egress probes blocked; gate cleared |
| E Scale | 55.0 | SSH session P95 ~3 s under concurrency 10 |
| F Static | 70.0 | SAST gate capped (predictable seed + findings) |

## Start here

1. [METHODOLOGY.md](METHODOLOGY.md)  
2. [TUTORIAL.md](TUTORIAL.md)  
3. [`full/SCORECARD.txt`](full/SCORECARD.txt) / [`full/report.json`](full/report.json)  

Back to the [reports index](../index.md).
