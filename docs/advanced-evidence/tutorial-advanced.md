# Advanced Tutorial: Design and Publish a Reproducible AEP Study

Audience: researchers, red teams, LLM-honeypot developers, and ICS evaluators.

## Dataset

Export the packaged advanced bundle (no git checkout required):

```bash
uhbs aep example advanced --out aep-advanced
cd aep-advanced
uhbs aep validate experiment.yaml
uhbs aep validate-trials trials.jsonl --experiment experiment.yaml
uhbs aep analyze \
  --experiment experiment.yaml \
  --trials trials.jsonl \
  --bootstrap-samples 500 \
  --confidence 0.95 \
  --seed 99 \
  --out advanced-evidence.json
uhbs aep report advanced-evidence.json --format markdown --out ADVANCED-EVIDENCE.md
```

A git checkout also keeps the same files under `examples/advanced-evidence/advanced/`.

## Study design walkthrough

1. **Pre-register** hypothesis + primary outcome (`fsv` in the example)
2. **Declare** capability tier, budget, timeout, randomization seed
3. **Collect** local trial JSONL from a separate sandboxed runner (not `uhbs aep`)
4. **Validate** before analysis
5. **Analyze** with fixed seeds; review `control_failed` / `inconclusive`
6. **Sensitivity:** re-run with alternate `--seed` / bootstrap counts; compare intervals
7. **Publish** `advanced-evidence.json`, `ADVANCED-EVIDENCE.md`, manifest, trial
   schema version, and hashes **beside** the UHQS scorecard

## Metric interpretation

| Metric | Read as |
| --- | --- |
| VoD | Depends entirely on the declared utility weights |
| FSV | Per-layer TPR/FPR; protocol may outperform network in the example |
| DTDR | Requires matched conditions; KM medians when censored |
| EER | Fraction of **declared** attacker budget, not universal cost |

## Scenario notes (still local files only)

### LLM / token cost

Record `costs.attacker_token_cost` and include it in `utility.weights` when VoD
should reflect token burn.

### Tarpit / dwell-time

Long decoy dwell can raise DTDR (beneficial friction) while Module E still
reports service latency for implementation quality.

### ICS / state consistency

Populate `detector.layer: state` with memory/register consistency outcomes from
**lab** fixtures. Never point collectors at production OT.

## Control failure drill

If any `evaluator_control` row sets `evaluator_control_passed: false`, analysis
status becomes `control_failed` and capability-linked claims must be withheld.

## Publishing checklist

- [ ] Scorecard + AEP addendum clearly separated  
- [ ] No certification language  
- [ ] Digests, seeds, and raw hashes included  
- [ ] Limitations section retained  
- [ ] UHQS re-validated unchanged  

See [Research foundations](research-foundations.md) and
[Improvement notes](improvement-notes.md).
