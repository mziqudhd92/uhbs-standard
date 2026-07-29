# Methodology: galah skip

**UHBS:** 4.2.2 · **HTTP** · **Status:** skipped (LLM API required)

Galah dynamically generates HTTP responses via external LLM APIs. The UHBS batch policy for this session disallowed OpenAI/Anthropic keys and did not provision Ollama. Skipping avoids misleading sub-zero scores from an idle binary.

Re-grade when LLM backend is pinned, rate-limited, and isolated from production networks.

See [READING-UHQS.md](../READING-UHQS.md).

## Evidence hierarchy (when graded later)

1. `full/SCORECARD.txt` — modules, UHQS, grade, δ_C
2. `full/report.json` — machine-readable
3. This methodology — scope and limits
4. Tutorial — replication commands

Until then, treat this page as a **skip / gap note**. See [READING-UHQS.md](../READING-UHQS.md).

## Trust

Informative only · UHBS 4.2.2 · not an endorsement. Isolate honeypot networks in real deployments; do not cite UHQS without SCORECARD proof.
