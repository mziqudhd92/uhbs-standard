# DataTrap (Thales dd-honeypot)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/ThalesGroup/dd-honeypot](https://github.com/ThalesGroup/dd-honeypot) · commit `7a906e11a0b19e75a32fead2ddd9a8b2b341beec`  
**Product name:** DataTrap — data-driven AI honeypot (dataset + optional AWS Bedrock LLM)


## What this decoy is

Multi-protocol decoy suite graded across SSH/HTTP/MySQL/Redis/Telnet/PostgreSQL in UHBS labs.

## Protocol survey

| DataTrap protocol | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [SSH](ssh/) | yes | **yes** | [59.88 / D](ssh/quick/) | [55.61 / D](ssh/full/) |
| [HTTP](http/) | yes | **yes** | [45.84 / F](http/quick/) | [65.85 / D](http/full/) |
| [MySQL](mysql/) | yes | **yes** | [40.35 / F](mysql/quick/) | [50.65 / D](mysql/full/) |
| [Redis](redis/) | yes | **yes** | [42.37 / F](redis/quick/) | [60.85 / D](redis/full/) |
| [Telnet](telnet/) | yes | **yes** | [43.38 / F](telnet/quick/) | [59.88 / D](telnet/full/) |
| [PostgreSQL](postgres/) | yes (`postgres`) | **yes** | [40.35 / F](postgres/quick/) | [57.94 / D](postgres/full/) |
| Generic TCP | `generic` | no | — | — | Not stood up in this lab tree |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.

## For CTI analysts

- Cross-protocol correlation from one product family aids campaign tracking.

**Primary signals:** Per-protocol auth/session telemetry.

## For blue teams / detection engineering

- Use per-protocol hubs; tune alerts per service risk.

## Trust & limitations

- Evaluation proof under UHBS 4.2.2 — not a certification or endorsement.
- Prefer **full/** over **quick/** for decisions.
- Reading guide: [READING-UHQS.md](../READING-UHQS.md).
