# HoneyMCP — MCP

**UHBS:** v4.2.2 · evaluation proof for the `mcp` protocol plugin (Web-API class)  
**Upstream:** [kosiorkosa47/honeymcp](https://github.com/kosiorkosa47/honeymcp) · commit `966bb908d140809957ba01e05132631c514ade5d`

| Run | UHQS | Grade | Notes |
| --- | --- | --- | --- |
| [Quick](quick/) | **43.04** | F | δ_C 0.56 · `surface_depth=interactive` |
| [Full](full/) | **42.93** | F | Prefer full for claim-grade |

Graded default Streamable HTTP surface `POST /mcp` (aws-admin persona). MCP grading differs from classic HTTP: JSON-RPC lifecycle, tool allowlists, and `surface_depth`. See [architecture/mcp-honeypot-grading.md](../../../../architecture/mcp-honeypot-grading.md).

Safety Gate dominated the composite (Module D C=75 → δ_C=0.5625) despite strong Module B (~94). Upstream applies a tight per-IP rate limit (~2 req/s, burst 20); the lab image raises that so Module A/B probes can finish — see [METHODOLOGY](../METHODOLOGY.md).

## Reproduce

```bash
# After honeymcp:uhbs-lab listens on :8080 (see TUTORIAL.md)
docker run --rm -v "$PWD:/work" -w /work --network uhbs-lab \
  -e UHBS_AIRGAP_ATTESTED=1 -e UHBS_QUICK=1 \
  uhbs:4.2.2 lab \
  --inventory /work/docs/conformance/labs/honeymcp/inventory.yaml \
  --target honeymcp-mcp \
  --tps /work/docs/conformance/labs/honeymcp/web_api_mcp_quick.yaml \
  --protocol mcp --quick --skip-sast-tools \
  --out /work/docs/conformance/reports/honeymcp/mcp/quick
```
