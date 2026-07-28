# Methodology: HoneyMCP UHBS lab

**Status:** Informative  
**UHBS:** 4.2.2  
**Upstream commit:** `966bb908d140809957ba01e05132631c514ade5d`

## What was graded

- **MCP** — Streamable HTTP on the default persona path `POST /mcp` (aws-admin). Quick **43.04 / F**, full **42.93 / F**. See [mcp/](mcp/) and [architecture/mcp-honeypot-grading.md](../../../architecture/mcp-honeypot-grading.md).

Other personas (`/github/mcp`, `/vercel/mcp`, `/stripe/mcp`) and stdio transport were **not** graded as separate UHQS targets in this proof.

## Environment notes

- Host map: `127.0.0.1:18080` → container `:8080` (avoids clash with other labs on `:8080`)
- Safety: `UHBS_AIRGAP_ATTESTED=1`
- Lab image `honeymcp:uhbs-lab` builds from upstream with a **rate-limit override** (see below)
- UHBS MCP client retries HTTP 429 with backoff (HoneyMCP “Wait for Ns” prose + `Retry-After`)

## Rate limit override

Upstream `tower_governor` defaults (~2 req/s, burst 20) are intentional anti-flood for a public sensor. UHBS Module A timing + FSM alone exceeds that burst from a single IP, so unpatched runs report `surface_depth=metadata_only` / `initialize failed` after Module A. The published scores use a lab-only raise to ~50 req/s / burst 500 so protocol fidelity and behavioral probes can complete. Production rate-limit behavior is therefore **not** reflected in Module E stress numbers.

## Limitations

- Module C partial when SQLite/JSONL telemetry is not mounted as STIX/OTel/ECS for the grader
- Safety Gate WARN path (δ_C=0.5625) under attestation-heavy Docker labs
- Grades are evaluation proof, not certification
