# qeeqbox/honeypots

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/qeeqbox/honeypots](https://github.com/qeeqbox/honeypots) · GitHub last push `2025-12-03`  
**Runtime:** `qeeqbox-honeypots:uhbs-lab` (pip install in Python 3.11)

## What this decoy is

Multi-protocol honeypot framework; UHBS published selected overlapping protocol grades.

## Protocol survey (graded)

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [ssh](ssh/index.md) | yes | **yes** | [59.88 / D](ssh/quick/README.md) | [59.68 / D](ssh/full/README.md) |
| [http](http/index.md) | yes | **yes** | [45.84 / F](http/quick/README.md) | [45.73 / F](http/full/README.md) |
| [ftp](ftp/index.md) | yes | **yes** | [42.71 / F](ftp/quick/README.md) | [40.31 / F](ftp/full/README.md) |
| [telnet](telnet/index.md) | yes | **yes** | [29.88 / F](telnet/quick/README.md) | [29.77 / F](telnet/full/README.md) |
| [smtp](smtp/index.md) | yes | **yes** | [30.9 / F](smtp/quick/README.md) | [30.78 / F](smtp/full/README.md) |
| [pop3](pop3/index.md) | yes | **yes** | [31.06 / F](pop3/quick/README.md) | [30.94 / F](pop3/full/README.md) |
| [mysql](mysql/index.md) | yes | **yes** | [34.38 / F](mysql/quick/README.md) | [34.27 / F](mysql/full/README.md) |
| [postgres](postgres/index.md) | yes | **yes** | [34.38 / F](postgres/quick/README.md) | [34.27 / F](postgres/full/README.md) |
| [redis](redis/index.md) | yes | **yes** | [34.61 / F](redis/quick/README.md) | [34.5 / F](redis/full/README.md) |
| [vnc](vnc/index.md) | yes | **yes** | [32.92 / F](vnc/quick/README.md) | [32.81 / F](vnc/full/README.md) |

## Skipped in this proof

| dhcp, dns, httpproxy, https, httpsproxy, imap, ipp, irc, ldap, memcache, mssql, oracle, pjl, socks5, elastic*, snmp*, ntp*, sip*, smb*, rdp* | — | **skipped** | — | — |

\* UHBS has plugins for snmp/ntp/sip/smb/rdp/elastic-as-http but they were not included in this lab batch (UDP/TLS/heavy deps deferred). `elastic` can be graded as `http` in a follow-up.

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

## For CTI analysts

- Protocol-by-protocol results vary widely — use per-protocol hubs, not a single composite “qeeqbox score”.

**Primary signals you can expect (when logging is wired):** Per-protocol auth/banner telemetry depending on enabled services.

## For blue teams / detection engineering

- Enable only needed protocols; each listener expands attack surface on the decoy host.
- Compare UHBS plugin coverage vs qeeqbox capabilities — unsupported protocols were not graded.

## Trust & limitations

- This page is **evaluation proof** under UHBS 4.2.2 — not a certification or vendor ranking.
- Prefer **full/** artifacts over **quick/** for operational decisions.
- Re-run via [TUTORIAL.md](TUTORIAL.md); environment notes in [METHODOLOGY.md](METHODOLOGY.md).
- How to read modules: [READING-UHQS.md](../READING-UHQS.md)
