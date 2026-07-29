# Methodology: HoneyPLC (skipped)

**UHBS:** 4.2.2 · **Status:** skipped in batch C — no SCORECARD artifacts.

HoneyPLC requires Honeyd, modified Snap7 binaries, snmpsim, lighttpd, and Python 2 tooling on the host. There is no maintained Dockerfile; installation steps assume Ubuntu 18.04 paths under `/usr/share/honeyd`. Standing up S7comm/SNMP/HTTP for UHBS ICS plugins exceeds the batch time budget, so the product remains a skip note only.

## Evidence hierarchy

1. `full/SCORECARD.txt` when graded  
2. `full/report.json`  
3. This methodology (scope / blockers)  
4. Tutorial replication commands  

Skip hubs explain why no SCORECARD exists yet. See [READING-UHQS.md](../READING-UHQS.md). Informative only · UHBS 4.2.2 · isolate honeypot networks in real deployments.
