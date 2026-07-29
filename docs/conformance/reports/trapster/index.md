# Trapster Community (UHBS multi-protocol proof)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/0xBallpoint/trapster-community](https://github.com/0xBallpoint/trapster-community) · commit `dfc2c43dad119578f9c7344a0077790ed7fee01b`  
**Scope:** Every UHBS-native protocol plugin that the lab container exposed was graded separately (quick + full).

| Protocol | Class / port | Quick | Full |
| --- | --- | --- | --- |
| [FTP](ftp/index.md) | Low-Interaction · FTP :2121 | [43.37 / F](ftp/quick/README.md) | [51.78 / D](ftp/full/README.md) |
| [HTTP](http/index.md) | Web-API · HTTP :8080 | [50.13 / D](http/quick/README.md) | [63.33 / D](http/full/README.md) |
| [SSH](ssh/index.md) | Low-Interaction · SSH :2222 | [40.06 / F](ssh/quick/README.md) | [44.38 / F](ssh/full/README.md) |
| [Telnet](telnet/index.md) | Low-Interaction · Telnet :2323 | [52.49 / D](telnet/quick/README.md) | [64.9 / D](telnet/full/README.md) |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.


## What this decoy is

Community multi-protocol honeypot graded on SSH/HTTP/FTP/Telnet in UHBS labs.

## For CTI analysts

- Per-protocol results vary — read each protocol hub.

**Primary signals:** Per-protocol connection/auth events.

## For blue teams / detection engineering

- Enable minimal listeners; verify logging destinations before Internet exposure.

## Trust & limitations

- Evaluation proof under UHBS 4.2.2 — not a certification or endorsement.
- Prefer **full/** over **quick/** for decisions.
- Reading guide: [READING-UHQS.md](../READING-UHQS.md).
