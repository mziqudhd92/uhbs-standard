# UHBS lab reports (evaluation proof)

**Status:** Informative  
**Purpose:** Published, reproducible UHBS-Lab outputs for named honeypots / decoys so the community can **audit**, **replicate**, and **compare** grades — not so UHBS can endorse products.

> UHBS is a personal open-source **beta** evaluation framework (v4.2.0).  
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
| [Endlessh (skeeto)](endlessh/index.md) | Low-Interaction | `ssh_tarpit` `:2222` | [46.55 / F](endlessh/quick/) | [54.07 / D](endlessh/full/) | [Step-by-step](endlessh/TUTORIAL.md) |
| [OpenCanary (thinkst)](opencanary/index.md) | multi | HTTP / FTP / SSH / Telnet / Redis / MySQL / RDP / SIP / SNMP / NTP / TFTP / VNC / Git / SMB | see hub | see hub | [Step-by-step](opencanary/TUTORIAL.md) |
| [Beelzebub](beelzebub/index.md) | multi | SSH / HTTP / Telnet / Redis / MCP | see hub | see hub | [Step-by-step](beelzebub/TUTORIAL.md) |
| [Trapster Community](trapster/index.md) | multi | SSH / HTTP / FTP / Telnet | see hub | see hub | [Step-by-step](trapster/TUTORIAL.md) |
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
