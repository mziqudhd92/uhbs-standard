# pghoney (betheroot)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/betheroot/pghoney](https://github.com/betheroot/pghoney) · GitHub last push `2024-05-20`  
**Runtime:** lab image `pghoney:uhbs-lab` (modern Go rebuild; HPFeeds disabled)

Low-interaction Postgres honeypot. Graded with the UHBS **postgres** plugin (`sticky_elephant` not needed).

## What this decoy is

Low-interaction PostgreSQL decoy focused on auth/handshake capture.

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [Postgres](postgres/) | yes (`postgres`) | **yes** | [43.72 / F](postgres/quick/) | [43.61 / F](postgres/full/) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.

## For CTI analysts

- Tracks database credential guessing and Postgres protocol scanners (startup/SSLRequest patterns).
- Limited post-auth realism — treat as a DB auth sensor for CTI, not a full query-interaction trap.

**Primary signals you can expect (when logging is wired):** Postgres StartupMessage / auth failures, client driver fingerprints when logged.

## For blue teams / detection engineering

- Useful on “fake DB” VLANs adjacent to real data tiers to catch lateral-movement credential stuffing.
- Monitor for SSLRequest vs cleartext startup mixes as environment fingerprinting.
- Ensure no route from honeypot to real Postgres; poison credentials only.

## Trust & limitations

- This page is **evaluation proof** under UHBS 4.2.2 — not a certification or vendor ranking.
- Prefer **full/** artifacts over **quick/** for operational decisions.
- Re-run via [TUTORIAL.md](TUTORIAL.md); environment notes in [METHODOLOGY.md](METHODOLOGY.md).
- How to read modules: [READING-UHQS.md](../READING-UHQS.md)
