# OpenCanary methodology & trust notes

**Status:** Informative · evaluation proof  
**Related:** [TUTORIAL.md](TUTORIAL.md) · [full/run-meta.json](full/run-meta.json) · [quick/run-meta.json](quick/run-meta.json)

---

## 1. Claims / non-claims

| We claim | We do **not** claim |
| --- | --- |
| Artifacts come from UHBS-Lab v4.0.0 against a live OpenCanary container HTTP `:80` | That OpenCanary is UHBS-certified |
| Full run used 1000-sample timing, source audit, SAST, and real log directory | That FTP / other canary services were graded in this report |
| Manifests include SHA-256 digests | That Docker Desktop equals a production air-gap |
| Grades follow normative UHQS / δ_C math | That UHBS is an industry consortium standard |

---

## 2. Software under test

| Field | Value |
| --- | --- |
| Project | [thinkst/opencanary](https://github.com/thinkst/opencanary) |
| Description | Multi-protocol network canary (Thinkst) |
| Git commit (source mount) | `bc231423aa40242cbd0bf34801f8788e23420dee` |
| Image | `thinkst/opencanary:latest` |
| Image id | `sha256:558c508742ebc768d979f545bf1889be9d7d58377bd0144058c7df713a88763f` |
| Graded listen | TCP **80** HTTP |
| Lab config | [`labs/opencanary/opencanary.conf`](../../labs/opencanary/opencanary.conf) (HTTP + FTP; SSH/HTTPS off) |

---

## 3. Grader

| Field | Full | Quick |
| --- | --- | --- |
| Image | `uhbs:4.0.0-full` | `uhbs:4.0.0` |
| TPS | [`labs/opencanary/web_api_http_full.yaml`](../../labs/opencanary/web_api_http_full.yaml) | [`labs/opencanary/web_api_http_quick.yaml`](../../labs/opencanary/web_api_http_quick.yaml) |
| Inventory | [`labs/opencanary/inventory.yaml`](../../labs/opencanary/inventory.yaml) | same inventory + quick TPS |
| Protocol plugin | **http** | same |
| Profile class | `Web-API` | same |
| Module E | concurrency **25**, requests **200** | `UHBS_QUICK` caps |

---

## 4. Topology

```text
┌──────────────────────┐   network uhbs-lab    ┌──────────────────────────┐
│ uhbs:4.0.0[-full]    │ ───────────────────── │ opencanary-lab           │
│ mounts /honeypot     │ ← source tree         │ HTTP :80 (graded)        │
│ mounts /telemetry    │ ← opencanary.log      │ FTP :21 (not graded)     │
└──────────────────────┘                       └──────────────────────────┘
```

Host OS for the published runs: macOS (Docker Desktop), Linux containers.

---

## 5. Module notes (full)

| Module | What ran | Outcome driver |
| --- | --- | --- |
| A | HTTP RFC 9110/9112 + 1000× timing | Framing / invalid-method partial → low fidelity |
| B | Consistent GET + binary fuzz | Survived blast |
| C | `/telemetry` with `opencanary.log` | JSON lines → schema-capped **55** |
| D | No `ports.ssh` → shell probes skipped; airgap + gateway | **C=90**, **δ_C=0.81** |
| E | 25×200 HTTP load | P95 ≈ 7.5 ms |
| F | bandit + semgrep on source | SAST gate → F capped at **70** |

---

## 6. Integrity

```bash
python - <<'PY'
import hashlib, json
from pathlib import Path
for mode in ("quick", "full"):
    root = Path(f"docs/conformance/reports/opencanary/{mode}")
    man = json.loads((root / "MANIFEST.json").read_text())
    print("==", mode, "==")
    for art in man["artifacts"]:
        p = root / art["path"]
        h = hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
        print(("OK" if h == art["sha256"] else "FAIL"), art["path"])
PY

uhbs validate-scorecard docs/conformance/fixtures/opencanary-web-api.scorecard.json --strict
```

---

## 7. Limitations

1. **HTTP-only grade** — FTP (and other canaries) not scored in this report.  
2. **No SSH exec surface** — Module D cannot run shell egress/LPE probes; gate stays below 95 with airgap+gateway.  
3. **Air-gap attested** — `UHBS_AIRGAP_ATTESTED=1` inside Docker Desktop.  
4. **Telemetry format** — OpenCanary JSON log is not STIX/OTel/ECS.  
5. **Non-endorsement** — naming OpenCanary ≠ UHBS requirement.

---

## 8. Replication

Follow [TUTORIAL.md](TUTORIAL.md). Compare image digests and `run-meta.json` if UHQS diverges.
