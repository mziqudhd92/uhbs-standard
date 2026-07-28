# MCP honeypot grading vs UHBS AI-host MCP

**Status:** Informative  
**UHBS:** 4.2.0

UHBS has **two** MCP-related surfaces. Do not confuse them:

| Surface | Package / entry | Purpose |
| --- | --- | --- |
| **MCP honeypot grading** | `uhbs[lab]` · protocol plugin `mcp` · `uhbs-lab --protocol mcp` | Live probe of network-facing MCP decoys (JSON-RPC over HTTP/SSE) |
| **UHBS AI-host MCP server** | `uhbs[mcp]` · `uhbs-mcp` | Stdio tools for IDEs/agents to validate scorecards/fixtures — **no** lab network probes |

## How MCP decoys are graded (P0)

Unlike classic Web-API HTTP GET checks, MCP grading requires:

1. JSON-RPC 2.0 error codes (`-32700` / `-32600` / `-32601`), not HTTP status alone
2. Lifecycle: `initialize` → `notifications/initialized` (**no `id`**) → `tools/list`
3. Tool allowlist + `inputSchema` denylist (never call shell/SSRF-shaped tools)
4. Schema-aware `tools/call` arguments (map nonces to string properties)
5. `surface_depth`: `interactive` vs `metadata_only` (empty / high-risk-only tools → Module B ceiling **50** with explicit reasons)

Profile class for v1 TPS: **Web-API** (`mcp_server.yaml`). Latency samples use **`tools/list` RTT**, not SSE connect time.

## Operator grade path

```bash
pip install -e '.[lab]'
uhbs-lab \
  --inventory docs/conformance/labs/beelzebub/inventory.yaml \
  --tps docs/conformance/labs/beelzebub/web_api_mcp_quick.yaml \
  --protocol mcp \
  --out docs/conformance/reports/beelzebub/mcp/quick
```

Inventory annotations:

```yaml
mcp_path: /mcp
mcp_transport: streamable_http   # or sse
mcp_custom_allowlist_tools: [check_weather, get_status]
```

Beelzebub’s default decoy tools (`tool:system-log`, `tool:user-account-manager`) are not builtin echo/ping keywords — the lab inventory allowlists them explicitly so Module B can exercise the interactive surface without calling shell/SSRF-shaped tools.

See also [`docs/plugin-authoring.md`](../plugin-authoring.md) and [`docs/tooling/mcp.md`](../tooling/mcp.md).
