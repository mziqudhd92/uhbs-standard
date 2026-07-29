# artillery (BinaryDefense)

**Status:** Informative · evaluation proof  
**Upstream:** [BinaryDefense/artillery](https://github.com/BinaryDefense/artillery)  
**Runtime:** lab image `artillery:uhbs-lab` on `127.0.0.1:18081`

Binary Defense Artillery honeypot thread on TCP/8080 only (banning and threat feeds disabled) graded via UHBS generic TCP plugin.

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [generic](generic/index.md) | yes (`generic`) | **yes** | [39.84 / F](generic/quick/README.md) | [37.55 / F](generic/full/README.md) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.

## For CTI analysts

Use the published SCORECARD modules to judge whether attackers reach interactive depth or stop at handshake/credential capture. This lab configuration intentionally disables outbound feeds (HPFeeds, Artillery ban lists, PyRDP player forwarding) to satisfy containment attestation.

## For blue teams

Treat δ_C and Module D as mandatory pre-flight checks before exposing any decoy on production networks. Module C reflects what the UHBS harness could read from local logs — mirror those fields into your SIEM if you reuse the same layout.
