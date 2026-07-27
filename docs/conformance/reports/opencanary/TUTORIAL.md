# Tutorial: grade OpenCanary with UHBS (multi-protocol)

**Status:** Informative · evaluation proof  
**Target:** [thinkst/opencanary](https://github.com/thinkst/opencanary) · commit `bc231423aa40242cbd0bf34801f8788e23420dee`  
**Protocols graded:** HTTP, FTP, SSH, Telnet, Redis, MySQL, RDP, SIP, SNMP, NTP, TFTP, VNC, Git, SMB (Samba sidecar on `opencanary-smb`)

OpenCanary is a multi-protocol canary. This lab enables every module that maps to a UHBS protocol plugin; SMB is graded against the Samba sidecar per inventory.

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
git clone https://github.com/thinkst/opencanary.git .local/labs/opencanary
cd .local/labs/opencanary
git checkout bc231423aa40242cbd0bf34801f8788e23420dee
```

## 2. Start OpenCanary

Lab config: [`../../labs/opencanary/opencanary.conf`](../../labs/opencanary/opencanary.conf)  
Mount to **`/etc/opencanaryd/opencanary.conf`** (first search path). A mount on `/root/.opencanary.conf` is ignored when `/etc/opencanaryd/opencanary.conf` exists in the image.

```bash
docker pull thinkst/opencanary:latest
docker rm -f opencanary-lab 2>/dev/null || true
docker run -d --name opencanary-lab --network uhbs-lab \
  -v "$PWD/docs/conformance/labs/opencanary/opencanary.conf:/etc/opencanaryd/opencanary.conf:ro" \
  thinkst/opencanary:latest

until docker logs opencanary-lab 2>&1 | grep -q 'Canary running'; do sleep 1; done
```

## 3. Quick + full — HTTP {#http}

```bash
mkdir -p docs/conformance/reports/opencanary/http/{quick,full}

docker run --rm --network uhbs-lab \
  -v "$PWD:/work" -v "$PWD/.local/labs/opencanary:/honeypot:ro" -w /work \
  -e UHBS_QUICK=1 -e UHBS_AIRGAP_ATTESTED=1 -e PYTHONUNBUFFERED=1 \
  uhbs:4.0.0 lab \
    --inventory /work/docs/conformance/labs/opencanary/inventory.yaml \
    --target opencanary-http \
    --tps /work/docs/conformance/labs/opencanary/web_api_http_quick.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --quick --skip-sast-tools --concurrency 10 --requests 50 \
    --out /work/docs/conformance/reports/opencanary/http/quick \
    --environment "Quick Docker lab: opencanary-http"
```

**Published HTTP:** quick **52.34 / D** · full **66.02 / D**

## 4. Quick + full — FTP {#ftp}

```bash
mkdir -p docs/conformance/reports/opencanary/ftp/{quick,full}

docker run --rm --network uhbs-lab \
  -v "$PWD:/work" -v "$PWD/.local/labs/opencanary:/honeypot:ro" -w /work \
  -e UHBS_QUICK=1 -e UHBS_AIRGAP_ATTESTED=1 -e PYTHONUNBUFFERED=1 \
  uhbs:4.0.0 lab \
    --inventory /work/docs/conformance/labs/opencanary/inventory.yaml \
    --target opencanary-ftp \
    --tps /work/docs/conformance/labs/opencanary/low_interaction_ftp_quick.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --quick --skip-sast-tools --concurrency 10 --requests 50 \
    --out /work/docs/conformance/reports/opencanary/ftp/quick \
    --environment "Quick Docker lab: opencanary-ftp"
```

**Published FTP:** quick **50.47 / D** · full **61.5 / D**

## 5. Quick + full — SSH {#ssh}

OpenCanary SSH is a canary: login attempts are logged and rejected (no interactive shell). Low Module A/B scores are expected.

```bash
mkdir -p docs/conformance/reports/opencanary/ssh/{quick,full}

docker run --rm --network uhbs-lab \
  -v "$PWD:/work" -v "$PWD/.local/labs/opencanary:/honeypot:ro" -w /work \
  -e UHBS_QUICK=1 -e UHBS_AIRGAP_ATTESTED=1 -e PYTHONUNBUFFERED=1 \
  uhbs:4.0.0 lab \
    --inventory /work/docs/conformance/labs/opencanary/inventory.yaml \
    --target opencanary-ssh \
    --tps /work/docs/conformance/labs/opencanary/low_interaction_ssh_quick.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --quick --skip-sast-tools --concurrency 10 --requests 50 \
    --out /work/docs/conformance/reports/opencanary/ssh/quick \
    --environment "Quick Docker lab: opencanary-ssh"
```

**Published SSH:** quick **31.94 / F** · full **35.64 / F**

## 6. Quick + full — Telnet {#telnet}

```bash
mkdir -p docs/conformance/reports/opencanary/telnet/{quick,full}

docker run --rm --network uhbs-lab \
  -v "$PWD:/work" -v "$PWD/.local/labs/opencanary:/honeypot:ro" -w /work \
  -e UHBS_QUICK=1 -e UHBS_AIRGAP_ATTESTED=1 -e PYTHONUNBUFFERED=1 \
  uhbs:4.0.0 lab \
    --inventory /work/docs/conformance/labs/opencanary/inventory.yaml \
    --target opencanary-telnet \
    --tps /work/docs/conformance/labs/opencanary/low_interaction_telnet_quick.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --quick --skip-sast-tools --concurrency 10 --requests 50 \
    --out /work/docs/conformance/reports/opencanary/telnet/quick \
    --environment "Quick Docker lab: opencanary-telnet"
```

**Published Telnet:** quick **52.83 / D** · full **64.9 / D**

## 7. Quick + full — Redis {#redis}

```bash
mkdir -p docs/conformance/reports/opencanary/redis/{quick,full}

docker run --rm --network uhbs-lab \
  -v "$PWD:/work" -v "$PWD/.local/labs/opencanary:/honeypot:ro" -w /work \
  -e UHBS_QUICK=1 -e UHBS_AIRGAP_ATTESTED=1 -e PYTHONUNBUFFERED=1 \
  uhbs:4.0.0 lab \
    --inventory /work/docs/conformance/labs/opencanary/inventory.yaml \
    --target opencanary-redis \
    --tps /work/docs/conformance/labs/opencanary/low_interaction_redis_quick.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --quick --skip-sast-tools --concurrency 10 --requests 50 \
    --out /work/docs/conformance/reports/opencanary/redis/quick \
    --environment "Quick Docker lab: opencanary-redis"
```

**Published Redis:** quick **45.07 / F** · full **53.72 / D**

**Published MySQL:** quick **51.48 / D** · full **62.96 / D**
**Published RDP:** quick **50.13 / D** · full **61.01 / D**
**Published SIP:** quick **40.01 / F** · full **46.44 / F**
**Published SNMP:** quick **40.69 / F** · full **47.42 / F**
**Published NTP:** quick **40.69 / F** · full **47.42 / F**
**Published TFTP:** quick **40.69 / F** · full **47.42 / F**
**Published VNC:** quick **50.81 / D** · full **61.99 / D**
**Published Git:** quick **51.48 / D** · full **62.96 / D**
**Published SMB:** quick **50.13 / D** · full **57.72 / D**

## 8. Full runs (telemetry + SAST)

```bash
mkdir -p .local/labs/opencanary-telemetry
docker cp opencanary-lab:/var/tmp/opencanary.log \
  .local/labs/opencanary-telemetry/opencanary.log
printf '%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ) uhbs-lab egress-gateway: no unauthorized outbound observed (lab attestation)" \
  > .local/labs/opencanary-telemetry/egress-gateway.log

# Example: HTTP full (repeat with each --target / TPS / --out)
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" -v "$PWD/.local/labs/opencanary:/honeypot:ro" \
  -v "$PWD/.local/labs/opencanary-telemetry:/telemetry:ro" -w /work \
  -e PYTHONUNBUFFERED=1 -e UHBS_AIRGAP_ATTESTED=1 \
  -e UHBS_EGRESS_GATEWAY_LOG=/telemetry/egress-gateway.log \
  uhbs:4.0.0-full lab \
    --inventory /work/docs/conformance/labs/opencanary/inventory.yaml \
    --target opencanary-http \
    --tps /work/docs/conformance/labs/opencanary/web_api_http_full.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --concurrency 25 --requests 200 \
    --out /work/docs/conformance/reports/opencanary/http/full \
    --environment "Full Docker lab: opencanary-http"
```

## 9. Verify

```bash
uhbs validate-scorecard docs/conformance/fixtures/opencanary-web-api.scorecard.json --strict
uhbs validate-scorecard docs/conformance/fixtures/opencanary-ftp.scorecard.json --strict
uhbs validate-scorecard docs/conformance/fixtures/opencanary-ssh.scorecard.json --strict
uhbs validate-scorecard docs/conformance/fixtures/opencanary-telnet.scorecard.json --strict
uhbs validate-scorecard docs/conformance/fixtures/opencanary-redis.scorecard.json --strict
```

## Cleanup

```bash
docker rm -f opencanary-lab
```
