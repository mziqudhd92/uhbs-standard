# mysql-honeypotd (sjinks)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/sjinks/mysql-honeypotd](https://github.com/sjinks/mysql-honeypotd) · GitHub last push `2026-07-28`  
**Runtime:** lab image `mysql-honeypotd:uhbs-lab` (Alpine + libev)

Low-interaction MySQL honeypot written in C, graded with the UHBS **mysql** plugin.

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [MySQL](mysql/) | yes (`mysql`) | **yes** | [40.35 / F](mysql/quick/) | [37.94 / F](mysql/full/) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.
