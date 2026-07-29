# wordpot (gbrindisi)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/gbrindisi/wordpot](https://github.com/gbrindisi/wordpot) · GitHub last push `2018-10-16`  
**Runtime:** `wordpot:uhbs-lab` (Python 2.7 + Flask 0.10.1)

WordPress fingerprint honeypot graded with the UHBS **http** plugin.

## What this decoy is

WordPress-themed HTTP honeypot for CMS scanner and plugin/theme probe capture.

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [HTTP](http/) | yes | **yes** | [41.71 / F](http/quick/) | [41.6 / F](http/full/) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.

## For CTI analysts

- Tracks WordPress attack automation (wp-login, xmlrpc, plugin path probes).
- Useful for campaign clustering by requested plugin/CVE paths.

**Primary signals you can expect (when logging is wired):** HTTP paths for WP admin/login/xmlrpc/plugins; credential posts when logged.

## For blue teams / detection engineering

- Label clearly as decoy; do not host adjacent to real WordPress with shared DB/creds.
- Detect xmlrpc multicall and wp-login brute force patterns from the honeypot logs.

## Trust & limitations

- This page is **evaluation proof** under UHBS 4.2.2 — not a certification or vendor ranking.
- Prefer **full/** artifacts over **quick/** for operational decisions.
- Re-run via [TUTORIAL.md](TUTORIAL.md); environment notes in [METHODOLOGY.md](METHODOLOGY.md).
- How to read modules: [READING-UHQS.md](../READING-UHQS.md)
