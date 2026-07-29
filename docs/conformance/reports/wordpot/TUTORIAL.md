# Tutorial: grade wordpot with UHBS (HTTP)

**Upstream:** [gbrindisi/wordpot](https://github.com/gbrindisi/wordpot) · last push `2018-10-16`

```bash
docker build -f .local/labs/wordpot/Dockerfile.lab -t wordpot:uhbs-lab .local/labs/wordpot
docker run -d --name wordpot-lab --network uhbs-lab -p 127.0.0.1:18082:8080 wordpot:uhbs-lab

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/wordpot-inventory.yaml --target wordpot-http \
  --tps docs/conformance/labs/wordpot/web_api_http_quick.yaml --protocol http \
  --quick --skip-sast-tools --out docs/conformance/reports/wordpot/http/quick
```

Published: quick **41.71 / F**, full **41.6 / F**.

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
