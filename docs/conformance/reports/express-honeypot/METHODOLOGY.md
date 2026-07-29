# Methodology: express-honeypot UHBS lab

**UHBS:** 4.2.2 · Graded **HTTP** RFI/LFI decoy.  
Lab config sets `remoteFileSave.dpaste=false` for air-gap.

Quick **45.84 / F**, full **45.73 / F**.

## Analyst trust notes

- **Role:** Small Express-based HTTP honeypot oriented at LFI/RFI-style web probing.
- **Evidence primary sources:** `full/SCORECARD.txt`, `full/report.json`, this methodology, and the tutorial commands.
- **Air-gap / Safety:** lab runs used `UHBS_AIRGAP_ATTESTED=1` where noted; still isolate honeypot networks in real deployments.
- **Not in scope:** UHBS does not certify detection content packs, MITRE mappings, or production SIEM pipelines.
- **Reading guide:** [READING-UHQS.md](../READING-UHQS.md)
