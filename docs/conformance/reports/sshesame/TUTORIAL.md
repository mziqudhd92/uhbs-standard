# Tutorial: grade jaksi/sshesame with UHBS (SSH)

**Upstream:** [jaksi/sshesame](https://github.com/jaksi/sshesame) · last push `2024-10-21`

```bash
docker network create uhbs-lab 2>/dev/null || true
docker pull ghcr.io/jaksi/sshesame:latest
docker run -d --name sshesame-lab --network uhbs-lab \
  -p 127.0.0.1:12022:2022 \
  -v "$PWD/.local/labs/sshesame-telemetry:/data" \
  ghcr.io/jaksi/sshesame:latest

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/sshesame-inventory.yaml --target sshesame-ssh \
  --tps docs/conformance/labs/sshesame/low_interaction_ssh_quick.yaml --protocol ssh \
  --quick --skip-sast-tools --out docs/conformance/reports/sshesame/ssh/quick
```

Published: quick **65.13 / D**, full **61.06 / D**.
