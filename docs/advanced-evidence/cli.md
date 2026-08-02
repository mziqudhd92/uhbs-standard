# AEP CLI Reference

```bash
python -m venv .venv
source .venv/bin/activate
pip install 'uhbs[aep]'
uhbs aep --help
```

`uhbs[aep]` is an offline analysis extra for **lab evidence files**. It does
**not** install networking, attack, agent, browser, cloud, container, or
protocol-probing packages, and it is **not** for real-world production testing.
Plain `pip install uhbs` stays base-only. Related extras:

| Extra | Purpose |
| --- | --- |
| `uhbs[lab]` | Controlled live Modules A–F harness |
| `uhbs[mcp]` | Local AI-host scorecard tools |
| `uhbs[aep]` | Offline advanced evidence analysis |
| `uhbs[aep-slm]` | Alpha SLM trial generator (marker extra; **disabled until you edit config**) — [full guide](slm-alpha.md) |
| `uhbs[all]` | Convenience meta-extra (`lab`+`mcp`+`scapy`) — still not an attack runner for AEP |

## Command-safety matrix

| Input | Accepted? |
| --- | --- |
| Local `experiment.yaml` / `trials.jsonl` / scorecard path | Yes |
| `--out` local path | Yes |
| URL / `host:port` / credentials / executable / container options | **No** |

No AEP command launches probes, SSH, HTTP clients, Docker, plugins, or `uhbs-lab`.

## Subcommands

### `uhbs aep init`

```bash
uhbs aep init --name my-study --class Web-API --trials 5 --seed 42 --out aep-experiment/
# overwrite an existing bundle only when intentional:
uhbs aep init --force --out aep-experiment/
```

Writes `experiment.yaml`, synthetic `trials.jsonl`, and a README. Replace
synthetic rows before publishing. `repetitions.minimum_per_arm` is always
≤ `--trials` so the generated bundle validates immediately.

### `uhbs aep example`

```bash
uhbs aep example beginner --out aep-beginner
uhbs aep example advanced --out aep-advanced
uhbs aep example template --out aep-template
```

Copies packaged synthetic bundles shipped inside the wheel (same content as
`examples/advanced-evidence/` / `templates/advanced-evidence/` in a checkout).

### `uhbs aep validate`

```bash
uhbs aep validate aep-experiment/experiment.yaml
uhbs aep validate aep-experiment/experiment.yaml --json
uhbs aep validate aep-experiment/experiment.yaml --no-strict
```

Exit code `1` on schema/attestation errors.

### `uhbs aep validate-trials`

```bash
uhbs aep validate-trials aep-experiment/trials.jsonl \
  --experiment aep-experiment/experiment.yaml --strict
```

Checks trial schema, IDs, timestamps, arm balance, and experiment cross-links.

### `uhbs aep analyze` {#uhbs-aep-analyze}

```bash
uhbs aep analyze \
  --experiment aep-experiment/experiment.yaml \
  --trials aep-experiment/trials.jsonl \
  --scorecard out/SCORECARD.json \
  --bootstrap-samples 1000 \
  --confidence 0.95 \
  --seed 42 \
  --out out/advanced-evidence.json
```

Deterministic for identical inputs and seed. Overwrites `--out` explicitly.
Never mutates the scorecard or trial files.

### `uhbs aep report`

```bash
uhbs aep report out/advanced-evidence.json \
  --format markdown --include-methodology \
  --out out/ADVANCED-EVIDENCE.md
```

`--format json` re-emits the validated addendum.

### AEP SLM commands (alpha, opt-in) {#aep-slm}

Full guide (what / why / unlock checklist / providers):
[SLM evaluator (alpha)](slm-alpha.md) ·
[GitHub Pages](https://uhbs.github.io/uhbs-standard/mkdocs/advanced-evidence/slm-alpha/).

Install does **not** activate it. Purpose: draft AEP trial JSONL for offline
analyze (dry-runs, recorded replay, or loopback local models). Does **not**
change UHQS.

```bash
uhbs aep slm init --out aep-slm.yaml
uhbs aep slm status aep-slm.yaml
uhbs aep slm validate aep-slm.yaml
# After editing the YAML unlock gates (enabled + phrase + attestations):
uhbs aep slm generate aep-slm.yaml
```

`generate` refuses default/locked configs. Providers: `mock` (default, offline),
`recorded`, or loopback-only `openai_compatible` (redirects refused; body capped).

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | Success |
| 1 | Validation / analysis / schema error |
| 2 | Click usage error |

## Status values

`valid | inconclusive | control_failed` on the addendum — not letter grades.

## Schema locations

Packaged under the installed `uhbs_cli/schemas/` directory (and repo `schemas/`).
Set `UHBS_SCHEMA_DIR` only for local overrides.
