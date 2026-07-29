# Methodology: telnet-iot-honeypot skip record

**UHBS:** 4.2.2 · **Result:** skipped (no UHQS)

## Skip reason

The IoT telnet honeypot is Python 2 with a Flask/SQLAlchemy backend and modern `argon2`/PEP517 dependencies that no longer install on maintained base images. Docker lab builds failed on setuptools constraints; skipping rather than patching upstream auth crypto in this batch.

## Evidence

No `SCORECARD.txt` or `report.json` was generated. This page exists so readers do not confuse absence of scores with a perfect or unknown grade.

## Analyst checklist

- Prefer published **full** SCORECARD artifacts when present; never invent UHQS for skip hubs.
- Confirm Safety Gate / δ_C before citing a composite score externally.
- Wire your own log shipping — Module C is harness visibility, not SIEM coverage.
- Re-run after upstream or TPS changes; keep class/protocol/target ids aligned with inventory.
- UHBS 4.2.2 remains an open-source beta-status evaluation framework (Apache-2.0) — informative proof only.
