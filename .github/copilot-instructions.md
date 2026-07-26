# Copilot / AI Contributor Instructions

You are assisting contributors to the **Universal Honeypot Benchmarking Standard (UHBS) v4.0** repository.

## Project context

- UHBS is a **protocol-agnostic quantitative benchmarking standard** for honeypots and deception technology.
- Normative scoring: \(\mathrm{UHQS} = \delta_C \cdot (w_A S_A + w_B S_B + w_C S_C + w_E S_E + w_F S_F)\).
- Safety Gate: \(\delta_C = 1\) if Module D \(C \ge 95\), else \((C/100)^2\).
- Machine-readable contracts live in `schemas/`. Docs are MkDocs Material under `docs/`.

## Rules for AI-assisted edits

1. **Do not invent normative requirements.** Prefer citing existing specification docs under `docs/specification/`.
2. **Never weaken the Safety Gate** without an explicit RFC and maintainer approval.
3. Keep schemas, CLI, docs, and example scorecards **consistent** when changing scoring logic.
4. **Remain vendor-neutral.** Refer to decoys by profile class and protocol (POSIX-Shell, ICS-SCADA, etc.). Do not use product or brand names in examples, scorecards, or docs.
5. Use Conventional Commits; remind authors to `git commit -s` (DCO).
6. **Do not** generate exploit payloads, malware, or attack scripts against live systems. Defensive tests and schema validation only.
7. Prefer Apache-2.0 compatible dependencies.
8. Python public APIs should be typed and tested (`tests/`).
9. When adding profile classes or weights, update: schema enums, docs weight tables, templates, and tests together.

## Useful commands

```bash
pip install -e ".[dev]"
pytest
uhbs validate-profile templates/profile.yaml
uhbs validate-scorecard docs/scorecards/examples/illustrative-posix-genai.scorecard.json
mkdocs serve
```
