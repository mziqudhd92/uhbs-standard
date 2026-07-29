# Tutorial: grade sjinks/ssh-honeypotd with UHBS (SSH)

**Upstream:** [sjinks/ssh-honeypotd](https://github.com/sjinks/ssh-honeypotd) · last push `2026-07-28`

```bash
docker network create uhbs-lab 2>/dev/null || true
docker pull wildwildangel/ssh-honeypotd:latest
docker run -d --name ssh-honeypotd-lab --network uhbs-lab \
  -p 127.0.0.1:12023:22 \
  -e ADDRESS=0.0.0.0 -e PORT=22 \
  wildwildangel/ssh-honeypotd:latest

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/ssh-honeypotd-inventory.yaml --target ssh-honeypotd-ssh \
  --tps docs/conformance/labs/ssh-honeypotd/low_interaction_ssh_quick.yaml --protocol ssh \
  --quick --skip-sast-tools --out docs/conformance/reports/ssh-honeypotd/ssh/quick
```

Published: quick **44.38 / F**, full **44.38 / F**.

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
