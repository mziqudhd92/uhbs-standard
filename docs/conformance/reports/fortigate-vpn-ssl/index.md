# FortiGate VPN-SSL Honeypot

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/PeterGabaldon/Fortigate.VPN-SSL.Honeypot](https://github.com/PeterGabaldon/Fortigate.VPN-SSL.Honeypot)  
**Runtime:** Flask FortiGate SSL-VPN portal (`fortigate-vpn-ssl:uhbs-lab`, nginx omitted in lab)

FortiGate SSL-VPN login deception with SQLite credential logging and optional external reporting pipelines.

## What this decoy is

FortiGate SSL-VPN login deception with SQLite credential logging and optional external reporting pipelines. Graded with the UHBS **http** plugin against a Docker lab on `127.0.0.1:18095`.

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [HTTP](http/index.md) | yes (`http`) | **yes** | [46.78 / F](http/quick/README.md) | [46.78 / F](http/full/README.md) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.

## For CTI analysts

- VPN credential brute force and symlink-exploit probes when nginx TLS front-end is deployed.
- Compare Module A/B when judging engagement depth versus credential-only sinks.

**Primary signals you can expect (when logging is wired):** HTTP paths, User-Agents, credential or upload attempts visible to the lab harness.

## For blue teams / detection engineering

- Graded against Flask service directly on :5000; production compose uses host-network nginx — replicate TLS fronting separately.
- Wire explicit log shipping; UHBS Module C reflects harness visibility, not SIEM maturity.

## Trust & limitations

- Evaluation proof under UHBS 4.2.2 — not certification or vendor ranking.
- Prefer **full/** artifacts over **quick/** for operational decisions.
- Re-run via [TUTORIAL.md](TUTORIAL.md); environment notes in [METHODOLOGY.md](METHODOLOGY.md).
