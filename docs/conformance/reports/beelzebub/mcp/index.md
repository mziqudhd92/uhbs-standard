# Beelzebub — MCP

**UHBS:** v4.2.1 · evaluation proof for the `mcp` protocol plugin (Web-API class)

| Run | UHQS | Grade | Notes |
| --- | --- | --- | --- |
| [Quick](quick/) | **43.04** | F | δ_C 0.56 · `surface_depth=interactive` |
| [Full](full/) | **42.93** | F | Prefer full for claim-grade |

MCP grading differs from classic HTTP: JSON-RPC lifecycle, tool allowlists, and `surface_depth`. See [architecture/mcp-honeypot-grading.md](../../../../architecture/mcp-honeypot-grading.md) and [METHODOLOGY.md](../METHODOLOGY.md).

Safety Gate dominated the composite (Module D C=75 → δ_C=0.5625) despite strong Module B (~94).

## Reproduce

```bash
# After Beelzebub exposes MCP on :8000 (see labs/beelzebub/configurations/services/mcp-8000.yaml)
docker run --rm -v "$PWD:/work" -w /work --network uhbs-lab \
  -e UHBS_AIRGAP_ATTESTED=1 -e UHBS_QUICK=1 \
  uhbs:4.2.1 lab \
  --inventory /work/docs/conformance/labs/beelzebub/inventory.yaml \
  --target beelzebub-mcp \
  --tps /work/docs/conformance/labs/beelzebub/web_api_mcp_quick.yaml \
  --protocol mcp --quick --skip-sast-tools \
  --out /work/docs/conformance/reports/beelzebub/mcp/quick
```
