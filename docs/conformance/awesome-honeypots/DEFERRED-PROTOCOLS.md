# Deferred: unsupported protocols (UHBS gaps)

Projects from the awesome-honeypots fresh queue that **are honeypots** but cannot be graded yet because UHBS lacks a plugin (or primary surface is out of scope / architecture). Do **not** run quick/full until a plugin exists *or* a hermetic lab recipe is available.

## Still deferred (no first-class UHBS plugin / out of scope)

| Project | Repo | Missing / blocker |
| --- | --- | --- |
| GasPot | [sjhilt/GasPot](https://github.com/sjhilt/GasPot) | Veeder-Root ATG / gas-pump protocol |
| dicompot | [nsmfoo/dicompot](https://github.com/nsmfoo/dicompot) | DICOM |
| HoneySat | [HoneySat/honeysat-deploy](https://github.com/HoneySat/honeysat-deploy) | Satellite/TMTC stack; incidental VNC/Telnet/HTTP not product focus |
| ADBHoney | [huuck/ADBHoney](https://github.com/huuck/ADBHoney) | Android Debug Bridge (ADB) |
| medpot | [schmalle/medpot](https://github.com/schmalle/medpot) | HL7 / FHIR |
| Honeyd | [DataSoft/Honeyd](https://github.com/DataSoft/Honeyd) | Classic multi-OS emulator; major build/ops |
| honssh | [tnich/honssh](https://github.com/tnich/honssh) | SSH MITM needing HI backend; archived / major work |

## Plugins added (re-queue grading)

The following protocol plugins are now built into UHBS **4.4.5**. Matching deferred projects can move to the grade queue when a hermetic lab recipe exists:

| Plugin | Previously deferred examples |
| --- | --- |
| `mongodb` | MongoDB-HoneyProxy |
| `imap` | imap-honey |
| `kubernetes` | helix-honeypot |
| `dns` | UDPot |
| `bluetooth` | bluepot |
| `dhcp`, `httpproxy`, `ipp`, `irc`, `ldap`, `memcache`, `mssql`, `oracle`, `pjl`, `socks5` | qeeqbox multi-protocol surfaces and similar |

When grading, publish reports in the same format as existing labs and update this file if a row is fully closed.
