# FaPro

**Status:** Surveyed · **skipped** (lab build/runtime)  
**Upstream:** [https://github.com/fofapro/fapro](https://github.com/fofapro/fapro) · GitHub last push `2025-01-02`

## Skip reason

FaPro ships as a prebuilt binary release (no application source in the public repo). In the UHBS lab image (`linux/amd64` under emulation), `fapro run -c …` consistently failed with “Can't find config file” even when JSON configs were present on disk (including `genConfig` output and bundled rule packs). The `-f` flag expects zip rule bundles, not JSON network configs. Without a reliable non-interactive start path on the `uhbs-lab` bridge network, SSH/HTTP grading was deferred rather than inventing UHQS numbers.

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
