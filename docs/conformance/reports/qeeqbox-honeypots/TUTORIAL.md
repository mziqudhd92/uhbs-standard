# Tutorial: grade qeeqbox/honeypots

```bash
docker build -f .local/labs/honeypots/Dockerfile.lab -t qeeqbox-honeypots:uhbs-lab .local/labs/honeypots
docker run -d --name qeeqbox-lab --network uhbs-lab \
  -p 127.0.0.1:19022:19022 -p 127.0.0.1:19080:19080 \
  # ... see inventory for ports ...
  qeeqbox-honeypots:uhbs-lab

# Example SSH:
UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/qeeqbox-inventory.yaml --target qeeqbox-ssh \
  --tps docs/conformance/labs/qeeqbox-honeypots/low_interaction_ssh_quick.yaml \
  --protocol ssh --quick --skip-sast-tools \
  --out docs/conformance/reports/qeeqbox-honeypots/ssh/quick
```
