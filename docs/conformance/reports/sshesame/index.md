# sshesame (jaksi)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/jaksi/sshesame](https://github.com/jaksi/sshesame) · GitHub last push `2024-10-21`  
**Runtime:** `ghcr.io/jaksi/sshesame:latest` (listen `:2022`, host-mapped `127.0.0.1:12022`)

Easy-to-run SSH honeypot that accepts connections and logs activity without executing host commands.

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [SSH](ssh/) | yes (`ssh`) | **yes** | [65.13 / D](ssh/quick/) | [61.06 / D](ssh/full/) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.
