# Official Benchmark Scorecards

Auditors must publish results using the standard scorecard layout validated by [`schemas/scorecard.schema.json`](https://github.com/mziqudhd92/uhbs-standard/blob/main/schemas/scorecard.schema.json).

UHBS is **vendor-neutral**. Scorecard examples use generic decoy class labels (e.g., POSIX-Shell, ICS-SCADA) — never product or brand names.

## Examples

- [Illustrative POSIX-Shell / GenAI-Augmented Decoy](illustrative-posix-genai.md) — vendor-neutral reference scorecard (evaluated 2026-07-26)

## Badge Snippets

After an official evaluation, maintainers can embed:

```markdown
![UHBS v4.0 Grade A](https://img.shields.io/badge/UHBS%20v4.0-Grade%20A-brightgreen)
![UHBS v4.0 Grade B](https://img.shields.io/badge/UHBS%20v4.0-Grade%20B-yellowgreen)
![UHBS v4.0 Grade C](https://img.shields.io/badge/UHBS%20v4.0-Grade%20C-yellow)
```

## Submitting a Scorecard

1. Complete a TPS `profile.yaml`
2. Run the five-phase audit
3. Emit a scorecard conforming to the schema
4. Open a PR or issue using the **Profile / Scorecard Submission** template
