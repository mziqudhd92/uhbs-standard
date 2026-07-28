# Tutorial: grade DataTrap (Thales dd-honeypot) with UHBS

**Status:** Informative · evaluation proof  
**Target:** [https://github.com/ThalesGroup/dd-honeypot](https://github.com/ThalesGroup/dd-honeypot) · `7a906e11a0b19e75a32fead2ddd9a8b2b341beec`  
**Protocols graded:** SSH, HTTP, MySQL, Redis, Telnet, PostgreSQL  
**Not graded:** generic TCP (not configured in this lab)

## 0. Prerequisites

```bash
git clone https://github.com/mziqudhd92/uhbs-standard.git
cd uhbs-standard
pip install -c constraints.txt -e ".[dev,lab]"
docker network create uhbs-lab 2>/dev/null || true
```

## 1. Clone + build

```bash
mkdir -p .local/labs
git clone https://github.com/ThalesGroup/dd-honeypot.git .local/labs/dd-honeypot
cd .local/labs/dd-honeypot && git checkout 7a906e11a0b19e75a32fead2ddd9a8b2b341beec
docker build -t datatrap:uhbs-lab .
```

Lab honeypot tree (from upstream `test/honeypots/`): [`../../labs/datatrap/honeypot/`](../../labs/datatrap/honeypot/).

## 2. Start multi-protocol lab

DataTrap writes SQLite under each honeypot folder — mount **read-write**:

```bash
RUNTIME=.local/labs/datatrap-runtime
rm -rf "$RUNTIME" && cp -R docs/conformance/labs/datatrap/honeypot "$RUNTIME"
docker rm -f datatrap-lab 2>/dev/null || true
docker run -d --name datatrap-lab --network uhbs-lab \
  -p 127.0.0.1:14222:2222 \
  -p 127.0.0.1:18088:8080 \
  -p 127.0.0.1:13306:3306 \
  -p 127.0.0.1:16379:6379 \
  -p 127.0.0.1:12323:2323 \
  -p 127.0.0.1:15432:5432 \
  -v "$PWD/$RUNTIME:/data/honeypot" \
  datatrap:uhbs-lab

# Expect logs: Redis/Postgres/SSH/MySQL/Telnet/HTTP starting (6 honeypots)
```

Bedrock LLM is **not** required for handshake/dataset hits; unknown queries may error without AWS credentials.

## 3. Grade each UHBS-overlapping protocol

Local inventory: `.local/datatrap-inventory.yaml` (host ports above).

```bash
# Example: SSH quick
UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 \
uhbs-lab --inventory .local/datatrap-inventory.yaml --target datatrap-ssh \
  --tps docs/conformance/labs/datatrap/low_interaction_ssh_quick.yaml \
  --protocol ssh --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
  --quick --skip-sast-tools --concurrency 10 --requests 50 \
  --out docs/conformance/reports/datatrap/ssh/quick \
  --environment "Quick Docker lab: datatrap-ssh"
```

Repeat for `datatrap-http` / `http` / `web_api_http_*.yaml`, `datatrap-mysql`,
`datatrap-redis`, `datatrap-telnet`, `datatrap-postgres` (quick + full). Full runs
omit `--quick` / `--skip-sast-tools` and use `*_full.yaml`.
