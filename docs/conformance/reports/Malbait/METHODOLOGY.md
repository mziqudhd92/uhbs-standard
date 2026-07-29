# Methodology: Malbait (skipped)

**UHBS:** 4.2.2 · **Status:** skipped in batch C — no SCORECARD artifacts.

Malbait is a Perl multi-process honeypot designed to bind many privileged ports via `-defaults` under root. Containerizing it safely while avoiding collisions with other UHBS labs (and without forking dozens of background listeners) was not completed within the batch window. Generic TCP grading on a single port was attempted conceptually but no reproducible image start was verified, so no UHQS was published.

## Evidence hierarchy

1. `full/SCORECARD.txt` when graded  
2. `full/report.json`  
3. This methodology (scope / blockers)  
4. Tutorial replication commands  

Skip hubs explain why no SCORECARD exists yet. See [READING-UHQS.md](../READING-UHQS.md). Informative only · UHBS 4.2.2 · isolate honeypot networks in real deployments.
