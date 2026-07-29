# Methodology: ssh-honeypotd UHBS lab

**UHBS:** 4.2.2 · Graded **SSH** Low-Interaction auth-logging decoy.  
Runtime: `wildwildangel/ssh-honeypotd:latest`; host inventory maps `127.0.0.1:12023` → container `:22`. Auth always fails (by design) → Module B/E stay low vs session-accepting honeypots.

Quick **44.38 / F**, full **44.38 / F**.

## Analyst trust notes

- **Role:** Minimal low-interaction SSH listener (C) oriented at capturing connection/auth attempts.
- **Evidence primary sources:** `full/SCORECARD.txt`, `full/report.json`, this methodology, and the tutorial commands.
- **Air-gap / Safety:** lab runs used `UHBS_AIRGAP_ATTESTED=1` where noted; still isolate honeypot networks in real deployments.
- **Not in scope:** UHBS does not certify detection content packs, MITRE mappings, or production SIEM pipelines.
- **Reading guide:** [READING-UHQS.md](../READING-UHQS.md)
