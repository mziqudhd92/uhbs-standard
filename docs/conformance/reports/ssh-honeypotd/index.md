# ssh-honeypotd (sjinks)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/sjinks/ssh-honeypotd](https://github.com/sjinks/ssh-honeypotd) · GitHub last push `2026-07-28`  
**Runtime:** `wildwildangel/ssh-honeypotd:latest` (listen `:22`, host-mapped `127.0.0.1:12023`)

Low-interaction C/libssh honeypot that logs authentication attempts and never grants a session.

## What this decoy is

Minimal low-interaction SSH listener (C) oriented at capturing connection/auth attempts.

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [SSH](ssh/) | yes (`ssh`) | **yes** | [44.38 / F](ssh/quick/) | [44.38 / F](ssh/full/) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.

## For CTI analysts

- Targets mass SSH scanning and credential guessing rather than long interactive post-exploitation.
- Limited behavioral depth in UHBS (low B) — interpret as a credential/connection sensor, not a full adversary playground.

**Primary signals you can expect (when logging is wired):** Inbound SSH handshakes and auth attempts (implementation-dependent logging).

## For blue teams / detection engineering

- Simple footprint for edge decoys; pair with external logging (syslog/file) before production use.
- Do not expose management interfaces of the host; containerize and drop capabilities.
- Low UHQS does not mean “ignore” — it means the decoy failed realism/telemetry bars under UHBS, not that attackers will never hit it.

## Trust & limitations

- This page is **evaluation proof** under UHBS 4.2.2 — not a certification or vendor ranking.
- Prefer **full/** artifacts over **quick/** for operational decisions.
- Re-run via [TUTORIAL.md](TUTORIAL.md); environment notes in [METHODOLOGY.md](METHODOLOGY.md).
- How to read modules: [READING-UHQS.md](../READING-UHQS.md)
