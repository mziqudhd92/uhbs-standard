# Methodology: DataTrap (Thales) UHBS lab

**Status:** Informative  
**UHBS:** 4.2.2  
**Upstream commit:** `7a906e11a0b19e75a32fead2ddd9a8b2b341beec`

## What DataTrap speaks vs what UHBS can grade

| DataTrap | UHBS plugin today | Notes |
| --- | --- | --- |
| SSH | `ssh` | Graded |
| HTTP/HTTPS | `http` | Graded HTTP (HTTPS not required in lab) |
| MySQL | `mysql` | Graded |
| Redis | `redis` | Graded |
| Telnet | `telnet` | Graded |
| PostgreSQL | `postgres` | Graded (alias `postgresql`) — Startup / SSLRequest / auth-deny |
| Generic TCP | `generic` | Product supports action/response TCP; this lab did not enable a `tcp` config |

## UHBS plugins DataTrap does not implement

UHBS also ships: `ftp`, `git`, `mcp`, `modbus`, `ntp`, `rdp`, `sip`, `smb`, `smtp`, `snmp`, `tftp`, `vnc` — not part of DataTrap’s advertised surface.

## Environment

- Image `datatrap:uhbs-lab` built from upstream Dockerfile
- Writable honeypot volume (SQLite `data_store.db` per service)
- No AWS Bedrock credentials in this lab (dataset-first paths still listen)
- Host maps: SSH `14222`, HTTP `18088`, MySQL `13306`, Redis `16379`, Telnet `12323`, Postgres `15432`

## Limitations

- Module C often partial without STIX/OTel mounts
- Safety Gate δ_C varies by protocol (SSH cleared C=100; others often attestation path)
- PostgreSQL Module B: DataTrap AuthOks any password (honeypot login capture) — Strict RFC auth-deny fails honestly
- Evaluation proof only — not certification
