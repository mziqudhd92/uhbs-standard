# Tutorial: grade LLMPot with UHBS

**Status:** Informative · evaluation proof  
**Target:** [https://github.com/momalab/LLMPot](https://github.com/momalab/LLMPot) · `9568b5ffe6f3626c70078e53eacaac4a9fcf1b9e`  
**Protocols graded:** Modbus TCP, S7comm, HTTP (WAGO WBM)  
**Not graded:** stock CUDA Lightning Modbus/S7 ByT5 path (unpublished `last.ckpt`)

## 0. Prerequisites

```bash
git clone https://github.com/mziqudhd92/uhbs-standard.git
cd uhbs-standard
pip install -c constraints.txt -e ".[dev,lab]"
docker network create uhbs-lab 2>/dev/null || true
```

## 1. Clone upstream

```bash
mkdir -p .local/labs
git clone https://github.com/momalab/LLMPot.git .local/labs/LLMPot
cd .local/labs/LLMPot && git checkout 9568b5ffe6f3626c70078e53eacaac4a9fcf1b9e
```

Apply the lab XFF fallback (or use the diff in [`../../labs/llmpot/xff-fallback.patch.md`](../../labs/llmpot/xff-fallback.patch.md)):

```bash
# In .local/labs/LLMPot — see methodology
```

## 2. Start HTTP (WAGO web) + Mongo

```bash
docker compose -f docs/conformance/labs/llmpot/compose.lab.yaml up -d --build
# Host: http://127.0.0.1:18081/wbm/
```

## 3. Start Modbus (HF CPU adapter)

Upstream Docker Modbus expects GPU + unpublished `honeypot/.../last.ckpt`. UHBS lab image:

```bash
docker build -t llmpot-modbus:uhbs-lab \
  -f docs/conformance/labs/llmpot/modbus.Dockerfile \
  docs/conformance/labs/llmpot
docker run -d --name llmpot-modbus --network uhbs-lab \
  -p 127.0.0.1:15020:5020 \
  -v llmpot-hf-cache:/root/.cache/huggingface \
  llmpot-modbus:uhbs-lab
# Wait for: listening Modbus TCP on 0.0.0.0:5020
```

## 3b. Start S7comm (Snap7 NoLogic gold)

Public tree has no ByT5 S7 weights. Dataset generation uses Snap7 — lab image:

```bash
docker build -t llmpot-s7:uhbs-lab \
  -f docs/conformance/labs/llmpot/s7.Dockerfile \
  docs/conformance/labs/llmpot
docker run -d --name llmpot-s7 --network uhbs-lab \
  -p 127.0.0.1:1102:102 llmpot-s7:uhbs-lab
# Wait for: listening S7comm on 0.0.0.0:102
```

## 4. Grade

Inventory: `.local/llmpot-inventory.yaml`

```bash
UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 \
uhbs-lab --inventory .local/llmpot-inventory.yaml --target llmpot-http \
  --tps docs/conformance/labs/llmpot/web_api_http_quick.yaml --protocol http \
  --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
  --quick --skip-sast-tools --concurrency 10 --requests 50 \
  --out docs/conformance/reports/llmpot/http/quick \
  --environment "Quick Docker lab: llmpot-http"

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 \
uhbs-lab --inventory .local/llmpot-inventory.yaml --target llmpot-s7comm \
  --tps docs/conformance/labs/llmpot/ics_s7comm_quick.yaml --protocol s7comm \
  --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
  --quick --skip-sast-tools --concurrency 10 --requests 50 \
  --out docs/conformance/reports/llmpot/s7comm/quick \
  --environment "Quick Docker lab: llmpot-s7comm (Snap7 NoLogic gold)"

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 \
uhbs-lab --inventory .local/llmpot-inventory.yaml --target llmpot-modbus \
  --tps docs/conformance/labs/llmpot/ics_modbus_quick.yaml --protocol modbus \
  --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
  --quick --skip-sast-tools --concurrency 2 --requests 10 \
  --out docs/conformance/reports/llmpot/modbus/quick \
  --environment "Quick Docker lab: llmpot-modbus (HF CPU adapter)"
```

Repeat with `*_full.yaml` for full runs (omit `--quick` / `--skip-sast-tools`).
