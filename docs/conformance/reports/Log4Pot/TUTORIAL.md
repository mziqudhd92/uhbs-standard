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
