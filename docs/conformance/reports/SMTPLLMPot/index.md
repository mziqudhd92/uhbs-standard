# SMTPLLMPot — skipped (LLM dependency)

**Status:** Informative · **not graded**  
**Upstream:** [https://github.com/referefref/SMTPLLMPot](https://github.com/referefref/SMTPLLMPot)

SMTPLLMPot is a proof-of-concept SMTP honeypot that uses **GPT-3.5 (OpenAI)** to craft SMTP dialog, fronted by `socat`. The README lists Python 3, the `openai` package, and socat as requirements; there is no non-LLM fallback path. This grading session had **no OpenAI or other LLM API keys**, so the pot cannot complete realistic SMTP exchanges for UHBS Module A/B dynamic probes.

Running the script without credentials would fail at initialization or return errors to clients, producing scores that measure missing API configuration rather than SMTP decoy fidelity. UHBS publishes this skip note instead of inventing UHQS. Re-queue with a sandbox API key, strict billing caps, and isolated egress if operators want a reproducible lab recipe comparable to [mailoney](../mailoney/smtp/index.md).

See [TUTORIAL.md](TUTORIAL.md) · [METHODOLOGY.md](METHODOLOGY.md).

## Trust

Informative UHBS 4.2.2 gap note — not an endorsement. [READING-UHQS.md](../READING-UHQS.md)
