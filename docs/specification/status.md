# Status of This Document

**Status:** Beta / Experimental  
**Specification version:** 4.2.0  
**Keywords:** The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**,
**SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** in this
document are to be interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119)
and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174) when, and only when, they
appear in all capitals, as shown here.

## Normative vs Informative

| Kind | Meaning |
| --- | --- |
| **Normative** | Requirements that define UHBS conformance |
| **Informative** | Guidance, examples, motivation — not required for conformance |

## Conformance levels

### UHBS-Core (REQUIRED for claiming schema conformance)

An implementation claiming **UHBS-Core** conformance **MUST**:

1. Accept a TPS `profile.yaml` validating against `schemas/profile.schema.json`
2. Emit a scorecard validating against `schemas/scorecard.schema.json`
3. Compute UHQS using the normative formula and Safety Gate δ_C
4. Apply profile-class weights that match § Profile-Adaptive Weight Distributions
5. Pass public conformance fixtures under `docs/conformance/fixtures/`

### UHBS-Lab (RECOMMENDED for production evaluations)

An implementation claiming **UHBS-Lab** conformance **MUST** satisfy UHBS-Core and **MUST**:

1. Execute Modules A–F (or document SKIPPED steps with justification)
2. Emit an evidence pack validating against `schemas/evidence-pack.schema.json`
3. Attest sandbox / air-gap preflight for Module D evaluations
4. Include step-level check results with digests for official/registry scorecards

The reference harness that implements UHBS-Lab is described in
[reference-implementation.md](../reference-implementation.md).

## Project posture

UHBS is a **personal open-source beta framework**. It is **not** a standards
body, consortium, or multi-party committee. Claims about committees, neutral
org hosting, and independent adopters belong only on
[ROADMAP.md](../roadmap.md) (Phase 6) until they are real.

## Production Baseline Profile (RECOMMENDED)

Language such as "mandatory industry standard" **MUST NOT** be used for UHBS
today. Organizations **MAY** adopt the beta as an **internal** gate.

For that use, it is **RECOMMENDED** that:

- Active decoys **SHOULD NOT** be deployed to production networks unless
  **UHQS > 80** and Module D Safety Gate passes (C ≥ 95 → δ_C = 1.0)
- Failure to meet that baseline **MAY** increase lateral-movement risk from
  compromised containment shells

This RECOMMENDED gate is called the **Production Baseline Profile**.
