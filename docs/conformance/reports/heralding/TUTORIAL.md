# Tutorial: grade Heralding with UHBS (SSH + FTP)

**Upstream:** [johnnykv/heralding](https://github.com/johnnykv/heralding) · last push `2024-02-28`

```bash
# heralding-lab.yml enables ssh+ftp only; hash_cracker disabled
docker build -t heralding:uhbs-lab .local/labs/heralding
docker run -d --name heralding-lab --network uhbs-lab \
  -p 127.0.0.1:12227:22 -p 127.0.0.1:19027:21 \
  -v "$PWD/.local/labs/heralding/heralding-lab.yml:/config/heralding.yml:ro" \
  -w /tmp heralding:uhbs-lab heralding -c /config/heralding.yml

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/heralding-inventory.yaml --target heralding-ssh \
  --tps docs/conformance/labs/heralding/low_interaction_ssh_quick.yaml --protocol ssh \
  --quick --skip-sast-tools --out docs/conformance/reports/heralding/ssh/quick
```

Published: SSH quick **44.38 / F**, full **44.18 / F**; FTP quick **35.96 / F**, full **35.85 / F**.

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
