# Tutorial: grade artillery with UHBS (generic)

**Upstream:** [BinaryDefense/artillery](https://github.com/BinaryDefense/artillery) · **UHBS:** 4.2.2

```bash
docker network create uhbs-lab 2>/dev/null || true
docker build -f .local/labs/artillery/Dockerfile.lab -t artillery:uhbs-lab .local/labs/artillery
docker run -d --name artillery-lab --network uhbs-lab -p 127.0.0.1:18081:<container-port> artillery:uhbs-lab

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/artillery-inventory.yaml --target artillery-generic \
  --tps docs/conformance/labs/artillery/<tps_quick>.yaml --protocol generic \
  --phases profile,static,sandbox,dynamic,score --quick --skip-sast-tools \
  --out docs/conformance/reports/artillery/generic/quick
```

Published: quick **39.84 / F**, full **37.55 / F**.

## What you get from this lab

This tutorial reproduces the published UHBS evaluation proof for analysts who need to verify numbers, not trust a screenshot. After a successful run you should have `SCORECARD.txt`, `report.json`, and optional telemetry under `.local/labs/artillery-telemetry`.

## How CTI / blue team should use the artifacts

Open the **full** SCORECARD first (authoritative). Treat **quick** as a smoke check. Read modules A–F with [READING-UHQS.md](../READING-UHQS.md). Confirm δ_C before citing UHQS externally. Wire your own log shipping; Module C is harness visibility, not SIEM coverage.

## Trust limits

UHBS 4.2.2 evaluation proof is **informative** — not a certification or endorsement. Re-run after upstream or TPS changes; do not invent scores without regenerating artifacts.
