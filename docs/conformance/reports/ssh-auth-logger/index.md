# ssh-auth-logger (JustinAzoff)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/JustinAzoff/ssh-auth-logger](https://github.com/JustinAzoff/ssh-auth-logger) · GitHub last push `2026-05-29`  
**Runtime:** `justinazoff/ssh-auth-logger:latest` (or local `ssh-auth-logger:uhbs-lab`; `SSHD_BIND=:2222`, host-mapped `127.0.0.1:12024`)

Low/zero-interaction SSH authentication logging honeypot (JSON logs; never grants a shell).

## What this decoy is

Zero/low-interaction SSH authentication logger — records auth, does not grant a real shell.

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [SSH](ssh/index.md) | yes (`ssh`) | **yes** | [44.38 / F](ssh/quick/README.md) | [44.38 / F](ssh/full/README.md) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.

## For CTI analysts

- Optimized for credential and auth-method telemetry (JSON logs) rather than post-auth command capture.
- Strong fit for CTI pipelines that enrich usernames/passwords/source ASNs from SSH noise.

**Primary signals you can expect (when logging is wired):** JSON auth events (user/password/key attempt metadata per upstream design).

## For blue teams / detection engineering

- Ideal as a pure auth sink: alert on volume, password spraying patterns, and novel client algorithms.
- Ensure log integrity and retention; these logs often contain cleartext attempted passwords — handle as sensitive.
- Earlier full runs were flaky under load in some lab conditions; prefer published full SCORECARD and re-validate if you change image tags.

## Trust & limitations

- This page is **evaluation proof** under UHBS 4.2.2 — not a certification or vendor ranking.
- Prefer **full/** artifacts over **quick/** for operational decisions.
- Re-run via [TUTORIAL.md](TUTORIAL.md); environment notes in [METHODOLOGY.md](METHODOLOGY.md).
- How to read modules: [READING-UHQS.md](../READING-UHQS.md)
