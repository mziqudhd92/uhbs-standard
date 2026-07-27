# Endlessh methodology & trust notes

**Status:** Informative · evaluation proof  
**Related:** [TUTORIAL.md](TUTORIAL.md) · [full/run-meta.json](full/run-meta.json) · [quick/run-meta.json](quick/run-meta.json)

---

## 1. Claims / non-claims

| We claim | We do **not** claim |
| --- | --- |
| Artifacts come from a live Endlessh process on loopback `:2223` | That Endlessh is UHBS-certified |
| Quick run completed Modules A–F against the tarpit | That Endlessh is an interactive SSH honeypot |
| Full publication uses tarpit-safe timeouts | That unbounded Paramiko suites are meaningful here |
| Manifests include SHA-256 digests | That Delay=100 ms matches every deployment |
| Grades follow normative UHQS / δ_C math | That UHBS endorses tarpits for production deception |

---

## 2. Software under test

| Field | Value |
| --- | --- |
| Project | [skeeto/endlessh](https://github.com/skeeto/endlessh) |
| Description | SSH tarpit — endless / slow fake banner drip |
| Git commit | `dfe44eb2c5b6fc3c48a39ed826fe0e4459cdf6ef` |
| Build | upstream `Makefile` (`cc -std=c99 …`) |
| Graded listen | TCP **2223** (lab; avoid clashing with other SSH decoys) |
| Lab auth | n/a |

---

## 3. Grader

| Field | Full | Quick |
| --- | --- | --- |
| TPS | [`labs/endlessh/low_interaction_ssh_full.yaml`](../../labs/endlessh/low_interaction_ssh_full.yaml) | [`labs/endlessh/low_interaction_ssh_quick.yaml`](../../labs/endlessh/low_interaction_ssh_quick.yaml) |
| Inventory | [`labs/endlessh/inventory.yaml`](../../labs/endlessh/inventory.yaml) | same |
| Protocol plugin | **ssh** | same |
| Profile class | `Low-Interaction` | same |

---

## 4. Topology

```text
┌──────────────────────┐                      ┌──────────────────────────┐
│ UHBS harness         │ ── TCP :2223 ─────── │ endlessh (local binary)  │
│ source → /honeypot   │                      │ Delay 100–1000 ms drip   │
└──────────────────────┘                      └──────────────────────────┘
```

---

## 5. Module notes

| Module | What ran | Outcome driver |
| --- | --- | --- |
| A | SSH RFC4253 probes | No identification / KEXINIT → **12.5** |
| B | Cross-session / payload | No session → **6.2** |
| C | Inject / schema | No session telemetry → **25** |
| D | Containment probes | No shell escape surface → **C=96**, **δ_C=1.0** |
| E | Concurrent SSH load | 100% client errors → **20** |
| F | White-box on C sources | Clean-ish; POSIX VFS N/A → **70** |

---

## 6. Integrity

```bash
python - <<'PY'
import hashlib, json
from pathlib import Path
for mode in ("quick", "full"):
    root = Path(f"docs/conformance/reports/endlessh/{mode}")
    man = json.loads((root / "MANIFEST.json").read_text())
    for art in man["artifacts"]:
        p = root / art["path"]
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        print(("OK" if h == art["sha256"] else "MISMATCH"), mode, art["path"])
PY
```

```bash
uhbs validate-scorecard docs/conformance/fixtures/endlessh-low-interaction.scorecard.json --strict
```
