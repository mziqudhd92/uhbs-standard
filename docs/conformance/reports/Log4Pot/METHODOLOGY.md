# Methodology: Log4Pot UHBS lab

**UHBS:** 4.2.2 · Graded **HTTP** Log4Shell decoy (`log4pot-server.py`).  
No payloader / Azure / S3 (air-gap). Chose Log4Pot over owa-honeypot for simpler stdlib HTTP.

Quick **41.71 / F**, full **38.0 / F**.

## Analyst trust notes

- **Role:** HTTP listener designed to capture Log4Shell (Log4j JNDI) exploitation attempts.
- **Evidence primary sources:** `full/SCORECARD.txt`, `full/report.json`, this methodology, and the tutorial commands.
- **Air-gap / Safety:** lab runs used `UHBS_AIRGAP_ATTESTED=1` where noted; still isolate honeypot networks in real deployments.
- **Not in scope:** UHBS does not certify detection content packs, MITRE mappings, or production SIEM pipelines.
- **Reading guide:** [READING-UHQS.md](../READING-UHQS.md)
