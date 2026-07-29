# Tutorial: grade SHIVA with UHBS (SMTP)

**Upstream:** [shiva-spampot/shiva](https://github.com/shiva-spampot/shiva) · last push `2025-03-31`

```bash
docker build -t shiva-receiver:uhbs-lab -f .local/labs/shiva/receiver/src/Dockerfile .local/labs/shiva/receiver/src
mkdir -p .local/labs/shiva/data/mails
docker run -d --name shiva-lab --network uhbs-lab \
  -p 127.0.0.1:2526:2525 \
  -v "$PWD/.local/labs/shiva/data/mails:/tmp/spam_queue" \
  -e QUEUE_DIR=/tmp/spam_queue/ -e SHIVA_HOST=0.0.0.0 -e SHIVA_PORT=2525 \
  shiva-receiver:uhbs-lab

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/shiva-inventory.yaml --target shiva-smtp \
  --tps docs/conformance/labs/shiva/low_interaction_smtp_quick.yaml --protocol smtp \
  --quick --skip-sast-tools --out docs/conformance/reports/shiva/smtp/quick
```

Published: quick **45.07 / F**, full **44.96 / F**.
