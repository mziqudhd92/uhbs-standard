# Methodology: node-ftp-honeypot UHBS lab

**UHBS:** 4.2.2 · Graded **FTP** via ftp-srv.  
Host map `12121→21`. Upload quarantine path unused during protocol grading.

Quick **35.96 / F**, full **35.85 / F**.

## Analyst trust notes

- **Role:** Lightweight FTP decoy for anonymous/auth FTP probing.
- **Evidence primary sources:** `full/SCORECARD.txt`, `full/report.json`, this methodology, and the tutorial commands.
- **Air-gap / Safety:** lab runs used `UHBS_AIRGAP_ATTESTED=1` where noted; still isolate honeypot networks in real deployments.
- **Not in scope:** UHBS does not certify detection content packs, MITRE mappings, or production SIEM pipelines.
- **Reading guide:** [READING-UHQS.md](../READING-UHQS.md)
