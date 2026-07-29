# Tutorial: grade Heralding with UHBS (SSH + FTP + SMTP)

**Upstream:** [johnnykv/heralding](https://github.com/johnnykv/heralding) · last push `2024-02-28`

```bash
# SSH + FTP (shared container)
docker build -t heralding:uhbs-lab .local/labs/heralding
docker run -d --name heralding-lab --network uhbs-lab \
  -p 127.0.0.1:12227:22 -p 127.0.0.1:19027:21 \
  -v "$PWD/.local/labs/heralding/heralding-lab.yml:/config/heralding.yml:ro" \
  -w /tmp heralding:uhbs-lab heralding -c /config/heralding.yml

# SMTP (dedicated container, port 17025)
docker run -d --name heralding-smtp-lab --network uhbs-lab -p 127.0.0.1:17025:25 \
  -v "$PWD/.local/labs/heralding/heralding-smtp-lab.yml:/config/heralding.yml:ro" \
  -w /tmp heralding:uhbs-lab heralding -c /config/heralding.yml

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/heralding-smtp-inventory.yaml --target heralding-smtp \
  --tps docs/conformance/labs/heralding/low_interaction_smtp_quick.yaml --protocol smtp \
  --quick --skip-sast-tools --out docs/conformance/reports/heralding/smtp/quick
```

Published: SSH quick **44.38 / F**, full **44.18 / F**; FTP quick **35.96 / F**, full **35.85 / F**; SMTP quick **45.07 / F**, full **45.07 / F**.

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
