# RFC 0000: Title

- **Status:** Draft
- **Author:** (maintainer / contributor)
- **UHBS version affected:** 4.2.2 → (proposed)
- **Created:** YYYY-MM-DD

## Problem

Describe the concrete failure or gap in the current UHBS specification, schemas, protocol plugins, or UHQS math. Prefer observable symptoms (broken grades, missing protocol coverage, ambiguous Safety Gate behavior) over abstract wishes.

## Proposal

Explain the change in enough detail that another engineer could implement it without guessing. If UHQS weights, modules, or δ_C behavior change, point at `src/uhbs_core/uhqs_math.py` as the single source of truth and list CLI/MCP/harness surfaces that must stay identical.

## Compatibility / migration

State whether existing SCORECARD artifacts remain comparable, whether published conformance reports need re-runs, and how schema version fields change.

## Alternatives considered

List at least one alternative (including “do nothing”) and why it was rejected.

## Security / Safety Gate notes

Call out any impact on Module D containment, air-gap attestation, or exposure of attack tooling via MCP.

## References

Link related issues, prior RFCs, and specification sections under `docs/specification/`.
