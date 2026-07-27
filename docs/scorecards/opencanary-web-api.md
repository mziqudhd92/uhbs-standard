# Scorecard: Web-API / HTTP decoy (OpenCanary proof)

**Status:** Informative · evaluation proof (not an endorsement)  
**Proof label:** [thinkst/opencanary](https://github.com/thinkst/opencanary) · report: [`../conformance/reports/opencanary/http/`](../conformance/reports/opencanary/http/index.md)

| Field | Value |
| --- | --- |
| Target | Web-API / HTTP decoy (multi-protocol canary; HTTP graded) |
| Class | Web-API |
| Protocol | HTTP `:80` |
| Evaluated | 2026-07-27 (full Docker lab) |
| Spec | UHBS 4.0.0 |

## Results

| Metric | Value |
| --- | --- |
| **Full UHQS** | **50.12** · Grade **D** |
| Quick UHQS | 41.30 / F |
| Hub | [OpenCanary multi-protocol](../conformance/reports/opencanary/index.md) |

## Artifacts

- Fixture: [`../conformance/fixtures/opencanary-web-api.scorecard.json`](../conformance/fixtures/opencanary-web-api.scorecard.json)
- Full scorecard: [`../conformance/reports/opencanary/http/full/SCORECARD.txt`](../conformance/reports/opencanary/http/full/SCORECARD.txt)
- Quick scorecard: [`../conformance/reports/opencanary/http/quick/SCORECARD.txt`](../conformance/reports/opencanary/http/quick/SCORECARD.txt)
- Tutorial: [`../conformance/reports/opencanary/TUTORIAL.md`](../conformance/reports/opencanary/TUTORIAL.md)

```bash
uhbs validate-scorecard docs/conformance/fixtures/opencanary-web-api.scorecard.json --strict
```
