# Methodology: OpenCanary multi-protocol UHBS lab

**Status:** Informative  
**UHBS:** 4.0.0 · Images `uhbs:4.0.0` (quick) / `uhbs:4.0.0-full` (full)  
**Upstream commit:** `bc231423aa40242cbd0bf34801f8788e23420dee`  
**Image:** `thinkst/opencanary:latest` (`sha256:558c508742ebc768d979f545bf1889be9d7d58377bd0144058c7df713a88763f`)

## What was graded

Only protocols with a dedicated UHBS harness plugin were scored:

| Protocol | Port | Quick | Full |
| --- | ---: | --- | --- |
| HTTP | 80 | 41.30 / F | 50.12 / D |
| FTP | 21 | 49.03 / F | 59.43 / D |
| SSH | 2222 | 24.74 / F | 28.44 / F |
| Telnet | 23 | 47.35 / F | 57.00 / D |
| Redis | 6379 | 41.27 / F | 48.26 / F |

**Not graded:** SMB (Samba required), MySQL, MSSQL, MongoDB, RDP, SIP, SNMP, NTP, TFTP, VNC, Git, HTTP-proxy, TCP banner, LLMNR, portscan.

## Environment notes

- Network: Docker `uhbs-lab`
- Config mount: `/etc/opencanaryd/opencanary.conf` (first OpenCanary search path)
- Safety: `UHBS_AIRGAP_ATTESTED=1`; egress gateway canary log mounted for full runs
- SSH canary rejects interactive auth by design (alerts on attempts)

## Limitations

- Module C often partial when product logs are not STIX/OTel/ECS
- Safety Gate frequently WARN (δ_C=0.81) under attestation-heavy Docker labs
- Grades are evaluation proof, not certification
