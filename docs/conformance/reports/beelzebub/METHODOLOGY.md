# Methodology: Beelzebub multi-protocol UHBS lab

**Status:** Informative  
**UHBS:** 4.0.0 · Images `uhbs:4.0.0` (quick) / `uhbs:4.0.0-full` (full)  
**Upstream commit:** `80e1428d023d564481acede9e63eb49e1631bfec`

## What was graded

Only protocols with a dedicated UHBS harness plugin (or intentional generic TCP mapping) were scored:

- **HTTP** — quick 41.73/F, full 50.12/D
- **Redis** — quick 46.77/F, full 55.55/D
- **SSH** — quick 60.31/D, full 45.74/F
- **Telnet** — quick 47.78/F, full 57.00/D

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
