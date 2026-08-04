# GenAI/MCP bench CLI (`uhbs genai-bench`)

Experimental. Replay-first (CI-safe). Does not change UHQS. Not MCP-exposed.

```bash
pip install 'uhbs[genai-bench]'
uhbs genai-bench example beginner --out genai-beginner
uhbs genai-bench analyze genai-beginner/replay.json --out genai-benchmark-report.json
uhbs genai-bench stub --out replay.json   # write deterministic stub
```

Live decoy probing requires `uhbs[lab]` and explicit experimental flags; keep sandboxed.
