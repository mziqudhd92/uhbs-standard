# ssh-honeypotd (sjinks)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/sjinks/ssh-honeypotd](https://github.com/sjinks/ssh-honeypotd) · GitHub last push `2026-07-28`  
**Runtime:** `wildwildangel/ssh-honeypotd:latest` (listen `:22`, host-mapped `127.0.0.1:12023`)

Low-interaction C/libssh honeypot that logs authentication attempts and never grants a session.

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [SSH](ssh/) | yes (`ssh`) | **yes** | [44.38 / F](ssh/quick/) | [44.38 / F](ssh/full/) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.
