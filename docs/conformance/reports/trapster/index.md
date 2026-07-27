# Trapster Community (UHBS multi-protocol proof)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/0xBallpoint/trapster-community](https://github.com/0xBallpoint/trapster-community) · commit `dfc2c43dad119578f9c7344a0077790ed7fee01b`  
**Scope:** Every UHBS-native protocol plugin that the lab container exposed was graded separately (quick + full).

| Protocol | Class / port | Quick | Full |
| --- | --- | --- | --- |
| [FTP](ftp/) | Low-Interaction · FTP :2121 | [41.94 / F](ftp/quick/) | [49.71 / F](ftp/full/) |
| [HTTP](http/) | Web-API · HTTP :8080 | [40.74 / F](http/quick/) | [49.82 / F](http/full/) |
| [SSH](ssh/) | Low-Interaction · SSH :2222 | [25.92 / F](ssh/quick/) | [30.24 / F](ssh/full/) |
| [Telnet](telnet/) | Low-Interaction · Telnet :2323 | [47.00 / F](telnet/quick/) | [57.00 / D](telnet/full/) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.
