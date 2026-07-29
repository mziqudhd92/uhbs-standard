# Tutorial: grade Heralding with UHBS (SSH + FTP)

**Upstream:** [johnnykv/heralding](https://github.com/johnnykv/heralding) · last push `2024-02-28`

```bash
# heralding-lab.yml enables ssh+ftp only; hash_cracker disabled
docker build -t heralding:uhbs-lab .local/labs/heralding
docker run -d --name heralding-lab --network uhbs-lab \
  -p 127.0.0.1:12227:22 -p 127.0.0.1:19027:21 \
  -v "$PWD/.local/labs/heralding/heralding-lab.yml:/config/heralding.yml:ro" \
  -w /tmp heralding:uhbs-lab heralding -c /config/heralding.yml

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/heralding-inventory.yaml --target heralding-ssh \
  --tps docs/conformance/labs/heralding/low_interaction_ssh_quick.yaml --protocol ssh \
  --quick --skip-sast-tools --out docs/conformance/reports/heralding/ssh/quick
```

Published: SSH quick **44.38 / F**, full **44.18 / F**; FTP quick **35.96 / F**, full **35.85 / F**.
