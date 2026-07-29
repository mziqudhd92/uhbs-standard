# Tutorial: grade Elastichoney with UHBS (HTTP)

**Upstream:** [jordan-wright/elastichoney](https://github.com/jordan-wright/elastichoney) · last push `2015-07-14`

```bash
# Build lab image (modern Go; set anonymous=true in config.json)
docker build -f .local/labs/elastichoney/Dockerfile.lab -t elastichoney:uhbs-lab .local/labs/elastichoney
docker run -d --name elastichoney-lab --network uhbs-lab -p 127.0.0.1:19200:9200 elastichoney:uhbs-lab

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/elastichoney-inventory.yaml --target elastichoney-http \
  --tps docs/conformance/labs/elastichoney/web_api_http_quick.yaml --protocol http \
  --quick --skip-sast-tools --out docs/conformance/reports/elastichoney/http/quick
```

Published: quick **45.84 / F**, full **45.73 / F**.
