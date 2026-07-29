# kippo (desaster)

**Status:** Informative · evaluation proof  
**Upstream:** [desaster/kippo](https://github.com/desaster/kippo)  
**Runtime:** lab image `kippo:uhbs-lab` on `127.0.0.1:12228`

Classic Python/Twisted SSH cowrie predecessor with emulated filesystem; lab listens on 2222 with auto-generated host keys.

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [ssh](ssh/index.md) | yes (`ssh`) | **yes** | [35.64 / F](ssh/quick/README.md) | [35.64 / F](ssh/full/README.md) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.

## For CTI analysts

Use the published SCORECARD modules to judge whether attackers reach interactive depth or stop at handshake/credential capture. This lab configuration intentionally disables outbound feeds (HPFeeds, Artillery ban lists, PyRDP player forwarding) to satisfy containment attestation.

## For blue teams

Treat δ_C and Module D as mandatory pre-flight checks before exposing any decoy on production networks. Module C reflects what the UHBS harness could read from local logs — mirror those fields into your SIEM if you reuse the same layout.
