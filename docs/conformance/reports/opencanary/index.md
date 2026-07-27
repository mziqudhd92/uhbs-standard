# OpenCanary (UHBS multi-protocol proof)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/thinkst/opencanary](https://github.com/thinkst/opencanary) · commit `bc231423aa40242cbd0bf34801f8788e23420dee`  
**Official capability:** multi-protocol network canary ([OpenCanary README](https://github.com/thinkst/opencanary)).  
**Graded here:** every UHBS-native plugin the Docker lab exposed (HTTP, FTP, SSH, Telnet, Redis).  
**Not graded:** SMB (requires Samba), MySQL/MSSQL/MongoDB/RDP/SIP/SNMP/NTP/TFTP/VNC/Git/HTTP-proxy (no UHBS plugin path in this lab).

| Protocol | Class / port | Quick | Full |
| --- | --- | --- | --- |
| [HTTP](http/) | Web-API · HTTP :80 | [41.30 / F](http/quick/) | [50.12 / D](http/full/) |
| [FTP](ftp/) | Low-Interaction · FTP :21 | [49.03 / F](ftp/quick/) | [59.43 / D](ftp/full/) |
| [SSH](ssh/) | Low-Interaction · SSH :2222 | [24.74 / F](ssh/quick/) | [28.44 / F](ssh/full/) |
| [TELNET](telnet/) | Low-Interaction · Telnet :23 | [47.35 / F](telnet/quick/) | [57.00 / D](telnet/full/) |
| [REDIS](redis/) | Low-Interaction · Redis :6379 | [41.27 / F](redis/quick/) | [48.26 / F](redis/full/) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.
