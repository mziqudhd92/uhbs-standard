# Tutorial: grade LLM Honeypot (Palisade) with UHBS

**Status:** Informative · evaluation proof  
**Target:** [https://github.com/PalisadeResearch/llm-honeypot](https://github.com/PalisadeResearch/llm-honeypot) · commit `156004a1b122f201448635417ee47bd44d7f28ca`  
**Protocol graded:** SSH `:2222` (SFTP subsystem on). Telnet is **disabled** in the shipped `configs/cowrie.cfg`.

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
git clone https://github.com/PalisadeResearch/llm-honeypot.git .local/labs/llm-honeypot
cd .local/labs/llm-honeypot
git checkout 156004a1b122f201448635417ee47bd44d7f28ca
```

Lab overlays (copied under UHBS): [`../../labs/llm-honeypot/configs/`](../../labs/llm-honeypot/configs/).

## 2. Start Cowrie with LLM-honeypot overlays

Do **not** replace `src/cowrie/commands/__init__.py` from this fork on Cowrie ≥3.x — it breaks the Twisted `cowrie` plugin. Mount individual trap modules instead:

```bash
LABCFG="$PWD/docs/conformance/labs/llm-honeypot/configs"
docker rm -f llm-honeypot-lab 2>/dev/null || true
docker run -d --name llm-honeypot-lab --network uhbs-lab \
  -p 127.0.0.1:12222:2222 \
  -v "$LABCFG/cowrie.cfg:/cowrie/cowrie-git/etc/cowrie.cfg:ro" \
  -v "$LABCFG/userdb.txt:/cowrie/cowrie-git/etc/userdb.txt:ro" \
  -v "$LABCFG/motd:/cowrie/cowrie-git/honeyfs/etc/motd:ro" \
  -v "$LABCFG/version:/cowrie/cowrie-git/honeyfs/proc/version:ro" \
  -v "$LABCFG/passwd:/cowrie/cowrie-git/honeyfs/etc/passwd:ro" \
  -v "$LABCFG/whoami.py:/cowrie/cowrie-git/src/cowrie/commands/whoami.py:ro" \
  -v "$LABCFG/ps.py:/cowrie/cowrie-git/src/cowrie/commands/ps.py:ro" \
  -v "$LABCFG/df.py:/cowrie/cowrie-git/src/cowrie/commands/df.py:ro" \
  -v "$LABCFG/pwd_cmd.py:/cowrie/cowrie-git/src/cowrie/commands/pwd_cmd.py:ro" \
  -v "$LABCFG/ls.py:/cowrie/cowrie-git/src/cowrie/commands/ls.py:ro" \
  -v "$LABCFG/llm_prompts.py:/cowrie/cowrie-git/src/cowrie/commands/llm_prompts.py:ro" \
  -v "$LABCFG/cat8193.py:/cowrie/cowrie-git/src/cowrie/commands/cat8193.py:ro" \
  cowrie/cowrie:latest

until docker logs llm-honeypot-lab 2>&1 | grep -q 'Ready to accept SSH'; do sleep 1; done
# Credentials: root / admin (see labs/.../userdb.txt)
```

## 3. SSH quick + full

```bash
mkdir -p docs/conformance/reports/llm-honeypot/ssh/{quick,full}

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 \
uhbs-lab \
  --inventory .local/llm-honeypot-inventory.yaml \
  --target llm-honeypot-ssh \
  --tps docs/conformance/labs/llm-honeypot/low_interaction_ssh_quick.yaml \
  --protocol ssh \
  --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
  --quick --skip-sast-tools --concurrency 10 --requests 50 \
  --out docs/conformance/reports/llm-honeypot/ssh/quick \
  --environment "Quick Docker lab: llm-honeypot-ssh"

UHBS_AIRGAP_ATTESTED=1 \
uhbs-lab \
  --inventory .local/llm-honeypot-inventory.yaml \
  --target llm-honeypot-ssh \
  --tps docs/conformance/labs/llm-honeypot/low_interaction_ssh_full.yaml \
  --protocol ssh \
  --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
  --concurrency 25 --requests 200 \
  --out docs/conformance/reports/llm-honeypot/ssh/full \
  --environment "Full Docker lab: llm-honeypot-ssh"
```

Local inventory maps host `127.0.0.1:12222` → container `:2222` (avoids clash with other labs on `:2222`).

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
