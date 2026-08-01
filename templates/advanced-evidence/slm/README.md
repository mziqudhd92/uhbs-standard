# AEP SLM evaluator config (alpha)

**Status:** alpha · **Default:** disabled · **UHQS impact:** none

This directory ships a *locked* `aep-slm.yaml`. Generation will refuse to run
until you actively edit the file.

## Activate (lab / sandbox only)

1. Ensure you have a valid local AEP `experiment.yaml` (e.g. `uhbs aep example beginner`).
2. Edit `aep-slm.yaml` and set **all** of:
   - `enabled: true`
   - `activation.unlock_phrase: I_ENABLE_AEP_SLM_ALPHA`
   - `activation.acknowledge_alpha: true`
   - `activation.lab_sandbox_only: true`
   - `activation.no_production_targets: true`
   - `activation.no_uhqs_scoring_impact: true`
   - For `openai_compatible` only: also `activation.allow_local_model_calls: true`
3. Keep `provider: mock` for offline deterministic trials, use `recorded` for
   local JSONL replay, or configure a **loopback-only** OpenAI-compatible
   local server after unlocking (`openai_compatible` refuses HTTP redirects).
4. Run:

```bash
uhbs aep slm validate aep-slm.yaml
uhbs aep slm generate aep-slm.yaml
uhbs aep validate-trials slm-trials.jsonl --experiment experiment.yaml
uhbs aep analyze --experiment experiment.yaml --trials slm-trials.jsonl --out advanced-evidence.json
```

Do **not** point this at production systems. Do **not** expect UHQS to change.
