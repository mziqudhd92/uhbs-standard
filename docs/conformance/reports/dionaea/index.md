# Dionaea (UHBS multi-protocol proof)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/dinotools/dionaea](https://github.com/dinotools/dionaea) · commit `4e459f1b672a5b4c1e8335c0bff1b93738019215`  
**Scope:** Every UHBS-native protocol plugin that the lab container exposed was graded separately (quick + full).

| Protocol | Class / port | Quick | Full |
| --- | --- | --- | --- |
| [FTP](ftp/index.md) | Low-Interaction · FTP :21 | [50.95 / D](ftp/quick/README.md) | [57.96 / D](ftp/full/README.md) |
| [HTTP](http/index.md) | Web-API · HTTP :80 | [46.21 / F](http/quick/README.md) | [51.14 / D](http/full/README.md) |
| [SMB](smb/index.md) | Low-Interaction · SMB :445 | [48.25 / F](smb/quick/README.md) | [54.07 / D](smb/full/README.md) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.


## What this decoy is

Malware-capture oriented honeypot; UHBS graded selected FTP/HTTP/SMB surfaces.

## For CTI analysts

- Strong for malware drop and exploit payload capture on graded protocols.

**Primary signals:** Exploits/payloads and protocol sessions on enabled services.

## For blue teams / detection engineering

- Isolate sample storage; automate submission to malware analysis — not manual open-on-host.

## Trust & limitations

- Evaluation proof under UHBS 4.2.2 — not a certification or endorsement.
- Prefer **full/** over **quick/** for decisions.
- Reading guide: [READING-UHQS.md](../READING-UHQS.md).
