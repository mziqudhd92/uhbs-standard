# qeeqbox/honeypots

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/qeeqbox/honeypots](https://github.com/qeeqbox/honeypots) · GitHub last push `2025-12-03`  
**Runtime:** `qeeqbox-honeypots:uhbs-lab` (pip install in Python 3.11)

## Protocol survey (graded)

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [ssh](ssh/) | yes | **yes** | [59.88 / D](ssh/quick/) | [59.68 / D](ssh/full/) |
| [http](http/) | yes | **yes** | [45.84 / F](http/quick/) | [45.73 / F](http/full/) |
| [ftp](ftp/) | yes | **yes** | [42.71 / F](ftp/quick/) | [40.31 / F](ftp/full/) |
| [telnet](telnet/) | yes | **yes** | [29.88 / F](telnet/quick/) | [29.77 / F](telnet/full/) |
| [smtp](smtp/) | yes | **yes** | [30.9 / F](smtp/quick/) | [30.78 / F](smtp/full/) |
| [pop3](pop3/) | yes | **yes** | [31.06 / F](pop3/quick/) | [30.94 / F](pop3/full/) |
| [mysql](mysql/) | yes | **yes** | [34.38 / F](mysql/quick/) | [34.27 / F](mysql/full/) |
| [postgres](postgres/) | yes | **yes** | [34.38 / F](postgres/quick/) | [34.27 / F](postgres/full/) |
| [redis](redis/) | yes | **yes** | [34.61 / F](redis/quick/) | [34.5 / F](redis/full/) |
| [vnc](vnc/) | yes | **yes** | [32.92 / F](vnc/quick/) | [32.81 / F](vnc/full/) |

## Skipped in this proof

| dhcp, dns, httpproxy, https, httpsproxy, imap, ipp, irc, ldap, memcache, mssql, oracle, pjl, socks5, elastic*, snmp*, ntp*, sip*, smb*, rdp* | — | **skipped** | — | — |

\* UHBS has plugins for snmp/ntp/sip/smb/rdp/elastic-as-http but they were not included in this lab batch (UDP/TLS/heavy deps deferred). `elastic` can be graded as `http` in a follow-up.

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)
