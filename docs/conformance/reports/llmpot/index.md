# LLMPot (momalab)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/momalab/LLMPot](https://github.com/momalab/LLMPot) · commit `9568b5ffe6f3626c70078e53eacaac4a9fcf1b9e`  
**Paper:** [arXiv:2405.05999](https://arxiv.org/abs/2405.05999) · HF sample: [cv43/llmpot](https://huggingface.co/cv43/llmpot)

LLM-based ICS honeypot (ByT5 Modbus/S7 emulation + WAGO PLC web decoy).


## What this decoy is

LLM-assisted industrial/protocol honeypot; UHBS graded Modbus/S7comm/HTTP surfaces.

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [Modbus TCP](modbus/index.md) | yes | **yes** (HF CPU lab adapter) | [38.48 / F](modbus/quick/README.md) | [55.24 / D](modbus/full/README.md) |
| [S7comm](s7comm/index.md) | yes | **yes** (Snap7 NoLogic gold) | [45.53 / F](s7comm/quick/README.md) | [65.41 / D](s7comm/full/README.md) |
| [HTTP WAGO WBM](http/index.md) | yes | **yes** | [45.84 / F](http/quick/README.md) | [63.11 / D](http/full/README.md) |
| Honeyd WAGO fingerprint (`docker/`) | partial | no | — | — | Separate Honeyd path; not this lab |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.

## For CTI analysts

- ICS + HTTP mix supports intel on both OT scanners and web probes against the same lure family.

**Primary signals:** Modbus/S7/HTTP interactions per graded listeners.

## For blue teams / detection engineering

- Isolate OT protocol listeners from real plants; LLM features may need egress — constrain tightly.

## Trust & limitations

- Evaluation proof under UHBS 4.2.2 — not a certification or endorsement.
- Prefer **full/** over **quick/** for decisions.
- Reading guide: [READING-UHQS.md](../READING-UHQS.md).
