# SHIVA Spampot (shiva-spampot)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/shiva-spampot/shiva](https://github.com/shiva-spampot/shiva) · GitHub last push `2025-03-31`  
**Runtime:** `shiva-receiver:uhbs-lab` (SMTP receiver only; analyzer/Postgres not required for protocol grading)

Spam honeypot SMTP receiver graded with the UHBS **smtp** plugin.

## What this decoy is

SMTP spam honeypot (receiver-oriented) for capturing spam/abuse mail traffic.

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [SMTP](smtp/index.md) | yes | **yes** | [45.07 / F](smtp/quick/README.md) | [44.96 / F](smtp/full/README.md) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.

## For CTI analysts

- Supports spam campaign and malware-delivery URL extraction from captured mail.
- Complements Mailoney-style SMTP sensors depending on deployment topology.

**Primary signals you can expect (when logging is wired):** SMTP sessions and message content captured by SHIVA receiver.

## For blue teams / detection engineering

- Quarantine and detonate attachments in isolated analysis — never on the honeypot OS.
- Confirm the graded lab was receiver-only; verify your deploy cannot relay.

## Trust & limitations

- This page is **evaluation proof** under UHBS 4.2.2 — not a certification or vendor ranking.
- Prefer **full/** artifacts over **quick/** for operational decisions.
- Re-run via [TUTORIAL.md](TUTORIAL.md); environment notes in [METHODOLOGY.md](METHODOLOGY.md).
- How to read modules: [READING-UHQS.md](../READING-UHQS.md)
