# node-ftp-honeypot (christophe77)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/christophe77/node-ftp-honeypot](https://github.com/christophe77/node-ftp-honeypot) · GitHub last push `2026-06-22`  
**Runtime:** lab image `node-ftp-honeypot:uhbs-lab` (Node 20 + ftp-srv)

Node.js FTP honeypot that accepts uploads into a pandora-box quarantine. Graded with the UHBS **ftp** plugin.

## What this decoy is

Lightweight FTP decoy for anonymous/auth FTP probing.

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [FTP](ftp/) | yes (`ftp`) | **yes** | [35.96 / F](ftp/quick/) | [35.85 / F](ftp/full/) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.

## For CTI analysts

- Captures FTP login attempts and basic command probing from legacy worm/scanner ecosystems.
- Lower fidelity than medium-interaction FTP honeypots — good for presence/volume, not deep malware drop analysis alone.

**Primary signals you can expect (when logging is wired):** FTP USER/PASS, LIST/RETR attempts, client banners.

## For blue teams / detection engineering

- Disable real filesystem writes; use disposable storage if enabling uploads.
- Watch for bounce-scan / PORT abuse patterns if the implementation allows.

## Trust & limitations

- This page is **evaluation proof** under UHBS 4.2.2 — not a certification or vendor ranking.
- Prefer **full/** artifacts over **quick/** for operational decisions.
- Re-run via [TUTORIAL.md](TUTORIAL.md); environment notes in [METHODOLOGY.md](METHODOLOGY.md).
- How to read modules: [READING-UHQS.md](../READING-UHQS.md)
