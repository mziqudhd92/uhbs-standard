# Tutorial: SMTPLLMPot (not graded — OpenAI required)

**Upstream:** [referefref/SMTPLLMPot](https://github.com/referefref/SMTPLLMPot)

Requires OpenAI credentials and socat. Not attempted in this batch.

```bash
git clone --depth 1 https://github.com/referefref/SMTPLLMPot.git .local/labs/SMTPLLMPot
# configure OPENAI_API_KEY, run socat + smtp LLM script per upstream
# then grade with mailoney-compatible smtp TPS + inventory on 127.0.0.1:17026
```

No published UHQS until artifacts are generated.

## What this skip means for analysts

This tutorial cannot reproduce a UHBS UHQS grade for this product in the current lab environment. The product hub explains the blocker. Do **not** invent scores. When the blocker is cleared (API keys, backend dependency, or buildable image), re-queue with the same proof pattern as graded labs: `SCORECARD.txt`, `report.json`, protocol hub with verbatim modules, and CTI/blue-team reading via [READING-UHQS.md](../READING-UHQS.md).

## Trust limits

UHBS 4.2.2 evaluation notes are informative only — not certifications or endorsements. Product names appear only under conformance as survey/evaluation evidence.
