# Methodology: acra (skipped)

Acra is a database encryption/SQL proxy suite with poison-record IDS, not a standalone protocol honeypot listener. No UHBS protocol grade applies.

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
