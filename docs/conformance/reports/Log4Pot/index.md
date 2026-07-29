# Log4Pot (thomaspatzke)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/thomaspatzke/Log4Pot](https://github.com/thomaspatzke/Log4Pot) · GitHub last push `2024-11-29`  
**Runtime:** lab image `log4pot:uhbs-lab` (stdlib HTTP; payloader/Azure off)

Log4Shell (CVE-2021-44228) honeypot. Chosen over `joda32/owa-honeypot` (Flask OWA) as the easier HTTP lab. Graded with the UHBS **http** plugin.

## What this decoy is

HTTP listener designed to capture Log4Shell (Log4j JNDI) exploitation attempts.

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [HTTP](http/index.md) | yes (`http`) | **yes** | [41.71 / F](http/quick/README.md) | [38.0 / F](http/full/README.md) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.

## For CTI analysts

- High value for tracking lingering Log4Shell scanning and callback infrastructure (LDAP/RMI/etc. in payloads).
- Extract JNDI URLs and staging hosts for CTI sharing; correlate with other HTTP sensors.

**Primary signals you can expect (when logging is wired):** HTTP requests containing JNDI/Log4Shell exploit strings; callback destinations in payloads.

## For blue teams / detection engineering

- Isolate heavily — payloads try to induce outbound callbacks; block egress except to sinkhole/analysis.
- Alert on `${jndi:` patterns and similar obfuscations in HTTP headers/bodies.
- UHBS HTTP grade measures protocol decoy quality, not “how many CVE variants are covered.”

## Trust & limitations

- This page is **evaluation proof** under UHBS 4.2.2 — not a certification or vendor ranking.
- Prefer **full/** artifacts over **quick/** for operational decisions.
- Re-run via [TUTORIAL.md](TUTORIAL.md); environment notes in [METHODOLOGY.md](METHODOLOGY.md).
- How to read modules: [READING-UHQS.md](../READING-UHQS.md)
