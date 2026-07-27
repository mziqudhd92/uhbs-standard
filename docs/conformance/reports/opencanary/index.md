# OpenCanary — published UHBS lab reports

**Proof label:** [thinkst/opencanary](https://github.com/thinkst/opencanary)  
**Class / protocol:** `Web-API` · HTTP · port `80`  
**UHBS:** v4.0.0 · evaluation proof only (not an endorsement)

OpenCanary is a multi-protocol network canary (Thinkst). Default sample also enables FTP `:21`; this published grade evaluates the **HTTP** listener only so results stay comparable to other single-protocol lab reports.

## Results at a glance

| Mode | UHQS | Grade | δ_C | Safety Gate | Folder |
| --- | --- | --- | --- | --- | --- |
| **Quick** | **41.30** | F | 0.5625 | not cleared (C=75) | [`quick/`](quick/) |
| **Full** | **50.12** | D | 0.81 | not cleared (C=90) | [`full/`](full/) |

Sanitized fixture (full run): [`../../fixtures/opencanary-web-api.scorecard.json`](../../fixtures/opencanary-web-api.scorecard.json)

### Why full scores higher than quick

Quick skips telemetry + SAST and shortens timing: Module C can look **optimistically high** (100) while Module D stays weak (75) without a gateway log — δ_C = 0.5625.  
Full measures telemetry honestly (C=55), runs SAST (F capped at 70), and records a clean gateway canary (D=90) — δ_C improves to 0.81.

**Takeaway:** compare modes carefully; **full/** is the claim-grade run.

## Contents

| Document | Purpose |
| --- | --- |
| [TUTORIAL.md](TUTORIAL.md) | Step-by-step: start OpenCanary, seed logs, run quick + full Docker grades |
| [METHODOLOGY.md](METHODOLOGY.md) | Environment, versions, image digests, limitations, verification |
| [`quick/SCORECARD.txt`](quick/SCORECARD.txt) | Human scorecard (quick) |
| [`quick/report.json`](quick/report.json) | Per-check machine evidence (quick) |
| [`quick/run-meta.json`](quick/run-meta.json) | Provenance flags (quick) |
| [`full/SCORECARD.txt`](full/SCORECARD.txt) | Human scorecard (full) |
| [`full/report.json`](full/report.json) | Per-check machine evidence (full) |
| [`full/static/semgrep-report.json`](full/static/semgrep-report.json) | Module F Semgrep output |
| [`full/static/bandit-report.json`](full/static/bandit-report.json) | Module F Bandit output |

## Module snapshot (full)

| Module | Score | Evidence highlight |
| --- | --- | --- |
| A Protocol | 21.5 | RFC 9110/9112 partial; **n=1000** timing samples |
| B Behavior | 82.5 | Consistent GET; survived binary blast |
| C Telemetry | 55.0 | JSON canary log — no STIX/OTel/ECS (schema-capped) |
| D Containment | 90.0 | HTTP-only grade (no shell-exec port); airgap + gateway canary; gate not cleared |
| E Scale | 100.0 | 200 req @ concurrency 25; P95 ≪ 150 ms |
| F Static | 70.0 | Bandit HIGH findings; SAST gate cap |

## Start here

1. Read [METHODOLOGY.md](METHODOLOGY.md) (trust / limitations).  
2. Follow [TUTORIAL.md](TUTORIAL.md) to reproduce.  
3. Open [`full/SCORECARD.txt`](full/SCORECARD.txt) and [`full/report.json`](full/report.json).  
4. Compare against [`quick/`](quick/) to see which knobs change the grade.

Back to the [reports index](../index.md).
