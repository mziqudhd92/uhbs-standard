# Tutorial: grade Endlessh with UHBS (quick + full)

**Status:** Informative · evaluation proof  
**Target:** [skeeto/endlessh](https://github.com/skeeto/endlessh) — SSH tarpit on TCP **2223**  
**Published artifacts:** [`quick/`](quick/) · [`full/`](full/) · trust notes: [METHODOLOGY.md](METHODOLOGY.md)

---

## 0. Prerequisites

```bash
git clone https://github.com/mziqudhd92/uhbs-standard.git
cd uhbs-standard
# UHBS CLI / Docker grader (optional if using a compatible harness):
# docker build -t uhbs:4.0.0 .
```

You need a C compiler (`cc`) to build Endlessh.

---

## 1. Clone & build Endlessh (source for Module F)

```bash
mkdir -p .local/labs
git clone --depth 1 https://github.com/skeeto/endlessh.git .local/labs/endlessh
cd .local/labs/endlessh
make
git rev-parse HEAD
# published proof used: dfe44eb2c5b6fc3c48a39ed826fe0e4459cdf6ef
```

---

## 2. Start Endlessh (loopback)

```bash
cat > /tmp/endlessh.conf <<'EOF'
Port 2223
Delay 100
MaxLineLength 32
MaxClients 4096
LogLevel 1
BindFamily 0
EOF

./endlessh -f /tmp/endlessh.conf &
nc -z 127.0.0.1 2223 && echo READY

# Smoke: tarpit drips non-SSH bytes (not a valid banner)
python3 -c "
import socket, time
s=socket.create_connection(('127.0.0.1',2223), timeout=3)
s.settimeout(2); time.sleep(0.3); print(s.recv(64)); s.close()
"
```

**Auth:** not applicable — Endlessh never completes SSH negotiation.

---

## 3. Quick run (smoke grade)

Lab assets: [`../../labs/endlessh/`](../../labs/endlessh/)

```bash
mkdir -p docs/conformance/reports/endlessh/quick

# Example with uhbs CLI (Docker) — adjust mounts to your harness:
# docker run --rm --network host -v "$PWD:/work" -v "$PWD/.local/labs/endlessh:/honeypot:ro" \
#   -e UHBS_QUICK=1 -e UHBS_AIRGAP_ATTESTED=1 uhbs:4.0.0 lab \
#   --inventory /work/docs/conformance/labs/endlessh/inventory.yaml \
#   --target endlessh --phases profile,static,dynamic,score \
#   --modules A,B,C,D,E,F --skip-sast-tools \
#   --out /work/docs/conformance/reports/endlessh/quick
```

**Published quick result:** UHQS **26.94** · Grade **F** · δ_C **1.0**  
See [`quick/SCORECARD.txt`](quick/SCORECARD.txt).

---

## 4. Full-lab notes (tarpit-safe)

A naive long SSH suite **hangs**: clients wait for `SSH-2.0-…` that never arrives.

Published **full/** remasures Module F and keeps the completed A–E evidence pack under
wall-clock limits. Composite matches quick: UHQS **26.94** / **F**.

See [`full/SCORECARD.txt`](full/SCORECARD.txt) · [METHODOLOGY.md](METHODOLOGY.md).

---

## 5. Interpret the grade

| Expectation | Reality |
| --- | --- |
| Interactive honeypot UHQS | Low — no SSH session |
| Tarpit / scanner delay tool | Working as designed |
| Safety gate | Usually passes (no shell) |

Endlessh is a strong **negative control** for UHBS: if a tarpit scored like Cowrie,
the harness would be wrong.

---

## 6. Cleanup

```bash
pkill -f endlessh || true
```

Back to the [report hub](index.md).
