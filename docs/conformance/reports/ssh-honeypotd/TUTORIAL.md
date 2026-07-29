# Tutorial: grade ssh-honeypotd with UHBS

**Upstream:** [https://github.com/sjinks/ssh-honeypotd](https://github.com/sjinks/ssh-honeypotd) · last push `2026-07-28`

```bash
# Lab container (example — see docs/conformance/labs/ssh-honeypotd/)
docker network create uhbs-lab 2>/dev/null || true

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/ssh-honeypotd-inventory.yaml --target <site> \
  --tps docs/conformance/labs/ssh-honeypotd/*_quick.yaml --protocol ssh \
  --quick --skip-sast-tools --out docs/conformance/reports/ssh-honeypotd/ssh/quick

UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/ssh-honeypotd-inventory.yaml --target <site> \
  --tps docs/conformance/labs/ssh-honeypotd/*_full.yaml --protocol ssh \
  --skip-sast-tools --out docs/conformance/reports/ssh-honeypotd/ssh/full
```

Published: quick **33.04 / F**, full **33.04 / F**.
