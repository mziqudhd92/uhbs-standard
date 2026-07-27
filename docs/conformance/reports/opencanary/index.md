# OpenCanary (UHBS multi-protocol proof)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/thinkst/opencanary](https://github.com/thinkst/opencanary) · commit `bc231423aa40242cbd0bf34801f8788e23420dee`  
**Official capability:** multi-protocol network canary ([OpenCanary README](https://github.com/thinkst/opencanary)).  
**Graded here:** HTTP, FTP, SSH, Telnet, Redis, MySQL, RDP, SIP, SNMP, NTP, TFTP, VNC, Git, SMB (Samba sidecar).  

| Protocol | Class / port | Quick | Full |
| --- | --- | --- | --- |
| [HTTP](http/) | Web-API · HTTP :80 | [52.34 / D](http/quick/) | [66.02 / D](http/full/) |
| [FTP](ftp/) | Low-Interaction · FTP :21 | [50.47 / D](ftp/quick/) | [61.5 / D](ftp/full/) |
| [SSH](ssh/) | Low-Interaction · SSH :2222 | [31.94 / F](ssh/quick/) | [35.64 / F](ssh/full/) |
| [TELNET](telnet/) | Low-Interaction · Telnet :23 | [52.83 / D](telnet/quick/) | [64.9 / D](telnet/full/) |
| [REDIS](redis/) | Low-Interaction · Redis :6379 | [45.07 / F](redis/quick/) | [53.72 / D](redis/full/) |
| [MYSQL](mysql/) | Low-Interaction · MySQL :3306 | [51.48 / D](mysql/quick/) | [62.96 / D](mysql/full/) |
| [RDP](rdp/) | Low-Interaction · RDP :3389 | [50.13 / D](rdp/quick/) | [61.01 / D](rdp/full/) |
| [SIP](sip/) | Low-Interaction · SIP :5060 | [40.01 / F](sip/quick/) | [46.44 / F](sip/full/) |
| [SNMP](snmp/) | Low-Interaction · SNMP :161 | [40.69 / F](snmp/quick/) | [47.42 / F](snmp/full/) |
| [NTP](ntp/) | Low-Interaction · NTP :123 | [40.69 / F](ntp/quick/) | [47.42 / F](ntp/full/) |
| [TFTP](tftp/) | Low-Interaction · TFTP :69 | [40.69 / F](tftp/quick/) | [47.42 / F](tftp/full/) |
| [VNC](vnc/) | Low-Interaction · VNC :5900 | [50.81 / D](vnc/quick/) | [61.99 / D](vnc/full/) |
| [GIT](git/) | Low-Interaction · Git :9418 | [51.48 / D](git/quick/) | [62.96 / D](git/full/) |
| [SMB](smb/) | Low-Interaction · SMB :445 | [50.13 / D](smb/quick/) | [57.72 / D](smb/full/) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.
