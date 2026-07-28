# Tutorial: grade HoneyMCP with UHBS (MCP)

**Status:** Informative · evaluation proof  
**Target:** [https://github.com/kosiorkosa47/honeymcp](https://github.com/kosiorkosa47/honeymcp) · commit `966bb908d140809957ba01e05132631c514ade5d`  
**Protocol graded:** MCP (Streamable HTTP)

## 0. Prerequisites

```bash
git clone https://github.com/mziqudhd92/uhbs-standard.git
cd uhbs-standard
pip install -c constraints.txt -e ".[dev,lab,mcp]"
docker network create uhbs-lab 2>/dev/null || true
```

## 1. Clone source (Module F)

```bash
mkdir -p .local/labs
git clone https://github.com/kosiorkosa47/honeymcp.git .local/labs/honeymcp
cd .local/labs/honeymcp
git checkout 966bb908d140809957ba01e05132631c514ade5d
```

## 2. Lab rate-limit override (required for UHBS probes)

Upstream throttles MCP POST routes at **~2 req/s with burst 20**. A full Module A/B handshake storm exceeds that and yields `HTTP 429`, collapsing Module B to `initialize failed`. For this evaluation proof, raise the governor before building:

```bash
# In .local/labs/honeymcp — keep the change local to the lab image
# per_second(50) / burst_size(500). Documented in METHODOLOGY.md.
```

Edit `src/transport/http.rs` governor builder (`.per_second(2)` / `.burst_size(20)`) to lab values above, then:

```bash
docker build -t honeymcp:uhbs-lab .local/labs/honeymcp
docker run -d --name honeymcp-lab --network uhbs-lab \
  -p 127.0.0.1:18080:8080 \
  honeymcp:uhbs-lab
```

Default image personas include **aws** at `POST /mcp` plus `/github/mcp`, `/vercel/mcp`, `/stripe/mcp`.

## 3. MCP quick + full

Target id: `honeymcp-mcp` · inventory: [`../../labs/honeymcp/inventory.yaml`](../../labs/honeymcp/inventory.yaml)

```bash
mkdir -p docs/conformance/reports/honeymcp/mcp/{quick,full}

# Local host inventory (127.0.0.1:18080) when not using Docker DNS:
#   .local/honeymcp-mcp-inventory.yaml

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 \
uhbs-lab \
  --inventory .local/honeymcp-mcp-inventory.yaml \
  --target honeymcp-mcp \
  --tps docs/conformance/labs/honeymcp/web_api_mcp_quick.yaml \
  --protocol mcp \
  --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
  --quick --skip-sast-tools --concurrency 10 --requests 50 \
  --out docs/conformance/reports/honeymcp/mcp/quick \
  --environment "Quick Docker lab: honeymcp-mcp"

UHBS_AIRGAP_ATTESTED=1 \
uhbs-lab \
  --inventory .local/honeymcp-mcp-inventory.yaml \
  --target honeymcp-mcp \
  --tps docs/conformance/labs/honeymcp/web_api_mcp_full.yaml \
  --protocol mcp \
  --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
  --concurrency 25 --requests 200 \
  --out docs/conformance/reports/honeymcp/mcp/full \
  --environment "Full Docker lab: honeymcp-mcp"
```

Inventory annotations used: `mcp_path: /mcp`, `mcp_transport: streamable_http`, and `mcp_custom_allowlist_tools` for aws-admin decoys (`get_caller_identity`, `list_secrets`, …).
