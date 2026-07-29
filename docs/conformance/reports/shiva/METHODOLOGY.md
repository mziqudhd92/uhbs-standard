# Methodology: SHIVA UHBS lab

**UHBS:** 4.2.2 · Graded **SMTP** receiver only (analyzer + PostgreSQL omitted).  
Host map `2526→2525`.

Quick **45.07 / F**, full **44.96 / F**.

## Analyst trust notes

- **Role:** SMTP spam honeypot (receiver-oriented) for capturing spam/abuse mail traffic.
- **Evidence primary sources:** `full/SCORECARD.txt`, `full/report.json`, this methodology, and the tutorial commands.
- **Air-gap / Safety:** lab runs used `UHBS_AIRGAP_ATTESTED=1` where noted; still isolate honeypot networks in real deployments.
- **Not in scope:** UHBS does not certify detection content packs, MITRE mappings, or production SIEM pipelines.
- **Reading guide:** [READING-UHQS.md](../READING-UHQS.md)

## Environment & containment

Labs are intended for an isolated Docker network (`uhbs-lab`) with host binds on `127.0.0.1` only. `UHBS_AIRGAP_ATTESTED=1` records an operator attestation for the lab harness; it does **not** replace real egress controls, image pinning, or VLAN isolation in production.

## Evidence hierarchy

1. `full/SCORECARD.txt` (human-readable proof of modules + UHQS + grade)
2. `full/report.json` (machine-readable)
3. This methodology (class, protocol scope, known limits)
4. Tutorial commands (replication)

Quick runs are for iteration speed. Prefer **full** when publishing or comparing products.

## What UHBS does not claim

- Not a vulnerability assessment of every dependency CVE
- Not a guarantee of attacker engagement volume on the Internet
- Not a SIEM content pack or MITRE ATT&CK coverage certificate
- Not an endorsement of the named open-source project

See [READING-UHQS.md](../READING-UHQS.md) for module-by-module analyst interpretation.
