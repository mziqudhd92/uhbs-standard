# sticky_elephant (betheroot)

**Status:** Informative · evaluation proof  
**Upstream:** [betheroot/sticky_elephant](https://github.com/betheroot/sticky_elephant)  
**Runtime:** lab image `sticky_elephant:uhbs-lab` on `127.0.0.1:15433`

Ruby medium-interaction PostgreSQL honeypot that logs authentication and query attempts; lab disables HPFeeds and binds 0.0.0.0:5432 in Docker.

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [postgres](postgres/index.md) | yes (`postgres`) | **yes** | [40.35 / F](postgres/quick/README.md) | [38.06 / F](postgres/full/README.md) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.

## For CTI analysts

Use the published SCORECARD modules to judge whether attackers reach interactive depth or stop at handshake/credential capture. This lab configuration intentionally disables outbound feeds (HPFeeds, Artillery ban lists, PyRDP player forwarding) to satisfy containment attestation.

## For blue teams

Treat δ_C and Module D as mandatory pre-flight checks before exposing any decoy on production networks. Module C reflects what the UHBS harness could read from local logs — mirror those fields into your SIEM if you reuse the same layout.
