# Cleanup: remove or fix broken GitHub links in awesome-honeypots

## Summary

This PR (or issue) proposes cleaning **broken / removed GitHub repositories** currently linked from
[paralax/awesome-honeypots](https://github.com/paralax/awesome-honeypots).

Checked on **2026-07-29** via GitHub API (`GET /repos/{owner}/{repo}`).
Links that return **404 Not Found** are listed below.

## Broken links (removed or inaccessible)

| Listed name | Broken URL | HTTP / API status | Suggested action |
| --- | --- | --- | --- |
| GetPageSpeed/nginx-honeypot | https://github.com/GetPageSpeed/nginx-honeypot | `not_found` (README ~L87) | Remove entry. |
| InnerWarden/innerwarden | https://github.com/InnerWarden/innerwarden | `not_found` (README ~L384) | Remove entry. |
| ls1911/GenAIPot | https://github.com/ls1911/GenAIPot | `not_found` (README ~L113) | Replace with a live fork if one is maintained, or remove the entry. |
| Novetta/delilah | https://github.com/Novetta/delilah | `not_found` (README ~L34) | Remove, or point to any maintained fork if documented. |
| packetflare/amthoneypot | https://github.com/packetflare/amthoneypot | `not_found` (README ~L107) | Remove entry. |
| schmalle/honeyalarmg2 | https://github.com/schmalle/honeyalarmg2 | `not_found` (README ~L554) | Remove entry (or replace if relocated). |
| shjalayeri/pwnypot | https://github.com/shjalayeri/pwnypot | `not_found` (README ~L354) | Remove entry. |
| threatstream/mhn | https://github.com/threatstream/mhn | `not_found` (README ~L204) | MHN upstream moved/removed — update to current Modern Honey Network home or remove. |
| threatstream/shockpot | https://github.com/threatstream/shockpot | `not_found` (README ~L90) | Remove or replace with maintained fork. |
| xiaoxiaoleo/HoneyMysql | https://github.com/xiaoxiaoleo/HoneyMysql | `not_found` (README ~L37) | Remove entry. |

## Optional: mark archived repositories

These still resolve but are **archived** on GitHub (consider a note `(archived)` in the list):

| Repo | Last push |
| --- | --- |
| [0x4D31/honeybits](https://github.com/0x4D31/honeybits) | `2019-03-20` |
| [0x4D31/honeyku](https://github.com/0x4D31/honeyku) | `2019-04-24` |
| [ashmckenzie/go-sshoney](https://github.com/ashmckenzie/go-sshoney) | `2017-05-31` |
| [CERT-Polska/HSN-Capture-HPC-NG](https://github.com/CERT-Polska/HSN-Capture-HPC-NG) | `2011-12-19` |
| [CERT-Polska/hsn2-bundle](https://github.com/CERT-Polska/hsn2-bundle) | `2016-05-04` |
| [darkarnium/kako](https://github.com/darkarnium/kako) | `2020-08-26` |
| [foospidy/HoneyPy](https://github.com/foospidy/HoneyPy) | `2024-03-21` |
| [GovCERT-CZ/Shockpot-Frontend](https://github.com/GovCERT-CZ/Shockpot-Frontend) | `2015-12-10` |
| [GovCERT-CZ/Wordpot-Frontend](https://github.com/GovCERT-CZ/Wordpot-Frontend) | `2015-12-10` |
| [johestephan/VerySimpleHoneypot](https://github.com/johestephan/VerySimpleHoneypot) | `2018-10-03` |
| [knalli/honeypot-for-tcp-32764](https://github.com/knalli/honeypot-for-tcp-32764) | `2014-02-06` |
| [utoni/potd](https://github.com/lnslbrty/potd) | `2020-07-12` |
| [magisterquis/sshlowpot](https://github.com/magisterquis/sshlowpot) | `2020-02-02` |
| [magisterquis/vnclowpot](https://github.com/magisterquis/vnclowpot) | `2019-08-10` |
| [SneakersInc/HoneyMalt](https://github.com/SneakersInc/HoneyMalt) | `2014-12-15` |
| [tnich/honssh](https://github.com/tnich/honssh) | `2022-01-02` |
| [Zeerg/helix-honeypot](https://github.com/Zeerg/helix-honeypot) | `2024-01-07` |

## Test plan

- [ ] Confirm each broken URL still 404s
- [ ] Remove or replace bullets in `README.md`
- [ ] Link-check remaining GitHub URLs
- [ ] Keep alphabetical / section structure consistent with the list guidelines

---

_Generated for a cleanup contribution to awesome-honeypots from the UHBS evaluation workspace._

