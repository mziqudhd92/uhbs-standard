# HellPot (yunginnanet)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/yunginnanet/HellPot](https://github.com/yunginnanet/HellPot) · GitHub last push `2025-12-19`  
**Runtime:** lab image `hellpot:uhbs-lab` (Go fasthttp; catch-all infinite Markov stream)

HTTP honeypot that traps bots with endless Nietzsche-flavored responses. Graded with the UHBS **http** plugin (client timeouts apply).

## What this decoy is

HTTP tarpit that keeps aggressive bots reading endless generated content (delay/exhaustion decoy).

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [HTTP](http/) | yes (`http`) | **yes** | [43.98 / F](http/quick/) | [43.87 / F](http/full/) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.

## For CTI analysts

- Not a content-management decoy — value is observing bots that follow infinite/slow HTTP responses.
- Useful for separating “curious scanners” from “sticky crawlers” that burn time/bandwidth.

**Primary signals you can expect (when logging is wired):** Long-lived HTTP sessions, User-Agents, request paths that hit the tarpit handler.

## For blue teams / detection engineering

- Place behind careful rate controls so tarpit traffic cannot DoS shared egress or upstream WAF budgets.
- Instrument connection duration and bytes-out as the primary KPIs; UHBS HTTP plugin times out by design.
- Do not use as your only web honeypot if you need exploit payload capture — pair with a content-aware HTTP decoy.

## Trust & limitations

- This page is **evaluation proof** under UHBS 4.2.2 — not a certification or vendor ranking.
- Prefer **full/** artifacts over **quick/** for operational decisions.
- Re-run via [TUTORIAL.md](TUTORIAL.md); environment notes in [METHODOLOGY.md](METHODOLOGY.md).
- How to read modules: [READING-UHQS.md](../READING-UHQS.md)
