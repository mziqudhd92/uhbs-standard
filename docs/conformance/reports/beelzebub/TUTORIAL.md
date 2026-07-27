# Tutorial: grade Beelzebub with UHBS (all UHBS-native protocols)

**Status:** Informative · evaluation proof  
**Target:** [https://github.com/beelzebub-labs/beelzebub](https://github.com/beelzebub-labs/beelzebub) · commit `80e1428d023d564481acede9e63eb49e1631bfec`  
**Protocols graded:** HTTP, Redis, SSH, Telnet

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
git clone https://github.com/beelzebub-labs/beelzebub.git .local/labs/beelzebub
cd .local/labs/beelzebub
git checkout 80e1428d023d564481acede9e63eb49e1631bfec
```

## 2. Start the lab container

```bash
docker build -t beelzebub:uhbs-lab .local/labs/beelzebub
docker run -d --name beelzebub-lab --network uhbs-lab \
  -v "$PWD/docs/conformance/labs/beelzebub/configurations:/configurations:ro" \
  beelzebub:uhbs-lab
```

## 3. Per-protocol quick + full

### HTTP `:8080` {#http}

Target id: `beelzebub-http` · inventory: [`../../labs/beelzebub/inventory.yaml`](../../labs/beelzebub/inventory.yaml)

```bash
mkdir -p docs/conformance/reports/beelzebub/http/{quick,full}

# Quick
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" -v "$PWD/.local/labs/beelzebub:/honeypot:ro" -w /work \
  -e UHBS_QUICK=1 -e UHBS_AIRGAP_ATTESTED=1 -e PYTHONUNBUFFERED=1 \
  uhbs:4.0.0 lab \
    --inventory /work/docs/conformance/labs/beelzebub/inventory.yaml \
    --target beelzebub-http \
    --tps /work/docs/conformance/labs/beelzebub/web_api_http_quick.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --quick --skip-sast-tools --concurrency 10 --requests 50 \
    --out /work/docs/conformance/reports/beelzebub/http/quick \
    --environment "Quick Docker lab: beelzebub-http"

# Full
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" -v "$PWD/.local/labs/beelzebub:/honeypot:ro" \
  -v "$PWD/.local/labs/beelzebub-telemetry:/telemetry:ro" -w /work \
  -e PYTHONUNBUFFERED=1 -e UHBS_AIRGAP_ATTESTED=1 \
  -e UHBS_EGRESS_GATEWAY_LOG=/telemetry/egress-gateway.log \
  uhbs:4.0.0-full lab \
    --inventory /work/docs/conformance/labs/beelzebub/inventory.yaml \
    --target beelzebub-http \
    --tps /work/docs/conformance/labs/beelzebub/web_api_http_full.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --concurrency 25 --requests 200 \
    --out /work/docs/conformance/reports/beelzebub/http/full \
    --environment "Full Docker lab: beelzebub-http"
```

**Published:** quick **52.77 / D** · full **66.02 / D**

### Redis `:6379` {#redis}

Target id: `beelzebub-redis` · inventory: [`../../labs/beelzebub/inventory.yaml`](../../labs/beelzebub/inventory.yaml)

```bash
mkdir -p docs/conformance/reports/beelzebub/redis/{quick,full}

# Quick
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" -v "$PWD/.local/labs/beelzebub:/honeypot:ro" -w /work \
  -e UHBS_QUICK=1 -e UHBS_AIRGAP_ATTESTED=1 -e PYTHONUNBUFFERED=1 \
  uhbs:4.0.0 lab \
    --inventory /work/docs/conformance/labs/beelzebub/inventory.yaml \
    --target beelzebub-redis \
    --tps /work/docs/conformance/labs/beelzebub/low_interaction_redis_quick.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --quick --skip-sast-tools --concurrency 10 --requests 50 \
    --out /work/docs/conformance/reports/beelzebub/redis/quick \
    --environment "Quick Docker lab: beelzebub-redis"

# Full
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" -v "$PWD/.local/labs/beelzebub:/honeypot:ro" \
  -v "$PWD/.local/labs/beelzebub-telemetry:/telemetry:ro" -w /work \
  -e PYTHONUNBUFFERED=1 -e UHBS_AIRGAP_ATTESTED=1 \
  -e UHBS_EGRESS_GATEWAY_LOG=/telemetry/egress-gateway.log \
  uhbs:4.0.0-full lab \
    --inventory /work/docs/conformance/labs/beelzebub/inventory.yaml \
    --target beelzebub-redis \
    --tps /work/docs/conformance/labs/beelzebub/low_interaction_redis_full.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --concurrency 25 --requests 200 \
    --out /work/docs/conformance/reports/beelzebub/redis/full \
    --environment "Full Docker lab: beelzebub-redis"
```

**Published:** quick **50.56 / D** · full **61.01 / D**

### SSH `:2222` {#ssh}

Target id: `beelzebub-ssh` · inventory: [`../../labs/beelzebub/inventory.yaml`](../../labs/beelzebub/inventory.yaml)

```bash
mkdir -p docs/conformance/reports/beelzebub/ssh/{quick,full}

# Quick
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" -v "$PWD/.local/labs/beelzebub:/honeypot:ro" -w /work \
  -e UHBS_QUICK=1 -e UHBS_AIRGAP_ATTESTED=1 -e PYTHONUNBUFFERED=1 \
  uhbs:4.0.0 lab \
    --inventory /work/docs/conformance/labs/beelzebub/inventory.yaml \
    --target beelzebub-ssh \
    --tps /work/docs/conformance/labs/beelzebub/low_interaction_ssh_quick.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --quick --skip-sast-tools --concurrency 10 --requests 50 \
    --out /work/docs/conformance/reports/beelzebub/ssh/quick \
    --environment "Quick Docker lab: beelzebub-ssh"

# Full
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" -v "$PWD/.local/labs/beelzebub:/honeypot:ro" \
  -v "$PWD/.local/labs/beelzebub-telemetry:/telemetry:ro" -w /work \
  -e PYTHONUNBUFFERED=1 -e UHBS_AIRGAP_ATTESTED=1 \
  -e UHBS_EGRESS_GATEWAY_LOG=/telemetry/egress-gateway.log \
  uhbs:4.0.0-full lab \
    --inventory /work/docs/conformance/labs/beelzebub/inventory.yaml \
    --target beelzebub-ssh \
    --tps /work/docs/conformance/labs/beelzebub/low_interaction_ssh_full.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --concurrency 25 --requests 200 \
    --out /work/docs/conformance/reports/beelzebub/ssh/full \
    --environment "Full Docker lab: beelzebub-ssh"
```

**Published:** quick **74.45 / C** · full **59.88 / D**

### Telnet `:23` {#telnet}

Target id: `beelzebub-telnet` · inventory: [`../../labs/beelzebub/inventory.yaml`](../../labs/beelzebub/inventory.yaml)

```bash
mkdir -p docs/conformance/reports/beelzebub/telnet/{quick,full}

# Quick
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" -v "$PWD/.local/labs/beelzebub:/honeypot:ro" -w /work \
  -e UHBS_QUICK=1 -e UHBS_AIRGAP_ATTESTED=1 -e PYTHONUNBUFFERED=1 \
  uhbs:4.0.0 lab \
    --inventory /work/docs/conformance/labs/beelzebub/inventory.yaml \
    --target beelzebub-telnet \
    --tps /work/docs/conformance/labs/beelzebub/low_interaction_telnet_quick.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --quick --skip-sast-tools --concurrency 10 --requests 50 \
    --out /work/docs/conformance/reports/beelzebub/telnet/quick \
    --environment "Quick Docker lab: beelzebub-telnet"

# Full
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" -v "$PWD/.local/labs/beelzebub:/honeypot:ro" \
  -v "$PWD/.local/labs/beelzebub-telemetry:/telemetry:ro" -w /work \
  -e PYTHONUNBUFFERED=1 -e UHBS_AIRGAP_ATTESTED=1 \
  -e UHBS_EGRESS_GATEWAY_LOG=/telemetry/egress-gateway.log \
  uhbs:4.0.0-full lab \
    --inventory /work/docs/conformance/labs/beelzebub/inventory.yaml \
    --target beelzebub-telnet \
    --tps /work/docs/conformance/labs/beelzebub/low_interaction_telnet_full.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --concurrency 25 --requests 200 \
    --out /work/docs/conformance/reports/beelzebub/telnet/full \
    --environment "Full Docker lab: beelzebub-telnet"
```

**Published:** quick **39.16 / F** · full **47.89 / F**


## 4. Validate a fixture

```bash
uhbs validate-scorecard docs/conformance/fixtures/beelzebub-http.scorecard.json --strict
```
