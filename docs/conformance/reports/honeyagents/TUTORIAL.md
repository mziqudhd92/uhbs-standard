# Tutorial: grade HoneyAgents with UHBS

**Status:** Informative · evaluation proof  
**Target:** [https://github.com/mrwadams/honeyagents](https://github.com/mrwadams/honeyagents) · commit `43d4114fe8b235c1646571f7bc50bacc7a32533a`  
**Protocol graded:** SSH `:2222` (Cowrie honeypot service). Telnet is mapped in compose but not enabled by stock Cowrie defaults.

## 0. Prerequisites

```bash
git clone https://github.com/uhbs/uhbs-standard.git
cd uhbs-standard
pip install -c constraints.txt -e ".[dev,lab]"
docker pull cowrie/cowrie:latest
docker network create uhbs-lab 2>/dev/null || true
```

## 1. Clone source (Module F)

```bash
mkdir -p .local/labs
git clone https://github.com/mrwadams/honeyagents.git .local/labs/honeyagents
cd .local/labs/honeyagents
git checkout 43d4114fe8b235c1646571f7bc50bacc7a32533a
```

## 2. Start the honeypot service only

Full `docker-compose up` also builds nginx, Apache, attacker, and AutoGen (needs `OPENAI_API_KEY`). For UHBS decoy grading, run the same Cowrie image the compose file uses:

```bash
docker rm -f honeyagents-honeypot 2>/dev/null || true
docker run -d --name honeyagents-honeypot --network uhbs-lab \
  -p 127.0.0.1:13222:2222 \
  -p 127.0.0.1:13223:2223 \
  cowrie/cowrie:latest

until docker logs honeyagents-honeypot 2>&1 | grep -q 'Ready to accept SSH'; do sleep 1; done
# Credentials: root / admin (Cowrie built-in defaults)
```

## 3. SSH quick + full

```bash
mkdir -p docs/conformance/reports/honeyagents/ssh/{quick,full}

# Local inventory: .local/honeyagents-inventory.yaml (127.0.0.1:13222)

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 \
uhbs-lab \
  --inventory .local/honeyagents-inventory.yaml \
  --target honeyagents-ssh \
  --tps docs/conformance/labs/honeyagents/low_interaction_ssh_quick.yaml \
  --protocol ssh \
  --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
  --quick --skip-sast-tools --concurrency 10 --requests 50 \
  --out docs/conformance/reports/honeyagents/ssh/quick \
  --environment "Quick Docker lab: honeyagents-ssh"

UHBS_AIRGAP_ATTESTED=1 \
uhbs-lab \
  --inventory .local/honeyagents-inventory.yaml \
  --target honeyagents-ssh \
  --tps docs/conformance/labs/honeyagents/low_interaction_ssh_full.yaml \
  --protocol ssh \
  --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
  --concurrency 25 --requests 200 \
  --out docs/conformance/reports/honeyagents/ssh/full \
  --environment "Full Docker lab: honeyagents-ssh"
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
