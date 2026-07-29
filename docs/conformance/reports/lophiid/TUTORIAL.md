# Tutorial: lophiid (skipped)

**Upstream:** [mrheinen/lophiid](https://github.com/mrheinen/lophiid)

This product was **not graded** in this UHBS round. lophiid is a hybrid AI / multi-service honeypot stack that expects OpenRouter (or similar) LLM API keys plus backend and agent containers. The lab environment has no paid LLM credentials and cannot honestly attest an air-gapped LLM path.

## What to do instead

1. Read the [skip hub](index.md) for the blocker.
2. When keys and a hermetic compose recipe exist, clone, bring up only the HTTP surface UHBS can probe, and run `uhbs-lab` like other Web-API labs (HellPot / express-honeypot pattern).
3. Publish `SCORECARD.txt` + `report.json` under `docs/conformance/reports/lophiid/http/` with verbatim module proof.

## Trust

Do not invent UHQS numbers. UHBS 4.2.2 evaluation notes are informative only — not endorsements. See [READING-UHQS.md](../READING-UHQS.md).
