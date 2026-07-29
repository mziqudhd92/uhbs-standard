# express-honeypot (christophe77)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/christophe77/express-honeypot](https://github.com/christophe77/express-honeypot) · GitHub last push `2026-06-22`  
**Runtime:** lab image `express-honeypot:uhbs-lab` (Node 20; dpaste remote save disabled)

Express RFI/LFI honeypot with fake vulnerable URL paths. Graded with the UHBS **http** plugin.

## What this decoy is

Small Express-based HTTP honeypot oriented at LFI/RFI-style web probing.

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [HTTP](http/index.md) | yes (`http`) | **yes** | [45.84 / F](http/quick/README.md) | [45.73 / F](http/full/README.md) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.

## For CTI analysts

- Captures web exploit reconnaissance (path traversal / inclusion style probes) against a lightweight Node surface.
- Useful for tracking scanner campaigns that spray LFI/RFI payloads across IP space.

**Primary signals you can expect (when logging is wired):** HTTP request lines, LFI/RFI-like parameters, scanner User-Agents.

## For blue teams / detection engineering

- Review application logs for payload strings; feed IOC extraction (paths, encoded traversals) into detections.
- Keep Node runtime patched; the decoy app is still an attack surface on the honeypot host.
- UHBS grades HTTP protocol behavior — not whether every CVE path is implemented.

## Trust & limitations

- This page is **evaluation proof** under UHBS 4.2.2 — not a certification or vendor ranking.
- Prefer **full/** artifacts over **quick/** for operational decisions.
- Re-run via [TUTORIAL.md](TUTORIAL.md); environment notes in [METHODOLOGY.md](METHODOLOGY.md).
- How to read modules: [READING-UHQS.md](../READING-UHQS.md)
