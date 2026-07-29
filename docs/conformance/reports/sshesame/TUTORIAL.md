# Tutorial: grade sshesame with UHBS

**Upstream:** [https://github.com/jaksi/sshesame](https://github.com/jaksi/sshesame) · last push `2024-10-21`

```bash
# Lab container (example — see docs/conformance/labs/sshesame/)
docker network create uhbs-lab 2>/dev/null || true

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/sshesame-inventory.yaml --target <site> \
  --tps docs/conformance/labs/sshesame/*_quick.yaml --protocol ssh \
  --quick --skip-sast-tools --out docs/conformance/reports/sshesame/ssh/quick

UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/sshesame-inventory.yaml --target <site> \
  --tps docs/conformance/labs/sshesame/*_full.yaml --protocol ssh \
  --skip-sast-tools --out docs/conformance/reports/sshesame/ssh/full
```

Published: quick **65.13 / D**, full **65.13 / D**.
