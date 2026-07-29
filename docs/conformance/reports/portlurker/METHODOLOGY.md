# Methodology: portlurker UHBS lab

**UHBS:** 4.2.2 · **generic** TCP on container port **8080**, host **19104**. Lab config `config.uhbs-lab.yml` enables a single TCP listener without banners to keep behavior deterministic for Module A.

## Evidence hierarchy

1. `full/SCORECARD.txt` when graded  
2. `full/report.json`  
3. This methodology (scope / blockers)  
4. Tutorial replication commands  

Skip hubs explain why no SCORECARD exists yet. See [READING-UHQS.md](../READING-UHQS.md). Informative only · UHBS 4.2.2 · isolate honeypot networks in real deployments.

## Analyst checklist

- Prefer published **full** SCORECARD artifacts when present; never invent UHQS for skip hubs.
- Confirm Safety Gate / δ_C before citing a composite score externally.
- Wire your own log shipping — Module C is harness visibility, not SIEM coverage.
- Re-run after upstream or TPS changes; keep class/protocol/target ids aligned with inventory.
- UHBS 4.2.2 remains a personal open-source beta evaluation framework (Apache-2.0) — informative proof only.
