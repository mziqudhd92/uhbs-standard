# OWASP Python-Honeypot

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/OWASP/Python-Honeypot](https://github.com/OWASP/Python-Honeypot) · GitHub last push (clone) `2026-07-29`  
**Runtime:** `owasp-python-honeypot:uhbs-lab` — Apache HTTP basic-auth weak-password module only

OWASP Honeypot orchestrates many Docker-backed protocol modules. This UHBS proof grades the **HTTP basic-auth weak password** surface in isolation (not the full multi-module orchestrator).

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [HTTP](http/index.md) | yes | **yes** | [43.98 / F](http/quick/README.md) | [43.98 / F](http/full/README.md) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.

## For CTI analysts

- Expect **401/basic-auth** engagement, not rich application pages. Module A reflects HTTP challenge fidelity; Module B reflects survival under fuzzing, not CMS exploit chains.
- Full OWASP orchestration can spawn FTP/SSH containers — that path was **not** graded here.

## For blue teams

- Treat as a lightweight web credential sink; ship Apache access logs and auth failures to SIEM (Module C is harness-only in this lab).
- Do not co-locate with production data; upstream README warns against shared networks.

## Trust & limitations

- UHBS 4.2.2 informative proof — prefer **full/** artifacts.
- Re-run via [TUTORIAL.md](TUTORIAL.md); see [METHODOLOGY.md](METHODOLOGY.md).
- [READING-UHQS.md](../READING-UHQS.md)
