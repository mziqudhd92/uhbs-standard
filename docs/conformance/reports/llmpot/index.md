# LLMPot (momalab)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/momalab/LLMPot](https://github.com/momalab/LLMPot) · commit `9568b5ffe6f3626c70078e53eacaac4a9fcf1b9e`  
**Paper:** [arXiv:2405.05999](https://arxiv.org/abs/2405.05999) · HF sample: [cv43/llmpot](https://huggingface.co/cv43/llmpot)

LLM-based ICS honeypot (ByT5 Modbus/S7 emulation + WAGO PLC web decoy).

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [Modbus TCP](modbus/) | yes | **yes** (HF CPU lab adapter) | [38.48 / F](modbus/quick/) | [55.24 / D](modbus/full/) |
| [S7comm](s7comm/) | yes | **yes** (Snap7 NoLogic gold) | [45.53 / F](s7comm/quick/) | [65.41 / D](s7comm/full/) |
| [HTTP WAGO WBM](http/) | yes | **yes** | [45.84 / F](http/quick/) | [63.11 / D](http/full/) |
| Honeyd WAGO fingerprint (`docker/`) | partial | no | — | — | Separate Honeyd path; not this lab |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.
