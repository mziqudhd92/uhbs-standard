# Conpot methodology & trust notes

**Status:** Informative · evaluation proof  
**Related:** [TUTORIAL.md](TUTORIAL.md) · [full/run-meta.json](full/run-meta.json) · [quick/run-meta.json](quick/run-meta.json)

---

## 1. Claims / non-claims

| We claim | We do **not** claim |
| --- | --- |
| Artifacts come from UHBS-Lab v4.0.1 against a live Conpot container Modbus `:5020` | That Conpot is UHBS-certified |
| Full run used 1000-sample timing, source audit, SAST, and real log directory | That Module A exercised every Modbus function code / every Conpot template |
| Manifests include SHA-256 digests | That Docker Desktop equals a production air-gap |
| Grades follow normative UHQS / δ_C math | That UHBS is an industry consortium standard |
| Module D skipped shell probes because this decoy has **no SSH listener** (correct for Modbus-primary ICS) | That other Conpot listeners (HTTP/S7/SNMP/…) were graded |

---

## 2. Software under test

| Field | Value |
| --- | --- |
| Project | [mushorg/conpot](https://github.com/mushorg/conpot) |
| Description | ICS/SCADA honeypot (default multi-protocol template) |
| Git commit | `b82b7a7fae8866c648f7be37f7033481a1b93482` |
| Image | `conpot:lab-fixed` (upstream build + `setuptools<81` wrapper) |
| Image id | `sha256:a59010a7d6b449906612343cb36e762e4d0f6f2cd1d3e7e0174381d9926f4abe` |
| Graded listen | TCP **5020** Modbus (host publish `502:5020`) |
| Template note | Default Modbus `mode=serial`, `delay=100`; slaves expose coils/discrete/analog — **not** holding registers at addr 0 |

---

## 3. Grader

| Field | Full | Quick |
| --- | --- | --- |
| Image | `uhbs:4.0.1-full` | `uhbs:4.0.1` |
| TPS | [`labs/conpot/ics_modbus_full.yaml`](../../labs/conpot/ics_modbus_full.yaml) | [`labs/conpot/ics_modbus_quick.yaml`](../../labs/conpot/ics_modbus_quick.yaml) |
| Inventory | [`labs/conpot/inventory.yaml`](../../labs/conpot/inventory.yaml) | CLI + quick TPS |
| Protocol plugin | **modbus** | same |
| Profile class | `ICS-SCADA` | same |
| Module E | concurrency **5**, requests **50** | `UHBS_QUICK` caps |

**Why ICS-SCADA?** Matches the industrial decoy class weights (heavy Module A).  
**Why Modbus-only?** UHBS has a first-class Modbus plugin; grading every Conpot listener in one UHQS would mix protocols and obscure failure modes.

---

## 4. Topology

```text
┌──────────────────────┐   network uhbs-lab    ┌──────────────────────────┐
│ uhbs:4.0.1[-full]    │ ───────────────────── │ conpot-lab               │
│ mounts /honeypot     │ ← source tree         │ Modbus :5020 (graded)    │
│ mounts /telemetry    │ ← conpot.log          │ (+ other listeners N/A)  │
└──────────────────────┘                       └──────────────────────────┘
```

---

## 5. Module notes (full)

| Module | What ran | Outcome driver |
| --- | --- | --- |
| A | Modbus FSM + FC03 nego + 1000× timing | FC03 illegal data address on default map → nego 30; timing strong |
| B | FC06 write/read + binary fuzz | Survives blast; write/read exchange completed |
| C | `/telemetry` with `conpot.log` | Text logs → no STIX/OTel → **capped at 55** |
| D | No shell-exec port | Airgap + clean gateway → C=90, **δ_C=0.81** |
| E | 5×50 connect load | P95 ~1.7 ms; moderated vs 25×200 (Conpot CLOSE_WAIT fragility) |
| F | bandit + semgrep on source | Template SSL keys + Bandit HIGH → F capped at **70** |

---

## 6. Integrity

```bash
python - <<'PY'
import hashlib, json
from pathlib import Path
for mode in ("quick", "full"):
    root = Path(f"docs/conformance/reports/conpot/{mode}")
    man = json.loads((root / "MANIFEST.json").read_text())
    print("==", mode, "==")
    for art in man["artifacts"]:
        p = root / art["path"]
        h = hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
        print(("OK" if h == art["sha256"] else "FAIL"), art["path"])
PY

uhbs validate-scorecard docs/conformance/fixtures/conpot-ics-scada.scorecard.json --strict
```

---

## 7. Limitations

1. **Holding-register probe vs default map** — Module A FC03 failure is template realism, not “Modbus dead.”  
2. **Air-gap attested** — `UHBS_AIRGAP_ATTESTED=1` inside Docker Desktop.  
3. **No remote shell containment probes** — Module D only Paramikos an *explicit* `ports.ssh` / `ssh_port`.  
4. **Telemetry format** — classic text logger, not detection-pipeline schemas.  
5. **Moderated Module E** — published full run is not a 25×200 storm (that wedged Conpot in this lab).  
6. **Other protocols** — HTTP/S7/SNMP/BACnet/… not included in UHQS.  
7. **Non-endorsement** — naming Conpot ≠ UHBS requirement.

---

## 8. Replication

Follow [TUTORIAL.md](TUTORIAL.md). Compare image digests and `run-meta.json` if UHQS diverges.
