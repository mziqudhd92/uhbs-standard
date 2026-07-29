# Tutorial: grade HoneyHTTPD with UHBS (HTTP)

**Upstream:** [bocajspear1/honeyhttpd](https://github.com/bocajspear1/honeyhttpd) · last push `2024-06-29`

```bash
docker build -f .local/labs/honeyhttpd/Dockerfile.lab -t honeyhttpd:uhbs-lab .local/labs/honeyhttpd
docker run -d --name honeyhttpd-lab --network uhbs-lab -p 127.0.0.1:18084:8080 honeyhttpd:uhbs-lab

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/honeyhttpd-inventory.yaml --target honeyhttpd-http \
  --tps docs/conformance/labs/honeyhttpd/web_api_http_quick.yaml --protocol http \
  --quick --skip-sast-tools --out docs/conformance/reports/honeyhttpd/http/quick
```

Published: quick **45.84 / F**, full **45.73 / F**.
