# Methodology: HoneyHTTPD UHBS lab

**UHBS:** 4.2.2 · Graded **HTTP** via `ApacheServer` handler (`config.lab.json`).  
Stock ApacheServer may answer some HTTP/1.1 probes with `426 Upgrade Required`; UHBS still scores the surface.

Quick **45.84 / F**, full **45.73 / F**.

## Analyst trust notes

- **Role:** Configurable Python HTTP imitation server for web decoy pages/endpoints.
- **Evidence primary sources:** `full/SCORECARD.txt`, `full/report.json`, this methodology, and the tutorial commands.
- **Air-gap / Safety:** lab runs used `UHBS_AIRGAP_ATTESTED=1` where noted; still isolate honeypot networks in real deployments.
- **Not in scope:** UHBS does not certify detection content packs, MITRE mappings, or production SIEM pipelines.
- **Reading guide:** [READING-UHQS.md](../READING-UHQS.md)
