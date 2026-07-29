# honeypot-ftp (alexbredo)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/alexbredo/honeypot-ftp](https://github.com/alexbredo/honeypot-ftp) · GitHub last push `2024-01-22`  
**Runtime:** `honeypot-ftp:uhbs-lab` (lab stubs for missing `base`/`handler` common-modules; plain FTP only)

## What this decoy is

Plain FTP honeypot (lab graded non-TLS FTP).

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [FTP](ftp/index.md) | yes | **yes** (plain `:21`) | [42.71 / F](ftp/quick/README.md) | [42.6 / F](ftp/full/README.md) |
| FTPS `:990` | yes (`ftp`) | no (lab skips SSL) | — | — |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

## For CTI analysts

- Captures FTP credential and file-oriented probing.

**Primary signals you can expect (when logging is wired):** FTP auth and file commands.

## For blue teams / detection engineering

- Prefer disposable storage; monitor uploads for malware drops if enabled.

## Trust & limitations

- This page is **evaluation proof** under UHBS 4.2.2 — not a certification or vendor ranking.
- Prefer **full/** artifacts over **quick/** for operational decisions.
- Re-run via [TUTORIAL.md](TUTORIAL.md); environment notes in [METHODOLOGY.md](METHODOLOGY.md).
- How to read modules: [READING-UHQS.md](../READING-UHQS.md)
