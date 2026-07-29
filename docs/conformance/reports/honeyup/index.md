# HoneyUp

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/LogoiLab/honeyup](https://github.com/LogoiLab/honeyup)  
**Runtime:** Rust upload honeypot (`honeyup:uhbs-lab`)

Uploader honeypot mimicking weak `/uploads` PHP endpoints to collect malware and spray-and-pray upload attempts.

## What this decoy is

Uploader honeypot mimicking weak `/uploads` PHP endpoints to collect malware and spray-and-pray upload attempts. Graded with the UHBS **http** plugin against a Docker lab on `127.0.0.1:18091`.

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [HTTP](http/index.md) | yes (`http`) | **yes** | [50.91 / D](http/quick/README.md) | [50.91 / D](http/full/README.md) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.

## For CTI analysts

- File-upload TTPs and staging payloads dropped by automated upload scanners.
- Compare Module A/B when judging engagement depth versus credential-only sinks.

**Primary signals you can expect (when logging is wired):** HTTP paths, User-Agents, credential or upload attempts visible to the lab harness.

## For blue teams / detection engineering

- Isolate uploaded blobs; lab uses placeholder canary env vars — rotate and never reuse production AWS keys in compose.
- Wire explicit log shipping; UHBS Module C reflects harness visibility, not SIEM maturity.

## Trust & limitations

- Evaluation proof under UHBS 4.2.2 — not certification or vendor ranking.
- Prefer **full/** artifacts over **quick/** for operational decisions.
- Re-run via [TUTORIAL.md](TUTORIAL.md); environment notes in [METHODOLOGY.md](METHODOLOGY.md).
