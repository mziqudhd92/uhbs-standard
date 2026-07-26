# UHBS Governance

This document describes how the Universal Honeypot Benchmarking Standard (UHBS) is stewarded so the framework retains institutional credibility for enterprise and academic adopters.

## 1. Principles

1. **Normative stability** — Breaking changes to scoring, modules, or TPS semantics are rare and versioned.
2. **Transparency** — Material decisions are recorded via RFCs and public GitHub discussion.
3. **Safety primacy** — The Module D Safety Gate (\(\delta_C\)) may not be weakened without an explicit RFC and steward approval.
4. **Protocol neutrality** — UHBS remains architecture-agnostic across IT, OT/ICS, Cloud, and GenAI decoys.

## 2. Roles

| Role | Responsibility |
| --- | --- |
| **Maintainers** | Day-to-day merge authority for docs, schemas, CLI, and CI |
| **Steering Committee** | Approves RFCs that change normative specification text |
| **Contributors** | Propose changes via issues, PRs, and RFCs |
| **Adopters** | Publish scorecards; may submit TPS profile classes for review |

Until a formal committee roster is published, repository CODEOWNERS act as interim stewards.

## 3. RFC Process (Request for Comments)

### When an RFC is required

- Changes to Modules A–F objectives or mandatory steps
- Changes to the UHQS formula or \(\delta_C\) Safety Gate
- New or altered profile weight tables
- New mandatory TPS fields
- License or patent-policy changes

### Lifecycle

1. **Draft** — Open an issue with label `rfc` and a markdown proposal under `docs/rfcs/` (or link a gist/PR).
2. **Discussion** — Minimum **14 days** of public comment for normative RFCs.
3. **Revision** — Author updates the proposal based on feedback.
4. **Decision** — Steering Committee (or interim maintainers) accepts, rejects, or defers.
5. **Implementation** — Merged PR updates specification docs, schemas, CLI, and `CITATION.cff` / version badges as needed.
6. **Versioning** — Normative accepted RFCs bump the specification version appropriately (`MAJOR.MINOR.PATCH`).

### RFC template (minimum)

```markdown
# RFC-NNNN: Title
- Status: Draft | Accepted | Rejected | Deferred
- Author(s):
- Spec impact: Modules / UHQS / TPS / Other
- Motivation
- Detailed design
- Compatibility & migration
- Alternatives considered
- Security & safety implications
```

## 4. Releases

- Specification releases are tagged (`v4.0.0`, `v4.1.0`, …).
- Prefer signed tags (`git tag -s`) for official specification cuts.
- GitHub Releases must summarize normative vs. non-normative changes.

## 5. Scorecard Integrity

Published official scorecards must:

- Reference a TPS `profile.yaml` conforming to `schemas/profile.schema.json`
- Emit results conforming to `schemas/scorecard.schema.json`
- Disclose evaluation date, target class, and Safety Gate outcome

Falsified or misleading scorecard claims may be disputed via a public issue labeled `scorecard-dispute`.

## 6. Amendments to Governance

Changes to this GOVERNANCE.md follow the RFC process with label `governance`.
