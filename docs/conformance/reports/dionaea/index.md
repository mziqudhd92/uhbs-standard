# Dionaea (UHBS multi-protocol proof)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/dinotools/dionaea](https://github.com/dinotools/dionaea) · commit `4e459f1b672a5b4c1e8335c0bff1b93738019215`  
**Scope:** Every UHBS-native protocol plugin that the lab container exposed was graded separately (quick + full).

| Protocol | Class / port | Quick | Full |
| --- | --- | --- | --- |
| [FTP](ftp/) | Low-Interaction · FTP :21 | [50.95 / D](ftp/quick/) | [57.96 / D](ftp/full/) |
| [HTTP](http/) | Web-API · HTTP :80 | [46.21 / F](http/quick/) | [51.14 / D](http/full/) |
| [SMB](smb/) | Low-Interaction · SMB :445 | [48.25 / F](smb/quick/) | [54.07 / D](smb/full/) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.
