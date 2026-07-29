# Elastichoney (jordan-wright)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/jordan-wright/elastichoney](https://github.com/jordan-wright/elastichoney) · GitHub last push `2015-07-14`  
**Runtime:** lab image `elastichoney:uhbs-lab` (modern Go rebuild; anonymous mode)

Simple Elasticsearch REST honeypot graded with the UHBS **http** plugin (same pattern as ESPot).

## What this decoy is

Elasticsearch-themed HTTP decoy for ES/CVE-era probing (historic but still scanned).

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [HTTP ES REST](http/index.md) | yes (`http`) | **yes** | [45.84 / F](http/quick/README.md) | [45.73 / F](http/full/README.md) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.

## For CTI analysts

- Observes Elasticsearch REST probing and exploit attempts against ES-like endpoints.

**Primary signals you can expect (when logging is wired):** HTTP requests to ES-like paths; exploit payloads for known ES issues when present.

## For blue teams / detection engineering

- Useful canary for “DB/search HTTP APIs” on wrong subnets; keep offline from real clusters.

## Trust & limitations

- This page is **evaluation proof** under UHBS 4.2.2 — not a certification or vendor ranking.
- Prefer **full/** artifacts over **quick/** for operational decisions.
- Re-run via [TUTORIAL.md](TUTORIAL.md); environment notes in [METHODOLOGY.md](METHODOLOGY.md).
- How to read modules: [READING-UHQS.md](../READING-UHQS.md)
