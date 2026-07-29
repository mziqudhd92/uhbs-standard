# ssh-auth-logger (JustinAzoff)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/JustinAzoff/ssh-auth-logger](https://github.com/JustinAzoff/ssh-auth-logger) · GitHub last push `2026-05-29`  
**Runtime:** `justinazoff/ssh-auth-logger:latest` (or local `ssh-auth-logger:uhbs-lab`; `SSHD_BIND=:2222`, host-mapped `127.0.0.1:12024`)

Low/zero-interaction SSH authentication logging honeypot (JSON logs; never grants a shell).

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [SSH](ssh/) | yes (`ssh`) | **yes** | [44.38 / F](ssh/quick/) | [44.38 / F](ssh/full/) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.
