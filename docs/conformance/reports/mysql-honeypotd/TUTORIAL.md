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

## What you get from this lab

This tutorial reproduces the published UHBS evaluation proof for analysts who need to verify numbers, not trust a screenshot. After a successful run you should have:

- `SCORECARD.txt` — verbatim module table, UHQS, letter grade, and δ_C Safety Gate
- `report.json` — machine-readable scores for automation / diffing
- Optional harness logs under the lab telemetry directory

## How CTI / blue team should use the artifacts

1. Open the **full** SCORECARD first (authoritative). Treat **quick** as a smoke check unless the methodology says otherwise.
2. Read modules **A–F** with [READING-UHQS.md](../READING-UHQS.md): low B is often “credential sink by design,” not a broken decoy.
3. Confirm **δ_C = 1.0** (or understand why containment failed) before citing UHQS externally.
4. Wire your own log shipping; UHBS Module C is harness visibility, not SIEM coverage.

## Trust limits

- UHBS 4.2.2 evaluation proof is **informative** — not a certification, endorsement, or ranking.
- Product names appear only under `docs/conformance/` as evaluation evidence.
- Re-run after upstream or TPS changes; do not invent scores without regenerating artifacts.
