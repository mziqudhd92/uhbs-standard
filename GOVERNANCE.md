# UHBS Project Notes (not institutional governance)

> **Honesty notice.** UHBS is a **personal open-source project** and a **draft
> evaluation framework**. It is **not** a standards body, consortium, or
> multi-party committee. There is no Steering Committee and no independent
> adopter roster today.
>
> Aspirations for multi-steward governance, a neutral GitHub organization, and
> independent academic/enterprise adopters live in [ROADMAP.md](ROADMAP.md)
> (Phase 6+). Do not read this file as evidence that those exist yet.

## 1. What this project is

| Claim | Reality today |
| --- | --- |
| Evaluation **framework** (spec + schemas + harness + fixtures) | Yes — Draft / Experimental |
| Vendor-neutral class/protocol methodology | Intentional design goal |
| Industry / academic **standard** with institutional backing | **No** — personal project |
| Multi-organization stewards / Steering Committee | **No** — see ROADMAP |
| Independent external adopters | **Not yet** — see ROADMAP |

## 2. Who decides (today)

One maintainer owns this repository and all merge/RFC decisions:

| Role | Person | Notes |
| --- | --- | --- |
| Author & maintainer | [@mziqudhd92](https://github.com/mziqudhd92) (Moran Zavdi) | Sole decision-maker |

See [MAINTAINERS.md](MAINTAINERS.md).

## 3. How changes are proposed

Contributions are welcome via issues and pull requests ([CONTRIBUTING.md](CONTRIBUTING.md)).

For material changes to scoring, modules, or TPS semantics, open a proposal under
`docs/rfcs/` so the rationale is public. **Acceptance is by the maintainer** —
not by a committee. Public comment is encouraged; there is no formal 14-day
committee vote because no committee exists.

### When a written RFC is useful

- Changes to Modules A–F objectives or mandatory steps
- Changes to the UHQS formula or \(\delta_C\) Safety Gate
- New or altered profile weight tables
- New mandatory TPS fields
- License changes

### Minimal RFC shape

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

## 4. Design principles (project intent)

1. **Normative stability** — Breaking changes to scoring are rare and versioned.
2. **Transparency** — Prefer public issues/PRs/RFCs over private decisions.
3. **Safety primacy** — Do not weaken the Module D Safety Gate without a clear,
   public rationale and a version bump.
4. **Protocol neutrality** — Stay architecture-agnostic across IT, OT/ICS, Cloud, GenAI.
5. **Vendor neutrality** — Normative text and templates use **classes and
   protocols** only; product names only in conformance proof fixtures.

## 5. Releases & scorecards

- Releases are tagged (`v4.0.0`, …). Prefer signed tags when practical.
- Published scorecards should validate against the schemas and disclose date,
  target class, and Safety Gate outcome.
- Disputes about misleading public claims: open an issue with label
  `scorecard-dispute`. The maintainer responds as capacity allows.

## 6. Changing this document

Updates to this file are ordinary PRs. Larger structural changes (e.g., forming
a real multi-steward body) belong on the [ROADMAP](ROADMAP.md) first.
