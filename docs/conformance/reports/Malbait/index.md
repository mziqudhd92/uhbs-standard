# Malbait

**Status:** Surveyed · **skipped** (lab build/runtime)  
**Upstream:** [https://github.com/batchmcnulty/Malbait](https://github.com/batchmcnulty/Malbait) · GitHub last push `2024-04-27`

## Skip reason

Malbait is a Perl multi-process honeypot designed to bind many privileged ports via `-defaults` under root. Containerizing it safely while avoiding collisions with other UHBS labs (and without forking dozens of background listeners) was not completed within the batch window. Generic TCP grading on a single port was attempted conceptually but no reproducible image start was verified, so no UHQS was published.

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
