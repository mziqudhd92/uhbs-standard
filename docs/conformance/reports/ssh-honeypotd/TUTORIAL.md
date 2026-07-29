# Tutorial: grade sjinks/ssh-honeypotd with UHBS (SSH)

**Upstream:** [sjinks/ssh-honeypotd](https://github.com/sjinks/ssh-honeypotd) · last push `2026-07-28`

```bash
docker network create uhbs-lab 2>/dev/null || true
docker pull wildwildangel/ssh-honeypotd:latest
docker run -d --name ssh-honeypotd-lab --network uhbs-lab \
  -p 127.0.0.1:12023:22 \
  -e ADDRESS=0.0.0.0 -e PORT=22 \
  wildwildangel/ssh-honeypotd:latest

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/ssh-honeypotd-inventory.yaml --target ssh-honeypotd-ssh \
  --tps docs/conformance/labs/ssh-honeypotd/low_interaction_ssh_quick.yaml --protocol ssh \
  --quick --skip-sast-tools --out docs/conformance/reports/ssh-honeypotd/ssh/quick
```

Published: quick **44.38 / F**, full **44.38 / F**.
