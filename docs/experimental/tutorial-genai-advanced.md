# Advanced tutorial: GenAI/MCP

1. Start from the beginner replay fixture.
2. Switch `timing_intent` between `tarpit` and `normal` and re-analyze — tarpit must not auto-fail high TTFT.
3. Live MCP decoy probing (optional): use `uhbs[lab]` in an air-gapped sandbox only; keep injection budgets and tool denylists. Never wire live probes into MCP hosts.

See [architecture](../architecture/experimental-benchmarks.md) and RFC 0002.
