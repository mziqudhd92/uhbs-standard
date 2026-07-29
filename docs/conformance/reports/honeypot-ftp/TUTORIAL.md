# Tutorial: grade alexbredo/honeypot-ftp (FTP)

Upstream needs external `common-modules`; this lab ships minimal `base`/`handler` stubs and `ftp_lab.py` (plain FTP).

```bash
docker build -f .local/labs/honeypot-ftp/Dockerfile.lab -t honeypot-ftp:uhbs-lab .local/labs/honeypot-ftp
docker run -d --name honeypot-ftp-lab --network uhbs-lab -p 127.0.0.1:19021:21 honeypot-ftp:uhbs-lab
```

Published: quick **42.71 / F**, full **42.6 / F**.

## What you get from this lab

This tutorial reproduces the published UHBS evaluation proof for analysts who need to verify numbers, not trust a screenshot. After a successful run you should have:

- `SCORECARD.txt` — verbatim module table, UHQS, letter grade, and δ_C Safety Gate
- `report.json` — machine-readable scores for automation / diffing
- Optional harness logs under the lab telemetry directory

## How CTI / blue team should use the artifacts

1. Open the **full** SCORECARD first (authoritative). Treat **quick** as a smoke check unless the methodology says otherwise.
2. Read modules **A–F** with [READING-UHQS.md](../READING-UHQS.md): low B is often “credential sink by design,” not a broken decoy.
3. Confirm **δ_C = 1.0** (or understand why containment failed) before citing UHQS externally.
4. Wire your own log shipping; UHBS Module C is harness visibility, not SIEM coverage.

## Trust limits

- UHBS 4.2.2 evaluation proof is **informative** — not a certification, endorsement, or ranking.
- Product names appear only under `docs/conformance/` as evaluation evidence.
- Re-run after upstream or TPS changes; do not invent scores without regenerating artifacts.
