# Beginner tutorial: GenAI/MCP replay bench

CI-safe **replay buffer** — no LLM sampling drift.

```bash
pip install 'uhbs[genai-bench]'
uhbs genai-bench example beginner --out genai-beginner
uhbs genai-bench analyze genai-beginner/replay.json --out report.json
```

Check `metrics.clr`, `metrics.scr`, and `metrics.ttft.penalize_high_latency` (false when `timing_intent` is `tarpit`).

Does **not** change UHQS. Not exposed via `uhbs-mcp`.
