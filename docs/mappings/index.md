# Mapping Index

Informative interoperability mappings for readers evaluating the UHBS beta framework against familiar security frameworks. These pages explain **how UHBS concepts relate** to external taxonomies — they are **not** certifications, compliance attestations, or claims that UHBS implements those standards.

Use these mappings when:

- A blue-team or GRC stakeholder asks how UHQS modules relate to NIST CSF / SP 800-53 control families
- A CTI analyst wants ATT&CK-oriented language for discussing decoy telemetry (without inventing ATT&CK coverage claims)
- An OT/ICS reader needs IEC 62443-oriented vocabulary for containment and safety-gate thinking around industrial decoys
- A deception engineer wants D3FEND **Deceive** labels for the *kind* of decoy graded, or Engage goals for *why* it was deployed

## Available mappings

- [MITRE ATT&CK](attack.md) — optional lens for discussing adversary techniques vs decoy signals
- [MITRE D3FEND](d3fend.md) — Decoy Environment / Decoy Object tags for graded surfaces
- [MITRE Engage](engage.md) — Expose / Affect / Elicit / Understand goals vs UHBS modules
- [NIST CSF / SP 800-53](nist.md) — informative crosswalk for governance readers
- [IEC 62443 (OT/ICS)](iec-62443.md) — OT-oriented reading notes for industrial honeypot evaluations
- [Related deception frameworks](related-frameworks.md) — evidence-graded comparison of 14 framework/model families vs UHBS

For controlled comparative experiments that stay outside UHQS, see the optional
[Advanced Evidence Profile (AEP)](../advanced-evidence/index.md).

## Scorecard `framework_refs` (optional)

Sanitized fixtures **MAY** include a display-only `framework_refs` object:

```json
"framework_refs": {
  "attack": ["T1595", "T1041"],
  "d3fend": ["D3-DNR", "D3-SHN"],
  "engage_goals": ["Expose", "Elicit"]
}
```

These tags do **not** affect UHQS, δ_C, or letter grade. See the
[scorecard schema](https://github.com/mziqudhd92/uhbs-standard/blob/main/schemas/scorecard.schema.json).

## Trust limits

Mappings are **informative**. They do not replace the verbatim SCORECARD / `report.json` proof for any graded product under `docs/conformance/`. Prefer absolute URLs on the published docs site when sharing externally. UHBS remains an open-source beta-status evaluation framework (Apache-2.0, v4.3.6) — not an adopted industry or academic standard.
