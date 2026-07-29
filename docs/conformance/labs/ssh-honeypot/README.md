# droberson/ssh-honeypot lab

**Status:** Skipped for UHBS grading this round.  
**Upstream:** [droberson/ssh-honeypot](https://github.com/droberson/ssh-honeypot)

Upstream `docker/Dockerfile` depends on the missing base image `nlss/base-alpine:3.12`, so a reproducible lab container could not be built for quick/full UHQS runs. See the evaluation note at [`docs/conformance/reports/ssh-honeypot/index.md`](../reports/ssh-honeypot/index.md).

## Lab packaging note

This directory is reserved for TPS YAML and inventory helpers used by `uhbs-lab` once a buildable image exists. It is not a substitute for a published SCORECARD. Analysts should not invent UHQS numbers for skipped products. When a maintained Dockerfile or alternate base image is available, re-queue this lab, regenerate `SCORECARD.txt` / `report.json`, and publish under `docs/conformance/reports/` with the same CTI/blue-team reading pattern as other graded SSH decoys.

## Trust

Informative skip note only · UHBS 4.2.2 · not an endorsement. Isolate honeypot networks and wire your own telemetry shipping in real deployments.
