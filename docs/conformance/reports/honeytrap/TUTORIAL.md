# Tutorial: grade Honeytrap with UHBS (SSH)

**Upstream:** [honeytrap/honeytrap](https://github.com/honeytrap/honeytrap) · last push `2023-10-09`

```bash
docker network create uhbs-lab 2>/dev/null || true
docker build -f .local/labs/honeytrap/Dockerfile.lab -t honeytrap:uhbs-lab .local/labs/honeytrap
docker run -d --name honeytrap-lab --network uhbs-lab \
  -p 127.0.0.1:19102:8022 honeytrap:uhbs-lab

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/honeytrap-inventory.yaml --target honeytrap-ssh \
  --tps docs/conformance/labs/honeytrap/low_interaction_ssh_quick.yaml --protocol ssh \
  --quick --skip-sast-tools --out docs/conformance/reports/honeytrap/ssh/quick
```

Repeat without `--quick` and with `low_interaction_ssh_full.yaml` for the full run.

## What you get / what this means

Graded labs produce `SCORECARD.txt` (verbatim modules + UHQS + δ_C) and `report.json`. Prefer **full** over quick. Read A–F with [READING-UHQS.md](../READING-UHQS.md). Module C is harness visibility — wire SIEM yourself. Skip notes mean no UHQS was invented; re-queue when a hermetic recipe exists. UHBS 4.2.2 proof is informative only — not an endorsement.

## Analyst checklist

- Prefer published **full** SCORECARD artifacts when present; never invent UHQS for skip hubs.
- Confirm Safety Gate / δ_C before citing a composite score externally.
- Wire your own log shipping — Module C is harness visibility, not SIEM coverage.
- Re-run after upstream or TPS changes; keep class/protocol/target ids aligned with inventory.
- UHBS 4.2.2 remains a personal open-source beta evaluation framework (Apache-2.0) — informative proof only.
