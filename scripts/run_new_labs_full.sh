#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

echo "===== FULL beelzebub-ssh ====="
mkdir -p docs/conformance/reports/beelzebub/ssh/full .local/labs/beelzebub-telemetry
touch .local/labs/beelzebub-telemetry/egress-gateway.log
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" \
  -v "$PWD/.local/labs/beelzebub:/honeypot:ro" \
  -v "$PWD/.local/labs/beelzebub-telemetry:/telemetry:ro" \
  -w /work \
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
rg -n "UHQS|Grade|FINAL|OVERALL" docs/conformance/reports/beelzebub/ssh/full/SCORECARD.txt || true
echo

echo "===== FULL beelzebub-http ====="
mkdir -p docs/conformance/reports/beelzebub/http/full .local/labs/beelzebub-telemetry
touch .local/labs/beelzebub-telemetry/egress-gateway.log
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" \
  -v "$PWD/.local/labs/beelzebub:/honeypot:ro" \
  -v "$PWD/.local/labs/beelzebub-telemetry:/telemetry:ro" \
  -w /work \
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
rg -n "UHQS|Grade|FINAL|OVERALL" docs/conformance/reports/beelzebub/http/full/SCORECARD.txt || true
echo

echo "===== FULL beelzebub-telnet ====="
mkdir -p docs/conformance/reports/beelzebub/telnet/full .local/labs/beelzebub-telemetry
touch .local/labs/beelzebub-telemetry/egress-gateway.log
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" \
  -v "$PWD/.local/labs/beelzebub:/honeypot:ro" \
  -v "$PWD/.local/labs/beelzebub-telemetry:/telemetry:ro" \
  -w /work \
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
rg -n "UHQS|Grade|FINAL|OVERALL" docs/conformance/reports/beelzebub/telnet/full/SCORECARD.txt || true
echo

echo "===== FULL beelzebub-redis ====="
mkdir -p docs/conformance/reports/beelzebub/redis/full .local/labs/beelzebub-telemetry
touch .local/labs/beelzebub-telemetry/egress-gateway.log
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" \
  -v "$PWD/.local/labs/beelzebub:/honeypot:ro" \
  -v "$PWD/.local/labs/beelzebub-telemetry:/telemetry:ro" \
  -w /work \
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
rg -n "UHQS|Grade|FINAL|OVERALL" docs/conformance/reports/beelzebub/redis/full/SCORECARD.txt || true
echo

echo "===== FULL trapster-ssh ====="
mkdir -p docs/conformance/reports/trapster/ssh/full .local/labs/trapster-telemetry
touch .local/labs/trapster-telemetry/egress-gateway.log
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" \
  -v "$PWD/.local/labs/trapster-community:/honeypot:ro" \
  -v "$PWD/.local/labs/trapster-telemetry:/telemetry:ro" \
  -w /work \
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
rg -n "UHQS|Grade|FINAL|OVERALL" docs/conformance/reports/trapster/ssh/full/SCORECARD.txt || true
echo

echo "===== FULL trapster-http ====="
mkdir -p docs/conformance/reports/trapster/http/full .local/labs/trapster-telemetry
touch .local/labs/trapster-telemetry/egress-gateway.log
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" \
  -v "$PWD/.local/labs/trapster-community:/honeypot:ro" \
  -v "$PWD/.local/labs/trapster-telemetry:/telemetry:ro" \
  -w /work \
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
rg -n "UHQS|Grade|FINAL|OVERALL" docs/conformance/reports/trapster/http/full/SCORECARD.txt || true
echo

echo "===== FULL trapster-ftp ====="
mkdir -p docs/conformance/reports/trapster/ftp/full .local/labs/trapster-telemetry
touch .local/labs/trapster-telemetry/egress-gateway.log
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" \
  -v "$PWD/.local/labs/trapster-community:/honeypot:ro" \
  -v "$PWD/.local/labs/trapster-telemetry:/telemetry:ro" \
  -w /work \
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
rg -n "UHQS|Grade|FINAL|OVERALL" docs/conformance/reports/trapster/ftp/full/SCORECARD.txt || true
echo

echo "===== FULL trapster-telnet ====="
mkdir -p docs/conformance/reports/trapster/telnet/full .local/labs/trapster-telemetry
touch .local/labs/trapster-telemetry/egress-gateway.log
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" \
  -v "$PWD/.local/labs/trapster-community:/honeypot:ro" \
  -v "$PWD/.local/labs/trapster-telemetry:/telemetry:ro" \
  -w /work \
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
rg -n "UHQS|Grade|FINAL|OVERALL" docs/conformance/reports/trapster/telnet/full/SCORECARD.txt || true
echo

echo "===== FULL dionaea-ftp ====="
mkdir -p docs/conformance/reports/dionaea/ftp/full .local/labs/dionaea-telemetry
touch .local/labs/dionaea-telemetry/egress-gateway.log
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" \
  -v "$PWD/.local/labs/dionaea:/honeypot:ro" \
  -v "$PWD/.local/labs/dionaea-telemetry:/telemetry:ro" \
  -w /work \
  -e PYTHONUNBUFFERED=1 -e UHBS_AIRGAP_ATTESTED=1 \
  -e UHBS_EGRESS_GATEWAY_LOG=/telemetry/egress-gateway.log \
  uhbs:4.0.0-full lab \
    --inventory /work/docs/conformance/labs/dionaea/inventory.yaml \
    --target dionaea-ftp \
    --tps /work/docs/conformance/labs/dionaea/low_interaction_ftp_full.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --concurrency 25 --requests 200 \
    --out /work/docs/conformance/reports/dionaea/ftp/full \
    --environment "Full Docker lab: dionaea-ftp"
rg -n "UHQS|Grade|FINAL|OVERALL" docs/conformance/reports/dionaea/ftp/full/SCORECARD.txt || true
echo

echo "===== FULL dionaea-http ====="
mkdir -p docs/conformance/reports/dionaea/http/full .local/labs/dionaea-telemetry
touch .local/labs/dionaea-telemetry/egress-gateway.log
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" \
  -v "$PWD/.local/labs/dionaea:/honeypot:ro" \
  -v "$PWD/.local/labs/dionaea-telemetry:/telemetry:ro" \
  -w /work \
  -e PYTHONUNBUFFERED=1 -e UHBS_AIRGAP_ATTESTED=1 \
  -e UHBS_EGRESS_GATEWAY_LOG=/telemetry/egress-gateway.log \
  uhbs:4.0.0-full lab \
    --inventory /work/docs/conformance/labs/dionaea/inventory.yaml \
    --target dionaea-http \
    --tps /work/docs/conformance/labs/dionaea/web_api_http_full.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --concurrency 25 --requests 200 \
    --out /work/docs/conformance/reports/dionaea/http/full \
    --environment "Full Docker lab: dionaea-http"
rg -n "UHQS|Grade|FINAL|OVERALL" docs/conformance/reports/dionaea/http/full/SCORECARD.txt || true
echo

echo "===== FULL dionaea-smb ====="
mkdir -p docs/conformance/reports/dionaea/smb/full .local/labs/dionaea-telemetry
touch .local/labs/dionaea-telemetry/egress-gateway.log
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" \
  -v "$PWD/.local/labs/dionaea:/honeypot:ro" \
  -v "$PWD/.local/labs/dionaea-telemetry:/telemetry:ro" \
  -w /work \
  -e PYTHONUNBUFFERED=1 -e UHBS_AIRGAP_ATTESTED=1 \
  -e UHBS_EGRESS_GATEWAY_LOG=/telemetry/egress-gateway.log \
  uhbs:4.0.0-full lab \
    --inventory /work/docs/conformance/labs/dionaea/inventory.yaml \
    --target dionaea-smb \
    --tps /work/docs/conformance/labs/dionaea/low_interaction_smb_full.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --concurrency 25 --requests 200 \
    --out /work/docs/conformance/reports/dionaea/smb/full \
    --environment "Full Docker lab: dionaea-smb"
rg -n "UHQS|Grade|FINAL|OVERALL" docs/conformance/reports/dionaea/smb/full/SCORECARD.txt || true
echo

