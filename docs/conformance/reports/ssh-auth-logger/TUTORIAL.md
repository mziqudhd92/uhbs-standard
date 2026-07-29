# Tutorial: grade JustinAzoff/ssh-auth-logger with UHBS (SSH)

**Upstream:** [JustinAzoff/ssh-auth-logger](https://github.com/JustinAzoff/ssh-auth-logger) · last push `2026-05-29`

```bash
docker network create uhbs-lab 2>/dev/null || true
docker pull justinazoff/ssh-auth-logger:latest
docker run -d --name ssh-auth-logger-lab --network uhbs-lab \
  -p 127.0.0.1:12024:2222 \
  -e SSHD_BIND=:2222 -e SSHD_RATE=5000000 -e SSHD_RSA_BITS=2048 \
  justinazoff/ssh-auth-logger:latest

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/ssh-auth-logger-inventory.yaml --target ssh-auth-logger-ssh \
  --tps docs/conformance/labs/ssh-auth-logger/low_interaction_ssh_quick.yaml --protocol ssh \
  --quick --skip-sast-tools --out docs/conformance/reports/ssh-auth-logger/ssh/quick
```

Lab note: default `SSHD_RATE=320` bytes/s starves Paramiko under Module A timing / Module E; grading used `SSHD_RATE=5000000` and `--concurrency 1` on full.

Published: quick **44.38 / F**, full **44.38 / F**.
