# Krawl

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/BlessedRebuS/Krawl](https://github.com/BlessedRebuS/Krawl)  
**Runtime:** GHCR `krawl:latest` standalone mode (SQLite, AI generation off)

Cloud-native deception server with spider traps, fake admin panels, and dashboard telemetry for crawler and scanner activity.

## What this decoy is

Cloud-native deception server with spider traps, fake admin panels, and dashboard telemetry for crawler and scanner activity. Graded with the UHBS **http** plugin against a Docker lab on `127.0.0.1:18093`.

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [HTTP](http/index.md) | yes (`http`) | **yes** | [50.91 / D](http/quick/README.md) | [50.91 / D](http/full/README.md) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.

## For CTI analysts

- High-volume crawler engagement, fake credential forms, and robots.txt advertised honeypot paths.
- Compare Module A/B when judging engagement depth versus credential-only sinks.

**Primary signals you can expect (when logging is wired):** HTTP paths, User-Agents, credential or upload attempts visible to the lab harness.

## For blue teams / detection engineering

- AI page generation disabled in lab; optional canary tokens unset — enable deliberately if you accept outbound callbacks.
- Wire explicit log shipping; UHBS Module C reflects harness visibility, not SIEM maturity.

## Trust & limitations

- Evaluation proof under UHBS 4.2.2 — not certification or vendor ranking.
- Prefer **full/** artifacts over **quick/** for operational decisions.
- Re-run via [TUTORIAL.md](TUTORIAL.md); environment notes in [METHODOLOGY.md](METHODOLOGY.md).
