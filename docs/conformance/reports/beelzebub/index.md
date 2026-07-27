# Beelzebub (UHBS multi-protocol proof)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/beelzebub-labs/beelzebub](https://github.com/beelzebub-labs/beelzebub) · commit `80e1428d023d564481acede9e63eb49e1631bfec`  
**Scope:** Every UHBS-native protocol plugin that the lab container exposed was graded separately (quick + full).

| Protocol | Class / port | Quick | Full |
| --- | --- | --- | --- |
| [HTTP](http/) | Web-API · HTTP :8080 | [52.77 / D](http/quick/) | [66.02 / D](http/full/) |
| [Redis](redis/) | Low-Interaction · Redis :6379 | [50.56 / D](redis/quick/) | [61.01 / D](redis/full/) |
| [SSH](ssh/) | Low-Interaction · SSH :2222 | [74.45 / C](ssh/quick/) | [59.88 / D](ssh/full/) |
| [Telnet](telnet/) | Low-Interaction · Telnet :23 | [39.16 / F](telnet/quick/) | [47.89 / F](telnet/full/) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.
