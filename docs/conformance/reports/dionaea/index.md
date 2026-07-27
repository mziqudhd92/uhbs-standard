# Dionaea (UHBS multi-protocol proof)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/dinotools/dionaea](https://github.com/dinotools/dionaea) · commit `4e459f1b672a5b4c1e8335c0bff1b93738019215`  
**Scope:** Every UHBS-native protocol plugin that the lab container exposed was graded separately (quick + full).

| Protocol | Class / port | Quick | Full |
| --- | --- | --- | --- |
| [FTP](ftp/) | Low-Interaction · FTP :21 | [49.10 / F](ftp/quick/) | [55.30 / D](ftp/full/) |
| [HTTP](http/) | Web-API · HTTP :80 | [40.93 / F](http/quick/) | [43.54 / F](http/full/) |
| [SMB](smb/) | Low-Interaction · SMB :445 | [44.55 / F](smb/quick/) | [48.74 / F](smb/full/) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.
