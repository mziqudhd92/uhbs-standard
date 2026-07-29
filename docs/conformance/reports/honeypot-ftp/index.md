# honeypot-ftp (alexbredo)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/alexbredo/honeypot-ftp](https://github.com/alexbredo/honeypot-ftp) · GitHub last push `2024-01-22`  
**Runtime:** `honeypot-ftp:uhbs-lab` (lab stubs for missing `base`/`handler` common-modules; plain FTP only)

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [FTP](ftp/) | yes | **yes** (plain `:21`) | [42.71 / F](ftp/quick/) | [42.6 / F](ftp/full/) |
| FTPS `:990` | yes (`ftp`) | no (lab skips SSL) | — | — |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)
