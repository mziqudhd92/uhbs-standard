# HoneyAgents (mrwadams)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/mrwadams/honeyagents](https://github.com/mrwadams/honeyagents) · commit `43d4114fe8b235c1646571f7bc50bacc7a32533a`  
**Scope:** PoC that pairs **stock Cowrie** with nginx/Apache (protected app) and an AutoGen agent. UHBS grades the **honeypot listen surface** only.

| Protocol | Class / port | Quick | Full | Notes |
| --- | --- | --- | --- | --- |
| [SSH](ssh/) | Low-Interaction · SSH :2222 (lab host :13222) | [67.94 / D](ssh/quick/) | [65.24 / D](ssh/full/) | Stock `cowrie/cowrie:latest` as in compose |
| Telnet | compose maps `:2223` | — | — | Stock Cowrie defaults leave Telnet **disabled** — not graded |
| HTTP (nginx→Apache) | `:80` / `:443` | — | — | Protected web app, **not** a honeypot decoy |
| AutoGen agent | — | — | — | Needs OpenAI API; not a network decoy |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.
