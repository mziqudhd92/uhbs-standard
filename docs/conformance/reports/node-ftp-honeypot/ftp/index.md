# node-ftp-honeypot — FTP

**Status:** Informative · evaluation proof  
**UHBS:** v4.2.2 · **Class:** Low-Interaction · **Protocol:** `ftp`  
**Target id:** `node-ftp-honeypot` · **Evaluated:** 2026-07-29

| Run | UHQS | Grade | δ_C | Artifacts |
| --- | ---: | --- | --- | --- |
| [Quick](quick/README.md) | **35.96** | F | 0.5625 | [`SCORECARD.txt`](quick/SCORECARD.txt) · [`report.json`](quick/report.json) |
| [Full](full/README.md) | **35.85** | F | 0.5625 | [`SCORECARD.txt`](full/SCORECARD.txt) · [`report.json`](full/report.json) |

## Full run — module breakdown (analyst view)

| Module | Score | Weight | Status | Notes |
| --- | ---: | --- | --- | --- |
| Module A: Protocol Fidelity | 60.0 | 0.30 | PARTIAL |  |
| Module B: Behavioral Realism | 54.5 | 0.15 | PARTIAL |  |
| Module C: Telemetry Quality | 55.0 | 0.25 | PARTIAL | no STIX objects found |
| Module D: Safety & Containment (C) | 75.0 | GATE | PASSED | UHBS_AIRGAP_ATTESTED=1 (operator attestation; not a substitute for shell probes on SSH decoys) |
| Module E: Scalability & Latency | 100.0 | 0.10 | PASSED | service alive after load (connect 0.3ms) |
| Module F: Static Code Audit | 69.0 | 0.20 | PARTIAL | POSIX coverage 0% (0/104) |
| Safety Gate δ_C | 0.5625 | GATE | — | Containment multiplier |


## Full scorecard (verbatim)

```text
====================================================================================
                  UNIVERSAL HONEYPOT BENCHMARK SCORECARD v4.2.2
====================================================================================
Target System         : node-ftp-honeypot
System Profile Class  : Low-Interaction
Protocols             : ftp
Evaluation Date       : 2026-07-29
Evaluation Type       : Full-Spectrum (Static Audit + Dynamic Sandbox)
Environment           : Isolated Sandbox
MCP Surface Depth     : unknown
------------------------------------------------------------------------------------
EVALUATION MODULE                     SCORE (0-100)    WEIGHT    STATUS
------------------------------------------------------------------------------------
Module A: Protocol Fidelity         :  60.0/100       0.30     PARTIAL (220-Welcome to VOFTP a very open FTP Server.
220 Ready
502 Command not whitelisted: RETR
502 Command not whitelisted:)
Module B: Behavioral Realism        :  54.5/100       0.15     PARTIAL (USER step failed: 220 Ready
)
Module C: Telemetry Quality         :  55.0/100       0.25     PARTIAL (no STIX objects found)
Module D: Safety & Containment (C)  :  75.0/100       GATE     PASSED (UHBS_AIRGAP_ATTESTED=1 (operator attestation; not a substitute for shell probes on SSH decoys))
Module E: Scalability & Latency     : 100.0/100       0.10     PASSED (service alive after load (connect 0.3ms))
Module F: Static Code Audit         :  69.0/100       0.20     PARTIAL (POSIX coverage 0% (0/104))
------------------------------------------------------------------------------------
SAFETY GATE MULTIPLIER                : δ_C = 0.5625 (C = 75.0 < 95 — exponential penalty)
FINAL COMPOSITE SCORE (UHQS 4.2.2)      : 35.85 / 100
OVERALL EVALUATION GRADE              : GRADE F (Fail)
====================================================================================
```



## CTI & blue-team reading

Lightweight FTP decoy for anonymous/auth FTP probing.

### Module interpretation (this protocol)

| Module | Score | Analyst reading |
| --- | ---: | --- |
| A — Protocol Fidelity | 60.0 | Protocol speak / banner-handshake quality for keeping automated clients engaged. |
| B — Behavioral Realism | 54.5 | Post-connect realism (auth/session). Low often means credential-only or reject-by-design. |
| C — Telemetry Quality | 55.0 | How much useful telemetry the *graded lab* exposed to UHBS — not your SIEM maturity. |
| D — Safety & Containment (C) | 75.0 | Containment/Safety Gate. Below threshold collapses UHQS via δ_C. |
| E — Scalability & Latency | 100.0 | Latency vs profile P95. Low can mean timeouts, tarpits, or slow handlers. |
| F — Static Code Audit | 69.0 | Static audit of the lab source tree — hygiene signal, not a full CVE program. |
| δ_C | 0.5625 | Safety Gate multiplier applied to composite UHQS. |

- Captures FTP login attempts and basic command probing from legacy worm/scanner ecosystems.
- Lower fidelity than medium-interaction FTP honeypots — good for presence/volume, not deep malware drop analysis alone.

- Disable real filesystem writes; use disposable storage if enabling uploads.
- Watch for bounce-scan / PORT abuse patterns if the implementation allows.

**Signals:** FTP USER/PASS, LIST/RETR attempts, client banners.

See product hub for full analyst notes and [READING-UHQS.md](../../READING-UHQS.md).

## Guides

- Product hub: [`../`](../index.md)
- [Tutorial](../TUTORIAL.md)
- [Methodology](../METHODOLOGY.md)
- Published scorecard page: [`../../../../scorecards/node-ftp-honeypot-ftp.md`](../../../../scorecards/node-ftp-honeypot-ftp.md)

> Named products appear only under conformance as evaluation proof — not UHBS requirements or endorsements.
