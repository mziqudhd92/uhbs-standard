# ssh-honeypot (droberson)

**Status:** Surveyed · **skipped** (lab build failed quickly)  
**Upstream:** [https://github.com/droberson/ssh-honeypot](https://github.com/droberson/ssh-honeypot) · GitHub last push `2024-10-29`  
**Attempted runtime:** `docker/Dockerfile` (experimental Docker support)

## Skip reason

Docker image build fails immediately: stage-2 base image `nlss/base-alpine:3.12` is unavailable (`pull access denied` / repository does not exist on Docker Hub). Upstream documents Docker as experimental; no alternate published image was used.

No UHBS quick/full SSH grade was published for this target.

> Named product is evaluation proof only — not a UHBS endorsement.
