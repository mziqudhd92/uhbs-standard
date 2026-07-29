# HoneyMCP (UHBS MCP proof)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/kosiorkosa47/honeymcp](https://github.com/kosiorkosa47/honeymcp) · commit `966bb908d140809957ba01e05132631c514ade5d`  
**Scope:** Streamable HTTP MCP (`POST /mcp`, default aws-admin persona) graded with the in-tree `mcp` plugin.

| Protocol | Class / port | Quick | Full |
| --- | --- | --- | --- |
| [MCP](mcp/index.md) | Web-API (MCP v1) · :8080 (lab host map :18080) | [43.04 / F](mcp/quick/README.md) | [42.93 / F](mcp/full/README.md) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.


## What this decoy is

MCP-oriented honeypot graded with the UHBS MCP protocol plugin.

## For CTI analysts

- Emerging surface: observe tool enumeration and JSON-RPC abuse against MCP decoys.

**Primary signals:** MCP initialize/tools/list and JSON-RPC calls.

## For blue teams / detection engineering

- Distinguish UHBS MCP *grading* from the `uhbs_mcp` host tooling — different roles.
- Strictly allowlist tools; assume prompt/tool injection attempts.

## Trust & limitations

- Evaluation proof under UHBS 4.2.2 — not a certification or endorsement.
- Prefer **full/** over **quick/** for decisions.
- Reading guide: [READING-UHQS.md](../READING-UHQS.md).
