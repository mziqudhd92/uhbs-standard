# Tutorial: grade FortiGate VPN-SSL Honeypot with UHBS (HTTP)

**Upstream:** [PeterGabaldon/Fortigate.VPN-SSL.Honeypot](https://github.com/PeterGabaldon/Fortigate.VPN-SSL.Honeypot)

```bash
docker build -f .local/labs/fortigate-vpn-ssl/Dockerfile.lab -t fortigate-vpn-ssl:uhbs-lab .local/labs/fortigate-vpn-ssl
docker run -d --name fortigate-vpn-ssl-lab --network uhbs-lab -p 127.0.0.1:18095:5000 fortigate-vpn-ssl:uhbs-lab

UHBS_QUICK=1 UHBS_AIRGAP_ATTESTED=1 uhbs-lab \
  --inventory .local/fortigate-vpn-ssl-inventory.yaml --target fortigate-vpn-ssl-http \
  --tps docs/conformance/labs/fortigate-vpn-ssl/web_api_http_quick.yaml --protocol http \
  --phases profile,static,sandbox,dynamic,score --quick --skip-sast-tools \
  --out docs/conformance/reports/fortigate-vpn-ssl/http/quick
```

Published: quick **46.78 / F**, full **46.78 / F**.

## What you get from this lab

After a successful run you should have `SCORECARD.txt`, `report.json`, and optional harness logs under the lab telemetry directory.

## How CTI / blue team should use the artifacts

1. Open the **full** SCORECARD first (authoritative).
2. Read modules **A–F** with [READING-UHQS.md](../READING-UHQS.md).
3. Confirm **δ_C** before citing UHQS externally.
4. Wire your own log shipping; Module C is harness visibility.

## Trust limits

UHBS 4.2.2 evaluation proof is **informative** — not a certification or endorsement.
