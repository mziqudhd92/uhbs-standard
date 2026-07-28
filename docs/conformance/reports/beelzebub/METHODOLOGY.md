# Methodology: Beelzebub multi-protocol UHBS lab

**Status:** Informative  
**UHBS:** 4.2.1 · Images `uhbs:4.2.1` (quick) / `uhbs:4.2.1-full` (full)  
**Upstream commit:** `80e1428d023d564481acede9e63eb49e1631bfec`

## What was graded

Only protocols with a dedicated UHBS harness plugin (or intentional generic TCP mapping) were scored:

- **HTTP** — quick 52.77/D, full 66.02/D
- **Redis** — quick 50.56/D, full 61.01/D
- **SSH** — quick 74.45/C, full 59.88/D
- **Telnet** — quick 39.16/F, full 47.89/F
- **MCP** — graded via the in-tree `mcp` plugin (Web-API class). See [mcp/](mcp/) and [architecture/mcp-honeypot-grading.md](../../../architecture/mcp-honeypot-grading.md). MCP is **not** the same as classic HTTP Web-API checks: JSON-RPC lifecycle, tool allowlists, and `surface_depth` apply.

Other services the product may advertise (for example DNS, RDP, MySQL without a UHBS plugin path in this lab) were **not** graded as separate UHQS targets.

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
