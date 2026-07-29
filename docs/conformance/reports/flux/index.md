# flux

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/andrewmichaelsmith/flux](https://github.com/andrewmichaelsmith/flux)  
**Runtime:** aiohttp trap server (`flux:uhbs-lab`, canary traps disabled for air-gap)

LLM-maintained async HTTP honeypot with extensive scanner trap families (fake VPNs, webshells, MCP, GraphQL, tarpits).

## What this decoy is

LLM-maintained async HTTP honeypot with extensive scanner trap families (fake VPNs, webshells, MCP, GraphQL, tarpits). Graded with the UHBS **http** plugin against a Docker lab on `127.0.0.1:18094`.

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [HTTP](http/index.md) | yes (`http`) | **yes** | [50.91 / D](http/quick/README.md) | [50.91 / D](http/full/README.md) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.

## For CTI analysts

- Breadth of modern scanner paths; JSONL logging when telemetry path is wired.
- Compare Module A/B when judging engagement depth versus credential-only sinks.

**Primary signals you can expect (when logging is wired):** HTTP paths, User-Agents, credential or upload attempts visible to the lab harness.

## For blue teams / detection engineering

- Lab disables Tracebit canary minting and tarpit saturation defaults; read upstream safety disclaimer before any Internet exposure.
- Wire explicit log shipping; UHBS Module C reflects harness visibility, not SIEM maturity.

## Trust & limitations

- Evaluation proof under UHBS 4.2.2 — not certification or vendor ranking.
- Prefer **full/** artifacts over **quick/** for operational decisions.
- Re-run via [TUTORIAL.md](TUTORIAL.md); environment notes in [METHODOLOGY.md](METHODOLOGY.md).
