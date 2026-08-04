# Triage: awesome-honeypots fresh queue (2026-07-29)

**Source:** [paralax/awesome-honeypots](https://github.com/paralax/awesome-honeypots) · age filter last push ≥ 2021-07-29  
**UHBS:** 4.5.1 (no bump)  
**Counts:** grade_now **45** · skip **34** · deferred_unsupported **12** · total **91**

See also: [PLAN.md](PLAN.md) · [DEFERRED-PROTOCOLS.md](DEFERRED-PROTOCOLS.md) · [SKIPPED.md](SKIPPED.md)

## grade_now (45) — UHBS-overlapping protocol honeypots

| Project | Repo | Protocol(s) |
| --- | --- | --- |
| sshesame | jaksi/sshesame | ssh |
| ssh-honeypotd | sjinks/ssh-honeypotd | ssh |
| mysql-honeypotd | sjinks/mysql-honeypotd | mysql |
| node-ftp-honeypot | christophe77/node-ftp-honeypot | ftp |
| express-honeypot | christophe77/express-honeypot | http |
| HellPot | yunginnanet/HellPot | http |
| ssh-auth-logger | JustinAzoff/ssh-auth-logger | ssh |
| Log4Pot | thomaspatzke/Log4Pot | http |
| droberson/ssh-honeypot | droberson/ssh-honeypot | ssh |
| owa-honeypot | joda32/owa-honeypot | http |
| mailoney | phin3has/mailoney | smtp |
| pghoney | betheroot/pghoney | postgres |
| SentryPeer | SentryPeer/SentryPeer | sip |
| honeyhttpd | bocajspear1/honeyhttpd | http |
| honeyup | LogoiLab/honeyup | http |
| wordpot | gbrindisi/wordpot | http |
| MockSSH | ncouture/MockSSH | ssh |
| portlurker | bartnv/portlurker | generic |
| modpot | referefref/modpot | http |
| heralding | johnnykv/heralding | ssh, ftp, telnet, http, smtp, pop3, vnc, postgres |
| FaPro | fofapro/fapro | multi (pick UHBS overlap) |
| snare | mushorg/snare | http |
| shiva | shiva-spampot/shiva | smtp |
| sticky_elephant | betheroot/sticky_elephant | postgres |
| Krawl | BlessedRebuS/Krawl | http |
| Malbait | batchmcnulty/Malbait | generic |
| flux | andrewmichaelsmith/flux | http |
| galah | 0x4D31/galah | http |
| lophiid | mrheinen/lophiid | http |
| Fortigate VPN-SSL Honeypot | PeterGabaldon/Fortigate.VPN-SSL.Honeypot | http |
| blacknet | morian/blacknet | ssh |
| tanner | mushorg/tanner | http |
| glastopf | mushorg/glastopf | http |
| SMTPLLMPot | referefref/SMTPLLMPot | smtp |
| OWASP Python-Honeypot | OWASP/Python-Honeypot | http |
| masscanned | ivre/masscanned | http, ssh, smb, generic |
| glutton | mushorg/glutton | multi |
| HoneyPy | foospidy/HoneyPy | multi |
| telnet-iot-honeypot | Phype/telnet-iot-honeypot | telnet |
| kippo | desaster/kippo | ssh |
| nosqlpot | torque59/nosqlpot | redis |
| honeytrap | honeytrap/honeytrap | multi |
| HoneyPLC | sefcom/honeyplc | s7comm, snmp, http |
| pyRDP | GoSecure/pyrdp | rdp |
| Artillery | BinaryDefense/artillery | generic |


## Graded this batch (quick + full published)

sshesame, ssh-honeypotd, ssh-auth-logger, HellPot, express-honeypot, mailoney, pghoney, mysql-honeypotd, Log4Pot, node-ftp-honeypot, SentryPeer, wordpot, MockSSH, Heralding (SSH+FTP+SMTP), HoneyHTTPD, SHIVA, OWASP Python-Honeypot (HTTP), owa-honeypot, honeyup, modpot, Krawl, flux, fortigate-vpn-ssl, honeytrap (SSH), portlurker (generic), sticky_elephant (postgres), kippo (SSH), nosqlpot (redis), pyRDP (rdp), Artillery (generic).

**Skipped (with published notes):** droberson/ssh-honeypot (missing Docker base); snare (needs Tanner); galah / SMTPLLMPot / lophiid (LLM API keys); tanner (backend, not standalone decoy); glastopf (ubuntu:14.04 image unbuildable); FaPro (binary config load failed); glutton (host net/TPROXY); HoneyPy (Python 2.7); masscanned (NET_ADMIN/userland stack); HoneyPLC (Honeyd/Snap7 host stack); Malbait (not containerized in time); blacknet (master/MySQL/PKI sensor fleet); telnet-iot-honeypot (Python 2 / PEP517 build failure).

**grade_now queue:** complete for this awesome-honeypots fresh triage round (graded or skip-noted). Re-queue skips when hermetic recipes or API keys exist.
