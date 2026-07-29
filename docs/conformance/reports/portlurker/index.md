# portlurker

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/bartnv/portlurker](https://github.com/bartnv/portlurker) · GitHub last push `2026-04-24`  
**Graded in this round:** **GENERIC** (single-protocol lab)

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [GENERIC](generic/index.md) | yes | **yes** | [39.84 / F](generic/quick/README.md) | [39.84 / F](generic/full/README.md) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.

## For CTI analysts

- Portlurker is a TCP listener with optional banners and file logging — UHBS grades it with the **generic** plugin (not HTTP), so Module A/B reflect connect-and-fuzz behavior rather than RFC HTTP parsing.
- **CTI:** useful for observing raw probe payloads on a single port; pair with your own protocol classifiers downstream.
- **Blue team:** enable `file_logging` or SQLite in production configs; this lab kept logging minimal for containment.

## Trust & limitations

- UHBS 4.2.2 evaluation proof is **informative** — not a certification or vendor ranking.
- Prefer **full/** artifacts over **quick/** for operational decisions.
- Re-run via [TUTORIAL.md](TUTORIAL.md); environment notes in [METHODOLOGY.md](METHODOLOGY.md).
- How to read modules: [READING-UHQS.md](../READING-UHQS.md)
