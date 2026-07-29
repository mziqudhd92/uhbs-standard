# LLM Honeypot (Palisade Research)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/PalisadeResearch/llm-honeypot](https://github.com/PalisadeResearch/llm-honeypot) · commit `156004a1b122f201448635417ee47bd44d7f28ca`  
**Scope:** Modified [Cowrie](https://github.com/cowrie/cowrie) with LLM prompt-injection traps. Shipped config enables **SSH only**.

| Protocol | Class / port | Quick | Full | Notes |
| --- | --- | --- | --- | --- |
| [SSH](ssh/) | Low-Interaction · SSH :2222 (lab host :12222) | [67.94 / D](ssh/quick/) | [61.17 / D](ssh/full/) | SFTP subsystem on (not a separate UHBS listen) |
| Telnet | — | — | — | Present in Cowrie `cowrie.cfg` but **`enabled = false`** — not graded |
| HTTP dashboard | — | — | — | `docker compose` web UI for logs — not a decoy listen surface |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.


## What this decoy is

LLM-augmented SSH honeypot (Palisade) graded on SSH in UHBS labs.

## For CTI analysts

- Post-auth dialogue may be LLM-generated — valuable for studying how actors probe “smart” shells, with prompt-injection caveats.

**Primary signals:** SSH sessions and command dialogue under LLM responses.

## For blue teams / detection engineering

- Control outbound model API access; treat LLM backends as part of the attack surface.

## Trust & limitations

- Evaluation proof under UHBS 4.2.2 — not a certification or endorsement.
- Prefer **full/** over **quick/** for decisions.
- Reading guide: [READING-UHQS.md](../READING-UHQS.md).
