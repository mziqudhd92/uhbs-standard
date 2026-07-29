# MockSSH (ncouture)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/ncouture/MockSSH](https://github.com/ncouture/MockSSH) · GitHub last push `2026-06-08`  
**Runtime:** `mockssh:uhbs-lab` (examples/mock_cisco.py on `:2222`, user `testadmin` / `x`)

SSH server emulator graded with the UHBS **ssh** plugin. Interactive Cisco-like shell; exec channels are limited.

## What this decoy is

Twisted-based mock SSH presenting scripted device-like behavior (lab used Cisco-style example).

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [SSH](ssh/) | yes | **yes** | [59.2 / D](ssh/quick/) | [59.0 / D](ssh/full/) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.

## For CTI analysts

- Can attract scanners expecting network-device SSH personalities; capture command sequences against the mock shell.
- Personality/script depth drives CTI value — shallow scripts yield shallow post-auth intel.

**Primary signals you can expect (when logging is wired):** SSH auth + scripted command transcripts per MockSSH configuration.

## For blue teams / detection engineering

- Validate the mock scripts match the narrative you want (router vs server) to avoid easy fingerprinting.
- Still isolate: MockSSH is not a hardened production SSHD.

## Trust & limitations

- This page is **evaluation proof** under UHBS 4.2.2 — not a certification or vendor ranking.
- Prefer **full/** artifacts over **quick/** for operational decisions.
- Re-run via [TUTORIAL.md](TUTORIAL.md); environment notes in [METHODOLOGY.md](METHODOLOGY.md).
- How to read modules: [READING-UHQS.md](../READING-UHQS.md)
