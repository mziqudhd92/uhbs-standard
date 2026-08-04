# MCP server (AI hosts)

**Status:** Informative · tooling  
**Package:** `uhbs[mcp]` · entry points `uhbs-mcp` / `python -m uhbs_mcp`  
**SDK:** Model Context Protocol Python SDK **`mcp>=2,<3`** (`MCPServer`; was `FastMCP` on 1.x)  
**Transport:** local **stdio** only (no remote HTTP / no `uhbs lab` execution)

The [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) is the open
standard AI clients use to call tools. UHBS ships a small MCP server so agents in
Cursor, Claude Desktop, VS Code Copilot, ChatGPT connectors, and similar hosts
can **validate scorecards**, **recompute UHQS**, and **read schemas** without
inventing math.

UHBS remains an open-source **beta-status** framework — not a consortium
standard. MCP is optional tooling for agents; the CLI and Docker lab stay the
primary human workflows ([CLI guide](cli.md)).

To **grade MCP honeypots** (live JSON-RPC probes), use `uhbs[lab]` / `uhbs-lab --protocol mcp` — see [MCP honeypot grading](../architecture/mcp-honeypot-grading.md). This AI-host server does **not** run lab probes.

---

## What is included (and what is not)

| Included | Deferred (intentionally) |
| --- | --- |
| `validate_scorecard` / `validate_profile` / `validate_evidence` | Streamable HTTP / remote hosting |
| `compute_uhqs` + `list_profile_classes` | `uhbs lab` / Docker live probes |
| `list_conformance_fixtures` / `get_scorecard_summary` / `list_lab_reports` | Shell egress or network attack tools |
| Resources: schemas + scoring-formula + this guide | OAuth remote gateways |

Normative UHQS math still lives in `uhbs_core.uhqs_math` — the MCP server wraps
the same helpers as `uhbs score` / `uhbs validate-scorecard`.

---

## Install

From a UHBS checkout:

```bash
git clone https://github.com/uhbs/uhbs-standard.git
cd uhbs-standard
python -m venv .venv
source .venv/bin/activate
pip install -c constraints.txt -e ".[mcp,dev]"
# Entry points (stdio JSON-RPC — run via an MCP host, not interactively):
#   uhbs-mcp
#   python -m uhbs_mcp
```

Extras:

- `uhbs[mcp]` — MCP SDK + server entry point  
- Keep using `uhbs[lab]` / Docker for live Modules A–F grades

Registry metadata (for a future official MCP Registry publish after PyPI):  
[`server.json`](https://github.com/uhbs/uhbs-standard/blob/main/server.json) at the repo root.

---

## Client configuration

Set `UHBS_ROOT` to the absolute checkout path so relative fixture paths and
schemas resolve.

### Cursor / VS Code (MCP)

```json
{
  "mcpServers": {
    "uhbs": {
      "command": "python",
      "args": ["-m", "uhbs_mcp"],
      "cwd": "/absolute/path/to/uhbs-standard",
      "env": {
        "UHBS_ROOT": "/absolute/path/to/uhbs-standard"
      }
    }
  }
}
```

Or after install, use the console script:

```json
{
  "mcpServers": {
    "uhbs": {
      "command": "uhbs-mcp",
      "cwd": "/absolute/path/to/uhbs-standard",
      "env": {
        "UHBS_ROOT": "/absolute/path/to/uhbs-standard"
      }
    }
  }
}
```

### Claude Desktop

Edit `claude_desktop_config.json` (macOS:
`~/Library/Application Support/Claude/claude_desktop_config.json`) with the same
`mcpServers.uhbs` block.

### uvx (after the `uhbs` package is on PyPI)

```json
{
  "mcpServers": {
    "uhbs": {
      "command": "uvx",
      "args": ["--from", "uhbs[mcp]", "uhbs-mcp"],
      "env": {
        "UHBS_ROOT": "/absolute/path/to/uhbs-standard"
      }
    }
  }
}
```

Until PyPI publish, prefer the editable git install above.

### Docker grading image

The published `uhbs:4.5.0` / `uhbs:4.5.0-full` images install `uhbs[lab]` only
(CLI + harness). They do **not** ship `uhbs-mcp`. Run the MCP server on the host
(or a dedicated venv) next to your AI client.

---

## Tools

| Tool | Purpose |
| --- | --- |
| `validate_scorecard` | Schema + optional UHQS integrity |
| `validate_profile` | TPS YAML schema + weights |
| `validate_evidence` | Evidence-pack schema |
| `compute_uhqs` | UHQS / δ_C / grade from A–F scores |
| `list_profile_classes` | Normative class weight tables |
| `list_conformance_fixtures` | Fixtures under `docs/conformance/fixtures/` |
| `get_scorecard_summary` | Compact module / gate summary |
| `list_lab_reports` | Published report hubs |

## Resources

| URI | Content |
| --- | --- |
| `uhbs://schema/scorecard` | `schemas/scorecard.schema.json` |
| `uhbs://schema/profile` | `schemas/profile.schema.json` |
| `uhbs://schema/evidence-pack` | `schemas/evidence-pack.schema.json` |
| `uhbs://docs/scoring-formula` | Spec scoring prose |
| `uhbs://docs/mcp` | This guide |

## Prompt

- `validate_and_explain_scorecard` — guided validate → summarize → explain δ_C workflow

---

## Publishing to the MCP Registry

1. Publish the `uhbs` distribution to PyPI (with the `mcp` extra).  
2. Confirm [`server.json`](https://github.com/uhbs/uhbs-standard/blob/main/server.json) `packages[].identifier` / version.  
3. Follow the official registry publish flow:  
   https://github.com/modelcontextprotocol/registry  
4. Keep **stdio-only** until auth and Safety Gate policy for remote/lab tools are defined.

---

## Verify

```bash
pip install -c constraints.txt -e ".[mcp,dev]"
pytest tests/test_mcp.py -q
uhbs validate-scorecard docs/conformance/fixtures/opencanary-web-api.scorecard.json --strict
```

### Advanced Evidence Profile (analysis-only boundary)

If AEP is later exposed through MCP, tools must remain **local schema validation,
deterministic calculation, and report rendering** only — never lab, network,
shell, container, agent, or attack execution. Today AEP is CLI-only:
[Advanced Evidence Profile](../advanced-evidence/index.md).

See also: [CLI & Validator](cli.md) · [llms.txt](https://github.com/uhbs/uhbs-standard/blob/main/llms.txt) · [AGENTS.md](https://github.com/uhbs/uhbs-standard/blob/main/AGENTS.md)
