# pyrdp (GoSecure)

**Status:** Informative · evaluation proof  
**Upstream:** [GoSecure/pyrdp](https://github.com/GoSecure/pyrdp)  
**Runtime:** lab image `pyrdp:uhbs-lab` on `127.0.0.1:13389`

RDP MITM listener graded as a decoy surface; slim image runs pyrdp-mitm on 3389 with loopback relay target for lab containment.

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [rdp](rdp/index.md) | yes (`rdp`) | **yes** | [33.93 / F](rdp/quick/README.md) | [33.93 / F](rdp/full/README.md) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.

## For CTI analysts

Use the published SCORECARD modules to judge whether attackers reach interactive depth or stop at handshake/credential capture. This lab configuration intentionally disables outbound feeds (HPFeeds, Artillery ban lists, PyRDP player forwarding) to satisfy containment attestation.

## For blue teams

Treat δ_C and Module D as mandatory pre-flight checks before exposing any decoy on production networks. Module C reflects what the UHBS harness could read from local logs — mirror those fields into your SIEM if you reuse the same layout.
