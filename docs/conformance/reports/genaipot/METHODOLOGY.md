# Methodology: GenAIPot UHBS lab

**Status:** Informative  
**UHBS:** 4.2.2  
**Upstream zip tree:** `205ffe40008f2e76e0decdb01bc19bf8e00acd8a`  
**Image:** `annls/genaipot:latest` @ `sha256:627d7fde6d4a6f937fde3b3366fb55605a90cea6370e1f5beac9c39d8ecfeeac` (reports v0.9.2)

## What was graded

- **SMTP** — host `:2525` → container `:25`. Quick **30.9 / F**, full **30.78 / F**. See [smtp/](smtp/).
- **POP3** — host `:1110` → container `:110`. Quick **44.24 / F**, full **44.13 / F**. See [pop3/](pop3/).

## Environment notes

- Mode: Docker `--docker` copies `var/no_ai` templates (no OpenAI/Azure/GCP calls)
- Banner / domain from offline config: `bankers.gov` / sendmail-themed EHLO ads (SMTP); POP3 banner uses generic localhost templates in this image
- Safety: `UHBS_AIRGAP_ATTESTED=1`
- Telemetry: SQLite `GenAIPot.db` copied to a host telemetry dir (not STIX/OTel/ECS) → Module C partial

## Fidelity observations

**SMTP (Module A ~30):** RFC 5321 probes expect **503** for bad command sequence and a clean `QUIT` close. Observed GenAIPot responses often used generic **500** (`Command unrecognized`), including for `QUIT` after EHLO.

**POP3 (Module A ~95):** Pre-auth `STAT`/`LIST` correctly return `-ERR`. `CAPA` (RFC 2449) is unsupported (`-ERR`) — treated as honest non-support (partial nego). `USER → PASS → STAT → QUIT` succeeds under anonymous offline config.

## Limitations

- Offline templates ≠ live GenAI response quality claimed in marketing demos
- Module C lacks STIX/OTel schema evidence
- Safety Gate WARN path under attestation-heavy Docker labs
- Grades are evaluation proof, not certification
