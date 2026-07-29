# galah — skipped (LLM dependency)

**Status:** Informative · **not graded**  
**Upstream:** [https://github.com/0x4D31/galah](https://github.com/0x4D31/galah)

Galah is an **LLM-powered HTTP honeypot**: every novel request can invoke a configured provider (OpenAI, Google AI, Anthropic, Cohere, GCP Vertex, or Ollama) to synthesize headers and bodies. The upstream CLI requires `--provider` and `--model`, and documents `LLM_API_KEY` / cloud credentials. This UHBS lab session had **no OpenAI, Anthropic, or other LLM API keys** in the environment, and spinning up a local Ollama model was out of scope for the air-gapped Docker grading window.

Without a live model, the service cannot answer UHBS HTTP fidelity and behavioral probes in a reproducible way; scores would reflect infrastructure failure, not decoy quality. UHBS therefore records a **skip note** rather than fabricated UHQS values. Re-queue when operators can supply keys with billing limits, or when a pinned local Ollama image is acceptable inside an isolated lab VLAN.

See [TUTORIAL.md](TUTORIAL.md) · [METHODOLOGY.md](METHODOLOGY.md).

## Trust

Informative UHBS 4.2.2 gap note — not an endorsement. [READING-UHQS.md](../READING-UHQS.md)
