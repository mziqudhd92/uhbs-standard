# RFC 0002: Experimental Benchmark Extensions (Informative)

- **Status:** Draft (informative)
- **Author:** Moran Zavdi
- **UHBS version affected:** 4.5.0 (no UHQS change)
- **Created:** 2026-08-04

## Problem

Operators and researchers need optional, machine-verifiable evidence for:

1. A multi-dimensional quality matrix (fingerprinting, interaction depth, fidelity, data quality, resource overhead)
2. GenAI / MCP resilience (canary leakage, indirect injection, multi-turn coherence, TTFT)
3. Host-side provenance for high-interaction Linux labs (collector-neutral, rate-limited)
4. Deeper IoT/OT protocol verification beyond shallow registration

None of these should silently rewrite normative UHQS, δ_C, or published grades.

## Proposal

Ship **opt-in experimental** CLI groups and schemas:

| Surface | CLI | Role |
| --- | --- | --- |
| Five-dimension matrix | `uhbs matrix` | Informative dimension scores + sensitivity |
| GenAI/MCP bench | `uhbs genai-bench` | Offline replay stubs + optional lab probes |
| Host provenance | `uhbs provenance` | Validate/summarize/attach filtered digests |
| OT plugins | `uhbs-lab` | Harden Modbus/S7; add BACnet/MQTT/CoAP |

Rules:

- Do **not** change `uhqs_math.py`, weights, or δ_C.
- Label all outputs `experimental` / `uhqs_unchanged: true`.
- Default CI uses deterministic replay stubs (no LLM sampling).
- Provenance attaches aggregated digests, not raw unbounded eBPF streams.
- Live probes stay on UHBS-Lab; never expose via `uhbs-mcp`.
- TTFT is distinct from Module E; TPS tarpit intent must not auto-penalize high TTFT.
- OT probes expose per-protocol timeouts and strict frame validation.

Promotion to normative UHQS requires a **separate RFC**, ≥3 profile-class corpus validation, and independent reproduction (see ROADMAP Phase 6).

## Compatibility / migration

Existing scorecards remain comparable. Optional `informative_refs` on scorecards is display-only. New schemas live under `experimental-*.schema.json`.

## Alternatives considered

- Fold dimensions into UHQS weights immediately — rejected; violates corpus/RFC gate.
- Ship privileged eBPF loader in the wheel — rejected; platform/privilege risk; collector-neutral ingestion first.
- Expose genai-bench via MCP — rejected (AGENTS.md Safety Gate).

## Security / Safety Gate notes

Lab/network probes remain CLI-only. AEP/offline analyzers keep forbidden-import firewall. Provenance collectors must sit on the sandbox host, not inside the decoy.

## References

- `docs/advanced-evidence/improvement-notes.md`
- `ROADMAP.md` Phase 6
- `AGENTS.md` MCP / lab boundaries
