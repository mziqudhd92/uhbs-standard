# miniprint methodology & trust notes

**Status:** Informative · evaluation proof  
**Related:** [TUTORIAL.md](TUTORIAL.md) · [full/run-meta.json](full/run-meta.json) · [quick/run-meta.json](quick/run-meta.json)

---

## 1. Claims / non-claims

| We claim | We do **not** claim |
| --- | --- |
| Artifacts come from UHBS-Lab v4.0.1 against a live miniprint container on `:9100` | That miniprint is UHBS-certified |
| Full run used 1000-sample timing, source audit, SAST, and real log directory | That Module A exercised full PJL command semantics / RFC-style suites |
| Manifests include SHA-256 digests | That Docker Desktop equals a production air-gap |
| Grades follow normative UHQS / δ_C math | That UHBS is an industry consortium standard |
| Module D skipped shell probes because this decoy has **no SSH listener** (correct for PJL) | That “SSH” is part of how a printer honeypot works |

---

## 2. Software under test

| Field | Value |
| --- | --- |
| Project | [sa7mon/miniprint](https://github.com/sa7mon/miniprint) |
| Description | Medium-interaction PJL printer honeypot |
| Git commit | `494d2fc75b94c19345c2db55d03b5cf74f75e3c2` |
| Image | `miniprint:lab` (upstream `Dockerfile`, `python:3.7-alpine`) |
| Image id | `sha256:49182ecdd8a682f0e72ea83ae3e733ed69930401be34131d876e51794df4b6f4` |
| Listen | TCP **9100** (raw / PJL) |
| Smoke check | `@PJL INFO ID` → `hp LaserJet 4200` |

---

## 3. Grader

| Field | Full | Quick |
| --- | --- | --- |
| Image | `uhbs:4.0.1-full` | `uhbs:4.0.1` |
| TPS | [`labs/miniprint/low_interaction_full.yaml`](../../labs/miniprint/low_interaction_full.yaml) | [`labs/miniprint/low_interaction_quick.yaml`](../../labs/miniprint/low_interaction_quick.yaml) |
| Inventory | [`labs/miniprint/inventory.yaml`](../../labs/miniprint/inventory.yaml) | CLI + quick TPS |
| Protocol plugin | **generic** (id `pjl`) | same |
| Profile class | `Low-Interaction` | same |

**Why Low-Interaction?** UHBS classes are protocol-family oriented. miniprint is a non-shell service decoy; Low-Interaction weights (heavy Module A/C) are the closest published table. The author’s “medium interaction” label is noted in the tutorial — it is **not** a separate UHBS class today.

**Why generic/PJL?** There is no dedicated PJL plugin yet. Unknown protocol ids fall through to `GenericTCPPlugin` (connect, optional banner, timing, fuzz). Scores must be read with that scope in mind.

---

## 4. Topology

```text
┌──────────────────────┐   network uhbs-lab    ┌──────────────────────┐
│ uhbs:4.0.1[-full]    │ ───────────────────── │ miniprint-lab :9100  │
│ mounts /honeypot     │ ← source tree         │ PJL raw listener     │
│ mounts /telemetry    │ ← miniprint.log       │ (full run only)      │
└──────────────────────┘                       └──────────────────────┘
```

---

## 5. Module notes (full)

| Module | What ran | Outcome driver |
| --- | --- | --- |
| A | Generic connect + 1000× timing | High latency jitter vs “native printer” heuristic |
| B | State/payload stubs + binary fuzz | Survives blast; limited PJL dialogue |
| C | `/telemetry` with `miniprint.log` | Text logs → no STIX/OTel → **capped at 55** |
| D | No shell-exec port | Airgap + clean gateway → C=90, **δ_C=0.81** |
| E | 25×200 connect load | Single-threaded `TCPServer` → P95 ~1 s |
| F | bandit + semgrep on source | 1 semgrep critical → F capped at **70** |

---

## 6. Integrity

```bash
python - <<'PY'
import hashlib, json
from pathlib import Path
for mode in ("quick", "full"):
    root = Path(f"docs/conformance/reports/miniprint/{mode}")
    man = json.loads((root / "MANIFEST.json").read_text())
    print("==", mode, "==")
    for art in man["artifacts"]:
        p = root / art["path"]
        h = hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
        print(("OK" if h == art["sha256"] else "FAIL"), art["path"])
PY

uhbs validate-scorecard docs/conformance/fixtures/miniprint-low-interaction.scorecard.json --strict
```

---

## 7. Limitations

1. **No PJL RFC suite** — do not treat Module A as “PJL conformance certified.”  
2. **Air-gap attested** — `UHBS_AIRGAP_ATTESTED=1` inside Docker Desktop.  
3. **No remote shell containment probes** — Module D only Paramikos an *explicit*
   `ports.ssh` / `ssh_port`. Printer/HTTP decoys are graded on gateway + airgap
   attestation only (by design, protocol-agnostic).  
4. **Telemetry format** — classic text logger, not detection-pipeline schemas.  
5. **Load model** — connect-storm Module E stresses accept latency, not full PJL job pipelines.  
6. **Non-endorsement** — naming miniprint ≠ UHBS requirement.

---

## 8. Replication

Follow [TUTORIAL.md](TUTORIAL.md). Compare image digests and `run-meta.json` if UHQS diverges.
