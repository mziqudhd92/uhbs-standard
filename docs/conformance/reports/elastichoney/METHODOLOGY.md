# Methodology: Elastichoney UHBS lab

**UHBS:** 4.2.2 · Graded **HTTP** Elasticsearch REST decoy.  
Upstream Go 1.3 Docker base replaced with `golang:1.22` lab image. `anonymous: true` avoids outbound public-IP fetch.

Quick **45.84 / F**, full **45.73 / F**.

## Analyst trust notes

- **Role:** Elasticsearch-themed HTTP decoy for ES/CVE-era probing (historic but still scanned).
- **Evidence primary sources:** `full/SCORECARD.txt`, `full/report.json`, this methodology, and the tutorial commands.
- **Air-gap / Safety:** lab runs used `UHBS_AIRGAP_ATTESTED=1` where noted; still isolate honeypot networks in real deployments.
- **Not in scope:** UHBS does not certify detection content packs, MITRE mappings, or production SIEM pipelines.
- **Reading guide:** [READING-UHQS.md](../READING-UHQS.md)
