# Methodology: masscanned (skipped)

**UHBS:** 4.2.2 · **Status:** skipped in batch C — no SCORECARD artifacts.

masscanned implements a userland network stack and expects to bind a dedicated interface inside `NET_ADMIN` containers or network namespaces (see upstream README). It does not behave like a normal single-port TCP service on the `uhbs-lab` bridge, so UHBS HTTP/SSH plugins cannot reach it the way they do for Cowrie-style listeners. Grading was deferred pending a documented namespace lab recipe.

## Evidence hierarchy

1. `full/SCORECARD.txt` when graded  
2. `full/report.json`  
3. This methodology (scope / blockers)  
4. Tutorial replication commands  

Skip hubs explain why no SCORECARD exists yet. See [READING-UHQS.md](../READING-UHQS.md). Informative only · UHBS 4.2.2 · isolate honeypot networks in real deployments.
