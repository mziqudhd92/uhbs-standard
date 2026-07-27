# Official Benchmark Scorecards

Auditors must publish results using the standard scorecard layout validated by [`schemas/scorecard.schema.json`](https://github.com/mziqudhd92/uhbs-standard/blob/main/schemas/scorecard.schema.json).

UHBS is **vendor-neutral**: decoy **classes** and **protocols** are the normative vocabulary. Named products appear only as **evaluation proof** (not requirements or endorsements). The three scorecards below are sanitized fixtures from live Docker lab runs; full artifacts and tutorials live under [Conformance lab reports](../conformance/reports/index.md).

## Examples

Published **full** UHBS-Lab scorecards (evaluated 2026-07-27):

| Scorecard | Class / protocol | UHQS | Grade | Fixture |
| --- | --- | ---: | --- | --- |
| [Web-API / HTTP decoy (ESPot proof)](espot-web-api.md) | Web-API · HTTP `:9200` | **49.82** | F | [`espot-web-api.scorecard.json`](../conformance/fixtures/espot-web-api.scorecard.json) |
| [Low-Interaction / PJL decoy (miniprint proof)](miniprint-low-interaction.md) | Low-Interaction · PJL `:9100` | **47.77** | F | [`miniprint-low-interaction.scorecard.json`](../conformance/fixtures/miniprint-low-interaction.scorecard.json) |
| [ICS-SCADA / Modbus decoy (Conpot proof)](conpot-ics-scada.md) | ICS-SCADA · Modbus `:5020` | **55.51** | D | [`conpot-ics-scada.scorecard.json`](../conformance/fixtures/conpot-ics-scada.scorecard.json) |
| [Low-Interaction / SSH decoy (Cowrie proof)](cowrie-ssh.md) | Low-Interaction · SSH `:2222` | **48.70** | F | [`cowrie-low-interaction.scorecard.json`](../conformance/fixtures/cowrie-low-interaction.scorecard.json) |
| [Low-Interaction / SSH tarpit (Endlessh proof)](endlessh-ssh-tarpit.md) | Low-Interaction · `ssh_tarpit` `:2222` | **51.90** | D | [`endlessh-low-interaction.scorecard.json`](../conformance/fixtures/endlessh-low-interaction.scorecard.json) |
| [Web-API / HTTP decoy (OpenCanary proof)](opencanary-web-api.md) | Web-API · HTTP `:80` | **50.12** | D | [`opencanary-web-api.scorecard.json`](../conformance/fixtures/opencanary-web-api.scorecard.json) |

Each page links to the matching report hub (`quick/` + `full/` scorecards, `report.json`, methodology, tutorial).

### Synthetic layout sample (not a lab run)

- [Illustrative POSIX-Shell / GenAI-Augmented Decoy](illustrative-posix-genai.md) — vendor-neutral **layout** sample only (evaluated 2026-07-26)

## Badge Snippets

After an official evaluation, maintainers can embed:

```markdown
![UHBS v4.0 Grade A](https://img.shields.io/badge/UHBS%20v4.0-Grade%20A-brightgreen)
![UHBS v4.0 Grade B](https://img.shields.io/badge/UHBS%20v4.0-Grade%20B-yellowgreen)
![UHBS v4.0 Grade C](https://img.shields.io/badge/UHBS%20v4.0-Grade%20C-yellow)
![UHBS v4.0 Grade D](https://img.shields.io/badge/UHBS%20v4.0-Grade%20D-orange)
![UHBS v4.0 Grade F](https://img.shields.io/badge/UHBS%20v4.0-Grade%20F-red)
```

## Submitting a Scorecard

1. Complete a TPS `profile.yaml`
2. Run the five-phase audit
3. Emit a scorecard conforming to the schema
4. Open a PR or issue using the **Profile / Scorecard Submission** template

Validate a published fixture locally:

```bash
uhbs validate-scorecard docs/conformance/fixtures/espot-web-api.scorecard.json --strict
uhbs validate-scorecard docs/conformance/fixtures/miniprint-low-interaction.scorecard.json --strict
uhbs validate-scorecard docs/conformance/fixtures/conpot-ics-scada.scorecard.json --strict
uhbs validate-scorecard docs/conformance/fixtures/cowrie-low-interaction.scorecard.json --strict
uhbs validate-scorecard docs/conformance/fixtures/endlessh-low-interaction.scorecard.json --strict
uhbs validate-scorecard docs/conformance/fixtures/opencanary-web-api.scorecard.json --strict
```
