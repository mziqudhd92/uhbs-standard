# UHBS Project Notes (not institutional governance)

> **Honesty notice.** UHBS is a **personal open-source project** and a **beta
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
| Evaluation **framework** (spec + schemas + harness + fixtures) | Yes — Beta / Experimental |
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
- Status: Beta | Accepted | Rejected | Deferred
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

- Releases are tagged (`v4.0.1`, …). Prefer signed tags when practical.
- Published scorecards should validate against the schemas and disclose date,
  target class, and Safety Gate outcome.
- Disputes about misleading public claims: open an issue with label
  `scorecard-dispute`. The maintainer responds as capacity allows.

## 6. Plugin maturity lifecycle

This describes **the maintainer's own review/merge criteria** for accepting a
protocol plugin into this repository's core (`src/uhbs_core/protocols/`) or
into `docs/conformance/` recognition. It is not a committee-approved policy —
there is no committee (see §1) — it is simply how the sole maintainer decides
what to merge, written down so it's predictable.

| Stage | Meaning | Bar to be here |
| --- | --- | --- |
| **Experimental** | Community-submitted, community-maintained | Registered via a `uhbs.plugins` [entry point](docs/plugin-authoring.md) (see `src/uhbs_core/protocols/registry.py`'s `load_external_plugins()`); loads without crashing the harness; nothing more is checked automatically. Lives in the plugin author's **own** package — it does not need to be merged into this repo at all. |
| **Standard** | Audited by the maintainer, RFC-compliant, has passing Golden Baseline coverage | Merged into `src/uhbs_core/protocols/` (or recognized in `docs/conformance/`) after: (1) an [RFC](docs/rfcs/README.md) if it changes Modules A–F objectives, UHQS, or TPS semantics; (2) manual maintainer code review; (3) a live test in `tests/test_plugin_baseline_live.py` that scores the plugin ≥90/100 against a genuine, non-honeypot reference implementation of the protocol (see [`docs/architecture/ci-baseline.md`](docs/architecture/ci-baseline.md) for the current, still-informational state of that CI job). |
| **Deprecated** | No longer recommended; kept for compatibility or removed on a version bump | Announced in `CHANGELOG.md`/release notes with a reason and, where possible, a replacement. Breaking removal follows the versioning rules in `VERSIONING.md`. |

**Honesty notes:**
- As of this writing, **all 17+ built-in plugins are `Standard` by inheritance**
  (they predate this lifecycle and are maintained in-tree), except that only
  two of them (`redis`, `smb`) currently have live Golden Baseline coverage —
  see [`docs/architecture/ci-baseline.md`](docs/architecture/ci-baseline.md)'s honest coverage table. This
  lifecycle description does not retroactively claim more baseline coverage
  exists than it does.
- There are currently **zero** real third-party (`Experimental`) plugins
  registered against this project. This section describes the intended
  process for when one shows up, not evidence that the ecosystem exists yet.

## 7. Supply-chain hygiene (pointer)

Concrete, current supply-chain steps (GitHub Actions pinning, `ruff`/`mypy`
scope, and what's still missing toward any SLSA level) are tracked in
[`docs/architecture/supply-chain.md`](docs/architecture/supply-chain.md) rather
than duplicated here.

## 8. Changing this document

Updates to this file are ordinary PRs. Larger structural changes (e.g., forming
a real multi-steward body) belong on the [ROADMAP](ROADMAP.md) first.
