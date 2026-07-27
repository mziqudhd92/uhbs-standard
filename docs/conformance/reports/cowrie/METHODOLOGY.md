# Methodology: Cowrie multi-protocol UHBS lab

**Status:** Informative  
**UHBS:** 4.0.1 · Images `uhbs:4.0.1` / `uhbs:4.0.1-full`  
**Upstream commit:** `e7d1854a9489fa78845af01e445232f854414f87`

## Verified product protocols

From Cowrie README / `cowrie.cfg.dist` / docs:

| Surface | Default | This lab | UHBS plugin |
| --- | --- | --- | --- |
| SSH | enabled `:2222` | enabled | `ssh` |
| SFTP | `sftp_enabled = true` (SSH subsystem) | smoke-verified (listdir) | covered under SSH (no separate `sftp` plugin) |
| SCP | SSH file transfer | not separately scored | under SSH interaction surface |
| Telnet | **disabled** by default `:2223` | enabled via lab `cowrie.cfg` | `telnet` |
| Proxy / backend-pool | optional | not deployed | n/a |

## Grades

- SSH full: **61.37 / D** (δ_C=1.0)
- Telnet full: **64.90 / D** (δ_C=0.81)

## Environment

- Network `uhbs-lab`; credentials `root`/`admin`
- Overlay config mounted at `/cowrie/cowrie-git/etc/cowrie.cfg`
- Full runs: telemetry mount + `UHBS_AIRGAP_ATTESTED=1`

## Limitations

- No UHBS `sftp` protocol id — SFTP is not double-counted as a second UHQS card
- Module C often partial without STIX/OTel/ECS-shaped logs
- Grades are evaluation proof, not certification
