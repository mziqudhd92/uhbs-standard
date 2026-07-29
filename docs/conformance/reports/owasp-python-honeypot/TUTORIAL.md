# Tutorial: grade OWASP Python-Honeypot with UHBS (HTTP)

**Upstream:** [OWASP/Python-Honeypot](https://github.com/OWASP/Python-Honeypot)

```bash
docker build -f .local/labs/owasp-python-honeypot/Dockerfile.lab -t owasp-python-honeypot:uhbs-lab .local/labs/owasp-python-honeypot
docker run -d --name owasp-python-honeypot-lab --network uhbs-lab -p 127.0.0.1:17080:80 owasp-python-honeypot:uhbs-lab

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/owasp-python-honeypot-inventory.yaml --target owasp-python-honeypot-http \
  --tps docs/conformance/labs/owasp-python-honeypot/web_api_http_quick.yaml --protocol http \
  --phases profile,static,sandbox,dynamic,score --quick --skip-sast-tools \
  --out docs/conformance/reports/owasp-python-honeypot/http/quick

UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/owasp-python-honeypot-inventory.yaml --target owasp-python-honeypot-http \
  --tps docs/conformance/labs/owasp-python-honeypot/web_api_http_full.yaml --protocol http \
  --phases profile,static,sandbox,dynamic,score --skip-sast-tools \
  --out docs/conformance/reports/owasp-python-honeypot/http/full
```

Published: quick **43.98 / F**, full **43.98 / F** (δ_C=0.5625).

## What you get from this lab

After a successful run you should have `SCORECARD.txt`, `report.json`, and optional static audit artifacts under the output directory.

## How CTI / blue team should use the artifacts

1. Open the **full** SCORECARD first.
2. Read modules A–F with [READING-UHQS.md](../READING-UHQS.md).
3. Confirm δ_C before citing UHQS externally.
4. Wire your own log shipping; Module C is harness visibility.

## Trust limits

Informative UHBS 4.2.2 evaluation proof — not a certification. Re-run after upstream or TPS changes.
