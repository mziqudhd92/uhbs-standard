# Beginner AEP example (synthetic, offline)

Safe synthetic trial evidence for the beginner tutorial. No network access required.

Prefer the packaged export (works from a PyPI install without this checkout):

```bash
pip install 'uhbs[aep]'
uhbs aep example beginner --out aep-beginner
cd aep-beginner
```

Or run from this directory in a git checkout:

```bash
uhbs aep validate experiment.yaml
uhbs aep validate-trials trials.jsonl --experiment experiment.yaml
uhbs aep analyze --experiment experiment.yaml --trials trials.jsonl \
  --scorecard linked-scorecard.json --seed 7 --out advanced-evidence.json
uhbs aep report advanced-evidence.json --format markdown --out ADVANCED-EVIDENCE.md
uhbs validate-scorecard linked-scorecard.json   # UHQS unchanged
```
