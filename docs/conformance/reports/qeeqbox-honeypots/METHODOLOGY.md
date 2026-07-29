# Methodology: qeeqbox/honeypots

Graded 10 UHBS-overlapping TCP listeners on high ports. Skipped package types without UHBS plugins (dhcp, dns, imap, …). Default credentials `test`/`test` where auth applies.

## Analyst trust notes

- **Role:** Multi-protocol honeypot framework; UHBS published selected overlapping protocol grades.
- **Evidence primary sources:** `full/SCORECARD.txt`, `full/report.json`, this methodology, and the tutorial commands.
- **Air-gap / Safety:** lab runs used `UHBS_AIRGAP_ATTESTED=1` where noted; still isolate honeypot networks in real deployments.
- **Not in scope:** UHBS does not certify detection content packs, MITRE mappings, or production SIEM pipelines.
- **Reading guide:** [READING-UHQS.md](../READING-UHQS.md)
