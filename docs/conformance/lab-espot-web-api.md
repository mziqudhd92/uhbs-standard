# Lab tutorial: ESPot (moved)

This tutorial moved into the published reports tree so quick + full artifacts
live next to the replication steps:

**→ [reports/espot/TUTORIAL.md](reports/espot/TUTORIAL.md)**  
**→ [reports/espot/](reports/espot/index.md)** (scorecards, `report.json`, methodology)  
**→ [reports/](reports/index.md)** (index of all honeypot reports)

Sanitized full fixture: [`fixtures/espot-web-api.scorecard.json`](fixtures/espot-web-api.scorecard.json)

## Analyst context

This page is the lab note for grading **ESPot** as a Web-API / HTTP surface under UHBS. Use it together with the published report hub, tutorial, and methodology under `docs/conformance/reports/espot/`. Prefer the **full** SCORECARD and `report.json` when citing UHQS. Treat product names as evaluation proof only — not endorsements. See [READING-UHQS.md](reports/READING-UHQS.md) for CTI and blue-team interpretation of modules A–F and the Safety Gate δ_C.

## Replication expectations

Run on an isolated Docker network with localhost binds, record air-gap attestation only when accurate, and do not expose lab attack tooling via MCP without an explicit Safety Gate design. Re-generate artifacts after TPS or upstream changes before updating published scorecards.
