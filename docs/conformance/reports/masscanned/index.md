# masscanned

**Status:** Surveyed · **skipped** (lab build/runtime)  
**Upstream:** [https://github.com/ivre/masscanned](https://github.com/ivre/masscanned) · GitHub last push `2026-06-17`

## Skip reason

masscanned implements a userland network stack and expects to bind a dedicated interface inside `NET_ADMIN` containers or network namespaces (see upstream README). It does not behave like a normal single-port TCP service on the `uhbs-lab` bridge, so UHBS HTTP/SSH plugins cannot reach it the way they do for Cowrie-style listeners. Grading was deferred pending a documented namespace lab recipe.

No UHBS quick/full grade was published for this target in batch C.

> Named product is evaluation proof only — not a UHBS endorsement.

## Why this page exists

UHBS publishes evaluation notes for products that were surveyed during conformance work even when a full UHQS grade is not available. Analysts should treat this as a **gap / skip note**, not a silent omission from the catalog.

## What analysts should do next

- Re-queue when a reproducible Docker or inventory recipe exists on the UHBS `uhbs-lab` bridge network without host-only networking tricks.
- Do not invent UHQS numbers for skipped products.
- Track deferred multi-protocol surfaces separately if only one protocol was ever graded elsewhere.

## Trust

Informative only · UHBS 4.2.2 · not an endorsement. See [READING-UHQS.md](../READING-UHQS.md) for how graded proofs should be read when artifacts exist.
