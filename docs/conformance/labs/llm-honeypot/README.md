# LLM Honeypot lab overlays

Configs from [PalisadeResearch/llm-honeypot](https://github.com/PalisadeResearch/llm-honeypot) for use with `cowrie/cowrie:latest` under the UHBS lab harness (SSH surface).

Replication steps, SCORECARD links, and methodology live under:

- [`docs/conformance/reports/llm-honeypot/TUTORIAL.md`](../../reports/llm-honeypot/TUTORIAL.md)
- [`docs/conformance/reports/llm-honeypot/`](../../reports/llm-honeypot/index.md)
- [`docs/conformance/reports/llm-honeypot/ssh/`](../../reports/llm-honeypot/ssh/index.md)

## Lab packaging note

This directory holds TPS YAML and inventory helpers used by `uhbs-lab` to grade the named product. Prefer the published **full** SCORECARD and `report.json` when citing UHQS. Read modules A–F with [READING-UHQS.md](../../reports/READING-UHQS.md): protocol fidelity, behavioral realism, telemetry, Safety Gate δ_C, latency, and static audit. UHBS 4.2.2 evaluation proof is informative only — isolate honeypot networks, treat LLM API keys as secrets, and wire your own telemetry shipping in real deployments. Do not invent scores without regenerating artifacts.
