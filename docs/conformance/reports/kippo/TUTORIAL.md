# Tutorial: grade kippo with UHBS (ssh)

**Upstream:** [desaster/kippo](https://github.com/desaster/kippo) · **UHBS:** 4.2.2

```bash
docker network create uhbs-lab 2>/dev/null || true
docker build -f .local/labs/kippo/Dockerfile.lab -t kippo:uhbs-lab .local/labs/kippo
docker run -d --name kippo-lab --network uhbs-lab -p 127.0.0.1:12228:<container-port> kippo:uhbs-lab

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/kippo-inventory.yaml --target kippo-ssh \
  --tps docs/conformance/labs/kippo/<tps_quick>.yaml --protocol ssh \
  --phases profile,static,sandbox,dynamic,score --quick --skip-sast-tools \
  --out docs/conformance/reports/kippo/ssh/quick
```

Published: quick **35.64 / F**, full **35.64 / F**.

## What you get from this lab

This tutorial reproduces the published UHBS evaluation proof for analysts who need to verify numbers, not trust a screenshot. After a successful run you should have `SCORECARD.txt`, `report.json`, and optional telemetry under `.local/labs/kippo-telemetry`.

## How CTI / blue team should use the artifacts

Open the **full** SCORECARD first (authoritative). Treat **quick** as a smoke check. Read modules A–F with [READING-UHQS.md](../READING-UHQS.md). Confirm δ_C before citing UHQS externally. Wire your own log shipping; Module C is harness visibility, not SIEM coverage.

## Trust limits

UHBS 4.2.2 evaluation proof is **informative** — not a certification or endorsement. Re-run after upstream or TPS changes; do not invent scores without regenerating artifacts.
