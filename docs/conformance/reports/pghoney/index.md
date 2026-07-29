# pghoney (betheroot)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/betheroot/pghoney](https://github.com/betheroot/pghoney) · GitHub last push `2024-05-20`  
**Runtime:** lab image `pghoney:uhbs-lab` (modern Go rebuild; HPFeeds disabled)

Low-interaction Postgres honeypot. Graded with the UHBS **postgres** plugin (`sticky_elephant` not needed).

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [Postgres](postgres/) | yes (`postgres`) | **yes** | [43.72 / F](postgres/quick/) | [43.61 / F](postgres/full/) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.
