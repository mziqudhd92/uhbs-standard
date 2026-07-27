# ESPot — published UHBS lab reports

**Proof label:** [mycert/ESPot](https://github.com/mycert/ESPot)  
**Class / protocol:** `Web-API` · HTTP · port `9200`  
**UHBS:** v4.0.1 · evaluation proof only (not an endorsement)

ESPot is an old Node.js Elasticsearch honeypot aimed at CVE-2014-3120. These reports show what UHBS-Lab produces for that decoy in Docker — including how a **quick** smoke grade differs from a **full** grade.

## Results at a glance

| Mode | UHQS | Grade | δ_C | Safety Gate | Folder |
| --- | --- | --- | --- | --- | --- |
| **Quick** | **49.34** | F | 0.5625 | not cleared (C=75) | [`quick/`](quick/) |
| **Full** | **63.33** | D | 0.81 | not cleared (C=90) | [`full/`](full/) |

Sanitized fixture (full run): [`../../fixtures/espot-web-api.scorecard.json`](../../fixtures/espot-web-api.scorecard.json)

### Why full can score *higher* than quick

Quick skips telemetry + SAST and shortens timing, but Module C can look **optimistically high** (100) while Module D stays weak (75) without a gateway log — so δ_C bites harder (0.5625).  
Full measures telemetry honestly (C=55), runs SAST (F capped at 70), and records a clean gateway canary (D=90) — δ_C improves to 0.81. Module A is **86.75** on both modes after 0–100 CheckResult normalization (illegal `HTTP/9.9` still returns 200).

**Takeaway for readers:** compare modes carefully; **full/** is the claim-grade run.

## Contents

| Document | Purpose |
| --- | --- |
| [TUTORIAL.md](TUTORIAL.md) | Step-by-step: revive ESPot, seed logs, run quick + full Docker grades |
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
| A Protocol | 86.75 | RFC 9110: `HTTP/9.9` still returns **200**; **n=1000** timing samples |
| B Behavior | 82.5 | Consistent GET; survived binary blast |
| C Telemetry | 55.0 | `access.log` only — no STIX/OTel/ECS (schema-capped) |
| D Containment | 90.0 | HTTP-only decoy (no shell-exec port); airgap + gateway canary; gate not cleared |
| E Scale | 100.0 | 200 req @ concurrency 25; P95 ≪ 150 ms |
| F Static | 70.0 | Semgrep 2 error/critical of 6; SAST gate cap |

## Start here

1. Read [METHODOLOGY.md](METHODOLOGY.md) (trust / limitations).  
2. Follow [TUTORIAL.md](TUTORIAL.md) to reproduce.  
3. Open [`full/SCORECARD.txt`](full/SCORECARD.txt) and [`full/report.json`](full/report.json).  
4. Compare against [`quick/`](quick/) to see which knobs change the grade.

Back to the [reports index](../index.md).
