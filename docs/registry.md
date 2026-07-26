# Scorecard Registry Rules

**Status:** Normative (registry policy) / Draft until independent auditors exist

## Goals

Prevent self-minted “Grade A” badges from undermining trust.

## Official vs illustrative

| Kind | Requirements | Badge allowed? |
| --- | --- | --- |
| **Illustrative** | Schema-valid; labeled non-official | No |
| **Conformance fixture** | Checked into `docs/conformance/fixtures/` | Docs only |
| **Attested (registry)** | UHBS-Lab run + `MANIFEST.json` digests + evidence pack | Yes |

## Attested submission checklist

1. TPS validates (`uhbs validate-profile --strict`)
2. Scorecard validates (`uhbs validate-scorecard --strict`)
3. Evidence pack validates (`uhbs validate-evidence`)
4. `MANIFEST.json` lists SHA-256 for scorecard, report, and evidence artifacts
5. Open PR or issue using the Profile / Scorecard Submission template
6. Declare evaluation environment (air-gap attestation for Module D)

## Disputes

Label: `scorecard-dispute`. Stewards respond within 14 days. Outcomes: uphold,
amend, or retract registry entry.

## Badge snippet (attested only)

```markdown
![UHBS v4.0 attested](https://img.shields.io/badge/UHBS%20v4.0-attested-blue)
```

Do **not** publish grade badges for unattested runs.
