# Tutorial: grade miniprint with UHBS (quick + full)

**Status:** Informative · evaluation proof  
**Target:** [sa7mon/miniprint](https://github.com/sa7mon/miniprint) — PJL printer honeypot on TCP **9100**  
**Published artifacts:** [`quick/`](quick/README.md) · [`full/`](full/README.md) · trust notes: [METHODOLOGY.md](METHODOLOGY.md)

---

## 0. Prerequisites

```bash
git clone https://github.com/uhbs/uhbs-standard.git
cd uhbs-standard
docker build -t uhbs:4.0.1 .
docker build -f Dockerfile.full -t uhbs:4.0.1-full .
```

---

## 1. Clone miniprint

```bash
mkdir -p .local/labs
git clone https://github.com/sa7mon/miniprint.git .local/labs/miniprint
cd .local/labs/miniprint
git rev-parse HEAD
```

Upstream already ships a `Dockerfile` (`python:3.7-alpine`, binds `0.0.0.0:9100`).

---

## 2. Build and start the honeypot

```bash
# from UHBS repo root
docker build -t miniprint:lab .local/labs/miniprint
docker network create uhbs-lab 2>/dev/null || true
docker rm -f miniprint-lab 2>/dev/null || true
docker run -d --name miniprint-lab --network uhbs-lab -p 9100:9100 miniprint:lab
docker logs miniprint-lab
# expect: Server started

# Smoke PJL INFO ID
python3 - <<'PY'
import socket
s = socket.create_connection(("127.0.0.1", 9100), timeout=3)
s.sendall(b"@PJL INFO ID\r\n")
s.settimeout(2)
print(s.recv(1024))
s.close()
PY
# expect: b'...hp LaserJet 4200...'
```

---

## 3. Quick run (smoke grade)

Uses a PJL-specific TPS (or class-only `low_interaction` **plus** `--protocol pjl`).
Do **not** use `--tps low_interaction_ssh` for printers — that profile is SSH/Telnet
only and UHBS will refuse the conflict.

Lab asset: [`../../labs/miniprint/low_interaction_quick.yaml`](../../labs/miniprint/low_interaction_quick.yaml)

```bash
mkdir -p docs/conformance/reports/miniprint/quick

docker run --rm \
  --network uhbs-lab \
  -v "$PWD:/work" \
  -v "$PWD/.local/labs/miniprint:/honeypot:ro" \
  -w /work \
  -e UHBS_QUICK=1 \
  -e UHBS_AIRGAP_ATTESTED=1 \
  uhbs:4.0.1 \
  lab \
    --tps /work/docs/conformance/labs/miniprint/low_interaction_quick.yaml \
    --protocol pjl \
    --class Low-Interaction \
    --target miniprint-lab \
    --port 9100 \
    --source-root /honeypot \
    --phases profile,static,sandbox,dynamic,score \
    --modules A,B,C,D,E,F \
    --quick \
    --skip-sast-tools \
    --out /work/docs/conformance/reports/miniprint/quick \
    --environment "Quick Docker lab: PJL/generic :9100, UHBS_QUICK=1, SAST skipped"
```

**Published quick result:** UHQS **41.83** · Grade **F** · δ_C **0.5625**  
See [`quick/SCORECARD.txt`](quick/SCORECARD.txt).

---

## 4. Seed telemetry for the full run

```bash
mkdir -p .local/labs/miniprint-telemetry

python3 - <<'PY'
import socket
for i in range(40):
    for cmd in (b"@PJL INFO ID\r\n", b"@PJL INFO STATUS\r\n"):
        s = socket.create_connection(("127.0.0.1", 9100), timeout=3)
        s.sendall(cmd)
        s.settimeout(1.5)
        try:
            s.recv(1024)
        except Exception:
            pass
        s.close()
print("seeded")
PY

docker cp miniprint-lab:/app/miniprint.log .local/labs/miniprint-telemetry/miniprint.log
printf '%s\n' '# UHBS egress gateway canary — no HIT lines means clean' \
  > .local/labs/miniprint-telemetry/egress-gateway.log
```

---

## 5. Full run (claim-grade Docker lab)

Assets:

- [`../../labs/miniprint/low_interaction_full.yaml`](../../labs/miniprint/low_interaction_full.yaml) — 1000-sample TPS  
- [`../../labs/miniprint/inventory.yaml`](../../labs/miniprint/inventory.yaml)

```bash
mkdir -p docs/conformance/reports/miniprint/full

docker run --rm \
  --network uhbs-lab \
  -v "$PWD:/work" \
  -v "$PWD/.local/labs/miniprint:/honeypot:ro" \
  -v "$PWD/.local/labs/miniprint-telemetry:/telemetry:ro" \
  -w /work \
  -e UHBS_AIRGAP_ATTESTED=1 \
  -e UHBS_EGRESS_GATEWAY_LOG=/telemetry/egress-gateway.log \
  uhbs:4.0.1-full \
  lab \
    --inventory /work/docs/conformance/labs/miniprint/inventory.yaml \
    --target miniprint \
    --phases profile,static,sandbox,dynamic,score \
    --modules A,B,C,D,E,F \
    --concurrency 25 \
    --requests 200 \
    --out /work/docs/conformance/reports/miniprint/full \
    --environment "Detailed Docker lab: PJL/generic :9100 + 1000-sample A3 + SAST + telemetry"
```

Expect ~2–3 minutes (1000 timing samples + Semgrep).

**Published full result:** UHQS **50.43** · Grade **D** · δ_C **0.81**  
See [`full/SCORECARD.txt`](full/SCORECARD.txt).

---

## 6. Verify

```bash
cat docs/conformance/reports/miniprint/quick/SCORECARD.txt
cat docs/conformance/reports/miniprint/full/SCORECARD.txt
uhbs validate-scorecard docs/conformance/fixtures/miniprint-low-interaction.scorecard.json --strict
ls docs/conformance/reports/miniprint/full/static/
```

---

## 7. How to read the grade

| Signal | Meaning |
| --- | --- |
| PJL `INFO ID` works | Liveness OK — necessary but not sufficient |
| Module A ≈ 65.4 | Generic TCP timing/jitter, **not** full PJL dialect scoring |
| Module E ≈ 55 | Accept queue stalls under concurrent connects |
| Module C = 55 (full) | Text logs without STIX/OTel/ECS |
| δ_C &lt; 1 | Safety Gate not cleared (no remote shell exec surface on this decoy) |
| UHQS 50.43 / D | Below beta Production Baseline (UHQS &gt; 80 + gate) |

---

## 8. Cleanup

```bash
docker rm -f miniprint-lab
# optional: docker network rm uhbs-lab
```

---

## 9. Pitfall (fixed in UHBS tooling)

Older UHBS builds silently let `--tps low_interaction` rewrite a target to
SSH/Telnet. Current behavior:

- `low_interaction` is **class-only** (weights / baselines; no forced protocol)
- `low_interaction_ssh` is the honest SSH/Telnet profile
- Mixing `--protocol pjl` with `low_interaction_ssh` **fails fast** with
  `ProtocolConflictError`
- Module D never Paramikos the application port unless `ports.ssh` / `ssh_port`
  is explicit

```bash
# OK — class-only TPS + explicit printer protocol
uhbs lab --tps low_interaction --protocol pjl --target miniprint-lab --port 9100 ...

# OK — dedicated lab TPS
uhbs lab --tps /work/docs/conformance/labs/miniprint/low_interaction_quick.yaml ...

# ERROR — SSH profile vs PJL target
uhbs lab --tps low_interaction_ssh --protocol pjl --target miniprint-lab --port 9100 ...
```

Back to [miniprint hub](index.md) · [all reports](../index.md).
