# GenAIPot (ls1911 / Nucleon)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/ls1911/GenAIPot](https://github.com/ls1911/GenAIPot) · tree from zip `205ffe40008f2e76e0decdb01bc19bf8e00acd8a`  
**Runtime:** Docker Hub [`annls/genaipot:latest`](https://hub.docker.com/r/annls/genaipot) (container banner **v0.9.2**, offline templates)

AI-assisted SMTP + POP3 mail honeypot (Twisted). Graded with UHBS in-tree `smtp` and `pop3` plugins in **offline** mode (pre-shipped response templates; no live LLM API).

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [SMTP](smtp/) | yes | **yes** (offline Docker) | [30.9 / F](smtp/quick/) | [30.78 / F](smtp/full/) |
| [POP3](pop3/) | yes | **yes** (offline Docker) | [44.24 / F](pop3/quick/) | [44.13 / F](pop3/full/) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.
