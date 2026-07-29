# lophiid

**Status:** Informative · evaluation gap (skip note)  
**Upstream:** [mrheinen/lophiid](https://github.com/mrheinen/lophiid)

## Why UHBS did not publish UHQS for HTTP in this batch

Lophiid is a **hybrid AI honeypot** with a distributed backend/agent architecture. The maintained [Quick Start](https://github.com/mrheinen/lophiid/blob/main/QUICK_START.md) path assumes **OpenRouter API keys** for AI triage/responders, optional VirusTotal integration, local CA generation, and multi-container Docker Compose wiring between backend and edge agents. This UHBS 4.2.2 lab batch runs under an **air-gap constraint with no paid LLM API keys**, so we cannot stand up the AI responder pipeline faithfully or grade HTTP engagement without inventing scores.

Static-only rules could theoretically be deployed, but that would not represent the project's documented operating mode (AI-driven request classification and specialized responders for injection, uploads, and shell sessions). Publishing a numeric UHQS without the AI stack would mislead CTI readers comparing against fully-featured deployments.

## What analysts should do instead

- Treat this entry as a **catalog gap note**, not a failing grade.
- If you operate lophiid with OpenRouter/VT keys and isolated agents, re-run `uhbs-lab` locally using the Web-API HTTP TPS stubs under `docs/conformance/labs/lophiid/` once your stack matches production intent.
- For OWA-style credential sinks without AI, see graded proof for [owa-honeypot](../owa-honeypot/index.md) in the same batch.

## Protocol survey

| Surface | UHBS plugin? | Graded? | Notes |
| --- | --- | --- | --- |
| HTTP (agent) | yes (`http`) | **no** | Skip — AI/OpenRouter dependency |

> Named product is survey documentation only — not a UHBS endorsement.
