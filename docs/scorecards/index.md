# Official Benchmark Scorecards

Auditors must publish results using the standard scorecard layout validated by [`schemas/scorecard.schema.json`](https://github.com/mziqudhd92/uhbs-standard/blob/main/schemas/scorecard.schema.json).

UHBS is **vendor-neutral**: decoy **classes** and **protocols** are the normative vocabulary. Named products appear only as **evaluation proof** (not requirements or endorsements).

Full artifacts (tutorials, methodology, `SCORECARD.txt`, `report.json`) live under [Conformance lab reports](../conformance/reports/index.md).

**CTI & blue team:** start with [How to read UHBS lab proof](../conformance/reports/READING-UHQS.md). Each scorecard page includes a module interpretation table (what A–F mean for sensors vs tarpits vs credential sinks).

## Published scorecards (all)

| Scorecard | Class / protocol | Full UHQS | Grade |
| --- | --- | ---: | --- |
| [OpenCanary — FTP](opencanary-ftp.md) | OpenCanary — FTP | **61.5** | D |
| [OpenCanary — GIT](opencanary-git.md) | OpenCanary — GIT | **62.96** | D |
| [OpenCanary — HTTP](opencanary-web-api.md) | OpenCanary — HTTP | **66.02** | D |
| [OpenCanary — MYSQL](opencanary-mysql.md) | OpenCanary — MYSQL | **62.96** | D |
| [OpenCanary — NTP](opencanary-ntp.md) | OpenCanary — NTP | **47.42** | F |
| [OpenCanary — RDP](opencanary-rdp.md) | OpenCanary — RDP | **61.01** | D |
| [OpenCanary — REDIS](opencanary-redis.md) | OpenCanary — REDIS | **53.72** | D |
| [OpenCanary — SIP](opencanary-sip.md) | OpenCanary — SIP | **46.44** | F |
| [OpenCanary — SMB](opencanary-smb.md) | OpenCanary — SMB | **57.72** | D |
| [OpenCanary — SNMP](opencanary-snmp.md) | OpenCanary — SNMP | **47.42** | F |
| [OpenCanary — SSH](opencanary-ssh.md) | OpenCanary — SSH | **35.64** | F |
| [OpenCanary — TELNET](opencanary-telnet.md) | OpenCanary — TELNET | **64.9** | D |
| [OpenCanary — TFTP](opencanary-tftp.md) | OpenCanary — TFTP | **47.42** | F |
| [OpenCanary — VNC](opencanary-vnc.md) | OpenCanary — VNC | **61.99** | D |
| [Beelzebub — HTTP :8080](beelzebub-http.md) | Web-API · HTTP | **66.02** | D |
| [Beelzebub — MCP :8000](beelzebub-mcp.md) | Web-API (MCP v1) · MCP | **42.93** | F |
| [Beelzebub — Redis :6379](beelzebub-redis.md) | Low-Interaction · Redis | **61.01** | D |
| [Beelzebub — SSH :2222](beelzebub-ssh.md) | Low-Interaction · SSH | **59.88** | D |
| [Beelzebub — Telnet :23](beelzebub-telnet.md) | Low-Interaction · Telnet | **47.89** | F |
| [Cowrie — SSH :2222](cowrie-ssh.md) | Low-Interaction · SSH | **61.37** | D |
| [Cowrie — Telnet :2223](cowrie-telnet.md) | Low-Interaction · Telnet | **64.9** | D |
| [DataTrap — HTTP :8080](datatrap-http.md) | Web-API · HTTP | **65.85** | D |
| [DataTrap — MYSQL :3306](datatrap-mysql.md) | Low-Interaction · MYSQL | **50.65** | D |
| [DataTrap — PostgreSQL :5432](datatrap-postgres.md) | Low-Interaction · PostgreSQL | **57.94** | D |
| [DataTrap — REDIS :6379](datatrap-redis.md) | Low-Interaction · REDIS | **60.85** | D |
| [DataTrap — SSH :2222](datatrap-ssh.md) | Low-Interaction · SSH | **55.61** | D |
| [DataTrap — TELNET :2323](datatrap-telnet.md) | Low-Interaction · TELNET | **59.88** | D |
| [Dionaea — FTP :21](dionaea-ftp.md) | Low-Interaction · FTP | **57.96** | D |
| [Dionaea — HTTP :80](dionaea-http.md) | Web-API · HTTP | **51.14** | D |
| [Dionaea — SMB :445](dionaea-smb.md) | Low-Interaction · SMB | **54.07** | D |
| [elastichoney — http](elastichoney-http.md) | Web-API · http | **45.73** | F |
| [express-honeypot — http](express-honeypot-http.md) | Web-API · http | **45.73** | F |
| [genaipot — pop3](genaipot-pop3.md) | Low-Interaction · pop3 | **44.13** | F |
| [genaipot — smtp](genaipot-smtp.md) | Low-Interaction · smtp | **30.78** | F |
| [HellPot — http](hellpot-http.md) | Web-API · http | **43.87** | F |
| [HoneyWire — http](honeywire-http.md) | Web-API · http | **45.84** | F |
| [heralding — ftp](heralding-ftp.md) | Low-Interaction · ftp | **35.85** | F |
| [heralding — smtp](heralding-smtp.md) | Low-Interaction · smtp | **45.07** | F |
| [owasp-python-honeypot — http](owasp-python-honeypot-http.md) | Web-API · http | **43.98** | F |
| [owa-honeypot — http](owa-honeypot-http.md) | Web-API · http | **41.71** | F |
| [honeyup — http](honeyup-http.md) | Web-API · http | **50.91** | D |
| [modpot — http](modpot-http.md) | Web-API · http | **50.91** | D |
| [Krawl — http](krawl-http.md) | Web-API · http | **50.91** | D |
| [flux — http](flux-http.md) | Web-API · http | **50.91** | D |
| [fortigate-vpn-ssl — http](fortigate-vpn-ssl-http.md) | Web-API · http | **46.78** | F |
| [honeytrap — ssh](honeytrap-ssh.md) | Low-Interaction · ssh | **44.38** | F |
| [portlurker — generic](portlurker-generic.md) | Low-Interaction · generic | **39.84** | F |
| [sticky_elephant — postgres](sticky_elephant-postgres.md) | Low-Interaction · postgres | **38.06** | F |
| [kippo — ssh](kippo-ssh.md) | Low-Interaction · ssh | **35.64** | F |
| [nosqlpot — redis](nosqlpot-redis.md) | Low-Interaction · redis | **40.08** | F |
| [pyRDP — rdp](pyrdp-rdp.md) | Low-Interaction · rdp | **33.93** | F |
| [Artillery — generic](artillery-generic.md) | Low-Interaction · generic | **37.55** | F |
| [heralding — ssh](heralding-ssh.md) | Low-Interaction · ssh | **44.18** | F |
| [HoneyAgents — SSH :2222](honeyagents-ssh.md) | Low-Interaction · SSH | **65.24** | D |
| [honeyhttpd — http](honeyhttpd-http.md) | Web-API · http | **45.73** | F |
| [HoneyMCP — MCP :8080](honeymcp-mcp.md) | Web-API (MCP v1) · MCP | **42.93** | F |
| [honeypot-ftp — ftp](honeypot-ftp.md) | Low-Interaction · ftp | **42.6** | F |
| [ICS-SCADA / Modbus decoy (Conpot proof)](conpot-ics-scada.md) | Scorecard: ICS-SCADA / Modbus decoy (Conpot proof) | — | — |
| [LLM Honeypot (Palisade) — SSH :2222](llm-honeypot-ssh.md) | Low-Interaction · SSH | **61.17** | D |
| [LLMPot — HTTP (WAGO WBM) :8080](llmpot-http.md) | Web-API · HTTP | **63.11** | D |
| [LLMPot — Modbus TCP :5020](llmpot-modbus.md) | ICS-SCADA · Modbus TCP | **55.24** | D |
| [LLMPot — S7comm :102](llmpot-s7comm.md) | ICS-SCADA · S7comm | **65.41** | D |
| [Log4Pot — http](log4pot-http.md) | Web-API · http | **38.0** | F |
| [Low-Interaction / PJL decoy (miniprint proof)](miniprint-low-interaction.md) | Scorecard: Low-Interaction / PJL decoy (miniprint proof) | — | — |
| [Low-Interaction / SSH tarpit (Endlessh proof)](endlessh-ssh-tarpit.md) | Scorecard: Low-Interaction / SSH tarpit (Endlessh proof) | — | — |
| [mailoney — smtp](mailoney-smtp.md) | Low-Interaction · smtp | **38.69** | F |
| [mockssh — ssh](mockssh-ssh.md) | Low-Interaction · ssh | **59.0** | D |
| [mysql-honeypotd — mysql](mysql-honeypotd-mysql.md) | Low-Interaction · mysql | **37.94** | F |
| [node-ftp-honeypot — ftp](node-ftp-honeypot-ftp.md) | Low-Interaction · ftp | **35.85** | F |
| [pghoney — postgres](pghoney-postgres.md) | Low-Interaction · postgres | **43.61** | F |
| [qeeqbox/honeypots — ftp](qeeqbox-ftp.md) | Low-Interaction · ftp | **40.31** | F |
| [qeeqbox/honeypots — http](qeeqbox-http.md) | Web-API · http | **45.73** | F |
| [qeeqbox/honeypots — mysql](qeeqbox-mysql.md) | Database · mysql | **34.27** | F |
| [qeeqbox/honeypots — pop3](qeeqbox-pop3.md) | Low-Interaction · pop3 | **30.94** | F |
| [qeeqbox/honeypots — postgres](qeeqbox-postgres.md) | Database · postgres | **34.27** | F |
| [qeeqbox/honeypots — redis](qeeqbox-redis.md) | Low-Interaction · redis | **34.5** | F |
| [qeeqbox/honeypots — smtp](qeeqbox-smtp.md) | Low-Interaction · smtp | **30.78** | F |
| [qeeqbox/honeypots — ssh](qeeqbox-ssh.md) | Low-Interaction · ssh | **59.68** | D |
| [qeeqbox/honeypots — telnet](qeeqbox-telnet.md) | Low-Interaction · telnet | **29.77** | F |
| [qeeqbox/honeypots — vnc](qeeqbox-vnc.md) | Low-Interaction · vnc | **32.81** | F |
| [sentrypeer — sip](sentrypeer-sip.md) | Low-Interaction · sip | **43.38** | F |
| [shiva — smtp](shiva-smtp.md) | Low-Interaction · smtp | **44.96** | F |
| [ssh-auth-logger — ssh](ssh-auth-logger-ssh.md) | Low-Interaction · ssh | **44.38** | F |
| [ssh-honeypotd — ssh](ssh-honeypotd-ssh.md) | Low-Interaction · ssh | **44.38** | F |
| [sshesame — ssh](sshesame-ssh.md) | Low-Interaction · ssh | **61.06** | D |
| [Trapster Community — FTP :2121](trapster-ftp.md) | Low-Interaction · FTP | **51.78** | D |
| [Trapster Community — HTTP :8080](trapster-http.md) | Web-API · HTTP | **63.33** | D |
| [Trapster Community — SSH :2222](trapster-ssh.md) | Low-Interaction · SSH | **44.38** | F |
| [Trapster Community — Telnet :2323](trapster-telnet.md) | Low-Interaction · Telnet | **64.9** | D |
| [Web-API / HTTP decoy (ESPot proof)](espot-web-api.md) | Scorecard: Web-API / HTTP decoy (ESPot proof) | — | — |
| [wordpot — http](wordpot-http.md) | Web-API · http | **41.6** | F |

### Synthetic layout sample (not a lab run)

- [Illustrative POSIX-Shell / GenAI-Augmented Decoy](illustrative-posix-genai.md) — vendor-neutral **layout** sample only

## Badge Snippets

After an official evaluation, maintainers can embed:

```markdown
![UHBS v4.3.0 Grade A](https://img.shields.io/badge/UHBS%20v4.3.0-Grade%20A-brightgreen)
![UHBS v4.3.0 Grade B](https://img.shields.io/badge/UHBS%20v4.3.0-Grade%20B-yellowgreen)
![UHBS v4.3.0 Grade C](https://img.shields.io/badge/UHBS%20v4.3.0-Grade%20C-yellow)
![UHBS v4.3.0 Grade D](https://img.shields.io/badge/UHBS%20v4.3.0-Grade%20D-orange)
![UHBS v4.3.0 Grade F](https://img.shields.io/badge/UHBS%20v4.3.0-Grade%20F-red)
```

## Submitting a Scorecard

1. Complete a TPS `profile.yaml`
2. Run the five-phase audit
3. Emit a scorecard conforming to the schema
4. Open a PR or issue using the **Profile / Scorecard Submission** template

Validate a published fixture locally:

```bash
uhbs validate-scorecard docs/conformance/fixtures/espot-web-api.scorecard.json --strict
```
