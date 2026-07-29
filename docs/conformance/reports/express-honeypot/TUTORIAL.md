# Tutorial: grade express-honeypot with UHBS (HTTP)

**Upstream:** [christophe77/express-honeypot](https://github.com/christophe77/express-honeypot) · last push `2026-06-22`

```bash
docker build -f .local/labs/express-honeypot/Dockerfile.lab -t express-honeypot:uhbs-lab .local/labs/express-honeypot
docker run -d --name express-honeypot-lab --network uhbs-lab -p 127.0.0.1:13001:3001 express-honeypot:uhbs-lab

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/express-honeypot-inventory.yaml --target express-honeypot-http \
  --tps docs/conformance/labs/express-honeypot/web_api_http_quick.yaml --protocol http \
  --phases profile,static,sandbox,dynamic,score --quick --skip-sast-tools \
  --out docs/conformance/reports/express-honeypot/http/quick
```

Published: quick **45.84 / F**, full **45.73 / F**.
