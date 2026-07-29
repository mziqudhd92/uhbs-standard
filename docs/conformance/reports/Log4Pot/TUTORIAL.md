# Tutorial: grade Log4Pot with UHBS (HTTP)

**Upstream:** [thomaspatzke/Log4Pot](https://github.com/thomaspatzke/Log4Pot) · last push `2024-11-29`

```bash
docker build -f .local/labs/Log4Pot/Dockerfile.lab -t log4pot:uhbs-lab .local/labs/Log4Pot
docker run -d --name Log4Pot-lab --network uhbs-lab -p 127.0.0.1:18081:8080 \
  -v "$PWD/.local/labs/Log4Pot-logs:/logs" log4pot:uhbs-lab

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/Log4Pot-inventory.yaml --target Log4Pot-http \
  --tps docs/conformance/labs/Log4Pot/web_api_http_quick.yaml --protocol http \
  --phases profile,static,sandbox,dynamic,score --quick --skip-sast-tools \
  --out docs/conformance/reports/Log4Pot/http/quick
```

Published: quick **41.71 / F**, full **38.0 / F**.

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
