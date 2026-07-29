# Methodology: wordpot UHBS lab

**UHBS:** 4.2.2 · Graded **HTTP**. Lab image uses Python 2.7 (upstream print syntax / Flask 0.10.1); hpfeeds editable git dep omitted.

Quick **41.71 / F**, full **41.6 / F**.

## Analyst trust notes

- **Role:** WordPress-themed HTTP honeypot for CMS scanner and plugin/theme probe capture.
- **Evidence primary sources:** `full/SCORECARD.txt`, `full/report.json`, this methodology, and the tutorial commands.
- **Air-gap / Safety:** lab runs used `UHBS_AIRGAP_ATTESTED=1` where noted; still isolate honeypot networks in real deployments.
- **Not in scope:** UHBS does not certify detection content packs, MITRE mappings, or production SIEM pipelines.
- **Reading guide:** [READING-UHQS.md](../READING-UHQS.md)
