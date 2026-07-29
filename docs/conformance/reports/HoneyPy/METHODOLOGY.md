# Methodology: HoneyPy (skipped)

**UHBS:** 4.2.2 · **Status:** skipped in batch C — no SCORECARD artifacts.

HoneyPy targets Python 2.7 with legacy dependencies (Twisted, old autopep8 pins). A minimal `Dockerfile.lab` could not resolve pip constraints on `python:2.7-slim` within the batch window, and the project is explicitly unmaintained (upstream recommends honeydb-agent). HTTP plugin grading was deferred until a pinned dependency lockfile or community image exists.

## Evidence hierarchy

1. `full/SCORECARD.txt` when graded  
2. `full/report.json`  
3. This methodology (scope / blockers)  
4. Tutorial replication commands  

Skip hubs explain why no SCORECARD exists yet. See [READING-UHQS.md](../READING-UHQS.md). Informative only · UHBS 4.2.2 · isolate honeypot networks in real deployments.
