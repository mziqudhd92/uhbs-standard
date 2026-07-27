# Tutorial: grade Trapster Community with UHBS (all UHBS-native protocols)

**Status:** Informative · evaluation proof  
**Target:** [https://github.com/0xBallpoint/trapster-community](https://github.com/0xBallpoint/trapster-community) · commit `dfc2c43dad119578f9c7344a0077790ed7fee01b`  
**Protocols graded:** FTP, HTTP, SSH, Telnet

## 0. Prerequisites

```bash
git clone https://github.com/mziqudhd92/uhbs-standard.git
cd uhbs-standard
docker build -t uhbs:4.0.0 .
docker build -f Dockerfile.full -t uhbs:4.0.0-full .
docker network create uhbs-lab 2>/dev/null || true
```

## 1. Clone source (Module F)

```bash
mkdir -p .local/labs
git clone https://github.com/0xBallpoint/trapster-community.git .local/labs/trapster-community
cd .local/labs/trapster-community
git checkout dfc2c43dad119578f9c7344a0077790ed7fee01b
```

## 2. Start the lab container

```bash
docker build -t trapster:uhbs-lab .local/labs/trapster-community
docker run -d --name trapster-lab --network uhbs-lab \
  -v "$PWD/docs/conformance/labs/trapster/trapster.conf:/etc/trapster/trapster.conf:ro" \
  trapster:uhbs-lab
```

## 3. Per-protocol quick + full

### FTP `:2121` {#ftp}

Target id: `trapster-ftp` · inventory: [`../../labs/trapster/inventory.yaml`](../../labs/trapster/inventory.yaml)

```bash
mkdir -p docs/conformance/reports/trapster/ftp/{quick,full}

# Quick
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" -v "$PWD/.local/labs/trapster-community:/honeypot:ro" -w /work \
  -e UHBS_QUICK=1 -e UHBS_AIRGAP_ATTESTED=1 -e PYTHONUNBUFFERED=1 \
  uhbs:4.0.0 lab \
    --inventory /work/docs/conformance/labs/trapster/inventory.yaml \
    --target trapster-ftp \
    --tps /work/docs/conformance/labs/trapster/low_interaction_ftp_quick.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --quick --skip-sast-tools --concurrency 10 --requests 50 \
    --out /work/docs/conformance/reports/trapster/ftp/quick \
    --environment "Quick Docker lab: trapster-ftp"

# Full
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" -v "$PWD/.local/labs/trapster-community:/honeypot:ro" \
  -v "$PWD/.local/labs/trapster-telemetry:/telemetry:ro" -w /work \
  -e PYTHONUNBUFFERED=1 -e UHBS_AIRGAP_ATTESTED=1 \
  -e UHBS_EGRESS_GATEWAY_LOG=/telemetry/egress-gateway.log \
  uhbs:4.0.0-full lab \
    --inventory /work/docs/conformance/labs/trapster/inventory.yaml \
    --target trapster-ftp \
    --tps /work/docs/conformance/labs/trapster/low_interaction_ftp_full.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --concurrency 25 --requests 200 \
    --out /work/docs/conformance/reports/trapster/ftp/full \
    --environment "Full Docker lab: trapster-ftp"
```

**Published:** quick **43.37 / F** · full **51.78 / D**

### HTTP `:8080` {#http}

Target id: `trapster-http` · inventory: [`../../labs/trapster/inventory.yaml`](../../labs/trapster/inventory.yaml)

```bash
mkdir -p docs/conformance/reports/trapster/http/{quick,full}

# Quick
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" -v "$PWD/.local/labs/trapster-community:/honeypot:ro" -w /work \
  -e UHBS_QUICK=1 -e UHBS_AIRGAP_ATTESTED=1 -e PYTHONUNBUFFERED=1 \
  uhbs:4.0.0 lab \
    --inventory /work/docs/conformance/labs/trapster/inventory.yaml \
    --target trapster-http \
    --tps /work/docs/conformance/labs/trapster/web_api_http_quick.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --quick --skip-sast-tools --concurrency 10 --requests 50 \
    --out /work/docs/conformance/reports/trapster/http/quick \
    --environment "Quick Docker lab: trapster-http"

# Full
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" -v "$PWD/.local/labs/trapster-community:/honeypot:ro" \
  -v "$PWD/.local/labs/trapster-telemetry:/telemetry:ro" -w /work \
  -e PYTHONUNBUFFERED=1 -e UHBS_AIRGAP_ATTESTED=1 \
  -e UHBS_EGRESS_GATEWAY_LOG=/telemetry/egress-gateway.log \
  uhbs:4.0.0-full lab \
    --inventory /work/docs/conformance/labs/trapster/inventory.yaml \
    --target trapster-http \
    --tps /work/docs/conformance/labs/trapster/web_api_http_full.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --concurrency 25 --requests 200 \
    --out /work/docs/conformance/reports/trapster/http/full \
    --environment "Full Docker lab: trapster-http"
```

**Published:** quick **50.13 / D** · full **63.33 / D**

### SSH `:2222` {#ssh}

Target id: `trapster-ssh` · inventory: [`../../labs/trapster/inventory.yaml`](../../labs/trapster/inventory.yaml)

```bash
mkdir -p docs/conformance/reports/trapster/ssh/{quick,full}

# Quick
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" -v "$PWD/.local/labs/trapster-community:/honeypot:ro" -w /work \
  -e UHBS_QUICK=1 -e UHBS_AIRGAP_ATTESTED=1 -e PYTHONUNBUFFERED=1 \
  uhbs:4.0.0 lab \
    --inventory /work/docs/conformance/labs/trapster/inventory.yaml \
    --target trapster-ssh \
    --tps /work/docs/conformance/labs/trapster/low_interaction_ssh_quick.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --quick --skip-sast-tools --concurrency 10 --requests 50 \
    --out /work/docs/conformance/reports/trapster/ssh/quick \
    --environment "Quick Docker lab: trapster-ssh"

# Full
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" -v "$PWD/.local/labs/trapster-community:/honeypot:ro" \
  -v "$PWD/.local/labs/trapster-telemetry:/telemetry:ro" -w /work \
  -e PYTHONUNBUFFERED=1 -e UHBS_AIRGAP_ATTESTED=1 \
  -e UHBS_EGRESS_GATEWAY_LOG=/telemetry/egress-gateway.log \
  uhbs:4.0.0-full lab \
    --inventory /work/docs/conformance/labs/trapster/inventory.yaml \
    --target trapster-ssh \
    --tps /work/docs/conformance/labs/trapster/low_interaction_ssh_full.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --concurrency 25 --requests 200 \
    --out /work/docs/conformance/reports/trapster/ssh/full \
    --environment "Full Docker lab: trapster-ssh"
```

**Published:** quick **40.06 / F** · full **44.38 / F**

### Telnet `:2323` {#telnet}

Target id: `trapster-telnet` · inventory: [`../../labs/trapster/inventory.yaml`](../../labs/trapster/inventory.yaml)

```bash
mkdir -p docs/conformance/reports/trapster/telnet/{quick,full}

# Quick
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" -v "$PWD/.local/labs/trapster-community:/honeypot:ro" -w /work \
  -e UHBS_QUICK=1 -e UHBS_AIRGAP_ATTESTED=1 -e PYTHONUNBUFFERED=1 \
  uhbs:4.0.0 lab \
    --inventory /work/docs/conformance/labs/trapster/inventory.yaml \
    --target trapster-telnet \
    --tps /work/docs/conformance/labs/trapster/low_interaction_telnet_quick.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --quick --skip-sast-tools --concurrency 10 --requests 50 \
    --out /work/docs/conformance/reports/trapster/telnet/quick \
    --environment "Quick Docker lab: trapster-telnet"

# Full
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" -v "$PWD/.local/labs/trapster-community:/honeypot:ro" \
  -v "$PWD/.local/labs/trapster-telemetry:/telemetry:ro" -w /work \
  -e PYTHONUNBUFFERED=1 -e UHBS_AIRGAP_ATTESTED=1 \
  -e UHBS_EGRESS_GATEWAY_LOG=/telemetry/egress-gateway.log \
  uhbs:4.0.0-full lab \
    --inventory /work/docs/conformance/labs/trapster/inventory.yaml \
    --target trapster-telnet \
    --tps /work/docs/conformance/labs/trapster/low_interaction_telnet_full.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --concurrency 25 --requests 200 \
    --out /work/docs/conformance/reports/trapster/telnet/full \
    --environment "Full Docker lab: trapster-telnet"
```

**Published:** quick **52.49 / D** · full **64.9 / D**


## 4. Validate a fixture

```bash
uhbs validate-scorecard docs/conformance/fixtures/trapster-ftp.scorecard.json --strict
```
