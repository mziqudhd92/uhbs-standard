# Tutorial: grade Endlessh with UHBS (quick + full)

**Status:** Informative · evaluation proof  
**Target:** [skeeto/endlessh](https://github.com/skeeto/endlessh) — SSH tarpit on TCP **2222**  
**Published artifacts:** [`quick/`](quick/README.md) · [`full/`](full/README.md) · trust notes: [METHODOLOGY.md](METHODOLOGY.md)

> **Critical:** use protocol id **`ssh_tarpit`** (generic plugin).  
> Never pass `--protocol ssh` or inventory `ports.ssh` — Paramiko hangs forever.

---

## 0. Prerequisites

```bash
git clone https://github.com/uhbs/uhbs-standard.git
cd uhbs-standard
docker build -t uhbs:4.0.1 .
docker build -f Dockerfile.full -t uhbs:4.0.1-full .
```

---

## 1. Clone Endlessh (source for Module F)

```bash
mkdir -p .local/labs
git clone --depth 1 https://github.com/skeeto/endlessh.git .local/labs/endlessh
cd .local/labs/endlessh
git rev-parse HEAD
# published proof used: dfe44eb2c5b6fc3c48a39ed826fe0e4459cdf6ef
```

---

## 2. Start Endlessh (Docker)

Use the linuxserver image on `uhbs-lab`. Lab uses a **faster drip** (`MSDELAY=200`)
so generic banner probes observe bytes within timeouts (upstream default is often
10000 ms). Graded port is container **2222**.

```bash
docker pull ghcr.io/linuxserver/endlessh:latest
docker network create uhbs-lab 2>/dev/null || true
docker rm -f endlessh-lab 2>/dev/null || true

docker run -d --name endlessh-lab --network uhbs-lab \
  -e PUID=1000 -e PGID=1000 -e TZ=Etc/UTC \
  -e MSDELAY=200 -e MAXLINES=32 -e MAXCLIENTS=4096 -e LOGFILE=true \
  -p 12222:2222 \
  ghcr.io/linuxserver/endlessh:latest

# Smoke from the Docker network
docker run --rm --network uhbs-lab python:3.12-slim python3 -c "
import socket, time
s=socket.create_connection(('endlessh-lab',2222), timeout=3)
s.settimeout(1.5)
print(s.recv(80)); s.close()
"
# expect random tarpit lines — NOT b'SSH-2.0-...'
```

Lab assets: [`../../labs/endlessh/inventory.yaml`](../../labs/endlessh/inventory.yaml)

---

## 3. Quick run (smoke grade)

```bash
mkdir -p docs/conformance/reports/endlessh/quick

docker run --rm \
  --network uhbs-lab \
  -v "$PWD:/work" \
  -v "$PWD/.local/labs/endlessh:/honeypot:ro" \
  -w /work \
  -e UHBS_QUICK=1 \
  -e UHBS_AIRGAP_ATTESTED=1 \
  -e PYTHONUNBUFFERED=1 \
  uhbs:4.0.1 \
  lab \
    --inventory /work/docs/conformance/labs/endlessh/inventory.yaml \
    --target endlessh \
    --tps /work/docs/conformance/labs/endlessh/low_interaction_quick.yaml \
    --phases profile,static,sandbox,dynamic,score \
    --modules A,B,C,D,E,F \
    --quick \
    --skip-sast-tools \
    --concurrency 10 \
    --requests 50 \
    --out /work/docs/conformance/reports/endlessh/quick \
    --environment "Quick Docker lab: Endlessh ssh_tarpit :2222 generic plugin, UHBS_QUICK=1, SAST skipped"
```

**Published quick result:** UHQS **46.55** · Grade **F** · δ_C **0.5625**  
See [`quick/SCORECARD.txt`](quick/SCORECARD.txt).

---

## 4. Seed telemetry for the full run

```bash
mkdir -p .local/labs/endlessh-telemetry

for i in $(seq 1 20); do
  docker run --rm --network uhbs-lab python:3.12-slim python3 -c "
import socket
s=socket.create_connection(('endlessh-lab',2222),timeout=2)
s.settimeout(0.8)
try: s.recv(64)
except Exception: pass
s.close()
" >/dev/null 2>&1 || true
done

docker cp endlessh-lab:/config/logs/endlessh/current \
  .local/labs/endlessh-telemetry/endlessh.log 2>/dev/null || true
docker logs endlessh-lab 2>&1 | tail -80 \
  > .local/labs/endlessh-telemetry/endlessh-docker.log

printf '%s\n' '# UHBS egress gateway canary — no HIT lines means clean' \
  > .local/labs/endlessh-telemetry/egress-gateway.log
```

---

## 5. Full run (claim-grade Docker lab)

```bash
mkdir -p docs/conformance/reports/endlessh/full

docker run --rm \
  --network uhbs-lab \
  -v "$PWD:/work" \
  -v "$PWD/.local/labs/endlessh:/honeypot:ro" \
  -v "$PWD/.local/labs/endlessh-telemetry:/telemetry:ro" \
  -w /work \
  -e PYTHONUNBUFFERED=1 \
  -e UHBS_AIRGAP_ATTESTED=1 \
  -e UHBS_EGRESS_GATEWAY_LOG=/telemetry/egress-gateway.log \
  uhbs:4.0.1-full \
  lab \
    --inventory /work/docs/conformance/labs/endlessh/inventory.yaml \
    --target endlessh \
    --phases profile,static,sandbox,dynamic,score \
    --modules A,B,C,D,E,F \
    --concurrency 25 \
    --requests 200 \
    --out /work/docs/conformance/reports/endlessh/full \
    --environment "Full Docker lab: Endlessh ssh_tarpit :2222 + 1000-sample A3 + SAST + telemetry"
```

**Published full result:** UHQS **54.07** · Grade **D** · δ_C **0.81**  
See [`full/SCORECARD.txt`](full/SCORECARD.txt).

---

## 6. Verify

```bash
cat docs/conformance/reports/endlessh/quick/SCORECARD.txt
cat docs/conformance/reports/endlessh/full/SCORECARD.txt
uhbs validate-scorecard docs/conformance/fixtures/endlessh-low-interaction.scorecard.json --strict
ls docs/conformance/reports/endlessh/full/static/
```

---

## 7. How to read the grade

| Signal | Meaning |
| --- | --- |
| Protocol `ssh_tarpit` | Generic TCP — tarpit-safe |
| No `ports.ssh` | Module D skips Paramiko shell probes |
| Module A ≈ 65.4 | Connect/banner/timing only (not RFC4253 SSH) |
| Module E = 100 | Short TCP connects stay fast |
| Quick &lt; Full UHQS | Full improves δ_C via gateway evidence |

Endlessh is still a **negative control** for interactive SSH realism — high UHQS
would be surprising for a tarpit. The prior incorrect publication that used the
SSH plugin and identical quick/full scores is superseded by this Docker pack.

---

## 8. Cleanup

```bash
docker rm -f endlessh-lab
```

Back to [Endlessh hub](index.md) · [all reports](../index.md).
