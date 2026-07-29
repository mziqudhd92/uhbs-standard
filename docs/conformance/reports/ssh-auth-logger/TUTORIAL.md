# Tutorial: grade JustinAzoff/ssh-auth-logger with UHBS (SSH)

**Upstream:** [JustinAzoff/ssh-auth-logger](https://github.com/JustinAzoff/ssh-auth-logger) · last push `2026-05-29`

```bash
docker network create uhbs-lab 2>/dev/null || true
docker pull justinazoff/ssh-auth-logger:latest
docker run -d --name ssh-auth-logger-lab --network uhbs-lab \
  -p 127.0.0.1:12024:2222 \
  -e SSHD_BIND=:2222 -e SSHD_RATE=5000000 -e SSHD_RSA_BITS=2048 \
  justinazoff/ssh-auth-logger:latest

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/ssh-auth-logger-inventory.yaml --target ssh-auth-logger-ssh \
  --tps docs/conformance/labs/ssh-auth-logger/low_interaction_ssh_quick.yaml --protocol ssh \
  --quick --skip-sast-tools --out docs/conformance/reports/ssh-auth-logger/ssh/quick
```

Lab note: default `SSHD_RATE=320` bytes/s starves Paramiko under Module A timing / Module E; grading used `SSHD_RATE=5000000` and `--concurrency 1` on full.

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
