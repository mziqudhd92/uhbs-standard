# GenAIPot — POP3

**UHBS:** v4.2.2 · evaluation proof for the `pop3` protocol plugin (Low-Interaction class)  
**Upstream:** [ls1911/GenAIPot](https://github.com/ls1911/GenAIPot) · zip tree `205ffe4` · Docker Hub `annls/genaipot:latest` (image reports **0.9.2**)

| Run | UHQS | Grade | Notes |
| --- | --- | --- | --- |
| [Quick](quick/) | **44.24** | F | δ_C 0.56 · offline AI templates |
| [Full](full/) | **44.13** | F | Prefer full for claim-grade |

POP3 greeting `+OK … POP3 server ready`; pre-auth `STAT`/`LIST` correctly return `-ERR`. `CAPA` is unsupported (`-ERR`) — scored as honest non-support. Module A ~95; Safety Gate (δ_C 0.56) dominates the composite.

## Reproduce

```bash
# Same genaipot-lab container as SMTP (see ../TUTORIAL.md)
UHBS_AIRGAP_ATTESTED=1 UHBS_QUICK=1 \
uhbs-lab \
  --inventory .local/genaipot-pop3-inventory.yaml \
  --target genaipot-pop3 \
  --tps docs/conformance/labs/genaipot/low_interaction_pop3_quick.yaml \
  --protocol pop3 --quick --skip-sast-tools \
  --out docs/conformance/reports/genaipot/pop3/quick
```
