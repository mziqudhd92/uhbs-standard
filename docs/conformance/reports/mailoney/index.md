# mailoney (phin3has)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/phin3has/mailoney](https://github.com/phin3has/mailoney) · GitHub last push `2026-05-22`  
**Runtime:** lab image `mailoney:uhbs-lab` (Python 3.11; SQLite DB)

Modern SMTP honeypot with credential capture and DB logging. Graded with the UHBS **smtp** plugin.

## What this decoy is

SMTP honeypot for spam/abuse and mail-oriented credential or relay abuse attempts.

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [SMTP](smtp/index.md) | yes (`smtp`) | **yes** | [38.8 / F](smtp/quick/README.md) | [38.69 / F](smtp/full/README.md) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.

## For CTI analysts

- Collects SMTP dialogue useful for spam campaign tracking (MAIL FROM/RCPT TO, payloads when offered).
- Complements HTTP/SSH sensors for actors that still probe mail submission paths.

**Primary signals you can expect (when logging is wired):** SMTP commands, auth attempts, envelope senders/recipients, message submissions.

## For blue teams / detection engineering

- Never allow open relay to the Internet; confirm lab/production config rejects relay.
- Quarantine captured message bodies; they may contain malware URLs.
- Alert on AUTH attempts and unusual RCPT patterns; tune to avoid drowning in Internet background radiation.

## Trust & limitations

- This page is **evaluation proof** under UHBS 4.2.2 — not a certification or vendor ranking.
- Prefer **full/** artifacts over **quick/** for operational decisions.
- Re-run via [TUTORIAL.md](TUTORIAL.md); environment notes in [METHODOLOGY.md](METHODOLOGY.md).
- How to read modules: [READING-UHQS.md](../READING-UHQS.md)
