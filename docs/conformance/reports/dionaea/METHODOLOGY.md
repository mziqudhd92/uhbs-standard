# Methodology: Dionaea multi-protocol UHBS lab

**Status:** Informative  
**UHBS:** 4.0.0 · Images `uhbs:4.0.0` (quick) / `uhbs:4.0.0-full` (full)  
**Upstream commit:** `4e459f1b672a5b4c1e8335c0bff1b93738019215`

## What was graded

Only protocols with a dedicated UHBS harness plugin (or intentional generic TCP mapping) were scored:

- **FTP** — quick 49.10/F, full 55.30/D
- **HTTP** — quick 40.93/F, full 43.54/F
- **SMB** — quick 44.55/F, full 48.74/F

Other services the product may advertise (for example MCP, DNS, RDP, MySQL without a UHBS plugin path in this lab) were **not** graded as separate UHQS targets.

## Environment notes

- Network: Docker `uhbs-lab`
- Safety: `UHBS_AIRGAP_ATTESTED=1`; empty egress gateway canary mounted for full runs
- Dionaea official image is `linux/amd64` (emulated on arm64 hosts)
- Trapster AI features disabled (no API key); static/service skins only
- Beelzebub lab overlay uses static SSH/HTTP/Telnet/Redis service YAMLs (no live LLM keys)

## Limitations

- Module C often partial when product logs are not STIX/OTel/ECS
- Safety Gate frequently WARN (δ_C=0.81) under attestation-heavy Docker labs
- Grades are evaluation proof, not certification
