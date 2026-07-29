# HoneyAgents (mrwadams)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/mrwadams/honeyagents](https://github.com/mrwadams/honeyagents) · commit `43d4114fe8b235c1646571f7bc50bacc7a32533a`  
**Scope:** PoC that pairs **stock Cowrie** with nginx/Apache (protected app) and an AutoGen agent. UHBS grades the **honeypot listen surface** only.

| Protocol | Class / port | Quick | Full | Notes |
| --- | --- | --- | --- | --- |
| [SSH](ssh/index.md) | Low-Interaction · SSH :2222 (lab host :13222) | [67.94 / D](ssh/quick/README.md) | [65.24 / D](ssh/full/README.md) | Stock `cowrie/cowrie:latest` as in compose |
| Telnet | compose maps `:2223` | — | — | Stock Cowrie defaults leave Telnet **disabled** — not graded |
| HTTP (nginx→Apache) | `:80` / `:443` | — | — | Protected web app, **not** a honeypot decoy |
| AutoGen agent | — | — | — | Needs OpenAI API; not a network decoy |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.


## What this decoy is

Agent-oriented honeypot graded primarily on SSH in UHBS labs.

## For CTI analysts

- SSH-focused telemetry similar to other low/medium interaction SSH decoys depending on config.

**Primary signals:** SSH auth/session events as configured.

## For blue teams / detection engineering

- Review which protocols are actually enabled before expecting multi-protocol coverage.

## Trust & limitations

- Evaluation proof under UHBS 4.2.2 — not a certification or endorsement.
- Prefer **full/** over **quick/** for decisions.
- Reading guide: [READING-UHQS.md](../READING-UHQS.md).
