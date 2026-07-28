# Methodology: HoneyAgents UHBS lab

**Status:** Informative  
**UHBS:** 4.2.2  
**Upstream commit:** `43d4114fe8b235c1646571f7bc50bacc7a32533a`

## Protocol survey

| Surface | In compose? | Live decoy? | UHBS plugin | Graded? |
| --- | --- | --- | --- | --- |
| Cowrie SSH `:2222` | yes | yes | `ssh` | **Yes** |
| Cowrie Telnet `:2223` | port published | **no** (stock defaults) | `telnet` | No |
| nginx → Apache | yes | protected app | `http` | No — not a honeypot |
| AutoGen | yes | LLM agent | — | No — needs OpenAI; not a listen decoy |

## Environment notes

- Image: `cowrie/cowrie:latest` (exact compose honeypot service)
- Host map: `127.0.0.1:13222` → container `:2222`
- Safety: `UHBS_AIRGAP_ATTESTED=1`; Module D C=100 → δ_C=1.0 on these runs
- Full stack (deny-list agent) not required for UHQS decoy scores

## Limitations

- Grades the Cowrie component HoneyAgents embeds, not AutoGen report quality
- Module C partial without STIX/OTel mounts
- Evaluation proof only — not certification
