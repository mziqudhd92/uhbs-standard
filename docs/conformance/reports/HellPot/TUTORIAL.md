# Tutorial: grade HellPot with UHBS (HTTP)

**Upstream:** [yunginnanet/HellPot](https://github.com/yunginnanet/HellPot) · last push `2025-12-19`

```bash
docker build -f .local/labs/HellPot/Dockerfile.lab -t hellpot:uhbs-lab .local/labs/HellPot
docker run -d --name HellPot-lab --network uhbs-lab -p 127.0.0.1:18080:8080 \
  -v "$PWD/.local/labs/HellPot-logs:/logs" hellpot:uhbs-lab

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/HellPot-inventory.yaml --target HellPot-http \
  --tps docs/conformance/labs/HellPot/web_api_http_quick.yaml --protocol http \
  --phases profile,static,sandbox,dynamic,score --quick --skip-sast-tools \
  --out docs/conformance/reports/HellPot/http/quick
```

Published: quick **43.98 / F**, full **43.87 / F**.
