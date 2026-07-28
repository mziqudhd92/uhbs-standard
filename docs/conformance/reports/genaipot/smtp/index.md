# GenAIPot — SMTP

**UHBS:** v4.2.2 · evaluation proof for the `smtp` protocol plugin (Low-Interaction class)  
**Upstream:** [ls1911/GenAIPot](https://github.com/ls1911/GenAIPot) · zip tree `205ffe4` · Docker Hub `annls/genaipot:latest` (image reports **0.9.2**)

| Run | UHQS | Grade | Notes |
| --- | --- | --- | --- |
| [Quick](quick/) | **30.9** | F | δ_C 0.56 · offline AI templates |
| [Full](full/) | **30.78** | F | Prefer full for claim-grade |

SMTP greeting presents as `220 bankers.gov ESMTP` with EHLO capability ads. Module A stayed low: bad-sequence / unknown-command paths often return **500** instead of RFC 5321 **503**, and `QUIT` was observed as `500 Command unrecognized`. POP3 is graded separately under [../pop3/](../pop3/).

## Reproduce

```bash
docker run -d --name genaipot-lab --network uhbs-lab \
  -p 127.0.0.1:2525:25 -p 127.0.0.1:1110:110 \
  annls/genaipot:latest

# Host inventory: .local/genaipot-smtp-inventory.yaml (see TUTORIAL.md)
UHBS_AIRGAP_ATTESTED=1 UHBS_QUICK=1 \
uhbs-lab \
  --inventory .local/genaipot-smtp-inventory.yaml \
  --target genaipot-smtp \
  --tps docs/conformance/labs/genaipot/low_interaction_smtp_quick.yaml \
  --protocol smtp --quick --skip-sast-tools \
  --out docs/conformance/reports/genaipot/smtp/quick
```
