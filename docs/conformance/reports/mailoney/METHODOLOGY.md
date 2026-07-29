# Methodology: mailoney UHBS lab

**UHBS:** 4.2.2 · Graded **SMTP** (SQLite-backed lab, no Postgres sidecar).  
Host map `10025→25`.

Quick **38.8 / F**, full **38.69 / F**.

## Analyst trust notes

- **Role:** SMTP honeypot for spam/abuse and mail-oriented credential or relay abuse attempts.
- **Evidence primary sources:** `full/SCORECARD.txt`, `full/report.json`, this methodology, and the tutorial commands.
- **Air-gap / Safety:** lab runs used `UHBS_AIRGAP_ATTESTED=1` where noted; still isolate honeypot networks in real deployments.
- **Not in scope:** UHBS does not certify detection content packs, MITRE mappings, or production SIEM pipelines.
- **Reading guide:** [READING-UHQS.md](../READING-UHQS.md)
