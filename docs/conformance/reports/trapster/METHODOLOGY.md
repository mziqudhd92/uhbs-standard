# Methodology: Trapster Community multi-protocol UHBS lab

**Status:** Informative  
**UHBS:** 4.0.1 · Images `uhbs:4.0.1` (quick) / `uhbs:4.0.1-full` (full)  
**Upstream commit:** `dfc2c43dad119578f9c7344a0077790ed7fee01b`

## What was graded

Only protocols with a dedicated UHBS harness plugin (or intentional generic TCP mapping) were scored:

- **FTP** — quick 43.37/F, full 51.78/D
- **HTTP** — quick 50.13/D, full 63.33/D
- **SSH** — quick 40.06/F, full 44.38/F
- **Telnet** — quick 52.49/D, full 64.9/D

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
