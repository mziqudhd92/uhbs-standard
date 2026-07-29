# Tutorial: grade node-ftp-honeypot with UHBS (FTP)

**Upstream:** [christophe77/node-ftp-honeypot](https://github.com/christophe77/node-ftp-honeypot) · last push `2026-06-22`

```bash
docker build -f .local/labs/node-ftp-honeypot/Dockerfile.lab -t node-ftp-honeypot:uhbs-lab .local/labs/node-ftp-honeypot
docker run -d --name node-ftp-honeypot-lab --network uhbs-lab -p 127.0.0.1:12121:21 node-ftp-honeypot:uhbs-lab

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/node-ftp-honeypot-inventory.yaml --target node-ftp-honeypot \
  --tps docs/conformance/labs/node-ftp-honeypot/low_interaction_ftp_quick.yaml --protocol ftp \
  --phases profile,static,sandbox,dynamic,score --quick --skip-sast-tools \
  --out docs/conformance/reports/node-ftp-honeypot/ftp/quick
```

Published: quick **35.96 / F**, full **35.85 / F**.
