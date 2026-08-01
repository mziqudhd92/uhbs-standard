# Beginner Tutorial: Analyze Your First Controlled AEP Experiment

This tutorial is fully **offline**, deterministic, and safe. You will analyze
packaged synthetic **lab** evidence — AEP never launches attacks and is **not**
for real-world production testing. Academic credit for the AEP design vocabulary:
[Research foundations](research-foundations.md).

## Plain-language terms

| Term | Meaning |
| --- | --- |
| Decoy | The honeypot / deception surface under study |
| Matched reference | A lab twin used for comparison (not production) |
| Evaluator control | A check that the tester can perform the task at all |
| Trial | One timed attempt on one arm |
| Censoring | Session hit timeout before a natural end |
| Confidence interval | A range consistent with sampling variability |

## 1. Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install 'uhbs[aep]'
```

From a git checkout you can also use:

```bash
pip install -e '.[aep,dev]'
```

## 2. Export the packaged beginner example

After `pip install 'uhbs[aep]'` (no git checkout required):

```bash
uhbs aep example beginner --out aep-beginner
cd aep-beginner
uhbs aep validate experiment.yaml
uhbs aep validate-trials trials.jsonl --experiment experiment.yaml
```

A git checkout also keeps the same files under `examples/advanced-evidence/beginner/`.

Inspect:

- `experiment.yaml` — hypothesis, three arms, utility, attestations  
- `trials.jsonl` — decoy / reference / evaluator_control rows  
- `linked-scorecard.json` — a normal UHBS scorecard (will stay unchanged)

## 3. Analyze and report

```bash
uhbs aep analyze \
  --experiment experiment.yaml \
  --trials trials.jsonl \
  --scorecard linked-scorecard.json \
  --seed 7 \
  --out advanced-evidence.json

uhbs aep report advanced-evidence.json \
  --format markdown --out ADVANCED-EVIDENCE.md
```

## 4. Interpret

Open `ADVANCED-EVIDENCE.md`:

- Expect **DTDR > 1** (synthetic decoy dwell is longer than reference)
- Read warnings (e.g. exploratory n) without treating them as UHQS failures
- Confirm the banner: AEP does not change UHQS

## 5. Confirm UHQS unchanged

```bash
uhbs validate-scorecard linked-scorecard.json
```

The scorecard UHQS/grade must match the pre-AEP values.

## Common mistakes

| Mistake | Fix |
| --- | --- |
| Missing reference or control | Include both arms; add evaluator_control for capability claims |
| Too few trials | Meet `repetitions.minimum_per_arm` |
| Mixed units / changed task mid-study | Hold task/budget/timeout constant |
| Ignoring timeouts | Set `censored: true` |
| Treating correlation as proof | Report intervals and limitations |
| Equating `delta_uhqs` with VoD | Forbidden — VoD needs an explicit utility model |

## Next steps

- [Advanced tutorial](tutorial-advanced.md)
- [Methodology](methodology.md) · [Metrics](metrics.md)
- Optional alpha: [SLM evaluator](slm-alpha.md) if you want mock/local trial drafting
  (**off by default** — skip unless you need it)
