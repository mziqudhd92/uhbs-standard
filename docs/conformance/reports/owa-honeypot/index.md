# owa-honeypot

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/joda32/owa-honeypot](https://github.com/joda32/owa-honeypot)  
**Runtime:** Flask OWA login decoy (Python 3.8 lab image)

Minimal Outlook Web Access themed HTTP honeypot that captures credential POST attempts and redirects browsers to a fake OWA logon page.

## What this decoy is

Minimal Outlook Web Access themed HTTP honeypot that captures credential POST attempts and redirects browsers to a fake OWA logon page. Graded with the UHBS **http** plugin against a Docker lab on `127.0.0.1:18090`.

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [HTTP](http/index.md) | yes (`http`) | **yes** | [41.71 / F](http/quick/README.md) | [41.71 / F](http/full/README.md) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.

## For CTI analysts

- Credential-spray and OWA-specific scanner traffic; useful when you need Exchange-flavored lures without deploying full Exchange emulation.
- Compare Module A/B when judging engagement depth versus credential-only sinks.

**Primary signals you can expect (when logging is wired):** HTTP paths, User-Agents, credential or upload attempts visible to the lab harness.

## For blue teams / detection engineering

- Run behind reverse proxy TLS termination; Flask dev patterns in upstream are not production-hardened — treat UHBS scores as lab proof only.
- Wire explicit log shipping; UHBS Module C reflects harness visibility, not SIEM maturity.

## Trust & limitations

- Evaluation proof under UHBS 4.2.2 — not certification or vendor ranking.
- Prefer **full/** artifacts over **quick/** for operational decisions.
- Re-run via [TUTORIAL.md](TUTORIAL.md); environment notes in [METHODOLOGY.md](METHODOLOGY.md).
