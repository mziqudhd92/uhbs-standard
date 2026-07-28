# Tutorial: grade GenAIPot with UHBS (SMTP + POP3)

**Status:** Informative · evaluation proof  
**Target:** [https://github.com/ls1911/GenAIPot](https://github.com/ls1911/GenAIPot) · zip tree `205ffe4`  
**Protocols graded:** SMTP + POP3

## 0. Prerequisites

```bash
git clone https://github.com/mziqudhd92/uhbs-standard.git
cd uhbs-standard
pip install -c constraints.txt -e ".[dev,lab]"
docker network create uhbs-lab 2>/dev/null || true
```

## 1. Source for Module F

```bash
mkdir -p .local
# From upstream zip or git clone into .local/genaipot
```

## 2. Start Docker lab (offline templates)

```bash
docker pull annls/genaipot:latest
docker rm -f genaipot-lab 2>/dev/null || true
docker run -d --name genaipot-lab --network uhbs-lab \
  -p 127.0.0.1:2525:25 -p 127.0.0.1:1110:110 \
  annls/genaipot:latest
```

Host inventories (not committed): `.local/genaipot-smtp-inventory.yaml` → `:2525`, `.local/genaipot-pop3-inventory.yaml` → `:1110`.

## 3. SMTP quick + full

```bash
mkdir -p docs/conformance/reports/genaipot/smtp/{quick,full}

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 \
uhbs-lab \
  --inventory .local/genaipot-smtp-inventory.yaml \
  --target genaipot-smtp \
  --tps docs/conformance/labs/genaipot/low_interaction_smtp_quick.yaml \
  --protocol smtp \
  --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
  --quick --skip-sast-tools --concurrency 10 --requests 50 \
  --out docs/conformance/reports/genaipot/smtp/quick \
  --environment "Quick Docker lab: genaipot-smtp"

UHBS_AIRGAP_ATTESTED=1 \
uhbs-lab \
  --inventory .local/genaipot-smtp-inventory.yaml \
  --target genaipot-smtp \
  --tps docs/conformance/labs/genaipot/low_interaction_smtp_full.yaml \
  --protocol smtp \
  --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
  --concurrency 25 --requests 200 \
  --out docs/conformance/reports/genaipot/smtp/full \
  --environment "Full Docker lab: genaipot-smtp"
```

Published: quick **30.9 / F**, full **30.78 / F**.

## 4. POP3 quick + full

```bash
mkdir -p docs/conformance/reports/genaipot/pop3/{quick,full}

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 \
uhbs-lab \
  --inventory .local/genaipot-pop3-inventory.yaml \
  --target genaipot-pop3 \
  --tps docs/conformance/labs/genaipot/low_interaction_pop3_quick.yaml \
  --protocol pop3 \
  --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
  --quick --skip-sast-tools --concurrency 10 --requests 50 \
  --out docs/conformance/reports/genaipot/pop3/quick \
  --environment "Quick Docker lab: genaipot-pop3"

UHBS_AIRGAP_ATTESTED=1 \
uhbs-lab \
  --inventory .local/genaipot-pop3-inventory.yaml \
  --target genaipot-pop3 \
  --tps docs/conformance/labs/genaipot/low_interaction_pop3_full.yaml \
  --protocol pop3 \
  --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
  --concurrency 25 --requests 200 \
  --out docs/conformance/reports/genaipot/pop3/full \
  --environment "Full Docker lab: genaipot-pop3"
```

Published: quick **44.24 / F**, full **44.13 / F**.
