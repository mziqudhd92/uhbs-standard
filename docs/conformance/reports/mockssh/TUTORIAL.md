# Tutorial: grade MockSSH with UHBS (SSH)

**Upstream:** [ncouture/MockSSH](https://github.com/ncouture/MockSSH) · last push `2026-06-08`

```bash
docker build -f .local/labs/mockssh/Dockerfile.lab -t mockssh:uhbs-lab .local/labs/mockssh
docker run -d --name mockssh-lab --network uhbs-lab -p 127.0.0.1:12224:2222 mockssh:uhbs-lab

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/mockssh-inventory.yaml --target mockssh-ssh \
  --tps docs/conformance/labs/mockssh/low_interaction_ssh_quick.yaml --protocol ssh \
  --quick --skip-sast-tools --out docs/conformance/reports/mockssh/ssh/quick
```

Credentials: `testadmin` / `x` (Cisco example). Published: quick **59.2 / D**, full **59.0 / D**.
