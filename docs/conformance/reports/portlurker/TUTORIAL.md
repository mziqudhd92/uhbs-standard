# Tutorial: grade portlurker with UHBS (generic TCP)

**Upstream:** [bartnv/portlurker](https://github.com/bartnv/portlurker)

```bash
docker build -f .local/labs/portlurker/Dockerfile.lab -t portlurker:uhbs-lab .local/labs/portlurker
docker run -d --name portlurker-lab --network uhbs-lab \
  -p 127.0.0.1:19104:8080 portlurker:uhbs-lab

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/portlurker-inventory.yaml --target portlurker-generic \
  --tps docs/conformance/labs/portlurker/low_interaction_generic_quick.yaml --protocol generic \
  --quick --skip-sast-tools --out docs/conformance/reports/portlurker/generic/quick
```

## What you get / what this means

Graded labs produce `SCORECARD.txt` (verbatim modules + UHQS + δ_C) and `report.json`. Prefer **full** over quick. Read A–F with [READING-UHQS.md](../READING-UHQS.md). Module C is harness visibility — wire SIEM yourself. Skip notes mean no UHQS was invented; re-queue when a hermetic recipe exists. UHBS 4.2.2 proof is informative only — not an endorsement.

## Analyst checklist

- Prefer published **full** SCORECARD artifacts when present; never invent UHQS for skip hubs.
- Confirm Safety Gate / δ_C before citing a composite score externally.
- Wire your own log shipping — Module C is harness visibility, not SIEM coverage.
- Re-run after upstream or TPS changes; keep class/protocol/target ids aligned with inventory.
- UHBS 4.2.2 remains an open-source beta-status evaluation framework (Apache-2.0) — informative proof only.
