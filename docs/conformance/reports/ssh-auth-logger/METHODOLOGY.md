# Methodology: ssh-auth-logger UHBS lab

**UHBS:** 4.2.2 · Graded **SSH** Low/zero-Interaction auth logger.  
Runtime: `justinazoff/ssh-auth-logger:latest` (`SSHD_BIND=:2222`). Host inventory maps `127.0.0.1:12024`. Auth always fails; elevated `SSHD_RATE` avoids tarpit-like banner stalls under 1000-sample Module A.

Quick **44.38 / F**, full **44.38 / F**.

## Analyst trust notes

- **Role:** Zero/low-interaction SSH authentication logger — records auth, does not grant a real shell.
- **Evidence primary sources:** `full/SCORECARD.txt`, `full/report.json`, this methodology, and the tutorial commands.
- **Air-gap / Safety:** lab runs used `UHBS_AIRGAP_ATTESTED=1` where noted; still isolate honeypot networks in real deployments.
- **Not in scope:** UHBS does not certify detection content packs, MITRE mappings, or production SIEM pipelines.
- **Reading guide:** [READING-UHQS.md](../READING-UHQS.md)
