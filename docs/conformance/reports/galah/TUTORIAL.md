# Tutorial: galah (not graded — LLM required)

**Upstream:** [0x4D31/galah](https://github.com/0x4D31/galah)

Galah cannot be graded in this lab without `--provider`, `--model`, and API credentials (or Ollama). Do **not** run without usage limits on cloud LLM accounts.

When re-attempting:

```bash
git clone --depth 1 https://github.com/0x4D31/galah.git .local/labs/galah
cd .local/labs/galah && go build -o bin/galah ./cmd/galah
export LLM_PROVIDER=openai LLM_MODEL=gpt-4o-mini LLM_API_KEY=...
./bin/galah -p openai -m gpt-4o-mini -i 127.0.0.1:17081
```

Then add inventory + `web_api_http` TPS and run `uhbs-lab` as for HellPot HTTP labs.

No UHQS numbers are published until a full artifact tree exists.

## What this skip means for analysts

This tutorial cannot reproduce a UHBS UHQS grade for this product in the current lab environment. The product hub explains the blocker. Do **not** invent scores. When the blocker is cleared (API keys, backend dependency, or buildable image), re-queue with the same proof pattern as graded labs: `SCORECARD.txt`, `report.json`, protocol hub with verbatim modules, and CTI/blue-team reading via [READING-UHQS.md](../READING-UHQS.md).

## Trust limits

UHBS 4.2.2 evaluation notes are informative only — not certifications or endorsements. Product names appear only under conformance as survey/evaluation evidence.
