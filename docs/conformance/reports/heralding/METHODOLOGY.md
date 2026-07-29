# Methodology: Heralding UHBS lab

**UHBS:** 4.2.2 · Graded **SSH** and **FTP** only (other capabilities disabled in `heralding-lab.yml`).  
Auth is intentionally rejected (credential logger). Stock SSH listen port in this build is **22**.

SSH quick **44.38 / F**, full **44.18 / F**. FTP quick **35.96 / F**, full **35.85 / F**.

## Analyst trust notes

- **Role:** Multi-protocol credential-harvesting honeypot; this UHBS proof graded SSH and FTP only.
- **Evidence primary sources:** `full/SCORECARD.txt`, `full/report.json`, this methodology, and the tutorial commands.
- **Air-gap / Safety:** lab runs used `UHBS_AIRGAP_ATTESTED=1` where noted; still isolate honeypot networks in real deployments.
- **Not in scope:** UHBS does not certify detection content packs, MITRE mappings, or production SIEM pipelines.
- **Reading guide:** [READING-UHQS.md](../READING-UHQS.md)
