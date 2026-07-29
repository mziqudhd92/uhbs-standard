# mysql-honeypotd (sjinks)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/sjinks/mysql-honeypotd](https://github.com/sjinks/mysql-honeypotd) · GitHub last push `2026-07-28`  
**Runtime:** lab image `mysql-honeypotd:uhbs-lab` (Alpine + libev)

Low-interaction MySQL honeypot written in C, graded with the UHBS **mysql** plugin.

## What this decoy is

Low-interaction MySQL listener for connection and auth attempt capture.

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [MySQL](mysql/index.md) | yes (`mysql`) | **yes** | [40.35 / F](mysql/quick/README.md) | [37.94 / F](mysql/full/README.md) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.

## For CTI analysts

- Observes MySQL brute-force and automated DB scanners common in opportunistic campaigns.
- Shallow interaction depth under UHBS — prioritize auth telemetry over expecting full SQL dialogue.

**Primary signals you can expect (when logging is wired):** MySQL handshake and authentication attempts.

## For blue teams / detection engineering

- Deploy as a canary DB port; alert on any successful-looking auth from production user namespaces.
- Combine with network detections for MySQL protocol on non-DB subnets.

## Trust & limitations

- This page is **evaluation proof** under UHBS 4.2.2 — not a certification or vendor ranking.
- Prefer **full/** artifacts over **quick/** for operational decisions.
- Re-run via [TUTORIAL.md](TUTORIAL.md); environment notes in [METHODOLOGY.md](METHODOLOGY.md).
- How to read modules: [READING-UHQS.md](../READING-UHQS.md)
