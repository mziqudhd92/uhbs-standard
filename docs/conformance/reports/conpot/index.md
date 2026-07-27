# Conpot — published UHBS lab reports

**Proof label:** [mushorg/conpot](https://github.com/mushorg/conpot)  
**Class / protocol:** `ICS-SCADA` · Modbus TCP · container port `5020` (host map `502→5020`)  
**UHBS:** v4.0.0 · evaluation proof only (not an endorsement)

Conpot is an **ICS/SCADA honeypot** (default template also enables HTTP, S7, SNMP, BACnet, ENIP, FTP, TFTP, IPMI). This published grade evaluates the **Modbus** listener only — the primary ICS protocol plugin UHBS ships — so results stay comparable to other single-protocol lab reports.

## Results at a glance

| Mode | UHQS | Grade | δ_C | Safety Gate | Folder |
| --- | --- | --- | --- | --- | --- |
| **Quick** | **44.62** | F | 0.5625 | not cleared (C=75) | [`quick/`](quick/) |
| **Full** | **55.51** | D | 0.81 | not cleared (C=90) | [`full/`](full/) |

Sanitized fixture (full): [`../../fixtures/conpot-ics-scada.scorecard.json`](../../fixtures/conpot-ics-scada.scorecard.json)

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
| A Protocol | 56.5 | Modbus plugin; FC03 holding-register read fails (default map is coils/inputs); **n=1000** timing |
| B Behavior | 82.5 | Write/read exchange + binary fuzz survived |
| C Telemetry | 55.0 | `conpot.log` text — no STIX/OTel/ECS (capped) |
| D Containment | 90.0 | No `ports.ssh`; airgap + gateway; gate not cleared |
| E Scale | 100.0 | P95 ~1.7 ms at concurrency **5** / 50 requests (moderated — see methodology) |
| F Static | 70.0 | Template SSL keys + Bandit HIGH findings → SAST gate cap |

## Start here

1. [METHODOLOGY.md](METHODOLOGY.md)  
2. [TUTORIAL.md](TUTORIAL.md)  
3. [`full/SCORECARD.txt`](full/SCORECARD.txt) / [`full/report.json`](full/report.json)  

Back to the [reports index](../index.md).
