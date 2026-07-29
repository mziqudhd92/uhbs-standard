# ssh-honeypot (droberson)

**Status:** Surveyed · **skipped** (lab build failed quickly)  
**Upstream:** [https://github.com/droberson/ssh-honeypot](https://github.com/droberson/ssh-honeypot) · GitHub last push `2024-10-29`  
**Attempted runtime:** `docker/Dockerfile` (experimental Docker support)

## Skip reason

Docker image build fails immediately: stage-2 base image `nlss/base-alpine:3.12` is unavailable (`pull access denied` / repository does not exist on Docker Hub). Upstream documents Docker as experimental; no alternate published image was used.

No UHBS quick/full SSH grade was published for this target.

> Named product is evaluation proof only — not a UHBS endorsement.

## Why this page exists

UHBS publishes evaluation notes for products that were surveyed during conformance work even when a full UHQS grade is not available. Analysts should treat this as a **gap / skip note**, not a silent omission from the catalog.

## What analysts should do next

- If the blocker is missing UHBS protocol support, track it under deferred-protocol notes until a plugin exists.
- If the blocker is operational (backend dependency, missing base image, API key), re-queue when a reproducible lab recipe exists.
- Do not invent UHQS numbers for skipped products.

## Trust

Informative only · UHBS 4.2.2 · not an endorsement. See [READING-UHQS.md](../READING-UHQS.md) for how graded proofs should be read when artifacts exist.
