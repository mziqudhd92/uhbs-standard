# Tutorial: grade Conpot with UHBS (quick + full)

**Status:** Informative · evaluation proof  
**Target:** [mushorg/conpot](https://github.com/mushorg/conpot) — ICS honeypot, **Modbus** on TCP **5020**  
**Published artifacts:** [`quick/`](quick/README.md) · [`full/`](full/README.md) · trust notes: [METHODOLOGY.md](METHODOLOGY.md)

---

## 0. Prerequisites

```bash
git clone https://github.com/mziqudhd92/uhbs-standard.git
cd uhbs-standard
docker build -t uhbs:4.0.1 .
docker build -f Dockerfile.full -t uhbs:4.0.1-full .
```

---

## 1. Clone Conpot

```bash
mkdir -p .local/labs
git clone https://github.com/mushorg/conpot.git .local/labs/conpot
cd .local/labs/conpot
git rev-parse HEAD
# published proof used: b82b7a7fae8866c648f7be37f7033481a1b93482
```

---

## 2. Build and start the honeypot

Upstream’s image currently ships with **setuptools ≥ 82**, which drops `pkg_resources` that Conpot’s `fs` dependency still imports. Use the lab wrapper:

```bash
# from UHBS repo root
docker build -t conpot:lab .local/labs/conpot
docker build -f docs/conformance/labs/conpot/Dockerfile.lab -t conpot:lab-fixed .
docker network create uhbs-lab 2>/dev/null || true
docker rm -f conpot-lab 2>/dev/null || true
docker run -d --name conpot-lab --network uhbs-lab -p 502:5020 -p 8800:8800 conpot:lab-fixed

# Wait until Modbus is actually listening (starts ~20s after container create)
until docker logs conpot-lab 2>&1 | grep -q 'Modbus server started'; do sleep 1; done
docker logs conpot-lab 2>&1 | grep -i 'Modbus server'

# Smoke Modbus TCP (host :502 → container :5020)
python3 - <<'PY'
import socket, struct
s = socket.create_connection(("127.0.0.1", 502), timeout=5)
# Read Holding Registers FC03 — default template often returns exception 0x02
s.sendall(struct.pack(">HHHBBHH", 1, 0, 6, 1, 3, 0, 1))
s.settimeout(3)
print(s.recv(64).hex())
s.close()
PY
```

**Inside `uhbs-lab`, grade against host `conpot-lab` port `5020`** (not host-mapped 502).

---

## 3. Quick run (smoke grade)

Lab asset: [`../../labs/conpot/ics_modbus_quick.yaml`](../../labs/conpot/ics_modbus_quick.yaml)

Do **not** use SSH/Telnet profiles for Conpot Modbus — UHBS will refuse protocol conflicts.

```bash
mkdir -p docs/conformance/reports/conpot/quick

docker run --rm \
  --network uhbs-lab \
  -v "$PWD:/work" \
  -v "$PWD/.local/labs/conpot:/honeypot:ro" \
  -w /work \
  -e UHBS_QUICK=1 \
  -e UHBS_AIRGAP_ATTESTED=1 \
  uhbs:4.0.1 \
  lab \
    --tps /work/docs/conformance/labs/conpot/ics_modbus_quick.yaml \
    --protocol modbus \
    --class ICS-SCADA \
    --target conpot-lab \
    --port 5020 \
    --source-root /honeypot \
    --phases profile,static,sandbox,dynamic,score \
    --modules A,B,C,D,E,F \
    --quick \
    --skip-sast-tools \
    --out /work/docs/conformance/reports/conpot/quick \
    --environment "Quick Docker lab: Conpot Modbus :5020, UHBS_QUICK=1, SAST skipped"
```

**Published quick result:** UHQS **44.55** · Grade **F** · δ_C **0.5625**  
See [`quick/SCORECARD.txt`](quick/SCORECARD.txt).

---

## 4. Seed telemetry for the full run

```bash
mkdir -p .local/labs/conpot-telemetry

python3 - <<'PY'
import socket, struct
for i in range(20):
    s = socket.create_connection(("127.0.0.1", 502), timeout=3)
    # FC01 Read Coils — matches default template block starting at address 1
    s.sendall(struct.pack(">HHHBBHH", i + 1, 0, 6, 1, 1, 1, 1))
    s.settimeout(2)
    try:
        s.recv(256)
    except Exception:
        pass
    s.close()
print("seeded")
PY

docker cp conpot-lab:/var/log/conpot/. .local/labs/conpot-telemetry/
printf '%s\n' '# UHBS egress gateway canary — no HIT lines means clean' \
  > .local/labs/conpot-telemetry/egress-gateway.log
```

---

## 5. Full run (claim-grade Docker lab)

Assets:

- [`../../labs/conpot/ics_modbus_full.yaml`](../../labs/conpot/ics_modbus_full.yaml) — 1000-sample TPS  
- [`../../labs/conpot/inventory.yaml`](../../labs/conpot/inventory.yaml)

**Note:** Conpot’s default Modbus template uses `mode=serial` with a **100 ms delay**. High Module E concurrency (e.g. 25×200) can leave the listener in CLOSE_WAIT and hang the grader. Published full run uses **concurrency 5 / requests 50**.

```bash
mkdir -p docs/conformance/reports/conpot/full

# Prefer a fresh Conpot if you already ran a heavy load test
docker rm -f conpot-lab
docker run -d --name conpot-lab --network uhbs-lab -p 502:5020 -p 8800:8800 conpot:lab-fixed
until docker logs conpot-lab 2>&1 | grep -q 'Modbus server started'; do sleep 1; done
# re-seed telemetry (section 4) if you wiped the container

docker run --rm \
  --network uhbs-lab \
  -v "$PWD:/work" \
  -v "$PWD/.local/labs/conpot:/honeypot:ro" \
  -v "$PWD/.local/labs/conpot-telemetry:/telemetry:ro" \
  -w /work \
  -e PYTHONUNBUFFERED=1 \
  -e UHBS_AIRGAP_ATTESTED=1 \
  -e UHBS_EGRESS_GATEWAY_LOG=/telemetry/egress-gateway.log \
  uhbs:4.0.1-full \
  lab \
    --inventory /work/docs/conformance/labs/conpot/inventory.yaml \
    --target conpot \
    --phases profile,static,sandbox,dynamic,score \
    --modules A,B,C,D,E,F \
    --concurrency 5 \
    --requests 50 \
    --out /work/docs/conformance/reports/conpot/full \
    --environment "Full Docker lab: Conpot Modbus :5020 + 1000-sample A3 + SAST + telemetry"
```

**Published full result:** UHQS **55.4** · Grade **D** · δ_C **0.81**  
See [`full/SCORECARD.txt`](full/SCORECARD.txt).

---

## 6. Verify

```bash
cat docs/conformance/reports/conpot/quick/SCORECARD.txt
cat docs/conformance/reports/conpot/full/SCORECARD.txt
uhbs validate-scorecard docs/conformance/fixtures/conpot-ics-scada.scorecard.json --strict
ls docs/conformance/reports/conpot/full/static/
```

---

## 7. How to read the grade

| Signal | Meaning |
| --- | --- |
| Listener on `:5020` | Liveness OK — necessary but not sufficient |
| Module A ≈ 79.0 | FC03 holding-register probe fails on default coil/input map (exception `0x02`); timing n=1000; 0–100 CheckResult scale |
| Module C = 55 (full) | Text `conpot.log` without STIX/OTel/ECS |
| Module E = 100 | Connect-storm at moderated load; not a claim about heavy ICS traffic |
| δ_C &lt; 1 | Safety Gate not cleared (no remote shell exec surface on this decoy) |
| UHQS 55.4 / D | Above F band; still below beta Production Baseline (UHQS &gt; 80 + gate) |

---

## 8. Cleanup

```bash
docker rm -f conpot-lab
# optional: docker network rm uhbs-lab
```

---

## 9. Pitfalls

1. **`pkg_resources` / setuptools** — use `conpot:lab-fixed` (`Dockerfile.lab` pins `setuptools<81`).  
2. **Port mapping** — host `502` ≠ container `5020`; grade on the Docker network at **5020**.  
3. **SSH profiles** — never pair Modbus with `low_interaction_ssh`; use ICS TPS + `--protocol modbus`.  
4. **Multi-protocol template** — HTTP `:8800`, S7, SNMP, etc. are **not** scored in this report.  
5. **Module E load** — keep concurrency low unless you have verified Conpot stays healthy.

Back to [Conpot hub](index.md) · [all reports](../index.md).
