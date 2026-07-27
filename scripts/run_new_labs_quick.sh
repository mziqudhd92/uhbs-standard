#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

echo "===== QUICK beelzebub-ssh ====="
mkdir -p docs/conformance/reports/beelzebub/ssh/quick
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" \
  -v "$PWD/.local/labs/beelzebub:/honeypot:ro" \
  -w /work \
  -e UHBS_QUICK=1 -e UHBS_AIRGAP_ATTESTED=1 -e PYTHONUNBUFFERED=1 \
  uhbs:4.0.0 lab \
    --inventory /work/docs/conformance/labs/beelzebub/inventory.yaml \
    --target beelzebub-ssh \
    --tps /work/docs/conformance/labs/beelzebub/low_interaction_ssh_quick.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --quick --skip-sast-tools --concurrency 10 --requests 50 \
    --out /work/docs/conformance/reports/beelzebub/ssh/quick \
    --environment "Quick Docker lab: beelzebub-ssh"
rg -n "UHQS|Grade|delta" docs/conformance/reports/beelzebub/ssh/quick/SCORECARD.txt || true
echo

echo "===== QUICK beelzebub-http ====="
mkdir -p docs/conformance/reports/beelzebub/http/quick
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" \
  -v "$PWD/.local/labs/beelzebub:/honeypot:ro" \
  -w /work \
  -e UHBS_QUICK=1 -e UHBS_AIRGAP_ATTESTED=1 -e PYTHONUNBUFFERED=1 \
  uhbs:4.0.0 lab \
    --inventory /work/docs/conformance/labs/beelzebub/inventory.yaml \
    --target beelzebub-http \
    --tps /work/docs/conformance/labs/beelzebub/web_api_http_quick.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --quick --skip-sast-tools --concurrency 10 --requests 50 \
    --out /work/docs/conformance/reports/beelzebub/http/quick \
    --environment "Quick Docker lab: beelzebub-http"
rg -n "UHQS|Grade|delta" docs/conformance/reports/beelzebub/http/quick/SCORECARD.txt || true
echo

echo "===== QUICK beelzebub-telnet ====="
mkdir -p docs/conformance/reports/beelzebub/telnet/quick
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" \
  -v "$PWD/.local/labs/beelzebub:/honeypot:ro" \
  -w /work \
  -e UHBS_QUICK=1 -e UHBS_AIRGAP_ATTESTED=1 -e PYTHONUNBUFFERED=1 \
  uhbs:4.0.0 lab \
    --inventory /work/docs/conformance/labs/beelzebub/inventory.yaml \
    --target beelzebub-telnet \
    --tps /work/docs/conformance/labs/beelzebub/low_interaction_telnet_quick.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --quick --skip-sast-tools --concurrency 10 --requests 50 \
    --out /work/docs/conformance/reports/beelzebub/telnet/quick \
    --environment "Quick Docker lab: beelzebub-telnet"
rg -n "UHQS|Grade|delta" docs/conformance/reports/beelzebub/telnet/quick/SCORECARD.txt || true
echo

echo "===== QUICK beelzebub-redis ====="
mkdir -p docs/conformance/reports/beelzebub/redis/quick
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" \
  -v "$PWD/.local/labs/beelzebub:/honeypot:ro" \
  -w /work \
  -e UHBS_QUICK=1 -e UHBS_AIRGAP_ATTESTED=1 -e PYTHONUNBUFFERED=1 \
  uhbs:4.0.0 lab \
    --inventory /work/docs/conformance/labs/beelzebub/inventory.yaml \
    --target beelzebub-redis \
    --tps /work/docs/conformance/labs/beelzebub/low_interaction_redis_quick.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --quick --skip-sast-tools --concurrency 10 --requests 50 \
    --out /work/docs/conformance/reports/beelzebub/redis/quick \
    --environment "Quick Docker lab: beelzebub-redis"
rg -n "UHQS|Grade|delta" docs/conformance/reports/beelzebub/redis/quick/SCORECARD.txt || true
echo

echo "===== QUICK trapster-ssh ====="
mkdir -p docs/conformance/reports/trapster/ssh/quick
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" \
  -v "$PWD/.local/labs/trapster-community:/honeypot:ro" \
  -w /work \
  -e UHBS_QUICK=1 -e UHBS_AIRGAP_ATTESTED=1 -e PYTHONUNBUFFERED=1 \
  uhbs:4.0.0 lab \
    --inventory /work/docs/conformance/labs/trapster/inventory.yaml \
    --target trapster-ssh \
    --tps /work/docs/conformance/labs/trapster/low_interaction_ssh_quick.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --quick --skip-sast-tools --concurrency 10 --requests 50 \
    --out /work/docs/conformance/reports/trapster/ssh/quick \
    --environment "Quick Docker lab: trapster-ssh"
rg -n "UHQS|Grade|delta" docs/conformance/reports/trapster/ssh/quick/SCORECARD.txt || true
echo

echo "===== QUICK trapster-http ====="
mkdir -p docs/conformance/reports/trapster/http/quick
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" \
  -v "$PWD/.local/labs/trapster-community:/honeypot:ro" \
  -w /work \
  -e UHBS_QUICK=1 -e UHBS_AIRGAP_ATTESTED=1 -e PYTHONUNBUFFERED=1 \
  uhbs:4.0.0 lab \
    --inventory /work/docs/conformance/labs/trapster/inventory.yaml \
    --target trapster-http \
    --tps /work/docs/conformance/labs/trapster/web_api_http_quick.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --quick --skip-sast-tools --concurrency 10 --requests 50 \
    --out /work/docs/conformance/reports/trapster/http/quick \
    --environment "Quick Docker lab: trapster-http"
rg -n "UHQS|Grade|delta" docs/conformance/reports/trapster/http/quick/SCORECARD.txt || true
echo

echo "===== QUICK trapster-ftp ====="
mkdir -p docs/conformance/reports/trapster/ftp/quick
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" \
  -v "$PWD/.local/labs/trapster-community:/honeypot:ro" \
  -w /work \
  -e UHBS_QUICK=1 -e UHBS_AIRGAP_ATTESTED=1 -e PYTHONUNBUFFERED=1 \
  uhbs:4.0.0 lab \
    --inventory /work/docs/conformance/labs/trapster/inventory.yaml \
    --target trapster-ftp \
    --tps /work/docs/conformance/labs/trapster/low_interaction_ftp_quick.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --quick --skip-sast-tools --concurrency 10 --requests 50 \
    --out /work/docs/conformance/reports/trapster/ftp/quick \
    --environment "Quick Docker lab: trapster-ftp"
rg -n "UHQS|Grade|delta" docs/conformance/reports/trapster/ftp/quick/SCORECARD.txt || true
echo

echo "===== QUICK trapster-telnet ====="
mkdir -p docs/conformance/reports/trapster/telnet/quick
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" \
  -v "$PWD/.local/labs/trapster-community:/honeypot:ro" \
  -w /work \
  -e UHBS_QUICK=1 -e UHBS_AIRGAP_ATTESTED=1 -e PYTHONUNBUFFERED=1 \
  uhbs:4.0.0 lab \
    --inventory /work/docs/conformance/labs/trapster/inventory.yaml \
    --target trapster-telnet \
    --tps /work/docs/conformance/labs/trapster/low_interaction_telnet_quick.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --quick --skip-sast-tools --concurrency 10 --requests 50 \
    --out /work/docs/conformance/reports/trapster/telnet/quick \
    --environment "Quick Docker lab: trapster-telnet"
rg -n "UHQS|Grade|delta" docs/conformance/reports/trapster/telnet/quick/SCORECARD.txt || true
echo

echo "===== QUICK dionaea-ftp ====="
mkdir -p docs/conformance/reports/dionaea/ftp/quick
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" \
  -v "$PWD/.local/labs/dionaea:/honeypot:ro" \
  -w /work \
  -e UHBS_QUICK=1 -e UHBS_AIRGAP_ATTESTED=1 -e PYTHONUNBUFFERED=1 \
  uhbs:4.0.0 lab \
    --inventory /work/docs/conformance/labs/dionaea/inventory.yaml \
    --target dionaea-ftp \
    --tps /work/docs/conformance/labs/dionaea/low_interaction_ftp_quick.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --quick --skip-sast-tools --concurrency 10 --requests 50 \
    --out /work/docs/conformance/reports/dionaea/ftp/quick \
    --environment "Quick Docker lab: dionaea-ftp"
rg -n "UHQS|Grade|delta" docs/conformance/reports/dionaea/ftp/quick/SCORECARD.txt || true
echo

echo "===== QUICK dionaea-http ====="
mkdir -p docs/conformance/reports/dionaea/http/quick
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" \
  -v "$PWD/.local/labs/dionaea:/honeypot:ro" \
  -w /work \
  -e UHBS_QUICK=1 -e UHBS_AIRGAP_ATTESTED=1 -e PYTHONUNBUFFERED=1 \
  uhbs:4.0.0 lab \
    --inventory /work/docs/conformance/labs/dionaea/inventory.yaml \
    --target dionaea-http \
    --tps /work/docs/conformance/labs/dionaea/web_api_http_quick.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --quick --skip-sast-tools --concurrency 10 --requests 50 \
    --out /work/docs/conformance/reports/dionaea/http/quick \
    --environment "Quick Docker lab: dionaea-http"
rg -n "UHQS|Grade|delta" docs/conformance/reports/dionaea/http/quick/SCORECARD.txt || true
echo

echo "===== QUICK dionaea-smb ====="
mkdir -p docs/conformance/reports/dionaea/smb/quick
docker run --rm --network uhbs-lab \
  -v "$PWD:/work" \
  -v "$PWD/.local/labs/dionaea:/honeypot:ro" \
  -w /work \
  -e UHBS_QUICK=1 -e UHBS_AIRGAP_ATTESTED=1 -e PYTHONUNBUFFERED=1 \
  uhbs:4.0.0 lab \
    --inventory /work/docs/conformance/labs/dionaea/inventory.yaml \
    --target dionaea-smb \
    --tps /work/docs/conformance/labs/dionaea/low_interaction_smb_quick.yaml \
    --phases profile,static,sandbox,dynamic,score --modules A,B,C,D,E,F \
    --quick --skip-sast-tools --concurrency 10 --requests 50 \
    --out /work/docs/conformance/reports/dionaea/smb/quick \
    --environment "Quick Docker lab: dionaea-smb"
rg -n "UHQS|Grade|delta" docs/conformance/reports/dionaea/smb/quick/SCORECARD.txt || true
echo

