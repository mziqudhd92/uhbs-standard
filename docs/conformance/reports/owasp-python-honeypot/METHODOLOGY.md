# Methodology: OWASP Python-Honeypot UHBS lab

**UHBS:** 4.2.2 · Graded **HTTP** basic-auth weak-password module (Apache httpd).  
Lab image builds from upstream tree with `Dockerfile.lab`; credentials `admin` / `123456` per module defaults.

Quick **43.98 / F**, full **43.98 / F** · δ_C **0.5625** (operator air-gap attestation; C=75).

## Analyst trust notes

- **Role:** Minimal HTTP credential sink emulating the `http/basic_auth_weak_password` module without the full OWASP orchestrator.
- **Evidence:** `http/full/SCORECARD.txt`, `http/full/report.json`, this methodology, tutorial commands.
- **Not graded:** FTP/SSH modules, API server, ElasticSearch/Mongo orchestration paths.

## Environment & containment

Docker network `uhbs-lab`, bind `127.0.0.1:17080`. `UHBS_AIRGAP_ATTESTED=1` records operator attestation; isolate production networks in real deployments.

## Evidence hierarchy

1. `http/full/SCORECARD.txt`
2. `http/full/report.json`
3. This methodology
4. Tutorial replication commands

See [READING-UHQS.md](../READING-UHQS.md).
