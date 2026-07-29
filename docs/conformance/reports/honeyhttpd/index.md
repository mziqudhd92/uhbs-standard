# HoneyHTTPD (bocajspear1)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/bocajspear1/honeyhttpd](https://github.com/bocajspear1/honeyhttpd) · GitHub last push `2024-06-29`  
**Runtime:** `honeyhttpd:uhbs-lab` (ApacheServer HTTP `:8080`)

Python HTTP honeypot framework graded with the UHBS **http** plugin.

## What this decoy is

Configurable Python HTTP imitation server for web decoy pages/endpoints.

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [HTTP](http/) | yes | **yes** | [45.84 / F](http/quick/) | [45.73 / F](http/full/) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.

## For CTI analysts

- Depends on configured site personality — CTI value scales with how convincingly paths/content match the lure.
- Captures generic web scanner traffic against the imitated surface.

**Primary signals you can expect (when logging is wired):** HTTP requests against configured imitation routes.

## For blue teams / detection engineering

- Treat templates as code: review for accidental SSRF/open-redirect if you customize handlers.
- Use distinct Host headers / TLS certs so analysts can filter decoy HTTP from production.

## Trust & limitations

- This page is **evaluation proof** under UHBS 4.2.2 — not a certification or vendor ranking.
- Prefer **full/** artifacts over **quick/** for operational decisions.
- Re-run via [TUTORIAL.md](TUTORIAL.md); environment notes in [METHODOLOGY.md](METHODOLOGY.md).
- How to read modules: [READING-UHQS.md](../READING-UHQS.md)
