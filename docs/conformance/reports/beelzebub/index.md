# Beelzebub (UHBS multi-protocol proof)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/beelzebub-labs/beelzebub](https://github.com/beelzebub-labs/beelzebub) · commit `80e1428d023d564481acede9e63eb49e1631bfec`  
**Scope:** Every UHBS-native protocol plugin that the lab container exposed was graded separately (quick + full).

| Protocol | Class / port | Quick | Full |
| --- | --- | --- | --- |
| [HTTP](http/index.md) | Web-API · HTTP :8080 | [52.77 / D](http/quick/README.md) | [66.02 / D](http/full/README.md) |
| [Redis](redis/index.md) | Low-Interaction · Redis :6379 | [50.56 / D](redis/quick/README.md) | [61.01 / D](redis/full/README.md) |
| [SSH](ssh/index.md) | Low-Interaction · SSH :2222 | [74.45 / C](ssh/quick/README.md) | [59.88 / D](ssh/full/README.md) |
| [Telnet](telnet/index.md) | Low-Interaction · Telnet :23 | [39.16 / F](telnet/quick/README.md) | [47.89 / F](telnet/full/README.md) |
| [MCP](mcp/index.md) | Web-API (MCP v1) · :8000 | [43.04 / F](mcp/quick/README.md) | [42.93 / F](mcp/full/README.md) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.


## What this decoy is

Multi-protocol honeypot including SSH/HTTP/Telnet/Redis and MCP surfaces in UHBS labs.

## For CTI analysts

- Protocol mix supports correlating the same source IP across SSH and HTTP/MCP lures.
- MCP grades are about decoy tool/JSON-RPC behavior — not endorsement of AI gateway products.

**Primary signals:** Per-protocol sessions; MCP tool/list and JSON-RPC exchanges when enabled.

## For blue teams / detection engineering

- Enable only needed listeners; review MCP tool allowlists carefully.
- Use per-protocol report hubs when tuning detections.

## Trust & limitations

- Evaluation proof under UHBS 4.2.2 — not a certification or endorsement.
- Prefer **full/** over **quick/** for decisions.
- Reading guide: [READING-UHQS.md](../READING-UHQS.md).
