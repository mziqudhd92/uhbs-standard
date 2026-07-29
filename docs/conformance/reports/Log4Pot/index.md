# Log4Pot (thomaspatzke)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/thomaspatzke/Log4Pot](https://github.com/thomaspatzke/Log4Pot) · GitHub last push `2024-11-29`  
**Runtime:** lab image `log4pot:uhbs-lab` (stdlib HTTP; payloader/Azure off)

Log4Shell (CVE-2021-44228) honeypot. Chosen over `joda32/owa-honeypot` (Flask OWA) as the easier HTTP lab. Graded with the UHBS **http** plugin.

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [HTTP](http/) | yes (`http`) | **yes** | [41.71 / F](http/quick/) | [38.0 / F](http/full/) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.
