# Tutorial: grade mailoney with UHBS (SMTP)

**Upstream:** [phin3has/mailoney](https://github.com/phin3has/mailoney) · last push `2026-05-22`

```bash
docker build -f .local/labs/mailoney/Dockerfile -t mailoney:uhbs-lab .local/labs/mailoney
docker run -d --name mailoney-lab --network uhbs-lab -p 127.0.0.1:10025:25 \
  -e MAILONEY_DB_URL=sqlite:///mailoney.db mailoney:uhbs-lab

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/mailoney-inventory.yaml --target mailoney-smtp \
  --tps docs/conformance/labs/mailoney/low_interaction_smtp_quick.yaml --protocol smtp \
  --phases profile,static,sandbox,dynamic,score --quick --skip-sast-tools \
  --out docs/conformance/reports/mailoney/smtp/quick
```

Published: quick **38.8 / F**, full **38.69 / F**.
