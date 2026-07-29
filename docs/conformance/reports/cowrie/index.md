# Cowrie (UHBS multi-protocol proof)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/cowrie/cowrie](https://github.com/cowrie/cowrie) · commit `e7d1854a9489fa78845af01e445232f854414f87`  
**Official capability:** medium/high-interaction **SSH and Telnet** honeypot; **SFTP/SCP** file transfer over SSH ([Cowrie README](https://github.com/cowrie/cowrie)).

| Protocol | Port | Quick | Full |
| --- | ---: | --- | --- |
| [SSH](ssh/index.md) (includes SFTP subsystem) | 2222 | 82.76 / B | 61.37 / D |
| [Telnet](telnet/index.md) | 2223 | 53.41 / D | 64.90 / D |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.


## What this decoy is

Medium-interaction SSH/Telnet honeypot widely used for interactive session and malware-download telemetry.

## For CTI analysts

- Rich post-auth command transcripts and downloaded malware samples (when enabled) support actor TTPs and tooling intel.
- SFTP/SCP may appear as SSH subsystems — UHBS grades SSH/Telnet plugins, not a separate SFTP protocol.

**Primary signals:** SSH/Telnet sessions, commands, downloaded artifacts, auth events.

## For blue teams / detection engineering

- Classic blue-team sensor: alert on successful auth to decoy creds and on outbound download behavior from the honeypot.
- Keep Cowrie isolated; downloaded malware must not reach production file shares.

## Trust & limitations

- Evaluation proof under UHBS 4.2.2 — not a certification or endorsement.
- Prefer **full/** over **quick/** for decisions.
- Reading guide: [READING-UHQS.md](../READING-UHQS.md).
