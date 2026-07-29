# Glutton

**Status:** Surveyed · **skipped** (lab build/runtime)  
**Upstream:** [https://github.com/mushorg/glutton](https://github.com/mushorg/glutton) · GitHub last push `2026-05-29`

## Skip reason

Glutton’s supported deployment model relies on Linux host networking, `NET_ADMIN`, and iptables TPROXY to capture all ports. The upstream Dockerfile explicitly warns that bridge-mode Docker will not see external traffic. Building Spicy parsers and satisfying iptables inside a macOS Docker Desktop lab exceeds the batch time budget, so no single-protocol HTTP/SSH grade was published on `uhbs-lab`.

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
