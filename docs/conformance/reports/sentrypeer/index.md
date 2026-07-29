# sentrypeer

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/SentryPeer/SentryPeer](https://github.com/SentryPeer/SentryPeer) · GitHub last push `2026-07-27`  
**UHBS:** 4.2.2 (no version bump)

## What this decoy is

SIP/VoIP honeypot oriented at toll-fraud and SIP abuse telemetry.

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [SIP](sip/) | yes | **yes** (`:5060` lab) | [43.38 / F](sip/quick/) | [43.38 / F](sip/full/) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

## For CTI analysts

- Collects SIP methods useful for VoIP fraud intelligence (INVITE/REGISTER floods, suspicious From/To).
- Correlate source IPs with known SIP scanners and fraud clusters.

**Primary signals you can expect (when logging is wired):** SIP REGISTER/INVITE/OPTIONS, user agents, called numbers, source IPs.

## For blue teams / detection engineering

- Keep SIP honeypots off corporate voice VLANs; fraud bots are noisy and can overwhelm shared SBCs if misrouted.
- Forward SentryPeer/API events into detections for REGISTER/INVITE anomalies.
- Confirm UDP/TCP SIP exposure matches your intentional decoy design.

## Trust & limitations

- This page is **evaluation proof** under UHBS 4.2.2 — not a certification or vendor ranking.
- Prefer **full/** artifacts over **quick/** for operational decisions.
- Re-run via [TUTORIAL.md](TUTORIAL.md); environment notes in [METHODOLOGY.md](METHODOLOGY.md).
- How to read modules: [READING-UHQS.md](../READING-UHQS.md)
