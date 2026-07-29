# Methodology: pghoney UHBS lab

**UHBS:** 4.2.2 · Graded **Postgres** low-interaction decoy.  
Lab rebuild modernizes Go modules; `hpfeedsConfig.enabled=false`; bind `0.0.0.0:5432`.

Quick **43.72 / F**, full **43.61 / F**.

## Analyst trust notes

- **Role:** Low-interaction PostgreSQL decoy focused on auth/handshake capture.
- **Evidence primary sources:** `full/SCORECARD.txt`, `full/report.json`, this methodology, and the tutorial commands.
- **Air-gap / Safety:** lab runs used `UHBS_AIRGAP_ATTESTED=1` where noted; still isolate honeypot networks in real deployments.
- **Not in scope:** UHBS does not certify detection content packs, MITRE mappings, or production SIEM pipelines.
- **Reading guide:** [READING-UHQS.md](../READING-UHQS.md)
