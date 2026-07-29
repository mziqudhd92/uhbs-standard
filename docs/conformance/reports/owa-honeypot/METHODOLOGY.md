# Methodology: owa-honeypot UHBS lab

**UHBS:** 4.2.2 · Graded **HTTP** Web-API profile.

Quick **41.71 / F**, full **41.71 / F**.

## Analyst trust notes

- **Role:** Minimal Outlook Web Access themed HTTP honeypot that captures credential POST attempts and redirects browsers to a fake OWA logon page.
- **Evidence primary sources:** `full/SCORECARD.txt`, `full/report.json`, this methodology, tutorial commands.
- **Air-gap / Safety:** `UHBS_AIRGAP_ATTESTED=1` operator attestation; isolate Docker network `uhbs-lab` with `127.0.0.1` binds.
- **Not in scope:** CVE completeness, MITRE mappings, production SIEM pipelines.

## Environment & containment

Labs use network `uhbs-lab`, host port `18090` → container `8080`. Telemetry directory: `.local/labs/owa-honeypot-telemetry` (create before runs if Module C file gates are required).

## Evidence hierarchy

1. `full/SCORECARD.txt` 2. `full/report.json` 3. This methodology 4. Tutorial commands.

See [READING-UHQS.md](../READING-UHQS.md) for module interpretation.
