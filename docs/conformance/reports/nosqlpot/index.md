# nosqlpot (torque59)

**Status:** Informative · evaluation proof  
**Upstream:** [torque59/nosqlpot](https://github.com/torque59/nosqlpot)  
**Runtime:** lab image `nosqlpot:uhbs-lab` on `127.0.0.1:16379`

Python 2 Twisted fake Redis (NoPo) with fakeredis-backed command handling; legacy stack pinned for reproducible lab builds.

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [redis](redis/index.md) | yes (`redis`) | **yes** | [42.37 / F](redis/quick/README.md) | [40.08 / F](redis/full/README.md) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.

## For CTI analysts

Use the published SCORECARD modules to judge whether attackers reach interactive depth or stop at handshake/credential capture. This lab configuration intentionally disables outbound feeds (HPFeeds, Artillery ban lists, PyRDP player forwarding) to satisfy containment attestation.

## For blue teams

Treat δ_C and Module D as mandatory pre-flight checks before exposing any decoy on production networks. Module C reflects what the UHBS harness could read from local logs — mirror those fields into your SIEM if you reuse the same layout.
