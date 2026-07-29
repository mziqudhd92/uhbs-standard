# Methodology: FaPro (skipped)

**UHBS:** 4.2.2 · **Status:** skipped in batch C — no SCORECARD artifacts.

FaPro ships as a prebuilt binary release (no application source in the public repo). In the UHBS lab image (`linux/amd64` under emulation), `fapro run -c …` consistently failed with “Can't find config file” even when JSON configs were present on disk (including `genConfig` output and bundled rule packs). The `-f` flag expects zip rule bundles, not JSON network configs. Without a reliable non-interactive start path on the `uhbs-lab` bridge network, SSH/HTTP grading was deferred rather than inventing UHQS numbers.

## Evidence hierarchy

1. `full/SCORECARD.txt` when graded  
2. `full/report.json`  
3. This methodology (scope / blockers)  
4. Tutorial replication commands  

Skip hubs explain why no SCORECARD exists yet. See [READING-UHQS.md](../READING-UHQS.md). Informative only · UHBS 4.2.2 · isolate honeypot networks in real deployments.
