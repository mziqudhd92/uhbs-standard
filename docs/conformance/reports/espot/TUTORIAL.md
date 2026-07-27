# Tutorial: grade ESPot with UHBS (quick + full)

**Status:** Informative · evaluation proof  
**Audience:** Researchers and defenders who want to **reproduce** the published ESPot reports  
**Outputs live in:** [`quick/`](quick/) and [`full/`](full/) · trust notes: [METHODOLOGY.md](METHODOLOGY.md)

This is the exact workflow used to produce the artifacts under
`docs/conformance/reports/espot/`. Product name = proof label only.

---

## 0. Prerequisites

- Docker Engine or Docker Desktop  
- `git`, `curl`, Python 3.11+ (for local `uhbs validate-scorecard`)  
- ~2 GB disk for Node 10 + UHBS images  

```bash
git clone https://github.com/mziqudhd92/uhbs-standard.git
cd uhbs-standard

# Base grader (CLI + lab)
docker build -t uhbs:4.0.0 .

# Full grader (+ bandit / semgrep; trivy when download succeeds)
docker build -f Dockerfile.full -t uhbs:4.0.0-full .
```

Confirm:

```bash
docker run --rm uhbs:4.0.0 --version
docker run --rm uhbs:4.0.0-full lab --list-protocols
```

---

## 1. Clone ESPot

```bash
mkdir -p .local/labs
git clone https://github.com/mycert/ESPot.git .local/labs/ESPot
cd .local/labs/ESPot
git rev-parse HEAD   # record in your run-meta if publishing
```

---

## 2. Revive the honeypot (expect modern Node to fail)

ESPot targets Node ~0.10 / Express 3. On Node 20, `npm install` fails on
`sqlite3@2` (`primordials is not defined`). That friction is part of the story.

**Shim used for these reports:**

1. Disable SQLite logging in `config.js`.  
2. Run under **Node 10** in Docker.

`config.js`:

```js
module.exports = {
  default_response: 'default',
  logging: {
    sqlite: { enable: false, dbpath: __dirname + "/logs/attack.db" },
    http_push: { enable: false, url: "http://localhost/path/path?query=string" }
  },
  tz: 'GMT+0'
};
```

`Dockerfile` next to `app.js`:

```dockerfile
FROM node:10-buster-slim
WORKDIR /opt/espot
RUN npm install --production express@3.16.5 ejs@2.7.4 request@2.88.2 \
 && npm cache clean --force
COPY . .
EXPOSE 9200
CMD ["node", "app.js"]
```

Build & smoke-test:

```bash
docker build -t espot:lab .
docker network create uhbs-lab 2>/dev/null || true
docker rm -f espot-lab 2>/dev/null || true
docker run -d --name espot-lab --network uhbs-lab -p 9200:9200 espot:lab
docker logs espot-lab
# expect: Express server listening on port 9200

curl -sS http://127.0.0.1:9200/
# expect JSON with "tagline": "You Know, for Search"
```

Return to the UHBS repo root for the next steps:

```bash
cd /path/to/uhbs-standard
```

---

## 3. Quick run (smoke grade)

**Intent:** prove the pipeline works fast. **Not** claim-grade.

```bash
mkdir -p docs/conformance/reports/espot/quick

docker run --rm \
  --network uhbs-lab \
  -v "$PWD:/work" \
  -v "$PWD/.local/labs/ESPot:/honeypot:ro" \
  -w /work \
  -e UHBS_QUICK=1 \
  -e UHBS_AIRGAP_ATTESTED=1 \
  uhbs:4.0.0 \
  lab \
    --tps web_api \
    --protocol http \
    --class Web-API \
    --target espot-lab \
    --port 9200 \
    --source-root /honeypot \
    --phases profile,static,sandbox,dynamic,score \
    --modules A,B,C,D,E,F \
    --quick \
    --skip-sast-tools \
    --out /work/docs/conformance/reports/espot/quick \
    --environment "Quick Docker lab demo (UHBS_QUICK=1, SAST skipped)"
```

Published result for this tree: **UHQS 39.95 / Grade F** — see [`quick/SCORECARD.txt`](quick/SCORECARD.txt).

Why it still fails despite “HTTP 200 works”:

- Module A protocol fidelity remains weak.  
- Module D cannot clear the Safety Gate without stronger containment evidence.  
- δ_C = 0.5625 multiplies the weighted sum.

---

## 4. Seed telemetry for the full run

```bash
mkdir -p .local/labs/ESPot-telemetry

for i in $(seq 1 30); do
  curl -sS -o /dev/null "http://127.0.0.1:9200/"
  curl -sS -o /dev/null "http://127.0.0.1:9200/_search?q=uhbs$i"
  curl -sS -o /dev/null -X PUT "http://127.0.0.1:9200/idx/doc/$i" \
    -H 'Content-Type: application/json' -d "{\"probe\":$i}"
done

docker cp espot-lab:/opt/espot/logs/. .local/labs/ESPot-telemetry/
printf '%s\n' '# UHBS egress gateway canary — no HIT lines means clean' \
  > .local/labs/ESPot-telemetry/egress-gateway.log
```

Lab assets (already in-repo):

- [`../../labs/espot/web_api_full.yaml`](../../labs/espot/web_api_full.yaml) — 1000-sample TPS  
- [`../../labs/espot/inventory.yaml`](../../labs/espot/inventory.yaml) — HTTP-only inventory  

If your clone path differs from `.local/labs/ESPot`, edit `source_root` / mounts accordingly (inventory paths inside the container stay `/honeypot` and `/telemetry`).

---

## 5. Full run (claim-grade Docker lab)

**Intent:** deepest practical UHBS-Lab grade in this topology — RFC depth, source, SAST, telemetry, load.

```bash
mkdir -p docs/conformance/reports/espot/full

docker run --rm \
  --network uhbs-lab \
  -v "$PWD:/work" \
  -v "$PWD/.local/labs/ESPot:/honeypot:ro" \
  -v "$PWD/.local/labs/ESPot-telemetry:/telemetry:ro" \
  -w /work \
  -e UHBS_AIRGAP_ATTESTED=1 \
  -e UHBS_EGRESS_GATEWAY_LOG=/telemetry/egress-gateway.log \
  uhbs:4.0.0-full \
  lab \
    --inventory /work/docs/conformance/labs/espot/inventory.yaml \
    --target espot \
    --phases profile,static,sandbox,dynamic,score \
    --modules A,B,C,D,E,F \
    --concurrency 25 \
    --requests 200 \
    --out /work/docs/conformance/reports/espot/full \
    --environment "Detailed Docker lab: RFC9110 + 1000-sample A3 + SAST + telemetry"
```

Published result: **UHQS 49.82 / Grade F** — see [`full/SCORECARD.txt`](full/SCORECARD.txt).

After the run, add/update provenance:

```bash
# edit run-meta.json with your digests/commits, then refresh MANIFEST hashes
python - <<'PY'
import hashlib, json
from pathlib import Path
root = Path("docs/conformance/reports/espot/full")
# ensure run-meta.json exists, then:
arts = []
for name in ["REPORT.txt","SCORECARD.txt","report.json","uhbs-run.log","run-meta.json"]:
    p = root/name
    if p.is_file():
        arts.append({"path": name, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()})
for p in sorted((root/"static").glob("*.json")):
    arts.append({"path": f"static/{p.name}", "sha256": hashlib.sha256(p.read_bytes()).hexdigest()})
rep = json.loads((root/"report.json").read_text())
man = {"uhbs_version":"4.0.0","artifacts":arts,"extra":{
  "target": rep["target"]["name"], "uhqs": rep["uhqs"]["uhqs"], "grade": rep["uhqs"]["grade"]}}
(root/"MANIFEST.json").write_text(json.dumps(man, indent=2)+"\n")
print("wrote", root/"MANIFEST.json")
PY
```

---

## 6. Read and verify the artifacts

```bash
# Human cards
cat docs/conformance/reports/espot/quick/SCORECARD.txt
cat docs/conformance/reports/espot/full/SCORECARD.txt

# Machine evidence (per-check)
python -m json.tool docs/conformance/reports/espot/full/report.json | less

# SAST
ls docs/conformance/reports/espot/full/static/

# Fixture integrity (sanitized full scorecard)
uhbs validate-scorecard docs/conformance/fixtures/espot-web-api.scorecard.json --strict
```

### Flag cheat-sheet

| Flag / mount | Why it matters |
| --- | --- |
| `--network uhbs-lab` | Grader resolves `espot-lab` / inventory host |
| `--source-root` / `/honeypot` | Module F white-box |
| `/telemetry` + inventory `telemetry_dir` | Honest Module C |
| `UHBS_QUICK=1` / `--quick` | Shorter A3 + lighter E |
| `--skip-sast-tools` | Skip bandit/semgrep/trivy |
| `uhbs:4.0.0-full` | Installs SAST tools |
| `UHBS_AIRGAP_ATTESTED=1` | Phase-3 / D attestation (documented limitation) |
| `UHBS_EGRESS_GATEWAY_LOG` | Canary file for D1 gateway evidence |
| `--concurrency` / `--requests` | Module E depth |

---

## 7. Interpret the grades

| Observation | Meaning |
| --- | --- |
| HTTP root returns 200 + ES banner | Liveness ≠ UHBS quality |
| Module A = 20 | Decoy accepts illegal HTTP versions |
| Full C = 55 | Real logs lack STIX/OTel/ECS schema |
| D &lt; 95 | Safety Gate applies exponential δ_C |
| Full UHQS 49.82 / F | Below draft Production Baseline (UHQS &gt; 80 + gate) |
| Quick UHQS 39.95 / F | Even lower once δ_C is harsh and D is weak |

For trust-facing narrative, cite **full/** and [METHODOLOGY.md](METHODOLOGY.md).

---

## 8. Cleanup

```bash
docker rm -f espot-lab
docker network rm uhbs-lab
```

---

## 9. Publishing checklist (for new honeypots)

When you add another decoy under `docs/conformance/reports/<id>/`:

1. [ ] `quick/` and `full/` both populated  
2. [ ] `run-meta.json` with image digests + commits  
3. [ ] `MANIFEST.json` hashes refreshed  
4. [ ] `TUTORIAL.md` + `METHODOLOGY.md` written  
5. [ ] Row added to [`../index.md`](../index.md)  
6. [ ] Optional sanitized fixture under `docs/conformance/fixtures/`  
7. [ ] Explicit non-endorsement language  

Back to [ESPot report hub](index.md) · [all reports](../index.md).
