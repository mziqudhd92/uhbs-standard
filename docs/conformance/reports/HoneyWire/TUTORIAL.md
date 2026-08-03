# Tutorial: grade HoneyWire WebRouterDecoy with UHBS (HTTP)

**Upstream:** [andreicscs/HoneyWire](https://github.com/andreicscs/HoneyWire) · last push `2026-07-19`

```bash
# 1) Hub (compose excerpt from upstream README; map 8080→18088)
docker compose -f .local/labs/HoneyWire/docker-compose.yml up -d
curl -sS http://127.0.0.1:18088/api/v2/setup -H 'Content-Type: application/json' \
  -d '{"password":"…","hubEndpoint":"http://honeywire-hub:8080","hubKey":"hw_sk_…"}'
# login → create node → note apiKey

# 2) WebRouterDecoy on uhbs-lab network
docker run -d --name honeywire-webdecoy --network uhbs-lab \
  -p 127.0.0.1:18081:8081 \
  -e HW_HUB_ENDPOINT=http://honeywire-hub:8080 \
  -e HW_HUB_KEY="$NODE_API_KEY" \
  -e HW_SENSOR_ID=hw-sensor-web-router-decoy \
  -e HW_BIND_PORT=8081 \
  -e HW_ROUTER_BRAND=Netgear \
  ghcr.io/andreicscs/honeywire-webrouterdecoy:latest

# 3) Grade (host-mapped port)
UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory docs/conformance/labs/HoneyWire/inventory.yaml \
  --target HoneyWire-http \
  --tps docs/conformance/labs/HoneyWire/web_api_http_quick.yaml \
  --protocol http --class Web-API \
  --source-root /path/to/HoneyWire/Sensors/official/WebRouterDecoy \
  --phases profile,static,sandbox,dynamic,score --quick --skip-sast-tools \
  --out docs/conformance/reports/HoneyWire/http/quick
```

Published: quick **45.84 / F**, full **45.84 / F**.

## What you get from this lab

This tutorial reproduces the published UHBS evaluation proof for analysts who need to verify numbers, not trust a screenshot. After a successful run you should have:

- `SCORECARD.txt` — verbatim module table, UHQS, letter grade, and δ_C Safety Gate
- `report.json` — machine-readable scores for automation / diffing
- Optional harness logs under the lab telemetry directory

## How CTI / blue team should use the artifacts

1. Open the **full** SCORECARD first (authoritative). Treat **quick** as a smoke check unless the methodology says otherwise.
2. Read modules **A–F** with [READING-UHQS.md](../READING-UHQS.md).
3. Confirm **δ_C** (or understand why containment failed) before citing UHQS externally.
4. Wire Hub/SIEM shipping separately; UHBS Module C is harness visibility, not SIEM coverage.

## Trust limits

- UHBS 4.4.4 evaluation proof is **informative** — not a certification, endorsement, or ranking.
- Product names appear only under `docs/conformance/` as evaluation evidence.
- Re-run after upstream or TPS changes; do not invent scores without regenerating artifacts.
