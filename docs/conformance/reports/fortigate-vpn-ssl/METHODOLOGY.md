# Methodology: FortiGate VPN-SSL Honeypot UHBS lab

**UHBS:** 4.2.2 · Graded **HTTP** Web-API profile.

Quick **46.78 / F**, full **46.78 / F**.

## Analyst trust notes

- **Role:** FortiGate SSL-VPN login deception with SQLite credential logging and optional external reporting pipelines.
- **Evidence primary sources:** `full/SCORECARD.txt`, `full/report.json`, this methodology, tutorial commands.
- **Air-gap / Safety:** `UHBS_AIRGAP_ATTESTED=1` operator attestation; isolate Docker network `uhbs-lab` with `127.0.0.1` binds.
- **Not in scope:** CVE completeness, MITRE mappings, production SIEM pipelines.

## Environment & containment

Labs use network `uhbs-lab`, host port `18095` → container `5000`. Telemetry directory: `.local/labs/fortigate-vpn-ssl-telemetry` (create before runs if Module C file gates are required).

## Evidence hierarchy

1. `full/SCORECARD.txt` 2. `full/report.json` 3. This methodology 4. Tutorial commands.

See [READING-UHQS.md](../READING-UHQS.md) for module interpretation.
