# Methodology: mysql-honeypotd UHBS lab

**UHBS:** 4.2.2 · Graded **MySQL** low-interaction decoy (C + libev).  
Lab image builds from source on Alpine; host map `13306→3306`.

Quick **40.35 / F**, full **37.94 / F**.

## Analyst trust notes

- **Role:** Low-interaction MySQL listener for connection and auth attempt capture.
- **Evidence primary sources:** `full/SCORECARD.txt`, `full/report.json`, this methodology, and the tutorial commands.
- **Air-gap / Safety:** lab runs used `UHBS_AIRGAP_ATTESTED=1` where noted; still isolate honeypot networks in real deployments.
- **Not in scope:** UHBS does not certify detection content packs, MITRE mappings, or production SIEM pipelines.
- **Reading guide:** [READING-UHQS.md](../READING-UHQS.md)
