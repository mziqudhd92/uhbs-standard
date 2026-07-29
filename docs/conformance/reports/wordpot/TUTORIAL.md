# Tutorial: grade wordpot with UHBS (HTTP)

**Upstream:** [gbrindisi/wordpot](https://github.com/gbrindisi/wordpot) · last push `2018-10-16`

```bash
docker build -f .local/labs/wordpot/Dockerfile.lab -t wordpot:uhbs-lab .local/labs/wordpot
docker run -d --name wordpot-lab --network uhbs-lab -p 127.0.0.1:18082:8080 wordpot:uhbs-lab

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/wordpot-inventory.yaml --target wordpot-http \
  --tps docs/conformance/labs/wordpot/web_api_http_quick.yaml --protocol http \
  --quick --skip-sast-tools --out docs/conformance/reports/wordpot/http/quick
```

Published: quick **41.71 / F**, full **41.6 / F**.
