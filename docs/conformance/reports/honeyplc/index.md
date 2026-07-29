# HoneyPLC

**Status:** Surveyed · **skipped** (lab build/runtime)  
**Upstream:** [https://github.com/sefcom/honeyplc](https://github.com/sefcom/honeyplc) · GitHub last push `2023-05-16`

## Skip reason

HoneyPLC requires Honeyd, modified Snap7 binaries, snmpsim, lighttpd, and Python 2 tooling on the host. There is no maintained Dockerfile; installation steps assume Ubuntu 18.04 paths under `/usr/share/honeyd`. Standing up S7comm/SNMP/HTTP for UHBS ICS plugins exceeds the batch time budget, so the product remains a skip note only.

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
