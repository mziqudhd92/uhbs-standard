# Methodology: MockSSH UHBS lab

**UHBS:** 4.2.2 · Graded **SSH** with the stock `mock_cisco.py` example (Twisted MockSSH 2.x).  
Auth succeeds; many Module B shell probes fail because the decoy is a Cisco CLI, not a POSIX shell.

Quick **59.2 / D**, full **59.0 / D**.

## Analyst trust notes

- **Role:** Twisted-based mock SSH presenting scripted device-like behavior (lab used Cisco-style example).
- **Evidence primary sources:** `full/SCORECARD.txt`, `full/report.json`, this methodology, and the tutorial commands.
- **Air-gap / Safety:** lab runs used `UHBS_AIRGAP_ATTESTED=1` where noted; still isolate honeypot networks in real deployments.
- **Not in scope:** UHBS does not certify detection content packs, MITRE mappings, or production SIEM pipelines.
- **Reading guide:** [READING-UHQS.md](../READING-UHQS.md)
