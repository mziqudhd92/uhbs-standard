# AEP Runbook

**Scope:** Laboratory / sandbox only — not real-world production testing.

## Operator workflow

1. **Produce and validate** the normal UHBS **lab** scorecard (`uhbs validate-scorecard`).
2. **Declare** hypothesis and primary outcome in `experiment.yaml`.
3. **Select** matched reference and evaluator control (**lab-safe only** — never production assets).
4. **Run** repeated **sandboxed** trials with an external collector; write local
   `trials.jsonl` (AEP does not launch trials).
5. **Validate** design and trials:
   ```bash
   uhbs aep validate experiment.yaml
   uhbs aep validate-trials trials.jsonl --experiment experiment.yaml
   ```
6. **Analyze** with uncertainty:
   ```bash
   uhbs aep analyze \
     --experiment experiment.yaml \
     --trials trials.jsonl \
     --scorecard SCORECARD.json \
     --seed 42 \
     --out advanced-evidence.json
   ```
7. **Publish** the addendum **beside** — not inside — the UHQS grade:
   ```bash
   uhbs aep report advanced-evidence.json \
     --format markdown --out ADVANCED-EVIDENCE.md
   ```

## Reproducibility checklist

- [ ] Scorecard validates under UHBS 4.4.0 (UHQS unchanged after AEP)
- [ ] Experiment attestations all `true` (sandbox, no production, local-only, informative)
- [ ] Digests/versions recorded for decoy and reference
- [ ] Randomization seed and analysis seed declared
- [ ] Primary outcome pre-registered (not changed post-hoc without disclosure)
- [ ] Raw evidence hashes present
- [ ] Sample sizes meet `repetitions.minimum_per_arm`
- [ ] Censoring flags set for timeouts
- [ ] Warnings reviewed (low n, failed controls, high censoring)

## Safety boundary

!!! note "Optional SLM (alpha)"
    To draft trials with a mock/local SLM instead of hand-written JSONL, see
    [SLM evaluator (alpha)](slm-alpha.md) — **off by default**; edit
    `aep-slm.yaml` to unlock. Then continue from validate-trials / analyze above.

`uhbs aep` accepts **local paths only**. It refuses URL / `host:port` style
inputs and never imports sockets, HTTP, SSH, subprocess, Docker, or `uhbs-lab`.
