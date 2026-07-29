# UHBS lab reports (evaluation proof)

**Status:** Informative  
**Purpose:** Published, reproducible UHBS-Lab outputs for named honeypots / decoys so the community can **audit**, **replicate**, and **compare** grades — not so UHBS can endorse products.

> UHBS is a personal open-source **beta** evaluation framework (v4.2.2).  
> Named products appear **only** under `docs/conformance/` as evaluation proof.  
> A grade is not a certification, badge program, or consortium verdict.

## How to use this directory

1. Open a honeypot folder (for example [`espot/`](espot/index.md)).
2. Read the **tutorial** (exact commands we ran).
3. Compare **`quick/`** vs **`full/`** artifacts (scorecards, `report.json`, logs, SAST).
4. Recompute UHQS yourself with `uhbs validate-scorecard` / `uhbs score`.
5. Optionally re-run the same Docker lab against a live target.

## Index of published reports

| Honeypot (proof label) | Class | Protocol | Quick UHQS | Full UHQS | Tutorial |
| --- | --- | --- | --- | --- | --- |
| [ESPot (mycert)](espot/index.md) | Web-API | HTTP `:9200` | [49.34 / F](espot/quick/) | [63.33 / D](espot/full/) | [Step-by-step](espot/TUTORIAL.md) |
| [miniprint (sa7mon)](miniprint/index.md) | Low-Interaction | PJL/raw `:9100` | [41.83 / F](miniprint/quick/) | [50.43 / D](miniprint/full/) | [Step-by-step](miniprint/TUTORIAL.md) |
| [Conpot (mushorg)](conpot/index.md) | ICS-SCADA | Modbus `:5020` | [44.55 / F](conpot/quick/) | [55.4 / D](conpot/full/) | [Step-by-step](conpot/TUTORIAL.md) |
| [Cowrie](cowrie/index.md) | Low-Interaction | SSH `:2222` + Telnet `:2223` (SFTP via SSH) | see hub | see hub | [Step-by-step](cowrie/TUTORIAL.md) |
| [LLM Honeypot (Palisade)](llm-honeypot/index.md) | Low-Interaction | SSH `:2222` (Telnet off) | [67.94 / D](llm-honeypot/ssh/quick/) | [61.17 / D](llm-honeypot/ssh/full/) | [Step-by-step](llm-honeypot/TUTORIAL.md) |
| [HoneyAgents](honeyagents/index.md) | Low-Interaction | SSH `:2222` (Telnet mapped, not enabled) | [67.94 / D](honeyagents/ssh/quick/) | [65.24 / D](honeyagents/ssh/full/) | [Step-by-step](honeyagents/TUTORIAL.md) |
| [LLMPot (momalab)](llmpot/index.md) | multi | Modbus `:5020` / S7comm `:102` / HTTP `:8080` | see hub | see hub | [Step-by-step](llmpot/TUTORIAL.md) |
| [DataTrap (Thales)](datatrap/index.md) | multi | SSH / HTTP / MySQL / Redis / Telnet / PostgreSQL | see hub | see hub | [Step-by-step](datatrap/TUTORIAL.md) |
| [Endlessh (skeeto)](endlessh/index.md) | Low-Interaction | `ssh_tarpit` `:2222` | [46.55 / F](endlessh/quick/) | [54.07 / D](endlessh/full/) | [Step-by-step](endlessh/TUTORIAL.md) |
| [OpenCanary (thinkst)](opencanary/index.md) | multi | HTTP / FTP / SSH / Telnet / Redis / MySQL / RDP / SIP / SNMP / NTP / TFTP / VNC / Git / SMB | see hub | see hub | [Step-by-step](opencanary/TUTORIAL.md) |
| [Beelzebub](beelzebub/index.md) | multi | SSH / HTTP / Telnet / Redis / MCP | see hub | see hub | [Step-by-step](beelzebub/TUTORIAL.md) |
| [HoneyMCP](honeymcp/index.md) | Web-API | MCP `:8080` | [43.04 / F](honeymcp/mcp/quick/) | [42.93 / F](honeymcp/mcp/full/) | [Step-by-step](honeymcp/TUTORIAL.md) |
| [GenAIPot (ls1911)](genaipot/index.md) | Low-Interaction | SMTP `:25` + POP3 `:110` | see hub | see hub | [Step-by-step](genaipot/TUTORIAL.md) |
| [Elastichoney](elastichoney/index.md) | Web-API | HTTP ES `:9200` | [45.84 / F](elastichoney/http/quick/) | [45.73 / F](elastichoney/http/full/) | [Step-by-step](elastichoney/TUTORIAL.md) |
| [honeypot-ftp (alexbredo)](honeypot-ftp/index.md) | Low-Interaction | FTP `:21` | [42.71 / F](honeypot-ftp/ftp/quick/) | [42.6 / F](honeypot-ftp/ftp/full/) | [Step-by-step](honeypot-ftp/TUTORIAL.md) |
| [qeeqbox/honeypots](qeeqbox-honeypots/index.md) | multi | SSH/HTTP/FTP/Telnet/SMTP/POP3/MySQL/Postgres/Redis/VNC | see hub | see hub | [Step-by-step](qeeqbox-honeypots/TUTORIAL.md) |
| [SentryPeer](sentrypeer/index.md) | Low-Interaction | SIP `:5060` | [41.09 / F](sentrypeer/sip/quick/) | [40.98 / F](sentrypeer/sip/full/) | [Step-by-step](sentrypeer/TUTORIAL.md) |
| [wordpot](wordpot/index.md) | Web-API | HTTP `:8080` | [41.71 / F](wordpot/http/quick/) | [41.6 / F](wordpot/http/full/) | [Step-by-step](wordpot/TUTORIAL.md) |
| [MockSSH](mockssh/index.md) | Low-Interaction | SSH `:2222` | [59.2 / D](mockssh/ssh/quick/) | [59.0 / D](mockssh/ssh/full/) | [Step-by-step](mockssh/TUTORIAL.md) |
| [Heralding](heralding/index.md) | Low-Interaction | SSH `:22` + FTP `:21` | see hub | see hub | [Step-by-step](heralding/TUTORIAL.md) |
| [HoneyHTTPD](honeyhttpd/index.md) | Web-API | HTTP `:8080` | [45.84 / F](honeyhttpd/http/quick/) | [45.73 / F](honeyhttpd/http/full/) | [Step-by-step](honeyhttpd/TUTORIAL.md) |
| [SHIVA](shiva/index.md) | Low-Interaction | SMTP `:2525` | [45.07 / F](shiva/smtp/quick/) | [44.96 / F](shiva/smtp/full/) | [Step-by-step](shiva/TUTORIAL.md) |
| [Acra (skipped)](acra/index.md) | — | DB proxy / poison records (not a protocol honeypot) | — | — | [Note](acra/TUTORIAL.md) |
| [ssh-honeypot / droberson (skipped)](ssh-honeypot/index.md) | — | SSH (Docker base image unavailable) | — | — | [Note](ssh-honeypot/index.md) |
| [Ensnare (skipped)](ensnare/index.md) | — | Rails gem HTTP traps (not standalone) | — | — | [Note](ensnare/TUTORIAL.md) |
| [snare (skipped)](snare/index.md) | — | Needs Tanner + page clone | — | — | [Note](snare/TUTORIAL.md) |
| [Trapster Community](trapster/index.md) | multi | SSH / HTTP / FTP / Telnet | see hub | see hub | [Step-by-step](trapster/TUTORIAL.md) |
| [sshesame](sshesame/index.md) | Low-Interaction | SSH | [65.13 / D](sshesame/ssh/quick/) | [61.06 / D](sshesame/ssh/full/) | [Step-by-step](sshesame/TUTORIAL.md) |
| [ssh-auth-logger](ssh-auth-logger/index.md) | Low-Interaction | SSH | [44.38 / F](ssh-auth-logger/ssh/quick/) | [44.38 / F](ssh-auth-logger/ssh/full/) | [Step-by-step](ssh-auth-logger/TUTORIAL.md) |
| [ssh-honeypotd](ssh-honeypotd/index.md) | Low-Interaction | SSH | [44.38 / F](ssh-honeypotd/ssh/quick/) | [44.38 / F](ssh-honeypotd/ssh/full/) | [Step-by-step](ssh-honeypotd/TUTORIAL.md) |
| [HellPot](HellPot/index.md) | Web-API | HTTP | [43.98 / F](HellPot/http/quick/) | [43.87 / F](HellPot/http/full/) | [Step-by-step](HellPot/TUTORIAL.md) |
| [express-honeypot](express-honeypot/index.md) | Web-API | HTTP | [45.84 / F](express-honeypot/http/quick/) | [45.73 / F](express-honeypot/http/full/) | [Step-by-step](express-honeypot/TUTORIAL.md) |
| [mailoney](mailoney/index.md) | Low-Interaction | SMTP | [38.8 / F](mailoney/smtp/quick/) | [38.69 / F](mailoney/smtp/full/) | [Step-by-step](mailoney/TUTORIAL.md) |
| [pghoney](pghoney/index.md) | Low-Interaction | PostgreSQL | [43.72 / F](pghoney/postgres/quick/) | [43.61 / F](pghoney/postgres/full/) | [Step-by-step](pghoney/TUTORIAL.md) |
| [mysql-honeypotd](mysql-honeypotd/index.md) | Low-Interaction | MySQL | [40.35 / F](mysql-honeypotd/mysql/quick/) | [37.94 / F](mysql-honeypotd/mysql/full/) | [Step-by-step](mysql-honeypotd/TUTORIAL.md) |
| [Log4Pot](Log4Pot/index.md) | Web-API | HTTP | [41.71 / F](Log4Pot/http/quick/) | [38.0 / F](Log4Pot/http/full/) | [Step-by-step](Log4Pot/TUTORIAL.md) |
| [node-ftp-honeypot](node-ftp-honeypot/index.md) | Low-Interaction | FTP | [35.96 / F](node-ftp-honeypot/ftp/quick/) | [35.85 / F](node-ftp-honeypot/ftp/full/) | [Step-by-step](node-ftp-honeypot/TUTORIAL.md) |
| [SentryPeer](sentrypeer/index.md) | Low-Interaction | SIP | [43.38 / F](sentrypeer/sip/quick/) | [43.38 / F](sentrypeer/sip/full/) | [Step-by-step](sentrypeer/TUTORIAL.md) |
| [wordpot](wordpot/index.md) | Web-API | HTTP | [41.71 / F](wordpot/http/quick/) | [41.6 / F](wordpot/http/full/) | [Step-by-step](wordpot/TUTORIAL.md) |
| [MockSSH](mockssh/index.md) | Low-Interaction | SSH | [59.2 / F](mockssh/ssh/quick/) | [59.0 / F](mockssh/ssh/full/) | [Step-by-step](mockssh/TUTORIAL.md) |
| [Heralding](heralding/index.md) | Low-Interaction | SSH + FTP | see hub | see hub | [Step-by-step](heralding/TUTORIAL.md) |
| [HoneyHTTPD](honeyhttpd/index.md) | Web-API | HTTP | [45.84 / F](honeyhttpd/http/quick/) | [45.73 / F](honeyhttpd/http/full/) | [Step-by-step](honeyhttpd/TUTORIAL.md) |
| [SHIVA](shiva/index.md) | Low-Interaction | SMTP | [45.07 / F](shiva/smtp/quick/) | [44.96 / F](shiva/smtp/full/) | [Step-by-step](shiva/TUTORIAL.md) |
| [awesome-honeypots triage](../awesome-honeypots/TRIAGE.md) | — | grade_now / skip / deferred | — | — | [Deferred protocols](../awesome-honeypots/DEFERRED-PROTOCOLS.md) |
| [Dionaea](dionaea/index.md) | multi | FTP / HTTP / SMB | see hub | see hub | [Step-by-step](dionaea/TUTORIAL.md) |

## Directory layout (per honeypot)

```text
docs/conformance/reports/<honeypot>/
├── index.md           # Summary, trust notes, links
├── TUTORIAL.md        # Step-by-step replication
├── METHODOLOGY.md     # Environment, versions, limitations
├── quick/             # UHBS_QUICK=1 / lighter Module E / often SAST skipped
│   ├── SCORECARD.txt
│   ├── report.json
│   ├── MANIFEST.json
│   ├── uhbs-run.log
│   └── run-meta.json
└── full/              # Formal TPS (e.g. 1000-sample A3), telemetry, SAST
    ├── SCORECARD.txt
    ├── report.json
    ├── MANIFEST.json
    ├── uhbs-run.log
    ├── run-meta.json
    └── static/        # bandit / semgrep / … when enabled
```

## Quick vs full (read this before comparing grades)

| | **quick/** | **full/** |
| --- | --- | --- |
| Intent | Smoke / CI-speed demo | Most realistic grade the harness can produce in Docker |
| `UHBS_QUICK` | usually `1` | unset |
| Module A timing | shortened (≤50) | formal (often **1000** samples) |
| RFC probes | yes | yes (`strict_rfc_enforcement`) |
| Source / Module F | optional | required (`source-root`) |
| SAST | often `--skip-sast-tools` | bandit / semgrep (+ trivy when available) |
| Telemetry dir | often unset (optimistic C) | mounted real logs |
| Safety Gate | may be partial / attested | stricter evidence (gateway log, honest HTTP-only D) |

**Do not treat a quick UHQS as production-ready evaluation.** Prefer **full/** for claims; use **quick/** to show the pipeline works.

## Trust & verification checklist

For every published run we aim to ship:

- [x] Human scorecard (`SCORECARD.txt`)
- [x] Machine report (`report.json`) with per-check evidence
- [x] SHA-256 `MANIFEST.json` over artifacts
- [x] Console transcript (`uhbs-run.log`)
- [x] Provenance (`run-meta.json`: UHBS version, image digests, dates, flags)
- [x] Replication tutorial with exact commands
- [x] Explicit limitations (what was attested vs measured)

Verify locally:

```bash
# Integrity of the sanitized fixture (full ESPot)
uhbs validate-scorecard docs/conformance/fixtures/espot-web-api.scorecard.json --strict

# Spot-check manifest hashes for a published run
python - <<'PY'
import hashlib, json
from pathlib import Path
root = Path("docs/conformance/reports/espot/full")
man = json.loads((root / "MANIFEST.json").read_text())
for art in man["artifacts"]:
    p = root / art["path"]
    if not p.is_file():
        print("MISSING", art["path"]); continue
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    ok = h == art["sha256"]
    print(("OK" if ok else "MISMATCH"), art["path"])
PY
```

## Adding another honeypot report

1. Create `docs/conformance/reports/<id>/` with `quick/` and `full/`.
2. Capture artifacts via `uhbs lab … --out docs/conformance/reports/<id>/<mode>`.
3. Write `TUTORIAL.md` + `METHODOLOGY.md` + `run-meta.json`.
4. Link the row in **this** index and in [`../index.md`](../index.md).
5. Optionally add a sanitized fixture under [`../fixtures/`](../fixtures/).

## Related

- [Conformance overview](../index.md)
- [CLI & Docker](../../tooling/cli.md)
- [Reference implementation](../../reference-implementation.md)
- [Scoring formula](../../specification/scoring-formula.md)
- [Roadmap / maturity](../../roadmap.md)
