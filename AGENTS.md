# Agent guide (UHBS)

Guidance for coding assistants and automated agents working in this repository.

## Project facts (do not invent)

- **UHBS** = open-source **beta-status** evaluation framework for honeypots / deception tech.
- **Not** a consortium, Steering Committee, or adopted industry/academic standard.
- Spec / package version: **4.4.4** · License: **Apache-2.0**
- Maintainer: see `MAINTAINERS.md` (single author today).
- Docs site: https://uhbs.github.io/uhbs-standard/ (landing) · https://uhbs.github.io/uhbs-standard/mkdocs/ (MkDocs)

## Where truth lives

| Concern | Source of truth |
| --- | --- |
| UHQS / δ_C / grades / weights | `src/uhbs_core/uhqs_math.py` (CLI + MCP wrap it via `uhbs_cli.scoring`) |
| Spec prose | `docs/specification/` |
| Schemas | `schemas/*.schema.json` |
| MCP tools for AI hosts | `src/uhbs_mcp/` · docs `docs/tooling/mcp.md` · `server.json` |
| AEP offline analysis | `src/uhbs_cli/aep.py` · docs `docs/advanced-evidence/` |
| AEP SLM (alpha, opt-in) | `src/uhbs_cli/aep_slm.py` · docs `docs/advanced-evidence/slm-alpha.md` (off until config edit; do **not** expose via MCP) |
| Maturity / future governance | `ROADMAP.md` only (do not claim Phase 6 done) |
| Vendor-neutrality | Classes/protocols in docs; product names only under `docs/conformance/` |

## Safe edit rules

1. Do **not** add `*@uhbs.dev` contacts or imply a project domain/email exists.
2. Do **not** invent stewards, committees, adopters, or “mandatory standard” language.
3. Keep CLI, MCP, and harness UHQS math identical — change `uhqs_math.py`, not a second copy.
4. Prefer absolute URLs when editing `llms.txt` / site discovery files.
5. Do **not** expose `uhbs lab` / network attack tools via MCP without explicit Safety Gate design.
6. Do **not** expose `uhbs aep slm` / model-calling paths via MCP; keep SLM opt-in via local config unlock only.
7. Run `pytest -q` and `ruff check` on touched Python before finishing.

## Install / verify

```bash
pip install -c constraints.txt -e ".[dev,lab,mcp]"
pytest -q
uhbs validate-scorecard docs/conformance/fixtures/cowrie-low-interaction.scorecard.json
# MCP (stdio) for AI hosts — see docs/tooling/mcp.md
python -c "from uhbs_mcp.server import list_profile_classes; print(list_profile_classes()['ok'])"
# optional Docker grading image:
docker build -t uhbs:4.4.4 .
docker run --rm -v "$PWD:/work" -w /work uhbs:4.4.4 validate-scorecard docs/conformance/fixtures/cowrie-low-interaction.scorecard.json
```

## Discovery files (absolute URLs preferred)

- Site root: https://uhbs.github.io/uhbs-standard/llms.txt ·
  https://uhbs.github.io/uhbs-standard/llms-full.txt ·
  https://uhbs.github.io/uhbs-standard/robots.txt ·
  https://uhbs.github.io/uhbs-standard/humans.txt ·
  https://uhbs.github.io/uhbs-standard/sitemap.xml ·
  https://uhbs.github.io/uhbs-standard/.well-known/security.txt ·
  https://uhbs.github.io/uhbs-standard/server.json
- MkDocs: https://uhbs.github.io/uhbs-standard/mkdocs/ ·
  https://uhbs.github.io/uhbs-standard/mkdocs/llms.txt ·
  https://uhbs.github.io/uhbs-standard/mkdocs/tooling/mcp/ ·
  https://uhbs.github.io/uhbs-standard/mkdocs/advanced-evidence/slm-alpha/
- Repo: `/llms.txt`, this `AGENTS.md`, `CITATION.cff`, `server.json`
