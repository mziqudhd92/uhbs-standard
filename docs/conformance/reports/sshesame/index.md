# sshesame (jaksi)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/jaksi/sshesame](https://github.com/jaksi/sshesame) · GitHub last push `2024-10-21`  
**Runtime:** `ghcr.io/jaksi/sshesame:latest` (listen `:2022`, host-mapped `127.0.0.1:12022`)

Easy-to-run SSH honeypot that accepts connections and logs activity without executing host commands.

## What this decoy is

Low-interaction SSH decoy that accepts sessions and logs activity without executing host commands.

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [SSH](ssh/) | yes (`ssh`) | **yes** | [65.13 / D](ssh/quick/) | [61.06 / D](ssh/full/) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.

## For CTI analysts

- Useful for collecting SSH brute-force / credential-stuffing attempts and client banners from opportunistic Internet noise.
- Expect session metadata and command attempts as logged by the decoy — not a full high-interaction filesystem for malware drop analysis unless you add other tooling.
- Good fit when CTI wants volume SSH auth telemetry with low host risk (no real shell).

**Primary signals you can expect (when logging is wired):** SSH auth attempts, channel/request activity, client versions — as emitted by sshesame logging.

## For blue teams / detection engineering

- Deploy only on isolated decoy segments; treat accepted credentials as poisoned (never reuse on real assets).
- Forward decoy logs to SIEM with clear `honeypot=sshesame` labels to avoid false-positive incident escalations.
- UHBS Module B/C reflect harness interaction depth — wire your own log shipping for production detection value.
- Safety Gate passed in lab (δ_C=1.0); still apply egress deny-by-default on the honeypot VLAN.

## Trust & limitations

- This page is **evaluation proof** under UHBS 4.2.2 — not a certification or vendor ranking.
- Prefer **full/** artifacts over **quick/** for operational decisions.
- Re-run via [TUTORIAL.md](TUTORIAL.md); environment notes in [METHODOLOGY.md](METHODOLOGY.md).
- How to read modules: [READING-UHQS.md](../READING-UHQS.md)
