# HoneyPy

**Status:** Surveyed · **skipped** (lab build/runtime)  
**Upstream:** [https://github.com/foospidy/HoneyPy](https://github.com/foospidy/HoneyPy) · GitHub last push `2024-03-21`

## Skip reason

HoneyPy targets Python 2.7 with legacy dependencies (Twisted, old autopep8 pins). A minimal `Dockerfile.lab` could not resolve pip constraints on `python:2.7-slim` within the batch window, and the project is explicitly unmaintained (upstream recommends honeydb-agent). HTTP plugin grading was deferred until a pinned dependency lockfile or community image exists.

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
