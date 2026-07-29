# Tutorial: grade sentrypeer with UHBS

**Upstream:** [https://github.com/SentryPeer/SentryPeer](https://github.com/SentryPeer/SentryPeer) · last push `2026-07-27`

```bash
# Lab container (example — see docs/conformance/labs/sentrypeer/)
docker network create uhbs-lab 2>/dev/null || true

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/sentrypeer-inventory.yaml --target <site> \
  --tps docs/conformance/labs/sentrypeer/*_quick.yaml --protocol sip \
  --quick --skip-sast-tools --out docs/conformance/reports/sentrypeer/sip/quick

UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/sentrypeer-inventory.yaml --target <site> \
  --tps docs/conformance/labs/sentrypeer/*_full.yaml --protocol sip \
  --skip-sast-tools --out docs/conformance/reports/sentrypeer/sip/full
```

Published: quick **43.38 / F**, full **43.38 / F**.
