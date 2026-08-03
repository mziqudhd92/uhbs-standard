# Scorecard Registry Rules

**Status:** Informative beta policy (aspirational until Phase 6)

UHBS is a **beta-status** evaluation framework. There is **no** live public registry of
attested third-party scorecards yet. The checklist below describes how such a
registry *could* work once independent submitters and maintainers exist
([ROADMAP.md](roadmap.md) Phase 6).

## Goals

Prevent self-minted “Grade A” badges from undermining trust — if and when a
public registry is stood up.

## Kinds of scorecards (today)

| Kind | Where | Badge? |
| --- | --- | --- |
| **Published lab (evaluation proof)** | `docs/scorecards/` + `docs/conformance/reports/` — named products as proof only | Docs only |
| **Illustrative (synthetic)** | `docs/scorecards/illustrative-*` — layout sample, not a lab run | No |
| **Conformance fixture** | `docs/conformance/fixtures/` — math/proof only | Docs only |
| **Attested (registry)** | Not operated yet | N/A |

## Future attested submission checklist (roadmap)

1. TPS validates (`uhbs validate-profile --strict`)
2. Scorecard validates (`uhbs validate-scorecard --strict`)
3. Evidence pack validates (`uhbs validate-evidence`)
4. `MANIFEST.json` lists SHA-256 for scorecard, report, and evidence artifacts
5. Open PR or issue using the Profile / Scorecard Submission template
6. Declare evaluation environment (air-gap attestation for Module D)

## Disputes

Until a multi-maintainer process exists, open an issue with label
`scorecard-dispute`. The project maintainer responds as capacity allows.

## Badge snippet (do not use yet)

```markdown
![UHBS v4.4.5 attested](https://img.shields.io/badge/UHBS%20v4.4.5-attested-blue)
```

Do **not** publish grade or “attested” badges for unattested runs, and do not
imply a UHBS registry endorsement that does not exist.
