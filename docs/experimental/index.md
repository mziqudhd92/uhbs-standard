# Experimental Benchmark Extensions (optional)

**Status:** Experimental · informative · **UHQS unchanged**

Opt-in surfaces shipped alongside UHBS 4.5.x for research and high-assurance labs.
They do **not** change normative Modules A–F, weights, δ_C, or letter grades.

| Surface | Install | CLI | Tutorials |
| --- | --- | --- | --- |
| Five-dimension matrix | `uhbs[experimental]` | [`uhbs matrix`](cli-matrix.md) | [Beginner](tutorial-matrix-beginner.md) · [Advanced](tutorial-matrix-advanced.md) |
| GenAI/MCP bench | `uhbs[genai-bench]` | [`uhbs genai-bench`](cli-genai-bench.md) | [Beginner](tutorial-genai-beginner.md) · [Advanced](tutorial-genai-advanced.md) |
| Host provenance | `uhbs[experimental]` | [`uhbs provenance`](cli-provenance.md) | [Beginner](tutorial-provenance-beginner.md) |
| OT plugins | `uhbs[lab]` | `uhbs-lab --protocol …` | See Conpot / plugin authoring |

RFC: [0002-experimental-benchmark-extensions](../rfcs/0002-experimental-benchmark-extensions.md) · Architecture: [overview](../architecture/experimental-benchmarks.md)

## Safety

- Offline analyzers never open sockets.
- Live GenAI/OT probes stay on UHBS-Lab; **not** exposed via `uhbs-mcp`.
- Provenance collectors are external; UHBS validates filtered digests only.
