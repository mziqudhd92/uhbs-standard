# Tutorial: grade mysql-honeypotd with UHBS (MySQL)

**Upstream:** [sjinks/mysql-honeypotd](https://github.com/sjinks/mysql-honeypotd) · last push `2026-07-28`

```bash
docker build -f .local/labs/mysql-honeypotd/Dockerfile.lab -t mysql-honeypotd:uhbs-lab .local/labs/mysql-honeypotd
docker run -d --name mysql-honeypotd-lab --network uhbs-lab -p 127.0.0.1:13306:3306 mysql-honeypotd:uhbs-lab

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/mysql-honeypotd-inventory.yaml --target mysql-honeypotd \
  --tps docs/conformance/labs/mysql-honeypotd/low_interaction_mysql_quick.yaml --protocol mysql \
  --phases profile,static,sandbox,dynamic,score --quick --skip-sast-tools \
  --out docs/conformance/reports/mysql-honeypotd/mysql/quick
```

Published: quick **40.35 / F**, full **37.94 / F**.
