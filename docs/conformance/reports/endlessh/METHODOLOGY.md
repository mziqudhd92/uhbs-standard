# Endlessh methodology & trust notes

**Status:** Informative · evaluation proof  
**Related:** [TUTORIAL.md](TUTORIAL.md) · [full/run-meta.json](full/run-meta.json) · [quick/run-meta.json](quick/run-meta.json)

---

## 1. Claims / non-claims

| We claim | We do **not** claim |
| --- | --- |
| Artifacts come from UHBS-Lab v4.0.0 against `endlessh-lab:2222` on `uhbs-lab` | That Endlessh is UHBS-certified |
| Protocol plugin was **generic** via id `ssh_tarpit` | That Endlessh is an interactive SSH honeypot |
| Full run used 1000-sample timing, SAST, telemetry dir, gateway canary | That SSH/Paramiko suites are safe against tarpits |
| Manifests include SHA-256 digests | That `MSDELAY=200` matches every production Endlessh deploy |
| Grades follow normative UHQS / δ_C math | That UHBS endorses tarpits for production deception |

---

## 2. Software under test

| Field | Value |
| --- | --- |
| Project | [skeeto/endlessh](https://github.com/skeeto/endlessh) |
| Description | SSH tarpit — slow random banner drip |
| Git commit (source mount) | `dfe44eb2c5b6fc3c48a39ed826fe0e4459cdf6ef` |
| Image | `ghcr.io/linuxserver/endlessh:latest` |
| Image id | `sha256:9f0dd7c1b4128acd1bf4dfefe910ff39accc5e300ab57df641c51ea74958ad37` |
| Graded listen | TCP **2222** (`ssh_tarpit`) |
| Lab knobs | `MSDELAY=200`, `LOGFILE=true` (faster drip for measurable banners) |

---

## 3. Grader

| Field | Full | Quick |
| --- | --- | --- |
| Image | `uhbs:4.0.0-full` | `uhbs:4.0.0` |
| TPS | [`labs/endlessh/low_interaction_full.yaml`](../../labs/endlessh/low_interaction_full.yaml) | [`labs/endlessh/low_interaction_quick.yaml`](../../labs/endlessh/low_interaction_quick.yaml) |
| Inventory | [`labs/endlessh/inventory.yaml`](../../labs/endlessh/inventory.yaml) | same + quick TPS |
| Protocol plugin | **generic** (`ssh_tarpit`) | same |
| Profile class | `Low-Interaction` | same |
| Module E | concurrency **25**, requests **200** | `UHBS_QUICK` + 10×50 |

---

## 4. Topology

```text
┌──────────────────────┐   network uhbs-lab    ┌──────────────────────────┐
│ uhbs:4.0.0[-full]    │ ───────────────────── │ endlessh-lab             │
│ mounts /honeypot     │ ← skeeto/endlessh src │ TCP :2222 tarpit         │
│ mounts /telemetry    │ ← logs + gateway      │ (no SSH handshake)       │
└──────────────────────┘                       └──────────────────────────┘
```

---

## 5. Module notes (full)

| Module | What ran | Outcome driver |
| --- | --- | --- |
| A | Generic TCP + 1000× timing | Connect/banner OK; no SSH RFC4253 |
| B | Fuzz / blast | Survived |
| C | `/telemetry` logs | Text logs → schema-capped **55** |
| D | No `ports.ssh`; airgap + gateway | **C=90**, **δ_C=0.81** |
| E | 25×200 TCP load | P95 ≈ 7.2 ms |
| F | bandit + semgrep | SAST gate → F capped at **70** |

---

## 6. Integrity

```bash
python - <<'PY'
import hashlib, json
from pathlib import Path
for mode in ("quick", "full"):
    root = Path(f"docs/conformance/reports/endlessh/{mode}")
    man = json.loads((root / "MANIFEST.json").read_text())
    print("==", mode, "==")
    for art in man["artifacts"]:
        p = root / art["path"]
        h = hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
        print(("OK" if h == art["sha256"] else "FAIL"), art["path"])
PY

uhbs validate-scorecard docs/conformance/fixtures/endlessh-low-interaction.scorecard.json --strict
```

---

## 7. Limitations

1. **Not SSH protocol fidelity** — tarpit by design; `ssh_tarpit` is TCP-only.  
2. **No shell surface** — Module D cannot run egress/LPE shell probes.  
3. **Lab delay** — `MSDELAY=200` for grading practicality.  
4. **linuxserver image deprecated** upstream — still usable for this proof; alternatives exist.  
5. **Non-endorsement** — naming Endlessh ≠ UHBS requirement.

---

## 8. Replication

Follow [TUTORIAL.md](TUTORIAL.md). Compare digests in `run-meta.json` if UHQS diverges.
