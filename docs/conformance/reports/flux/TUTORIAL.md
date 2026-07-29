# Tutorial: grade flux with UHBS (HTTP)

**Upstream:** [andrewmichaelsmith/flux](https://github.com/andrewmichaelsmith/flux)

```bash
docker build -f .local/labs/flux/Dockerfile.lab -t flux:uhbs-lab .local/labs/flux
docker run -d --name flux-lab --network uhbs-lab -p 127.0.0.1:18094:8080 flux:uhbs-lab

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/flux-inventory.yaml --target flux-http \
  --tps docs/conformance/labs/flux/web_api_http_quick.yaml --protocol http \
  --phases profile,static,sandbox,dynamic,score --quick --skip-sast-tools \
  --out docs/conformance/reports/flux/http/quick
```

Published: quick **50.91 / D**, full **50.91 / D**.

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
