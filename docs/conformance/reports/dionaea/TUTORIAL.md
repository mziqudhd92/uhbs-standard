# Tutorial: grade Dionaea with UHBS (all UHBS-native protocols)

**Status:** Informative · evaluation proof  
**Target:** [https://github.com/dinotools/dionaea](https://github.com/dinotools/dionaea) · commit `4e459f1b672a5b4c1e8335c0bff1b93738019215`  
**Protocols graded:** FTP, HTTP, SMB

## 0. Prerequisites

```bash
git clone https://github.com/mziqudhd92/uhbs-standard.git
cd uhbs-standard
docker build -t uhbs:4.0.1 .
docker build -f Dockerfile.full -t uhbs:4.0.1-full .
docker network create uhbs-lab 2>/dev/null || true
```

## 1. Clone source (Module F)

```bash
mkdir -p .local/labs
git clone https://github.com/dinotools/dionaea.git .local/labs/dionaea
cd .local/labs/dionaea
git checkout 4e459f1b672a5b4c1e8335c0bff1b93738019215
```

## 2. Start the lab container

```bash
docker pull dinotools/dionaea:latest
docker run -d --name dionaea-lab --network uhbs-lab --platform linux/amd64 \
  -v "$PWD/.local/labs/dionaea-telemetry:/opt/dionaea/var/log/dionaea" \
  dinotools/dionaea:latest
```

## 3. Per-protocol quick + full

### FTP `:21` {#ftp}

Target id: `dionaea-ftp` · inventory: [`../../labs/dionaea/inventory.yaml`](../../labs/dionaea/inventory.yaml)

```bash
mkdir -p docs/conformance/reports/dionaea/ftp/{quick,full}

# Quick
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" -v "$PWD/.local/labs/dionaea:/honeypot:ro" -w /work \
  -e UHBS_QUICK=1 -e UHBS_AIRGAP_ATTESTED=1 -e PYTHONUNBUFFERED=1 \
  uhbs:4.0.1 lab \
    --inventory /work/docs/conformance/labs/dionaea/inventory.yaml \
    --target dionaea-ftp \
    --tps /work/docs/conformance/labs/dionaea/low_interaction_ftp_quick.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --quick --skip-sast-tools --concurrency 10 --requests 50 \
    --out /work/docs/conformance/reports/dionaea/ftp/quick \
    --environment "Quick Docker lab: dionaea-ftp"

# Full
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" -v "$PWD/.local/labs/dionaea:/honeypot:ro" \
  -v "$PWD/.local/labs/dionaea-telemetry:/telemetry:ro" -w /work \
  -e PYTHONUNBUFFERED=1 -e UHBS_AIRGAP_ATTESTED=1 \
  -e UHBS_EGRESS_GATEWAY_LOG=/telemetry/egress-gateway.log \
  uhbs:4.0.1-full lab \
    --inventory /work/docs/conformance/labs/dionaea/inventory.yaml \
    --target dionaea-ftp \
    --tps /work/docs/conformance/labs/dionaea/low_interaction_ftp_full.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --concurrency 25 --requests 200 \
    --out /work/docs/conformance/reports/dionaea/ftp/full \
    --environment "Full Docker lab: dionaea-ftp"
```

**Published:** quick **50.95 / D** · full **57.96 / D**

### HTTP `:80` {#http}

Target id: `dionaea-http` · inventory: [`../../labs/dionaea/inventory.yaml`](../../labs/dionaea/inventory.yaml)

```bash
mkdir -p docs/conformance/reports/dionaea/http/{quick,full}

# Quick
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" -v "$PWD/.local/labs/dionaea:/honeypot:ro" -w /work \
  -e UHBS_QUICK=1 -e UHBS_AIRGAP_ATTESTED=1 -e PYTHONUNBUFFERED=1 \
  uhbs:4.0.1 lab \
    --inventory /work/docs/conformance/labs/dionaea/inventory.yaml \
    --target dionaea-http \
    --tps /work/docs/conformance/labs/dionaea/web_api_http_quick.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --quick --skip-sast-tools --concurrency 10 --requests 50 \
    --out /work/docs/conformance/reports/dionaea/http/quick \
    --environment "Quick Docker lab: dionaea-http"

# Full
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" -v "$PWD/.local/labs/dionaea:/honeypot:ro" \
  -v "$PWD/.local/labs/dionaea-telemetry:/telemetry:ro" -w /work \
  -e PYTHONUNBUFFERED=1 -e UHBS_AIRGAP_ATTESTED=1 \
  -e UHBS_EGRESS_GATEWAY_LOG=/telemetry/egress-gateway.log \
  uhbs:4.0.1-full lab \
    --inventory /work/docs/conformance/labs/dionaea/inventory.yaml \
    --target dionaea-http \
    --tps /work/docs/conformance/labs/dionaea/web_api_http_full.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --concurrency 25 --requests 200 \
    --out /work/docs/conformance/reports/dionaea/http/full \
    --environment "Full Docker lab: dionaea-http"
```

**Published:** quick **46.21 / F** · full **51.14 / D**

### SMB `:445` {#smb}

Target id: `dionaea-smb` · inventory: [`../../labs/dionaea/inventory.yaml`](../../labs/dionaea/inventory.yaml)

```bash
mkdir -p docs/conformance/reports/dionaea/smb/{quick,full}

# Quick
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" -v "$PWD/.local/labs/dionaea:/honeypot:ro" -w /work \
  -e UHBS_QUICK=1 -e UHBS_AIRGAP_ATTESTED=1 -e PYTHONUNBUFFERED=1 \
  uhbs:4.0.1 lab \
    --inventory /work/docs/conformance/labs/dionaea/inventory.yaml \
    --target dionaea-smb \
    --tps /work/docs/conformance/labs/dionaea/low_interaction_smb_quick.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --quick --skip-sast-tools --concurrency 10 --requests 50 \
    --out /work/docs/conformance/reports/dionaea/smb/quick \
    --environment "Quick Docker lab: dionaea-smb"

# Full
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" -v "$PWD/.local/labs/dionaea:/honeypot:ro" \
  -v "$PWD/.local/labs/dionaea-telemetry:/telemetry:ro" -w /work \
  -e PYTHONUNBUFFERED=1 -e UHBS_AIRGAP_ATTESTED=1 \
  -e UHBS_EGRESS_GATEWAY_LOG=/telemetry/egress-gateway.log \
  uhbs:4.0.1-full lab \
    --inventory /work/docs/conformance/labs/dionaea/inventory.yaml \
    --target dionaea-smb \
    --tps /work/docs/conformance/labs/dionaea/low_interaction_smb_full.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --concurrency 25 --requests 200 \
    --out /work/docs/conformance/reports/dionaea/smb/full \
    --environment "Full Docker lab: dionaea-smb"
```

**Published:** quick **48.25 / F** · full **54.07 / D**


## 4. Validate a fixture

```bash
uhbs validate-scorecard docs/conformance/fixtures/dionaea-ftp.scorecard.json --strict
```

## What you get from this lab

This tutorial reproduces the published UHBS evaluation proof for analysts who need to verify numbers, not trust a screenshot. After a successful run you should have:

- `SCORECARD.txt` — verbatim module table, UHQS, letter grade, and δ_C Safety Gate
- `report.json` — machine-readable scores for automation / diffing
- Optional harness logs under the lab telemetry directory

## How CTI / blue team should use the artifacts

1. Open the **full** SCORECARD first (authoritative). Treat **quick** as a smoke check unless the methodology says otherwise.
2. Read modules **A–F** with [READING-UHQS.md](../READING-UHQS.md): low B is often “credential sink by design,” not a broken decoy.
3. Confirm **δ_C = 1.0** (or understand why containment failed) before citing UHQS externally.
4. Wire your own log shipping; UHBS Module C is harness visibility, not SIEM coverage.

## Trust limits

- UHBS 4.2.2 evaluation proof is **informative** — not a certification, endorsement, or ranking.
- Product names appear only under `docs/conformance/` as evaluation evidence.
- Re-run after upstream or TPS changes; do not invent scores without regenerating artifacts.
