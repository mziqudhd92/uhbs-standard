# Deferred: unsupported protocols (UHBS gaps)

Projects from the awesome-honeypots fresh queue that **are honeypots** but cannot be graded yet because UHBS lacks a plugin (or primary surface is out of scope). Do **not** run quick/full until a plugin exists.

| Project | Repo | Missing / blocker |
| --- | --- | --- |
| GasPot | [sjhilt/GasPot](https://github.com/sjhilt/GasPot) | Veeder-Root ATG / gas-pump protocol |
| dicompot | [nsmfoo/dicompot](https://github.com/nsmfoo/dicompot) | DICOM |
| bluepot | [andrewmichaelsmith/bluepot](https://github.com/andrewmichaelsmith/bluepot) | Bluetooth |
| UDPot | [jekil/UDPot](https://github.com/jekil/UDPot) | DNS (UHBS has NTP/SNMP, not DNS) |
| HoneySat | [HoneySat/honeysat-deploy](https://github.com/HoneySat/honeysat-deploy) | Satellite/TMTC stack; incidental VNC/Telnet/HTTP not product focus |
| ADBHoney | [huuck/ADBHoney](https://github.com/huuck/ADBHoney) | Android Debug Bridge (ADB) |
| medpot | [schmalle/medpot](https://github.com/schmalle/medpot) | HL7 / FHIR |
| helix-honeypot | [Zeerg/helix-honeypot](https://github.com/Zeerg/helix-honeypot) | Kubernetes API (archived) |
| Honeyd | [DataSoft/Honeyd](https://github.com/DataSoft/Honeyd) | Classic multi-OS emulator; major build/ops |
| MongoDB-HoneyProxy | [Plazmaz/MongoDB-HoneyProxy](https://github.com/Plazmaz/MongoDB-HoneyProxy) | MongoDB |
| imap-honey | [yvesago/imap-honey](https://github.com/yvesago/imap-honey) | IMAP primary (IMAP not in UHBS) |
| honssh | [tnich/honssh](https://github.com/tnich/honssh) | SSH MITM needing HI backend; archived / major work |

Also defer **qeeqbox-only** protocols already noted elsewhere (dhcp, dns, httpproxy, imap, ipp, irc, ldap, memcache, mssql, oracle, pjl, socks5) when grading multi-protocol frameworks.

When a new UHBS plugin lands, move the matching row to the grade queue and publish reports in the same format as existing labs.
