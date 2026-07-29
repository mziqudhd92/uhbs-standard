# Tutorial: grade jaksi/sshesame with UHBS (SSH)

**Upstream:** [jaksi/sshesame](https://github.com/jaksi/sshesame) · last push `2024-10-21`

```bash
docker network create uhbs-lab 2>/dev/null || true
docker pull ghcr.io/jaksi/sshesame:latest
docker run -d --name sshesame-lab --network uhbs-lab \
  -p 127.0.0.1:12022:2022 \
  -v "$PWD/.local/labs/sshesame-telemetry:/data" \
  ghcr.io/jaksi/sshesame:latest

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/sshesame-inventory.yaml --target sshesame-ssh \
  --tps docs/conformance/labs/sshesame/low_interaction_ssh_quick.yaml --protocol ssh \
  --quick --skip-sast-tools --out docs/conformance/reports/sshesame/ssh/quick
```

Published: quick **65.13 / D**, full **61.06 / D**.

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
