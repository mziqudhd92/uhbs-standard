# Tutorial: grade Cowrie with UHBS (SSH + Telnet)

**Status:** Informative · evaluation proof  
**Target:** [https://github.com/cowrie/cowrie](https://github.com/cowrie/cowrie) · commit `e7d1854a9489fa78845af01e445232f854414f87`  
**Protocols graded:** SSH `:2222` (SFTP subsystem on), Telnet `:2223`

Cowrie documentation describes SSH and Telnet frontends; SFTP/SCP are SSH features (`[ssh] sftp_enabled`), not a separate listen port. UHBS grades **ssh** and **telnet** with dedicated plugins.

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
git clone https://github.com/cowrie/cowrie.git .local/labs/cowrie
cd .local/labs/cowrie
git checkout e7d1854a9489fa78845af01e445232f854414f87
```

## 2. Start Cowrie with Telnet enabled

Lab overlay: [`../../labs/cowrie/cowrie.cfg`](../../labs/cowrie/cowrie.cfg) enables `[telnet]` on `:2223` and keeps `[ssh] sftp_enabled = true`.

```bash
docker pull cowrie/cowrie:latest
docker rm -f cowrie-lab 2>/dev/null || true
docker run -d --name cowrie-lab --network uhbs-lab \
  -v "$PWD/docs/conformance/labs/cowrie/cowrie.cfg:/cowrie/cowrie-git/etc/cowrie.cfg:ro" \
  cowrie/cowrie:latest

until docker logs cowrie-lab 2>&1 | grep -q 'Ready to accept Telnet'; do sleep 1; done
# Credentials: root / admin
```

Smoke SFTP (SSH subsystem)::

```bash
python3 -c "import paramiko; t=paramiko.Transport(('cowrie-lab',2222)); t.connect(username='root',password='admin'); s=paramiko.SFTPClient.from_transport(t); print(s.listdir('.')); s.close(); t.close()"
# run from a container on uhbs-lab, or use host-mapped ports
```

## 3. Quick + full — SSH {#ssh}

```bash
mkdir -p docs/conformance/reports/cowrie/ssh/{quick,full}

docker run --rm --network uhbs-lab \
  -v "$PWD:/work" -v "$PWD/.local/labs/cowrie:/honeypot:ro" -w /work \
  -e UHBS_QUICK=1 -e UHBS_AIRGAP_ATTESTED=1 -e PYTHONUNBUFFERED=1 \
  uhbs:4.0.1 lab \
    --inventory /work/docs/conformance/labs/cowrie/inventory.yaml \
    --target cowrie-ssh \
    --tps /work/docs/conformance/labs/cowrie/low_interaction_ssh_quick.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --quick --skip-sast-tools --concurrency 10 --requests 50 \
    --out /work/docs/conformance/reports/cowrie/ssh/quick \
    --environment "Quick Docker lab: cowrie-ssh"

docker run --rm --network uhbs-lab \
  -v "$PWD:/work" -v "$PWD/.local/labs/cowrie:/honeypot:ro" \
  -v "$PWD/.local/labs/cowrie-telemetry:/telemetry:ro" -w /work \
  -e PYTHONUNBUFFERED=1 -e UHBS_AIRGAP_ATTESTED=1 \
  -e UHBS_EGRESS_GATEWAY_LOG=/telemetry/egress-gateway.log \
  uhbs:4.0.1-full lab \
    --inventory /work/docs/conformance/labs/cowrie/inventory.yaml \
    --target cowrie-ssh \
    --tps /work/docs/conformance/labs/cowrie/low_interaction_ssh_full.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --concurrency 25 --requests 200 \
    --out /work/docs/conformance/reports/cowrie/ssh/full \
    --environment "Full Docker lab: cowrie-ssh"
```

**Published SSH:** quick **82.76 / B** · full **61.37 / D**

## 4. Quick + full — Telnet {#telnet}

```bash
mkdir -p docs/conformance/reports/cowrie/telnet/{quick,full}

docker run --rm --network uhbs-lab \
  -v "$PWD:/work" -v "$PWD/.local/labs/cowrie:/honeypot:ro" -w /work \
  -e UHBS_QUICK=1 -e UHBS_AIRGAP_ATTESTED=1 -e PYTHONUNBUFFERED=1 \
  uhbs:4.0.1 lab \
    --inventory /work/docs/conformance/labs/cowrie/inventory.yaml \
    --target cowrie-telnet \
    --tps /work/docs/conformance/labs/cowrie/low_interaction_telnet_quick.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --quick --skip-sast-tools --concurrency 10 --requests 50 \
    --out /work/docs/conformance/reports/cowrie/telnet/quick \
    --environment "Quick Docker lab: cowrie-telnet"

docker run --rm --network uhbs-lab \
  -v "$PWD:/work" -v "$PWD/.local/labs/cowrie:/honeypot:ro" \
  -v "$PWD/.local/labs/cowrie-telemetry:/telemetry:ro" -w /work \
  -e PYTHONUNBUFFERED=1 -e UHBS_AIRGAP_ATTESTED=1 \
  -e UHBS_EGRESS_GATEWAY_LOG=/telemetry/egress-gateway.log \
  uhbs:4.0.1-full lab \
    --inventory /work/docs/conformance/labs/cowrie/inventory.yaml \
    --target cowrie-telnet \
    --tps /work/docs/conformance/labs/cowrie/low_interaction_telnet_full.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --concurrency 25 --requests 200 \
    --out /work/docs/conformance/reports/cowrie/telnet/full \
    --environment "Full Docker lab: cowrie-telnet"
```

**Published Telnet:** quick **53.41 / D** · full **64.90 / D**

## 5. Validate fixtures

```bash
uhbs validate-scorecard docs/conformance/fixtures/cowrie-ssh.scorecard.json --strict
uhbs validate-scorecard docs/conformance/fixtures/cowrie-telnet.scorecard.json --strict
```
