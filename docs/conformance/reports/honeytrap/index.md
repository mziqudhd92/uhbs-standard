# Honeytrap (DutchSec)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/honeytrap/honeytrap](https://github.com/honeytrap/honeytrap) · GitHub last push `2023-10-09`  
**Graded in this round:** **SSH** (single-protocol lab)

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [SSH](ssh/index.md) | yes | **yes** | [44.38 / F](ssh/quick/README.md) | [44.38 / F](ssh/full/README.md) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.

## For CTI analysts

- Honeytrap’s standalone agent exposes an SSH simulator on container port **8022** in this lab; UHBS Module B reflects credential-style interaction rather than a full Cowrie-class shell.
- **CTI:** treat captures as auth and banner intelligence unless you enable higher-interaction directors yourself.
- **Blue team:** stdout logging in this config is harness-visible only — wire Elasticsearch/Kafka yourself for production.

## Trust & limitations

- UHBS 4.2.2 evaluation proof is **informative** — not a certification or vendor ranking.
- Prefer **full/** artifacts over **quick/** for operational decisions.
- Re-run via [TUTORIAL.md](TUTORIAL.md); environment notes in [METHODOLOGY.md](METHODOLOGY.md).
- How to read modules: [READING-UHQS.md](../READING-UHQS.md)
