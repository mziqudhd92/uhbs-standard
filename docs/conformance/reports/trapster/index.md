# Trapster Community (UHBS multi-protocol proof)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/0xBallpoint/trapster-community](https://github.com/0xBallpoint/trapster-community) · commit `dfc2c43dad119578f9c7344a0077790ed7fee01b`  
**Scope:** Every UHBS-native protocol plugin that the lab container exposed was graded separately (quick + full).

| Protocol | Class / port | Quick | Full |
| --- | --- | --- | --- |
| [FTP](ftp/) | Low-Interaction · FTP :2121 | [43.37 / F](ftp/quick/) | [51.78 / D](ftp/full/) |
| [HTTP](http/) | Web-API · HTTP :8080 | [50.13 / D](http/quick/) | [63.33 / D](http/full/) |
| [SSH](ssh/) | Low-Interaction · SSH :2222 | [40.06 / F](ssh/quick/) | [44.38 / F](ssh/full/) |
| [Telnet](telnet/) | Low-Interaction · Telnet :2323 | [52.49 / D](telnet/quick/) | [64.9 / D](telnet/full/) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.
