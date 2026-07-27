# Agent guide (UHBS)

Guidance for coding assistants and automated agents working in this repository.

## Project facts (do not invent)

- **UHBS** = personal open-source **draft** evaluation framework for honeypots / deception tech.
- **Not** a consortium, Steering Committee, or adopted industry/academic standard.
- Spec / package version: **4.0.0** · License: **Apache-2.0**
- Maintainer: see `MAINTAINERS.md` (single author today).
- Docs site: https://mziqudhd92.github.io/uhbs-standard/

## Where truth lives

| Concern | Source of truth |
| --- | --- |
| UHQS / δ_C / grades / weights | `src/uhbs_core/uhqs_math.py` (CLI wraps it via `uhbs_cli.scoring`) |
| Spec prose | `docs/specification/` |
| Schemas | `schemas/*.schema.json` |
| Maturity / future governance | `ROADMAP.md` only (do not claim Phase 6 done) |
| Vendor-neutrality | Classes/protocols in docs; product names only under `docs/conformance/` |

## Safe edit rules

1. Do **not** add `*@uhbs.dev` contacts or imply a project domain/email exists.
2. Do **not** invent stewards, committees, adopters, or “mandatory standard” language.
3. Keep CLI and harness UHQS math identical — change `uhqs_math.py`, not a second copy.
4. Prefer absolute URLs when editing `llms.txt` / site discovery files.
5. Run `pytest -q` and `ruff check` on touched Python before finishing.

## Install / verify

```bash
pip install -c constraints.txt -e ".[dev,lab]"
pytest -q
uhbs validate-scorecard docs/conformance/fixtures/cowrie-low-interaction.scorecard.json
# optional Docker grading image:
docker build -t uhbs:4.0.0 .
docker run --rm -v "$PWD:/work" -w /work uhbs:4.0.0 validate-scorecard docs/conformance/fixtures/cowrie-low-interaction.scorecard.json
```

## Discovery files

- Site: `/llms.txt`, `/llms-full.txt`, `/robots.txt`, `/humans.txt`, `/sitemap.xml`
- Repo: `/llms.txt`, this `AGENTS.md`, `CITATION.cff`
