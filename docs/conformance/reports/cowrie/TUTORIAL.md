# Tutorial: grade Cowrie with UHBS (quick + full)

**Status:** Informative · evaluation proof  
**Target:** [cowrie/cowrie](https://github.com/cowrie/cowrie) — SSH honeypot on TCP **2222**  
**Published artifacts:** [`quick/`](quick/) · [`full/`](full/) · trust notes: [METHODOLOGY.md](METHODOLOGY.md)

---

## 0. Prerequisites

```bash
git clone https://github.com/mziqudhd92/uhbs-standard.git
cd uhbs-standard
docker build -t uhbs:4.0.0 .
docker build -f Dockerfile.full -t uhbs:4.0.0-full .
```

---

## 1. Clone Cowrie (source for Module F)

```bash
mkdir -p .local/labs
git clone https://github.com/cowrie/cowrie.git .local/labs/cowrie
cd .local/labs/cowrie
git rev-parse HEAD
# published proof used: e7d1854a9489fa78845af01e445232f854414f87
```

---

## 2. Start Cowrie

Use the official image on the Docker lab network. Host port publish is optional
(grading uses `cowrie-lab:2222` inside `uhbs-lab`).

```bash
docker pull cowrie/cowrie:latest
docker network create uhbs-lab 2>/dev/null || true
docker rm -f cowrie-lab 2>/dev/null || true
docker run -d --name cowrie-lab --network uhbs-lab cowrie/cowrie:latest
# optional host map if free: -p 2222:2222

until docker logs cowrie-lab 2>&1 | grep -q 'Ready to accept SSH'; do sleep 1; done
docker logs cowrie-lab 2>&1 | tail -20

# Smoke banner from the Docker network
docker run --rm --network uhbs-lab python:3.12-slim python3 -c "
import socket
s=socket.create_connection(('cowrie-lab',2222),timeout=5)
s.settimeout(3); print(s.recv(128)); s.close()
"
```

**Credentials:** current `cowrie/cowrie` image accepts `root` / `admin` (not `root`/`root`).
Lab inventory sets `user: root` and `password: admin`.

---

## 3. Quick run (smoke grade)

Lab asset: [`../../labs/cowrie/low_interaction_ssh_quick.yaml`](../../labs/cowrie/low_interaction_ssh_quick.yaml)

Use the **SSH** Low-Interaction profile (`low_interaction_ssh`), not class-only
`low_interaction` alone without `--protocol ssh`.

```bash
mkdir -p docs/conformance/reports/cowrie/quick

docker run --rm \
  --network uhbs-lab \
  -v "$PWD:/work" \
  -v "$PWD/.local/labs/cowrie:/honeypot:ro" \
  -w /work \
  -e UHBS_QUICK=1 \
  -e UHBS_AIRGAP_ATTESTED=1 \
  -e PYTHONUNBUFFERED=1 \
  uhbs:4.0.0 \
  lab \
    --inventory /work/docs/conformance/labs/cowrie/inventory.yaml \
    --target cowrie \
    --tps /work/docs/conformance/labs/cowrie/low_interaction_ssh_quick.yaml \
    --phases profile,static,sandbox,dynamic,score \
    --modules A,B,C,D,E,F \
    --quick \
    --skip-sast-tools \
    --out /work/docs/conformance/reports/cowrie/quick \
    --environment "Quick Docker lab: Cowrie SSH :2222 root/admin, UHBS_QUICK=1, SAST skipped"
```

**Published quick result:** UHQS **63.52** · Grade **D** · δ_C **1.0**  
See [`quick/SCORECARD.txt`](quick/SCORECARD.txt).

---

## 4. Seed telemetry for the full run

```bash
mkdir -p .local/labs/cowrie-telemetry

docker run --rm --network uhbs-lab python:3.12-slim bash -c '
pip install -q paramiko >/dev/null
python3 - <<'"'"'PY'"'"'
import paramiko, time
for i in range(8):
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect("cowrie-lab", 2222, username="root", password="admin",
              timeout=10, allow_agent=False, look_for_keys=False)
    chan = c.invoke_shell(); time.sleep(0.3)
    chan.send("uname -a\n"); time.sleep(0.4)
    c.close()
print("seeded")
PY
'

docker cp cowrie-lab:/cowrie/cowrie-git/var/log/cowrie/. .local/labs/cowrie-telemetry/
printf '%s\n' '# UHBS egress gateway canary — no HIT lines means clean' \
  > .local/labs/cowrie-telemetry/egress-gateway.log
```

---

## 5. Full run (claim-grade Docker lab)

Assets:

- [`../../labs/cowrie/low_interaction_ssh_full.yaml`](../../labs/cowrie/low_interaction_ssh_full.yaml) — 1000-sample TPS  
- [`../../labs/cowrie/inventory.yaml`](../../labs/cowrie/inventory.yaml)

```bash
mkdir -p docs/conformance/reports/cowrie/full

docker run --rm \
  --network uhbs-lab \
  -v "$PWD:/work" \
  -v "$PWD/.local/labs/cowrie:/honeypot:ro" \
  -v "$PWD/.local/labs/cowrie-telemetry:/telemetry:ro" \
  -w /work \
  -e PYTHONUNBUFFERED=1 \
  -e UHBS_AIRGAP_ATTESTED=1 \
  -e UHBS_EGRESS_GATEWAY_LOG=/telemetry/egress-gateway.log \
  uhbs:4.0.0-full \
  lab \
    --inventory /work/docs/conformance/labs/cowrie/inventory.yaml \
    --target cowrie \
    --phases profile,static,sandbox,dynamic,score \
    --modules A,B,C,D,E,F \
    --concurrency 10 \
    --requests 50 \
    --out /work/docs/conformance/reports/cowrie/full \
    --environment "Full Docker lab: Cowrie SSH :2222 + 1000-sample A3 + SAST + telemetry"
```

**Published full result:** UHQS **48.70** · Grade **F** · δ_C **1.0**  
See [`full/SCORECARD.txt`](full/SCORECARD.txt).

---

## 6. Verify

```bash
cat docs/conformance/reports/cowrie/quick/SCORECARD.txt
cat docs/conformance/reports/cowrie/full/SCORECARD.txt
uhbs validate-scorecard docs/conformance/fixtures/cowrie-low-interaction.scorecard.json --strict
ls docs/conformance/reports/cowrie/full/static/
```

---

## 7. How to read the grade

| Signal | Meaning |
| --- | --- |
| SSH banner `OpenSSH_9.2p1` | Transport liveness OK |
| Module A ≈ 21.5 | Null-in-ID accepted; timing n=1000 |
| Module D = 100 / δ_C = 1 | Safety Gate cleared (SSH shell egress probes) |
| Module C = 55 (full) | JSON logs without STIX/OTel/ECS schema evidence |
| Module E ≈ 55 | SSH session load P95 ≫ 100 ms |
| Quick &gt; Full UHQS | Quick skips telemetry schema gates / SAST — prefer **full/** |

---

## 8. Cleanup

```bash
docker rm -f cowrie-lab
```

Back to [Cowrie hub](index.md) · [all reports](../index.md).
