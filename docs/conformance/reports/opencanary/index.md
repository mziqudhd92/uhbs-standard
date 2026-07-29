# OpenCanary (UHBS multi-protocol proof)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/thinkst/opencanary](https://github.com/thinkst/opencanary) · commit `bc231423aa40242cbd0bf34801f8788e23420dee`  
**Official capability:** multi-protocol network canary ([OpenCanary README](https://github.com/thinkst/opencanary)).  
**Graded here:** HTTP, FTP, SSH, Telnet, Redis, MySQL, RDP, SIP, SNMP, NTP, TFTP, VNC, Git, SMB (Samba sidecar).  

| Protocol | Class / port | Quick | Full |
| --- | --- | --- | --- |
| [HTTP](http/index.md) | Web-API · HTTP :80 | [52.34 / D](http/quick/README.md) | [66.02 / D](http/full/README.md) |
| [FTP](ftp/index.md) | Low-Interaction · FTP :21 | [50.47 / D](ftp/quick/README.md) | [61.5 / D](ftp/full/README.md) |
| [SSH](ssh/index.md) | Low-Interaction · SSH :2222 | [31.94 / F](ssh/quick/README.md) | [35.64 / F](ssh/full/README.md) |
| [TELNET](telnet/index.md) | Low-Interaction · Telnet :23 | [52.83 / D](telnet/quick/README.md) | [64.9 / D](telnet/full/README.md) |
| [REDIS](redis/index.md) | Low-Interaction · Redis :6379 | [45.07 / F](redis/quick/README.md) | [53.72 / D](redis/full/README.md) |
| [MYSQL](mysql/index.md) | Low-Interaction · MySQL :3306 | [51.48 / D](mysql/quick/README.md) | [62.96 / D](mysql/full/README.md) |
| [RDP](rdp/index.md) | Low-Interaction · RDP :3389 | [50.13 / D](rdp/quick/README.md) | [61.01 / D](rdp/full/README.md) |
| [SIP](sip/index.md) | Low-Interaction · SIP :5060 | [40.01 / F](sip/quick/README.md) | [46.44 / F](sip/full/README.md) |
| [SNMP](snmp/index.md) | Low-Interaction · SNMP :161 | [40.69 / F](snmp/quick/README.md) | [47.42 / F](snmp/full/README.md) |
| [NTP](ntp/index.md) | Low-Interaction · NTP :123 | [40.69 / F](ntp/quick/README.md) | [47.42 / F](ntp/full/README.md) |
| [TFTP](tftp/index.md) | Low-Interaction · TFTP :69 | [40.69 / F](tftp/quick/README.md) | [47.42 / F](tftp/full/README.md) |
| [VNC](vnc/index.md) | Low-Interaction · VNC :5900 | [50.81 / D](vnc/quick/README.md) | [61.99 / D](vnc/full/README.md) |
| [GIT](git/index.md) | Low-Interaction · Git :9418 | [51.48 / D](git/quick/README.md) | [62.96 / D](git/full/README.md) |
| [SMB](smb/index.md) | Low-Interaction · SMB :445 | [50.13 / D](smb/quick/README.md) | [57.72 / D](smb/full/README.md) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.


## What this decoy is

Multi-service canary/honeypot framework (many protocols); UHBS publishes per-protocol grades.

## For CTI analysts

- Per-protocol canaries yield precise “someone touched this fake service” intel for lateral-movement detection.
- Use protocol-specific hubs — OpenCanary is not a single UHQS number.

**Primary signals:** Per-service connection/auth events as configured.

## For blue teams / detection engineering

- Deploy canaries on sensitive VLANs; any connection is high-signal for blue teams.
- Integrate OpenCanary alerts into SOAR with asset/context tags to avoid alert fatigue.

## Trust & limitations

- Evaluation proof under UHBS 4.2.2 — not a certification or endorsement.
- Prefer **full/** over **quick/** for decisions.
- Reading guide: [READING-UHQS.md](../READING-UHQS.md).
