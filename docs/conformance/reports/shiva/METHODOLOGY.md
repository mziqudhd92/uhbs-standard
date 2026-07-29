# Methodology: SHIVA UHBS lab

**UHBS:** 4.2.2 · Graded **SMTP** receiver only (analyzer + PostgreSQL omitted).  
Host map `2526→2525`.

Quick **45.07 / F**, full **44.96 / F**.

## Analyst trust notes

- **Role:** SMTP spam honeypot (receiver-oriented) for capturing spam/abuse mail traffic.
- **Evidence primary sources:** `full/SCORECARD.txt`, `full/report.json`, this methodology, and the tutorial commands.
- **Air-gap / Safety:** lab runs used `UHBS_AIRGAP_ATTESTED=1` where noted; still isolate honeypot networks in real deployments.
- **Not in scope:** UHBS does not certify detection content packs, MITRE mappings, or production SIEM pipelines.
- **Reading guide:** [READING-UHQS.md](../READING-UHQS.md)
