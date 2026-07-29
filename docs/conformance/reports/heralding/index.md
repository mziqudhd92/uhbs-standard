# Heralding (johnnykv)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/johnnykv/heralding](https://github.com/johnnykv/heralding) · GitHub last push `2024-02-28`  
**Runtime:** `heralding:uhbs-lab` with lab config enabling **SSH + FTP only**

Credential-harvesting multi-protocol honeypot; only SSH and FTP graded in this round.

## What this decoy is

Multi-protocol credential-harvesting honeypot; this UHBS proof graded SSH and FTP only.

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [SSH](ssh/index.md) | yes | **yes** | [44.38 / F](ssh/quick/README.md) | [44.18 / F](ssh/full/README.md) |
| [FTP](ftp/index.md) | yes | **yes** | [35.96 / F](ftp/quick/README.md) | [35.85 / F](ftp/full/README.md) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.

## For CTI analysts

- Designed to capture credentials across protocols — UHBS shows strong protocol speak (A) but weak post-auth behavior (B) because auth is rejected by design.
- Interpret low B/C as “credential sink,” not failure to attract scanners.

**Primary signals you can expect (when logging is wired):** Rejected auth attempts with captured credentials on SSH/FTP (per Heralding logging).

## For blue teams / detection engineering

- Excellent mental model for auth-only sensors: alert on username/password pairs, never on “missing shell”.
- Protect credential logs as highly sensitive; hash or encrypt at rest per policy.
- Only SSH+FTP were enabled in the graded lab config — do not assume other Heralding protocols were tested here.

## Trust & limitations

- This page is **evaluation proof** under UHBS 4.2.2 — not a certification or vendor ranking.
- Prefer **full/** artifacts over **quick/** for operational decisions.
- Re-run via [TUTORIAL.md](TUTORIAL.md); environment notes in [METHODOLOGY.md](METHODOLOGY.md).
- How to read modules: [READING-UHQS.md](../READING-UHQS.md)
