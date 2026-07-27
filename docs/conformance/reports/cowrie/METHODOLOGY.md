# Cowrie methodology & trust notes

**Status:** Informative · evaluation proof  
**Related:** [TUTORIAL.md](TUTORIAL.md) · [full/run-meta.json](full/run-meta.json) · [quick/run-meta.json](quick/run-meta.json)

---

## 1. Claims / non-claims

| We claim | We do **not** claim |
| --- | --- |
| Artifacts come from UHBS-Lab v4.0.0 against a live Cowrie container SSH `:2222` | That Cowrie is UHBS-certified |
| Full run used 1000-sample timing, source audit, SAST, and real log directory | That Telnet was graded in this report |
| Manifests include SHA-256 digests | That Docker Desktop equals a production air-gap |
| Grades follow normative UHQS / δ_C math | That UHBS is an industry consortium standard |
| Module D exercised SSH shell containment probes | That `root`/`root` is a universal Cowrie default |

---

## 2. Software under test

| Field | Value |
| --- | --- |
| Project | [cowrie/cowrie](https://github.com/cowrie/cowrie) |
| Description | Medium-interaction SSH/Telnet honeypot |
| Git commit (source mount) | `e7d1854a9489fa78845af01e445232f854414f87` |
| Image | `cowrie/cowrie:latest` |
| Image id | `sha256:a54c1a0f0d3f025dbbef83149c1b8521b811a193625287a97247c7fee2415909` |
| Graded listen | TCP **2222** SSH |
| Lab auth | `root` / `admin` |

---

## 3. Grader

| Field | Full | Quick |
| --- | --- | --- |
| Image | `uhbs:4.0.0-full` | `uhbs:4.0.0` |
| TPS | [`labs/cowrie/low_interaction_ssh_full.yaml`](../../labs/cowrie/low_interaction_ssh_full.yaml) | [`labs/cowrie/low_interaction_ssh_quick.yaml`](../../labs/cowrie/low_interaction_ssh_quick.yaml) |
| Inventory | [`labs/cowrie/inventory.yaml`](../../labs/cowrie/inventory.yaml) | same inventory + quick TPS |
| Protocol plugin | **ssh** | same |
| Profile class | `Low-Interaction` | same |
| Module E | concurrency **10**, requests **50** | `UHBS_QUICK` caps |

---

## 4. Topology

```text
┌──────────────────────┐   network uhbs-lab    ┌──────────────────────────┐
│ uhbs:4.0.0[-full]    │ ───────────────────── │ cowrie-lab               │
│ mounts /honeypot     │ ← source tree         │ SSH :2222 (graded)       │
│ mounts /telemetry    │ ← cowrie.json         │                          │
└──────────────────────┘                       └──────────────────────────┘
```

---

## 5. Module notes (full)

| Module | What ran | Outcome driver |
| --- | --- | --- |
| A | SSH RFC4253 + 1000× timing | Null ID accepted → low fidelity score |
| B | Cross-session marker + echo + fuzz | Echo OK; marker missing |
| C | `/telemetry` with `cowrie.json` | Text/JSON logs → schema-capped **55** |
| D | SSH shell egress / LPE probes | Blocked → **C=100**, **δ_C=1.0** |
| E | 10×50 SSH load | P95 ~3 s |
| F | bandit + semgrep on source | SAST gate → F capped at **70** |

---

## 6. Integrity

```bash
python - <<'PY'
import hashlib, json
from pathlib import Path
for mode in ("quick", "full"):
    root = Path(f"docs/conformance/reports/cowrie/{mode}")
    man = json.loads((root / "MANIFEST.json").read_text())
    print("==", mode, "==")
    for art in man["artifacts"]:
        p = root / art["path"]
        h = hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
        print(("OK" if h == art["sha256"] else "FAIL"), art["path"])
PY

uhbs validate-scorecard docs/conformance/fixtures/cowrie-low-interaction.scorecard.json --strict
```

---

## 7. Limitations

1. **SSH-only grade** — Telnet listener not scored in this report.  
2. **Auth** — image-specific `root`/`admin`; document in inventory.  
3. **Air-gap attested** — `UHBS_AIRGAP_ATTESTED=1` inside Docker Desktop.  
4. **Telemetry format** — Cowrie JSON log is not STIX/OTel/ECS.  
5. **Non-endorsement** — naming Cowrie ≠ UHBS requirement.

---

## 8. Replication

Follow [TUTORIAL.md](TUTORIAL.md). Compare image digests and `run-meta.json` if UHQS diverges.
