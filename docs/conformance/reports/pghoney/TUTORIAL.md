# Tutorial: grade pghoney with UHBS (Postgres)

**Upstream:** [betheroot/pghoney](https://github.com/betheroot/pghoney) · last push `2024-05-20`

```bash
docker build -f .local/labs/pghoney/Dockerfile.lab -t pghoney:uhbs-lab .local/labs/pghoney
docker run -d --name pghoney-lab --network uhbs-lab -p 127.0.0.1:15432:5432 pghoney:uhbs-lab

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/pghoney-inventory.yaml --target pghoney-postgres \
  --tps docs/conformance/labs/pghoney/database_postgres_quick.yaml --protocol postgres \
  --phases profile,static,sandbox,dynamic,score --quick --skip-sast-tools \
  --out docs/conformance/reports/pghoney/postgres/quick
```

Published: quick **43.72 / F**, full **43.61 / F**.
