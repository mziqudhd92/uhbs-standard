# Beelzebub (UHBS multi-protocol proof)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/beelzebub-labs/beelzebub](https://github.com/beelzebub-labs/beelzebub) · commit `80e1428d023d564481acede9e63eb49e1631bfec`  
**Scope:** Every UHBS-native protocol plugin that the lab container exposed was graded separately (quick + full).

| Protocol | Class / port | Quick | Full |
| --- | --- | --- | --- |
| [HTTP](http/) | Web-API · HTTP :8080 | [41.73 / F](http/quick/) | [50.12 / D](http/full/) |
| [Redis](redis/) | Low-Interaction · Redis :6379 | [46.77 / F](redis/quick/) | [55.55 / D](redis/full/) |
| [SSH](ssh/) | Low-Interaction · SSH :2222 | [60.31 / D](ssh/quick/) | [45.74 / F](ssh/full/) |
| [Telnet](telnet/) | Low-Interaction · Telnet :23 | [47.78 / F](telnet/quick/) | [57.00 / D](telnet/full/) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.
