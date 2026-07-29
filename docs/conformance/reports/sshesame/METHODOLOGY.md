# Methodology: sshesame UHBS lab

**UHBS:** 4.2.2 · Graded **SSH** Low-Interaction decoy.  
Runtime: official `ghcr.io/jaksi/sshesame` image; host inventory maps `127.0.0.1:12022` → container `:2022`. Accepts any password (medium session surface vs auth-only honeypots).

Quick **65.13 / D**, full **61.06 / D**.

## Analyst trust notes

- **Role:** Low-interaction SSH decoy that accepts sessions and logs activity without executing host commands.
- **Evidence primary sources:** `full/SCORECARD.txt`, `full/report.json`, this methodology, and the tutorial commands.
- **Air-gap / Safety:** lab runs used `UHBS_AIRGAP_ATTESTED=1` where noted; still isolate honeypot networks in real deployments.
- **Not in scope:** UHBS does not certify detection content packs, MITRE mappings, or production SIEM pipelines.
- **Reading guide:** [READING-UHQS.md](../READING-UHQS.md)
