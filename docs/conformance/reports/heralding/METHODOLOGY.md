# Methodology: Heralding UHBS lab

**UHBS:** 4.2.2 · Graded **SSH**, **FTP**, and **SMTP** (dedicated SMTP config `heralding-smtp-lab.yml` on host port **17025**).  
Auth is intentionally rejected on credential protocols (credential logger).

SSH quick **44.38 / F**, full **44.18 / F**. FTP quick **35.96 / F**, full **35.85 / F**. SMTP quick **45.07 / F**, full **45.07 / F** (δ_C=0.5625 on SMTP lab).

## Analyst trust notes

- **Role:** Multi-protocol credential-harvesting honeypot; SSH/FTP share one container; SMTP uses a separate container with logging disabled like the SSH/FTP lab.
- **Evidence primary sources:** `full/SCORECARD.txt`, `full/report.json`, this methodology, and the tutorial commands.
- **Air-gap / Safety:** lab runs used `UHBS_AIRGAP_ATTESTED=1` where noted; still isolate honeypot networks in real deployments.
- **Not in scope:** UHBS does not certify detection content packs, MITRE mappings, or production SIEM pipelines.
- **Reading guide:** [READING-UHQS.md](../READING-UHQS.md)
