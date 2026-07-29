# modpot

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/referefref/modpot](https://github.com/referefref/modpot)  
**Runtime:** Go/gin modular HTML honeypot (`modpot:uhbs-lab`, lab config on :8080)

Modular web-application honeypot framework serving static honeypages with regex-triggered responders and a management UI on :1337.

## What this decoy is

Modular web-application honeypot framework serving static honeypages with regex-triggered responders and a management UI on :1337. Graded with the UHBS **http** plugin against a Docker lab on `127.0.0.1:18096`.

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [HTTP](http/index.md) | yes (`http`) | **yes** | [50.91 / D](http/quick/README.md) | [50.91 / D](http/full/README.md) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.

## For CTI analysts

- Form/query exploitation attempts matched against per-app regex rules; SQLite-backed request logs in lab.
- Compare Module A/B when judging engagement depth versus credential-only sinks.

**Primary signals you can expect (when logging is wired):** HTTP paths, User-Agents, credential or upload attempts visible to the lab harness.

## For blue teams / detection engineering

- Disable outbound responders in isolated labs; upstream responders can invoke shell — lab config clears responders and uses a non-matching regex.
- Wire explicit log shipping; UHBS Module C reflects harness visibility, not SIEM maturity.

## Trust & limitations

- Evaluation proof under UHBS 4.2.2 — not certification or vendor ranking.
- Prefer **full/** artifacts over **quick/** for operational decisions.
- Re-run via [TUTORIAL.md](TUTORIAL.md); environment notes in [METHODOLOGY.md](METHODOLOGY.md).
