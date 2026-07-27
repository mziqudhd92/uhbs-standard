# miniprint — published UHBS lab reports

**Proof label:** [sa7mon/miniprint](https://github.com/sa7mon/miniprint)  
**Class / protocol:** `Low-Interaction` · PJL / raw TCP · port `9100`  
**UHBS:** v4.0.1 · evaluation proof only (not an endorsement)

miniprint is a **medium-interaction printer honeypot** that speaks Printer Job Language (PJL) on the classic raw print port. UHBS does not yet ship a first-class PJL RFC suite — Module A uses the **generic TCP** plugin under protocol id `pjl` (connect / banner / timing / fuzz). That limitation is documented so grades stay interpretable.

## Results at a glance

| Mode | UHQS | Grade | δ_C | Safety Gate | Folder |
| --- | --- | --- | --- | --- | --- |
| **Quick** | **41.83** | F | 0.5625 | not cleared (C=75) | [`quick/`](quick/) |
| **Full** | **50.43** | D | 0.81 | not cleared (C=90) | [`full/`](full/) |

Sanitized fixture (full): [`../../fixtures/miniprint-low-interaction.scorecard.json`](../../fixtures/miniprint-low-interaction.scorecard.json)

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
| A Protocol | 65.4 | Generic PJL/TCP; high IAT jitter; **n=1000** samples |
| B Behavior | 62.5 | Survived binary blast; limited PJL state probes |
| C Telemetry | 55.0 | `miniprint.log` text — no STIX/OTel/ECS (capped) |
| D Containment | 90.0 | No remote shell listener configured; airgap + gateway; gate not cleared |
| E Scale | 55.0 | P95 ~1 s under concurrency 25 (single-threaded server) |
| F Static | 70.0 | Semgrep 1 critical → SAST gate cap |

## Start here

1. [METHODOLOGY.md](METHODOLOGY.md)  
2. [TUTORIAL.md](TUTORIAL.md)  
3. [`full/SCORECARD.txt`](full/SCORECARD.txt) / [`full/report.json`](full/report.json)  

Back to the [reports index](../index.md).
