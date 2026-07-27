# ESPot methodology & trust notes

**Status:** Informative · evaluation proof  
**Related:** [TUTORIAL.md](TUTORIAL.md) · [full/run-meta.json](full/run-meta.json) · [quick/run-meta.json](quick/run-meta.json)

This page exists so reviewers can answer: *Who graded what, with which bits, under which limitations?*

---

## 1. What we claim (and do not claim)

| We claim | We do **not** claim |
| --- | --- |
| These artifacts were produced by UHBS-Lab v4.0.0 against a runnable ESPot container | That ESPot is “certified” or “UHBS-approved” |
| Full run used formal TPS (`timing_samples: 1000`, strict RFC) + source + SAST + telemetry | That Module D fully proved host containment via remote shell |
| Manifests include SHA-256 digests for key artifacts | That Docker Desktop networking equals a production air-gap |
| Grades follow normative UHQS / δ_C math in `uhqs_math.py` | That UHBS is an industry consortium standard |

UHBS is a **personal draft** framework. Product names appear only under `docs/conformance/` as proof labels.

---

## 2. Software under test (SUT)

| Field | Value |
| --- | --- |
| Project | [mycert/ESPot](https://github.com/mycert/ESPot) |
| Description | Elasticsearch honeypot (Node/Express) for CVE-2014-3120 |
| Git commit (lab clone) | `0b126a7783da69d543239606df59211c5d21f1db` |
| Runtime | Docker image `espot:lab` based on `node:10-buster-slim` |
| Image id | `sha256:7186a31a5ce7e9b806e17ad08164e13bd6c2fd6f3dd8bdeb8286da6476e1f869` |
| Listen | TCP `9200` / HTTP |
| Compatibility shim | SQLite logger **disabled** (native `sqlite3@2` fails on modern Node) |

---

## 3. Grader (UHBS)

| Field | Full run | Quick run |
| --- | --- | --- |
| Package | `uhbs` 4.0.0 | same |
| Docker image | `uhbs:4.0.0-full` | `uhbs:4.0.0` |
| Image id | see `full/run-meta.json` | see `quick/run-meta.json` |
| UHBS git commit | `9c6e9cf730cb7099699ce4479997881034cf2544` | same tree |
| TPS | [`labs/espot/web_api_full.yaml`](../../labs/espot/web_api_full.yaml) | builtin `web_api` |
| Inventory | [`labs/espot/inventory.yaml`](../../labs/espot/inventory.yaml) | CLI flags only |

Normative math: `src/uhbs_core/uhqs_math.py` (CLI wraps the same formulas).

---

## 4. Lab topology

```text
┌─────────────────────┐     Docker network uhbs-lab      ┌──────────────────────┐
│  uhbs:4.0.0[-full]  │ ──────────────────────────────── │  espot-lab :9200     │
│  Modules A–F        │   DNS: espot-lab                 │  Express ES decoy    │
│  mounts:            │                                  │                      │
│   /honeypot (ro)    │ ←── ESPot source tree            │  logs → copied out   │
│   /telemetry (ro)   │ ←── access.log + gateway canary  │  for full/ Module C  │
└─────────────────────┘                                  └──────────────────────┘
```

Host OS for the published runs: macOS (Docker Desktop), Linux containers (`linux/arm64`).

---

## 5. What each module measured

### Module A — Protocol & RFC fidelity

- Plugin: `http`  
- RFC suite: RFC 9110 / 9112 (`rfc_probes.probe_http_rfc9110`)  
- Full: **1000** connect-latency samples (`timing_samples`)  
- Quick: shortened via `UHBS_QUICK=1`  
- Key fail: unknown version `HTTP/9.9` answered with **200** (want 400/505/close)

### Module B — Behavioral realism

- Consistent GET responses; binary fuzz survival

### Module C — Telemetry

- Full: `telemetry_dir=/telemetry` with Express `access.log`  
- No STIX 2.1 / OTel / ECS documents → schema checks fail; score **capped at 55** when schema evidence is absent  
- Quick: no telemetry dir → C1 largely skipped (headline can read 100 — **not** claim-grade)

### Module D — Safety / containment (Safety Gate)

- ESPot is an **HTTP** decoy. Inventory is HTTP-only (`ports.http: 9200`) with **no**
  `ports.ssh`, so Module D does **not** open a shell session against `:9200`.
- Full: airgap attestation + clean `UHBS_EGRESS_GATEWAY_LOG` → C=90 (still **&lt; 95**, δ_C=0.81)  
- Quick: airgap only → C=75, δ_C=0.5625  
- Clearing the gate on non-shell decoys needs stronger gateway evidence (or an
  explicit side-channel SSH admin port if you intentionally expose one for lab exec)

### Module E — Scale

- Full: `--concurrency 25 --requests 200`  
- Quick: harness shortens under `UHBS_QUICK`

### Module F — Static / source

- `source_root=/honeypot`  
- Full: bandit + semgrep (2 error/critical → SAST gate caps F at 70); reports in `full/static/`  
- Quick: `--skip-sast-tools`

---

## 6. Integrity

Each mode directory includes `MANIFEST.json` with SHA-256 digests. Recompute:

```bash
python - <<'PY'
import hashlib, json
from pathlib import Path
for mode in ("quick", "full"):
    root = Path(f"docs/conformance/reports/espot/{mode}")
    man = json.loads((root / "MANIFEST.json").read_text())
    print("==", mode, "==")
    for art in man["artifacts"]:
        p = root / art["path"]
        h = hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
        print(("OK" if h == art["sha256"] else "FAIL"), art["path"])
PY
```

Validate the sanitized full fixture:

```bash
uhbs validate-scorecard docs/conformance/fixtures/espot-web-api.scorecard.json --strict
```

---

## 7. Known limitations (please read)

1. **Compatibility shim** — ESPot’s original `sqlite3` logger is disabled to boot on Node 10; behavior may differ from a 2014-era install.  
2. **Air-gap is attested** — `UHBS_AIRGAP_ATTESTED=1` is operator assertion inside Docker Desktop, not a Faraday cage.  
3. **HTTP-only containment** — Module D cannot exec inside ESPot; grades must not be read as “proven unbreakable jail.”  
4. **Telemetry format** — classic access logs ≠ detection-pipeline quality.  
5. **No gold baseline host** — Module A KS compare vs native Elasticsearch was skipped (`gold_baseline_host` unset).  
6. **Trivy** — not present in the published full image build used here; FS/image CVE scan skipped.  
7. **Non-endorsement** — naming ESPot does not make it a UHBS requirement.

---

## 8. Independent replication

Follow [TUTORIAL.md](TUTORIAL.md). If your UHQS differs, check: image digests, TPS path, `UHBS_QUICK`, telemetry mount, SAST image (`uhbs:4.0.0` vs `uhbs:4.0.0-full`), and UHBS git commit. File discrepancies with the reproduced `report.json` attached.
