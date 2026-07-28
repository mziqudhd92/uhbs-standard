# Methodology: LLM Honeypot (Palisade) UHBS lab

**Status:** Informative  
**UHBS:** 4.2.2  
**Upstream commit:** `156004a1b122f201448635417ee47bd44d7f28ca`

## Protocol survey

| Surface | In repo? | Live listen (shipped cfg)? | UHBS plugin | Graded? |
| --- | --- | --- | --- | --- |
| SSH | Cowrie `[ssh]` | Yes `:2222` | `ssh` | **Yes** |
| SFTP | `[ssh] sftp_enabled = true` | Via SSH subsystem | (under SSH) | Via SSH |
| Telnet | Cowrie `[telnet]` | **No** (`enabled = false`) | `telnet` | No |
| Web dashboard | `web/` + compose | Log/stats UI, not a decoy | — | No |

Only protocols that actually listen under the product’s shipped configuration are graded.

## Environment notes

- Image: `cowrie/cowrie:latest` + bind-mounted overlays from `docs/conformance/labs/llm-honeypot/configs/`
- Host map: `127.0.0.1:12222` → container `:2222`
- Safety: `UHBS_AIRGAP_ATTESTED=1`; Module D cleared (C=100, δ_C=1.0) on these runs
- Do not mount the fork’s `commands/__init__.py` onto modern Cowrie — Twisted fails with `Unknown command: cowrie`

## Limitations

- LLM detection efficacy (ANSI traps / goal hijacking) is **out of scope** for UHQS
- Module C partial without STIX/OTel/ECS-shaped telemetry mounts
- Grades are evaluation proof, not certification
