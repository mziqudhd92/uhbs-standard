# Official Benchmark Scorecards

Auditors must publish results using the standard scorecard layout validated by [`schemas/scorecard.schema.json`](https://github.com/mziqudhd92/uhbs-standard/blob/main/schemas/scorecard.schema.json).

UHBS is **vendor-neutral**: decoy **classes** and **protocols** are the normative vocabulary. Named products appear only as **evaluation proof** (not requirements or endorsements). The three scorecards below are sanitized fixtures from live Docker lab runs; full artifacts and tutorials live under [Conformance lab reports](../conformance/reports/index.md).

## Examples

Published **full** UHBS-Lab scorecards (evaluated 2026-07-27):

| Scorecard | Class / protocol | UHQS | Grade | Fixture |
| --- | --- | ---: | --- | --- |
| [Web-API / HTTP decoy (ESPot proof)](espot-web-api.md) | Web-API · HTTP `:9200` | **49.82** | F | [`espot-web-api.scorecard.json`](../conformance/fixtures/espot-web-api.scorecard.json) |
| [Low-Interaction / PJL decoy (miniprint proof)](miniprint-low-interaction.md) | Low-Interaction · PJL `:9100` | **47.77** | F | [`miniprint-low-interaction.scorecard.json`](../conformance/fixtures/miniprint-low-interaction.scorecard.json) |
| [ICS-SCADA / Modbus decoy (Conpot proof)](conpot-ics-scada.md) | ICS-SCADA · Modbus `:5020` | **55.51** | D | [`conpot-ics-scada.scorecard.json`](../conformance/fixtures/conpot-ics-scada.scorecard.json) |
| [Low-Interaction / SSH decoy (Cowrie proof)](cowrie-ssh.md) | Low-Interaction · SSH `:2222` | **61.37** | D | [`cowrie-ssh.scorecard.json`](../conformance/fixtures/cowrie-ssh.scorecard.json) |
| [Low-Interaction / Telnet decoy (Cowrie proof)](cowrie-telnet.md) | Low-Interaction · Telnet `:2223` | **64.90** | D | [`cowrie-telnet.scorecard.json`](../conformance/fixtures/cowrie-telnet.scorecard.json) |
| [OpenCanary HTTP](opencanary-web-api.md) | Web-API · HTTP :80 | **66.02** | D | [`opencanary-web-api.scorecard.json`](../conformance/fixtures/opencanary-web-api.scorecard.json) |
| [OpenCanary FTP](opencanary-ftp.md) | Low-Interaction · FTP :21 | **61.5** | D | [`opencanary-ftp.scorecard.json`](../conformance/fixtures/opencanary-ftp.scorecard.json) |
| [OpenCanary SSH](opencanary-ssh.md) | Low-Interaction · SSH :2222 | **35.64** | F | [`opencanary-ssh.scorecard.json`](../conformance/fixtures/opencanary-ssh.scorecard.json) |
| [OpenCanary TELNET](opencanary-telnet.md) | Low-Interaction · Telnet :23 | **64.9** | D | [`opencanary-telnet.scorecard.json`](../conformance/fixtures/opencanary-telnet.scorecard.json) |
| [OpenCanary REDIS](opencanary-redis.md) | Low-Interaction · Redis :6379 | **53.72** | D | [`opencanary-redis.scorecard.json`](../conformance/fixtures/opencanary-redis.scorecard.json) |
| [OpenCanary MYSQL](opencanary-mysql.md) | Low-Interaction · MySQL :3306 | **62.96** | D | [`opencanary-mysql.scorecard.json`](../conformance/fixtures/opencanary-mysql.scorecard.json) |
| [OpenCanary RDP](opencanary-rdp.md) | Low-Interaction · RDP :3389 | **61.01** | D | [`opencanary-rdp.scorecard.json`](../conformance/fixtures/opencanary-rdp.scorecard.json) |
| [OpenCanary SIP](opencanary-sip.md) | Low-Interaction · SIP :5060 | **46.44** | F | [`opencanary-sip.scorecard.json`](../conformance/fixtures/opencanary-sip.scorecard.json) |
| [OpenCanary SNMP](opencanary-snmp.md) | Low-Interaction · SNMP :161 | **47.42** | F | [`opencanary-snmp.scorecard.json`](../conformance/fixtures/opencanary-snmp.scorecard.json) |
| [OpenCanary NTP](opencanary-ntp.md) | Low-Interaction · NTP :123 | **47.42** | F | [`opencanary-ntp.scorecard.json`](../conformance/fixtures/opencanary-ntp.scorecard.json) |
| [OpenCanary TFTP](opencanary-tftp.md) | Low-Interaction · TFTP :69 | **47.42** | F | [`opencanary-tftp.scorecard.json`](../conformance/fixtures/opencanary-tftp.scorecard.json) |
| [OpenCanary VNC](opencanary-vnc.md) | Low-Interaction · VNC :5900 | **61.99** | D | [`opencanary-vnc.scorecard.json`](../conformance/fixtures/opencanary-vnc.scorecard.json) |
| [OpenCanary GIT](opencanary-git.md) | Low-Interaction · Git :9418 | **62.96** | D | [`opencanary-git.scorecard.json`](../conformance/fixtures/opencanary-git.scorecard.json) |
| [OpenCanary SMB](opencanary-smb.md) | Low-Interaction · SMB :445 | **57.72** | D | [`opencanary-smb.scorecard.json`](../conformance/fixtures/opencanary-smb.scorecard.json) |
| [Low-Interaction / SSH tarpit (Endlessh proof)](endlessh-ssh-tarpit.md) | Low-Interaction · `ssh_tarpit` `:2222` | **51.90** | D | [`endlessh-low-interaction.scorecard.json`](../conformance/fixtures/endlessh-low-interaction.scorecard.json) |
| [Beelzebub HTTP](beelzebub-http.md) | Web-API · HTTP `:8080` | **50.12** | D | [`beelzebub-http.scorecard.json`](../conformance/fixtures/beelzebub-http.scorecard.json) |
| [Beelzebub SSH](beelzebub-ssh.md) | Low-Interaction · SSH `:2222` | **45.74** | F | [`beelzebub-ssh.scorecard.json`](../conformance/fixtures/beelzebub-ssh.scorecard.json) |
| [Beelzebub Telnet](beelzebub-telnet.md) | Low-Interaction · Telnet `:23` | **57.00** | D | [`beelzebub-telnet.scorecard.json`](../conformance/fixtures/beelzebub-telnet.scorecard.json) |
| [Beelzebub Redis](beelzebub-redis.md) | Low-Interaction · Redis `:6379` | **55.55** | D | [`beelzebub-redis.scorecard.json`](../conformance/fixtures/beelzebub-redis.scorecard.json) |
| [Trapster HTTP](trapster-http.md) | Web-API · HTTP `:8080` | **49.82** | F | [`trapster-http.scorecard.json`](../conformance/fixtures/trapster-http.scorecard.json) |
| [Trapster SSH](trapster-ssh.md) | Low-Interaction · SSH `:2222` | **30.24** | F | [`trapster-ssh.scorecard.json`](../conformance/fixtures/trapster-ssh.scorecard.json) |
| [Trapster FTP](trapster-ftp.md) | Low-Interaction · FTP `:2121` | **49.71** | F | [`trapster-ftp.scorecard.json`](../conformance/fixtures/trapster-ftp.scorecard.json) |
| [Trapster Telnet](trapster-telnet.md) | Low-Interaction · Telnet `:2323` | **57.00** | D | [`trapster-telnet.scorecard.json`](../conformance/fixtures/trapster-telnet.scorecard.json) |
| [Dionaea FTP](dionaea-ftp.md) | Low-Interaction · FTP `:21` | **55.30** | D | [`dionaea-ftp.scorecard.json`](../conformance/fixtures/dionaea-ftp.scorecard.json) |
| [Dionaea HTTP](dionaea-http.md) | Web-API · HTTP `:80` | **43.54** | F | [`dionaea-http.scorecard.json`](../conformance/fixtures/dionaea-http.scorecard.json) |
| [Dionaea SMB](dionaea-smb.md) | Low-Interaction · SMB `:445` | **48.74** | F | [`dionaea-smb.scorecard.json`](../conformance/fixtures/dionaea-smb.scorecard.json) |

Each page links to the matching report hub (`quick/` + `full/` scorecards, `report.json`, methodology, tutorial).

### Synthetic layout sample (not a lab run)

- [Illustrative POSIX-Shell / GenAI-Augmented Decoy](illustrative-posix-genai.md) — vendor-neutral **layout** sample only (evaluated 2026-07-26)

## Badge Snippets

After an official evaluation, maintainers can embed:

```markdown
![UHBS v4.0 Grade A](https://img.shields.io/badge/UHBS%20v4.0-Grade%20A-brightgreen)
![UHBS v4.0 Grade B](https://img.shields.io/badge/UHBS%20v4.0-Grade%20B-yellowgreen)
![UHBS v4.0 Grade C](https://img.shields.io/badge/UHBS%20v4.0-Grade%20C-yellow)
![UHBS v4.0 Grade D](https://img.shields.io/badge/UHBS%20v4.0-Grade%20D-orange)
![UHBS v4.0 Grade F](https://img.shields.io/badge/UHBS%20v4.0-Grade%20F-red)
```

## Submitting a Scorecard

1. Complete a TPS `profile.yaml`
2. Run the five-phase audit
3. Emit a scorecard conforming to the schema
4. Open a PR or issue using the **Profile / Scorecard Submission** template

Validate a published fixture locally:

```bash
uhbs validate-scorecard docs/conformance/fixtures/espot-web-api.scorecard.json --strict
uhbs validate-scorecard docs/conformance/fixtures/miniprint-low-interaction.scorecard.json --strict
uhbs validate-scorecard docs/conformance/fixtures/conpot-ics-scada.scorecard.json --strict
uhbs validate-scorecard docs/conformance/fixtures/cowrie-low-interaction.scorecard.json --strict
uhbs validate-scorecard docs/conformance/fixtures/endlessh-low-interaction.scorecard.json --strict
uhbs validate-scorecard docs/conformance/fixtures/opencanary-web-api.scorecard.json --strict
```
