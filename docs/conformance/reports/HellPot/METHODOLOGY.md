# Methodology: HellPot UHBS lab

**UHBS:** 4.2.2 · Graded **HTTP** endless honeypot (fasthttp + Markov).  
Lab `docker_config.toml` binds `0.0.0.0:8080` with catch-all router.

Quick **43.98 / F**, full **43.87 / F**.

## Analyst trust notes

- **Role:** HTTP tarpit that keeps aggressive bots reading endless generated content (delay/exhaustion decoy).
- **Evidence primary sources:** `full/SCORECARD.txt`, `full/report.json`, this methodology, and the tutorial commands.
- **Air-gap / Safety:** lab runs used `UHBS_AIRGAP_ATTESTED=1` where noted; still isolate honeypot networks in real deployments.
- **Not in scope:** UHBS does not certify detection content packs, MITRE mappings, or production SIEM pipelines.
- **Reading guide:** [READING-UHQS.md](../READING-UHQS.md)
