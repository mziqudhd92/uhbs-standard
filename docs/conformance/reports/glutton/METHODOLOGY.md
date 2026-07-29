# Methodology: Glutton (skipped)

**UHBS:** 4.2.2 · **Status:** skipped in batch C — no SCORECARD artifacts.

Glutton’s supported deployment model relies on Linux host networking, `NET_ADMIN`, and iptables TPROXY to capture all ports. The upstream Dockerfile explicitly warns that bridge-mode Docker will not see external traffic. Building Spicy parsers and satisfying iptables inside a macOS Docker Desktop lab exceeds the batch time budget, so no single-protocol HTTP/SSH grade was published on `uhbs-lab`.

## Evidence hierarchy

1. `full/SCORECARD.txt` when graded  
2. `full/report.json`  
3. This methodology (scope / blockers)  
4. Tutorial replication commands  

Skip hubs explain why no SCORECARD exists yet. See [READING-UHQS.md](../READING-UHQS.md). Informative only · UHBS 4.2.2 · isolate honeypot networks in real deployments.
