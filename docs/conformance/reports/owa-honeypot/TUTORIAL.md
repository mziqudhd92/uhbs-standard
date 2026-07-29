# Tutorial: grade owa-honeypot with UHBS (HTTP)

**Upstream:** [joda32/owa-honeypot](https://github.com/joda32/owa-honeypot)

```bash
docker build -f .local/labs/owa-honeypot/Dockerfile.lab -t owa-honeypot:uhbs-lab .local/labs/owa-honeypot
docker run -d --name owa-honeypot-lab --network uhbs-lab -p 127.0.0.1:18090:8080 owa-honeypot:uhbs-lab

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/owa-honeypot-inventory.yaml --target owa-honeypot-http \
  --tps docs/conformance/labs/owa-honeypot/web_api_http_quick.yaml --protocol http \
  --phases profile,static,sandbox,dynamic,score --quick --skip-sast-tools \
  --out docs/conformance/reports/owa-honeypot/http/quick
```

Published: quick **41.71 / F**, full **41.71 / F**.

## What you get from this lab

After a successful run you should have `SCORECARD.txt`, `report.json`, and optional harness logs under the lab telemetry directory.

## How CTI / blue team should use the artifacts

1. Open the **full** SCORECARD first (authoritative).
2. Read modules **A–F** with [READING-UHQS.md](../READING-UHQS.md).
3. Confirm **δ_C** before citing UHQS externally.
4. Wire your own log shipping; Module C is harness visibility.

## Trust limits

UHBS 4.2.2 evaluation proof is **informative** — not a certification or endorsement.

## What you get from this lab

After a successful run you should have `SCORECARD.txt` (verbatim modules + UHQS + δ_C) and `report.json`. Prefer **full** over quick for operational decisions. Read modules A–F with [READING-UHQS.md](../READING-UHQS.md). Module C is harness visibility — wire your own SIEM shipping. UHBS 4.2.2 proof is informative only, not an endorsement.
