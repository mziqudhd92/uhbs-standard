# Tutorial: grade OpenCanary with UHBS (quick + full)

**Status:** Informative · evaluation proof  
**Target:** [thinkst/opencanary](https://github.com/thinkst/opencanary) — HTTP canary on TCP **80**  
**Published artifacts:** [`quick/`](quick/) · [`full/`](full/) · trust notes: [METHODOLOGY.md](METHODOLOGY.md)

---

## 0. Prerequisites

```bash
git clone https://github.com/mziqudhd92/uhbs-standard.git
cd uhbs-standard
docker build -t uhbs:4.0.0 .
docker build -f Dockerfile.full -t uhbs:4.0.0-full .
```

---

## 1. Clone OpenCanary (source for Module F)

```bash
mkdir -p .local/labs
git clone https://github.com/thinkst/opencanary.git .local/labs/opencanary
cd .local/labs/opencanary
git rev-parse HEAD
# published proof used: bc231423aa40242cbd0bf34801f8788e23420dee
```

---

## 2. Start OpenCanary

Use the official image with the lab config that enables **HTTP :80** (and FTP :21;
FTP is **not** graded). Host port publish is optional — grading uses
`opencanary-lab:80` inside `uhbs-lab`.

Lab config: [`../../labs/opencanary/opencanary.conf`](../../labs/opencanary/opencanary.conf)

```bash
docker pull thinkst/opencanary:latest
docker network create uhbs-lab 2>/dev/null || true
docker rm -f opencanary-lab 2>/dev/null || true

docker run -d --name opencanary-lab --network uhbs-lab \
  -p 18080:80 -p 12021:21 \
  -v "$PWD/docs/conformance/labs/opencanary/opencanary.conf:/root/.opencanary.conf:ro" \
  thinkst/opencanary:latest

# Smoke from the host
curl -sS -m 3 -o /dev/null -w '%{http_code}\n' http://127.0.0.1:18080/
# expect a login-skin HTTP response (200 or 401-class depending on skin/path)
```

---

## 3. Quick run (smoke grade)

Lab assets:

- [`../../labs/opencanary/inventory.yaml`](../../labs/opencanary/inventory.yaml)
- [`../../labs/opencanary/web_api_http_quick.yaml`](../../labs/opencanary/web_api_http_quick.yaml)

```bash
mkdir -p docs/conformance/reports/opencanary/quick

docker run --rm \
  --network uhbs-lab \
  -v "$PWD:/work" \
  -v "$PWD/.local/labs/opencanary:/honeypot:ro" \
  -w /work \
  -e UHBS_QUICK=1 \
  -e UHBS_AIRGAP_ATTESTED=1 \
  -e PYTHONUNBUFFERED=1 \
  uhbs:4.0.0 \
  lab \
    --inventory /work/docs/conformance/labs/opencanary/inventory.yaml \
    --target opencanary \
    --tps /work/docs/conformance/labs/opencanary/web_api_http_quick.yaml \
    --phases profile,static,sandbox,dynamic,score \
    --modules A,B,C,D,E,F \
    --quick \
    --skip-sast-tools \
    --out /work/docs/conformance/reports/opencanary/quick \
    --environment "Quick Docker lab: OpenCanary HTTP :80, UHBS_QUICK=1, SAST skipped"
```

**Published quick result:** UHQS **41.30** · Grade **F** · δ_C **0.5625**  
See [`quick/SCORECARD.txt`](quick/SCORECARD.txt).

---

## 4. Seed telemetry for the full run

```bash
mkdir -p .local/labs/opencanary-telemetry

for i in $(seq 1 30); do
  curl -sS -m 2 http://127.0.0.1:18080/ >/dev/null || true
  curl -sS -m 2 http://127.0.0.1:18080/index.html >/dev/null || true
done

docker cp opencanary-lab:/var/tmp/opencanary.log \
  .local/labs/opencanary-telemetry/opencanary.log

printf '%s\n' '# UHBS egress gateway canary — no HIT lines means clean' \
  > .local/labs/opencanary-telemetry/egress-gateway.log
```

---

## 5. Full run (claim-grade Docker lab)

Assets:

- [`../../labs/opencanary/web_api_http_full.yaml`](../../labs/opencanary/web_api_http_full.yaml) — 1000-sample TPS  
- [`../../labs/opencanary/inventory.yaml`](../../labs/opencanary/inventory.yaml)

```bash
mkdir -p docs/conformance/reports/opencanary/full

docker run --rm \
  --network uhbs-lab \
  -v "$PWD:/work" \
  -v "$PWD/.local/labs/opencanary:/honeypot:ro" \
  -v "$PWD/.local/labs/opencanary-telemetry:/telemetry:ro" \
  -w /work \
  -e PYTHONUNBUFFERED=1 \
  -e UHBS_AIRGAP_ATTESTED=1 \
  -e UHBS_EGRESS_GATEWAY_LOG=/telemetry/egress-gateway.log \
  uhbs:4.0.0-full \
  lab \
    --inventory /work/docs/conformance/labs/opencanary/inventory.yaml \
    --target opencanary \
    --phases profile,static,sandbox,dynamic,score \
    --modules A,B,C,D,E,F \
    --concurrency 25 \
    --requests 200 \
    --out /work/docs/conformance/reports/opencanary/full \
    --environment "Full Docker lab: OpenCanary HTTP :80 + 1000-sample A3 + SAST + telemetry"
```

**Published full result:** UHQS **50.12** · Grade **D** · δ_C **0.81**  
See [`full/SCORECARD.txt`](full/SCORECARD.txt).

---

## 6. Verify

```bash
cat docs/conformance/reports/opencanary/quick/SCORECARD.txt
cat docs/conformance/reports/opencanary/full/SCORECARD.txt
uhbs validate-scorecard docs/conformance/fixtures/opencanary-web-api.scorecard.json --strict
ls docs/conformance/reports/opencanary/full/static/
```

---

## 7. How to read the grade

| Signal | Meaning |
| --- | --- |
| HTTP skin on `:80` | Graded protocol (FTP enabled but not scored) |
| Module A ≈ 21.5 | RFC 9110/9112 partial; timing n=1000 |
| Module D = 90 / δ_C = 0.81 | No SSH exec surface; airgap + clean gateway canary; gate not cleared |
| Module C = 55 (full) | JSON canary log without STIX/OTel/ECS schema evidence |
| Module E = 100 | HTTP load P95 ≪ 150 ms |
| Quick &lt; Full UHQS | Full improves δ_C via gateway evidence — prefer **full/** |

---

## 8. Cleanup

```bash
docker rm -f opencanary-lab
```

Back to [OpenCanary hub](index.md) · [all reports](../index.md).
