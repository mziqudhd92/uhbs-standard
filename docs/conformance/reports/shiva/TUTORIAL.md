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
