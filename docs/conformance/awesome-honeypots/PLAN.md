# Plan: awesome-honeypots vs UHBS grading coverage

**Source:** [paralax/awesome-honeypots](https://github.com/paralax/awesome-honeypots) README (fetched 2026-07-29)  
**Cutoff:** GitHub `pushed_at` before **2021-07-29** → treat as stale (>5 years) and exclude from the grading queue.  
**UHBS version:** 4.2.2 (no bump in this doc).

**Triage outputs:** [TRIAGE.md](TRIAGE.md) (grade_now 45) · [DEFERRED-PROTOCOLS.md](DEFERRED-PROTOCOLS.md) (12) · [SKIPPED.md](SKIPPED.md) (34) · upstream cleanup [PR #157](https://github.com/paralax/awesome-honeypots/pull/157)

## Snapshot

| Bucket | Count |
| --- | ---: |
| Unique GitHub repos linked from the list | 237 |
| Accessible (`ok`) | 227 |
| Broken / not found / inaccessible | 10 |
| Accessible & pushed within 5 years (fresh) | 104 |
| Accessible & stale (>5 years) | 123 |
| Already graded by UHBS (matched in awesome list) | 14 |
| **Ungraded + fresh (grading candidates)** | **91** |
| Ungraded + stale (excluded by age filter) | 120 |

## Already graded (appear in awesome-honeypots)

| Repo | Last push | Notes |
| --- | --- | --- |
| [0xBallpoint/trapster-community](https://github.com/0xBallpoint/trapster-community) | `2026-07-27` |  |
| [ahoernecke/ensnare](https://github.com/ahoernecke/ensnare) | `2017-04-18` | surveyed / skipped (not standalone protocol honeypot) |
| [alexbredo/honeypot-ftp](https://github.com/alexbredo/honeypot-ftp) | `2024-01-22` |  |
| [cossacklabs/acra](https://github.com/cossacklabs/acra) | `2026-04-23` | surveyed / skipped (not standalone protocol honeypot) |
| [cowrie/cowrie](https://github.com/cowrie/cowrie) | `2026-07-29` |  |
| [DinoTools/dionaea](https://github.com/DinoTools/dionaea) | `2024-08-01` |  |
| [jordan-wright/elastichoney](https://github.com/jordan-wright/elastichoney) | `2015-07-14` |  |
| [beelzebub-labs/beelzebub](https://github.com/mariocandela/beelzebub) | `2026-07-29` |  |
| [mushorg/conpot](https://github.com/mushorg/conpot) | `2026-07-25` |  |
| [mycert/ESPot](https://github.com/mycert/ESPot) | `2014-08-25` |  |
| [qeeqbox/honeypots](https://github.com/qeeqbox/honeypots) | `2025-12-03` |  |
| [sa7mon/miniprint](https://github.com/sa7mon/miniprint) | `2023-07-09` |  |
| [skeeto/endlessh](https://github.com/skeeto/endlessh) | `2024-06-03` |  |
| [thinkst/opencanary](https://github.com/thinkst/opencanary) | `2026-07-22` |  |

Also graded by UHBS but **not linked** (or linked under a broken URL) on awesome-honeypots:
HoneyMCP, HoneyAgents, LLM Honeypot, LLMPot, DataTrap, and GenAIPot
(`ls1911/GenAIPot` is 404 — see cleanup).

## Phase plan

1. **Cleanup PR upstream** — open PR against `paralax/awesome-honeypots` using [`CLEANUP-PR.md`](CLEANUP-PR.md) (broken links + archived callouts).
2. **Age filter** — do not prioritize the stale appendix for new UHBS labs.
3. **Triage queue** — for each *Ungraded + fresh* entry, skip non-honeypots (analysis tools, frameworks, canary tokens, WordPress plugins) after a quick README check.
4. **Protocol fit** — map live listeners to UHBS plugins; if none overlap, record as UHBS gap.
5. **Publish** — quick/full reports + tutorial/methodology + Results hub.
6. **Scale Results UI** — before the queue grows past ~30–40 rows, land the performance/UX changes below so the landing page stays fast.

## Scaling Results without slow loads or UX damage

Today Results live as a large inline `LAB_RESULTS` array in `web/src/pages/Home.tsx`
(one row per protocol surface). Cards already paginate (`pageSize = 3`); **list mode still
renders every filtered row**. Shipping ~90 fresh grades as-is would bloat the JS bundle,
clog the `#results` section, and fight the existing landing composition (hero first, Results later).

### Goals

- First paint of the marketing page stays light; Results do not dominate load or layout.
- Adding a lab is data-only (no hand-editing a 2k-line TSX catalog).
- Users can find a project in seconds (filter / search / sort) without scrolling a wall of cards.
- Heavy artifacts (scorecards, logs, `report.json`) stay on MkDocs / static paths — never inlined into the SPA.

### Do now (keep UX stable while count grows)

| Practice | Why |
| --- | --- |
| **One card / list row per *product***, not per protocol | Multi-protocol labs (OpenCanary, DataTrap, qeeqbox) already explode row count. Hub link + protocol chips on the card; detail stays on the report hub. |
| **Keep card pagination** (3–6 visible) | Matches current carousel; avoid mounting dozens of bordered cards + framer variants at once. |
| **Paginate or virtualize list mode** | List currently maps *all* `filteredLabs` — fix before ~50 rows. |
| **Lazy motion** | Animate the Results *section chrome* once; do not stagger-animate every row/card as the catalog grows. |
| **Protocol filter + name search** | Filters already exist; add a small text search (`name` / `repo`) so long catalogs stay usable without more chrome. |
| **Skip / gap notes stay out of the main grid** | Acra/Ensnare-style “not a honeypot” entries belong in a collapsed “Surveyed / skipped” fold or MkDocs-only, not competing with graded cards. |

### Do next (architecture — unlock ~100+ labs)

1. **Extract catalog from `Home.tsx`**
   - Build-time (or CI) generate `web/public/results-catalog.json` (or `web/src/data/results-catalog.json`) from `docs/conformance/reports/**` manifests / scorecards.
   - `Results` fetches or imports that JSON; TSX only owns presentation.
   - Schema stays the slim `LabResult` fields (scores, grades, paths, `repoUpdated`) — **not** full report bodies.

2. **Code-split Results**
   - Dynamic `import()` for the Results section (or a `/results` route) so KaTeX / above-the-fold marketing JS does not wait on the catalog.
   - Optional: dedicated Results page linked from the nav CTA; keep a **compact teaser** (top 3 by recency or UHQS) on the home `#results` anchor so the landing composition stays calm.

3. **Static hosting cost stays on MkDocs**
   - Tutorials, methodology, `SCORECARD.txt`, logs remain under `mkdocs/conformance/reports/…`.
   - Landing links out; no client-side fetch of scorecard text for the grid.
   - Report hubs can be many; GitHub Pages already serves them as static files (no SPA parse cost).

4. **Index vs detail**
   - Catalog JSON ≈ tens of KB even at 100 products.
   - Detail pages = existing MkDocs trees (OK if large).
   - Never embed `uhbs-run.log` / full `report.json` in the React bundle.

5. **Sort / filter UX without clutter**
   - Keep one filter row: protocol chips + search + cards/list toggle + sort (UHQS quick/full).
   - Prefer **collapsible “More protocols”** if chip count grows (don’t wrap three rows of pills).
   - Default sort: **recent grade date** or **repoUpdated**, with UHQS sort opt-in (already partially there).

6. **CI guardrails**
   - Fail or warn if `results-catalog.json` entry count × average card DOM would exceed a budget, or if `Home.tsx` grows past a line/byte threshold (forces catalog extraction).
   - Optional Lighthouse / bundle-size check on `web` build in CI when Results change.

### What not to do

- Do not dump every protocol surface as its own full-width card on the home page.
- Do not load remote GitHub API at page runtime for `repoUpdated` (bake dates into the catalog at publish time — already the pattern).
- Do not add dashboards, stat strips, or dense tables above the Results headline; keep the section’s job: **find a lab → open hub/tutorial**.
- Do not block first paint on MkDocs HTML scraping.

### Suggested rollout order (tied to grading queue)

1. Group OpenCanary / DataTrap / qeeqbox / Trapster / Beelzebub / Cowrie to **product-level** Results rows (immediate UX win, fewer visible items).
2. Paginate list mode + add search.
3. Generate `results-catalog.json` from reports; delete inline `LAB_RESULTS`.
4. Then batch-grade fresh awesome-honeypots candidates without fear of melting the landing page.

## Ungraded honeypots we have not graded yet (fresh only)

Repos with GitHub activity on or after **2021-07-29**, not yet in UHBS conformance reports.

| Project | Repo | Last push | Archived? |
| --- | --- | --- | --- |
| thinkst/canarytokens | [thinkst/canarytokens](https://github.com/thinkst/canarytokens) | `2026-07-29` |  |
| andrewmichaelsmith/flux | [andrewmichaelsmith/flux](https://github.com/andrewmichaelsmith/flux) | `2026-07-29` |  |
| WebDecoy/FCaptcha | [WebDecoy/FCaptcha](https://github.com/WebDecoy/FCaptcha) | `2026-07-28` |  |
| Cloud Active Defense | [SAP/cloud-active-defense](https://github.com/SAP/cloud-active-defense) | `2026-07-28` |  |
| sjinks/ssh-honeypotd | [sjinks/ssh-honeypotd](https://github.com/sjinks/ssh-honeypotd) | `2026-07-28` |  |
| joshrendek/hnypots-agent | [joshrendek/threat.gg-agent](https://github.com/joshrendek/hnypots-agent) | `2026-07-28` |  |
| sjinks/mysql-honeypotd | [sjinks/mysql-honeypotd](https://github.com/sjinks/mysql-honeypotd) | `2026-07-28` |  |
| SentryPeer/SentryPeer | [SentryPeer/SentryPeer](https://github.com/SentryPeer/SentryPeer) | `2026-07-27` |  |
| rabbitstack/fibratus | [rabbitstack/fibratus](https://github.com/rabbitstack/fibratus) | `2026-07-27` |  |
| ivre/ivre | [ivre/ivre](https://github.com/ivre/ivre) | `2026-07-26` |  |
| WebDecoy/wordpress-plugin | [WebDecoy/wordpress-plugin](https://github.com/WebDecoy/wordpress-plugin) | `2026-07-26` |  |
| BlessedRebuS/Krawl | [BlessedRebuS/Krawl](https://github.com/BlessedRebuS/Krawl) | `2026-07-26` |  |
| buffer/thug | [buffer/thug](https://github.com/buffer/thug) | `2026-07-22` |  |
| sjhilt/GasPot | [sjhilt/GasPot](https://github.com/sjhilt/GasPot) | `2026-07-22` |  |
| ncouture/MockSSH | [ncouture/MockSSH](https://github.com/ncouture/MockSSH) | `2026-07-09` |  |
| PeterGabaldon/Fortigate.VPN-SSL.Honeypot | [PeterGabaldon/Fortigate.VPN-SSL.Honeypot](https://github.com/PeterGabaldon/Fortigate.VPN-SSL.Honeypot) | `2026-06-28` |  |
| dtag-dev-sec/tpotce | [telekom-security/tpotce](https://github.com/dtag-dev-sec/tpotce) | `2026-06-23` |  |
| christophe77/node-ftp-honeypot | [christophe77/node-ftp-honeypot](https://github.com/christophe77/node-ftp-honeypot) | `2026-06-22` |  |
| christophe77/express-honeypot | [christophe77/express-honeypot](https://github.com/christophe77/express-honeypot) | `2026-06-22` |  |
| antonsatt/ssh-radar | [AntonSatt/SSH-Radar](https://github.com/antonsatt/ssh-radar) | `2026-06-21` |  |
| ivre/masscanned | [ivre/masscanned](https://github.com/ivre/masscanned) | `2026-06-17` |  |
| f0rw4rd/potsnitch | [f0rw4rd/potsnitch](https://github.com/f0rw4rd/potsnitch) | `2026-06-14` |  |
| androguard/androguard | [androguard/androguard](https://github.com/androguard/androguard) | `2026-06-05` |  |
| JustinAzoff/ssh-auth-logger | [JustinAzoff/ssh-auth-logger](https://github.com/JustinAzoff/ssh-auth-logger) | `2026-05-29` |  |
| mushorg/glutton | [mushorg/glutton](https://github.com/mushorg/glutton) | `2026-05-29` |  |
| phin3has/mailoney | [phin3has/mailoney](https://github.com/phin3has/mailoney) | `2026-05-22` |  |
| gosecure/pyrdp | [GoSecure/pyrdp](https://github.com/gosecure/pyrdp) | `2026-05-13` |  |
| nsmfoo/dicompot | [nsmfoo/dicompot](https://github.com/nsmfoo/dicompot) | `2026-05-11` |  |
| mrheinen/lophiid | [mrheinen/lophiid](https://github.com/mrheinen/lophiid) | `2026-04-28` |  |
| bartnv/portlurker | [bartnv/portlurker](https://github.com/bartnv/portlurker) | `2026-04-24` |  |
| msurguy/Honeypot | [msurguy/Honeypot](https://github.com/msurguy/Honeypot) | `2026-04-08` |  |
| andrewmichaelsmith/bluepot | [andrewmichaelsmith/bluepot](https://github.com/andrewmichaelsmith/bluepot) | `2026-04-02` |  |
| chaitin/mimicry | [chaitin/mimicry](https://github.com/chaitin/mimicry) | `2026-03-20` |  |
| eymengunay/EoHoneypotBundle | [eymengunay/EoHoneypotBundle](https://github.com/eymengunay/EoHoneypotBundle) | `2026-02-19` |  |
| jekil/UDPot | [jekil/UDPot](https://github.com/jekil/UDPot) | `2026-01-23` |  |
| yunginnanet/HellPot | [yunginnanet/HellPot](https://github.com/yunginnanet/HellPot) | `2025-12-19` |  |
| 0x4D31/galah | [0x4D31/galah](https://github.com/0x4D31/galah) | `2025-07-24` |  |
| HoneySat/honeysat-deploy | [HoneySat/honeysat-deploy](https://github.com/HoneySat/honeysat-deploy) | `2025-07-08` |  |
| LogoiLab/honeyup | [mrcbax/honeyup](https://github.com/LogoiLab/honeyup) | `2025-04-19` |  |
| shiva-spampot/shiva | [shiva-spampot/shiva](https://github.com/shiva-spampot/shiva) | `2025-03-31` |  |
| referefref/honeydet | [referefref/honeydet](https://github.com/referefref/honeydet) | `2025-03-22` |  |
| huuck/ADBHoney | [huuck/ADBHoney](https://github.com/huuck/ADBHoney) | `2025-03-05` |  |
| fofapro/fapro | [fofapro/fapro](https://github.com/fofapro/fapro) | `2025-01-02` |  |
| thomaspatzke/Log4Pot | [thomaspatzke/Log4Pot](https://github.com/thomaspatzke/Log4Pot) | `2024-11-29` |  |
| droberson/ssh-honeypot | [droberson/ssh-honeypot](https://github.com/droberson/ssh-honeypot) | `2024-10-29` |  |
| jaksi/sshesame | [jaksi/sshesame](https://github.com/jaksi/sshesame) | `2024-10-21` |  |
| free5ty1e/honeypotpi | [free5ty1e/honeypotpi](https://github.com/free5ty1e/honeypotpi) | `2024-09-25` |  |
| OWASP/Python-Honeypot | [OWASP/Python-Honeypot](https://github.com/OWASP/Python-Honeypot) | `2024-09-15` |  |
| mushorg/tanner | [mushorg/tanner](https://github.com/mushorg/tanner) | `2024-08-19` |  |
| jesparza/peepdf | [jesparza/peepdf](https://github.com/jesparza/peepdf) | `2024-08-19` |  |
| betheroot/sticky_elephant | [betheroot/sticky_elephant](https://github.com/betheroot/sticky_elephant) | `2024-08-06` |  |
| mushorg/glastopf | [mushorg/glastopf](https://github.com/mushorg/glastopf) | `2024-07-23` |  |
| bocajspear1/honeyhttpd | [bocajspear1/honeyhttpd](https://github.com/bocajspear1/honeyhttpd) | `2024-06-29` |  |
| mushorg/snare | [mushorg/snare](https://github.com/mushorg/snare) | `2024-06-10` |  |
| johnnykv/heralding | [johnnykv/heralding](https://github.com/johnnykv/heralding) | `2024-05-21` |  |
| betheroot/pghoney | [betheroot/pghoney](https://github.com/betheroot/pghoney) | `2024-05-20` |  |
| schmalle/medpot | [schmalle/medpot](https://github.com/schmalle/medpot) | `2024-05-20` |  |
| hatching/vmcloak | [hatching/vmcloak](https://github.com/hatching/vmcloak) | `2024-05-14` |  |
| referefref/modpot | [referefref/modpot](https://github.com/referefref/modpot) | `2024-05-08` |  |
| batchmcnulty/Malbait | [batchmcnulty/Malbait](https://github.com/batchmcnulty/Malbait) | `2024-04-27` |  |
| dmpayton/django-admin-honeypot | [dmpayton/django-admin-honeypot](https://github.com/dmpayton/django-admin-honeypot) | `2024-04-10` |  |
| buffer/libemu | [buffer/libemu](https://github.com/buffer/libemu) | `2024-03-27` |  |
| morian/blacknet | [morian/blacknet](https://github.com/morian/blacknet) | `2024-03-21` |  |
| foospidy/HoneyPy | [foospidy/HoneyPy](https://github.com/foospidy/HoneyPy) | `2024-03-21` | yes |
| Phype/telnet-iot-honeypot | [Phype/telnet-iot-honeypot](https://github.com/Phype/telnet-iot-honeypot) | `2024-02-02` |  |
| Zeerg/helix-honeypot | [Zeerg/helix-honeypot](https://github.com/Zeerg/helix-honeypot) | `2024-01-07` | yes |
| referefref/canarytokendetector | [referefref/canarytokendetector](https://github.com/referefref/canarytokendetector) | `2023-12-09` |  |
| referefref/honeyfs | [referefref/honeyfs](https://github.com/referefref/honeyfs) | `2023-12-05` |  |
| referefref/SMTPLLMPot | [referefref/SMTPLLMPot](https://github.com/referefref/SMTPLLMPot) | `2023-12-01` |  |
| buffer/pylibemu | [buffer/pylibemu](https://github.com/buffer/pylibemu) | `2023-11-29` |  |
| desaster/kippo | [desaster/kippo](https://github.com/desaster/kippo) | `2023-11-19` |  |
| jeremyfritzen/Ethereum-honey-pot | [jeremyfritzen/Ethereum-honey-pot](https://github.com/jeremyfritzen/Ethereum-honey-pot) | `2023-11-17` |  |
| Cymmetria/honeycomb_plugins | [Cymmetria/honeycomb_plugins](https://github.com/Cymmetria/honeycomb_plugins) | `2023-10-19` |  |
| rep/hpfeeds | [hpfeeds/hpfeeds](https://github.com/rep/hpfeeds) | `2023-10-19` |  |
| torque59/nosqlpot | [torque59/nosqlpot](https://github.com/torque59/nosqlpot) | `2023-10-17` |  |
| honeytrap/honeytrap | [honeytrap/honeytrap](https://github.com/honeytrap/honeytrap) | `2023-10-09` |  |
| m4rco-/dorothy2 | [m4rco-/dorothy2](https://github.com/m4rco-/dorothy2) | `2023-09-26` |  |
| DataSoft/Nova | [DataSoft/Nova](https://github.com/DataSoft/Nova) | `2023-06-08` |  |
| Honeydsum.pl | [DataSoft/Honeyd](https://github.com/DataSoft/Honeyd) | `2023-05-20` |  |
| sefcom/honeyplc | [sefcom/honeyplc](https://github.com/sefcom/honeyplc) | `2023-05-16` |  |
| joda32/owa-honeypot | [joda32/owa-honeypot](https://github.com/joda32/owa-honeypot) | `2023-05-02` |  |
| Plazmaz/MongoDB-HoneyProxy | [Plazmaz/MongoDB-HoneyProxy](https://github.com/Plazmaz/MongoDB-HoneyProxy) | `2023-02-20` |  |
| gbrindisi/wordpot | [gbrindisi/wordpot](https://github.com/gbrindisi/wordpot) | `2023-02-07` |  |
| deroux/longitudinal-analysis-cowrie | [deroux/longitudinal-analysis-cowrie](https://github.com/deroux/longitudinal-analysis-cowrie) | `2022-11-14` |  |
| nsmfoo/antivmdetection | [nsmfoo/antivmdetection](https://github.com/nsmfoo/antivmdetection) | `2022-11-05` |  |
| secureworks/dcept | [secureworks/dcept](https://github.com/secureworks/dcept) | `2022-07-13` |  |
| pjlantz/Hale | [pjlantz/Hale](https://github.com/pjlantz/Hale) | `2022-05-23` |  |
| yvesago/imap-honey | [yvesago/imap-honey](https://github.com/yvesago/imap-honey) | `2022-04-22` |  |
| MattCarothers/mhn-core-docker | [MattCarothers/mhn-core-docker](https://github.com/MattCarothers/mhn-core-docker) | `2022-03-28` |  |
| BinaryDefense/artillery | [BinaryDefense/artillery](https://github.com/BinaryDefense/artillery) | `2022-01-06` |  |
| tnich/honssh | [tnich/honssh](https://github.com/tnich/honssh) | `2022-01-02` | yes |

_Total: 91 candidates (includes tools/related projects still linked as GitHub repos)._

## Removed by age filter (ungraded, last push >5 years)

Out of the UHBS grading queue by the 5-year rule.

<details><summary>Expand full stale list (120)</summary>

| Project | Repo | Last push |
| --- | --- | --- |
| mfontani/kippo-stats | [mfontani/kippo-stats](https://github.com/mfontani/kippo-stats) | `2011-05-04` |
| CERT-Polska/HSN-Capture-HPC-NG | [CERT-Polska/HSN-Capture-HPC-NG](https://github.com/CERT-Polska/HSN-Capture-HPC-NG) | `2011-12-19` |
| jedie/django-kippo | [jedie/django-kippo](https://github.com/jedie/django-kippo) | `2012-07-09` |
| schmalle/MysqlPot | [schmalle/MysqlPot](https://github.com/schmalle/MysqlPot) | `2012-10-14` |
| upa/ofpot | [upa/ofpot](https://github.com/upa/ofpot) | `2013-01-05` |
| yuchincheng/HpfeedsHoneyGraph | [yuchincheng/HpfeedsHoneyGraph](https://github.com/yuchincheng/HpfeedsHoneyGraph) | `2013-02-13` |
| honeynet/apkinspector | [honeynet/apkinspector](https://github.com/honeynet/apkinspector) | `2013-02-25` |
| oguzy/ovizart | [oguzy/ovizart](https://github.com/oguzy/ovizart) | `2013-04-22` |
| ayrus/afterglow-cloud | [ayrus/afterglow-cloud](https://github.com/ayrus/afterglow-cloud) | `2013-05-04` |
| schmalle/servletpot | [schmalle/Servletpot](https://github.com/schmalle/servletpot) | `2013-05-12` |
| hexgolems/pint | [hexgolems/pint](https://github.com/hexgolems/pint) | `2013-11-06` |
| hbhzwj/imalse | [jingconan/imalse](https://github.com/hbhzwj/imalse) | `2013-12-10` |
| PaulMaddox/gohoney | [PaulMaddox/gohoney](https://github.com/PaulMaddox/gohoney) | `2013-12-12` |
| mdp/honeypot.go | [mdp/honeypot.go](https://github.com/mdp/honeypot.go) | `2013-12-20` |
| CHH/stack-honeypot | [CHH/stack-honeypot](https://github.com/CHH/stack-honeypot) | `2014-01-30` |
| knalli/honeypot-for-tcp-32764 | [knalli/honeypot-for-tcp-32764](https://github.com/knalli/honeypot-for-tcp-32764) | `2014-02-06` |
| fygrave/honeyntp | [fygrave/honeyntp](https://github.com/fygrave/honeyntp) | `2014-03-27` |
| freak3dot/smart-honeypot | [freak3dot/smart-honeypot](https://github.com/freak3dot/smart-honeypot) | `2014-04-19` |
| dutchcoders/troje | [dutchcoders/troje](https://github.com/dutchcoders/troje) | `2014-08-12` |
| andrew-morris/kippo_detect | [andrew-morris/kippo_detect](https://github.com/andrew-morris/kippo_detect) | `2014-12-10` |
| SneakersInc/HoneyMalt | [SneakersInc/HoneyMalt](https://github.com/SneakersInc/HoneyMalt) | `2014-12-15` |
| sreinhardt/Docker-Honeynet | [sreinhardt/Docker-Honeynet](https://github.com/sreinhardt/Docker-Honeynet) | `2014-12-21` |
| madirish/kojoney2 | [madirish/kojoney2](https://github.com/madirish/kojoney2) | `2015-01-06` |
| bjeborn/basic-auth-pot | [bjeborn/basic-auth-pot](https://github.com/bjeborn/basic-auth-pot) | `2015-01-15` |
| provos/honeyd | [provos/honeyd](https://github.com/provos/honeyd) | `2015-03-14` |
| andrewmichaelsmith/manuka | [andrewmichaelsmith/manuka](https://github.com/andrewmichaelsmith/manuka) | `2015-03-21` |
| sk4ld/gridpot | [sk4ld/gridpot](https://github.com/sk4ld/gridpot) | `2015-03-23` |
| honeynet/ghost-usb-honeypot | [honeynet/ghost-usb-honeypot](https://github.com/honeynet/ghost-usb-honeypot) | `2015-03-24` |
| urule99/jsunpack-n | [urule99/jsunpack-n](https://github.com/urule99/jsunpack-n) | `2015-04-02` |
| fzerorubigd/go0r | [fzerorubigd/go0r](https://github.com/fzerorubigd/go0r) | `2015-04-07` |
| csirtgadgets/csirtg-honeypot | [csirtgadgets/csirtg-honeypot](https://github.com/csirtgadgets/csirtg-honeypot) | `2015-04-24` |
| inguardians/toms_honeypot | [inguardians/toms_honeypot](https://github.com/inguardians/toms_honeypot) | `2015-04-27` |
| mrschyte/dockerpot | [mrschyte/dockerpot](https://github.com/mrschyte/dockerpot) | `2015-05-05` |
| honeynet/phoneyc | [honeynet/phoneyc](https://github.com/honeynet/phoneyc) | `2015-05-22` |
| SecurityTW/delilah | [SecurityTW/delilah](https://github.com/SecurityTW/delilah) | `2015-06-11` |
| alexbredo/honeypot-camera | [alexbredo/honeypot-camera](https://github.com/alexbredo/honeypot-camera) | `2015-06-18` |
| schmalle/Nodepot | [schmalle/Nodepot](https://github.com/schmalle/Nodepot) | `2015-08-23` |
| CanadianJeff/honeywrt | [CanadianJeff/honeywrt](https://github.com/CanadianJeff/honeywrt) | `2015-08-25` |
| hgascon/acapulco | [hgascon/acapulco](https://github.com/hgascon/acapulco) | `2015-10-05` |
| jpyorre/IntelligentHoneyNet | [jpyorre/IntelligentHoneyNet](https://github.com/jpyorre/IntelligentHoneyNet) | `2015-11-05` |
| hexgolems/schem | [hexgolems/schem](https://github.com/hexgolems/schem) | `2015-11-11` |
| GovCERT-CZ/Shockpot-Frontend | [GovCERT-CZ/Shockpot-Frontend](https://github.com/GovCERT-CZ/Shockpot-Frontend) | `2015-12-10` |
| GovCERT-CZ/Wordpot-Frontend | [GovCERT-CZ/Wordpot-Frontend](https://github.com/GovCERT-CZ/Wordpot-Frontend) | `2015-12-10` |
| katkad/Glastopf-Analytics | [katkad/Glastopf-Analytics](https://github.com/katkad/Glastopf-Analytics) | `2015-12-14` |
| gregcmartin/Kippo_JunOS | [gregcmartin/Kippo_JunOS](https://github.com/gregcmartin/Kippo_JunOS) | `2015-12-22` |
| balte/TelnetHoney | [balte/TelnetHoney](https://github.com/balte/TelnetHoney) | `2016-01-20` |
| jadb/honeypot | [jadb/honeypot](https://github.com/jadb/honeypot) | `2016-01-23` |
| glaslos/honeyprint | [glaslos/honeyprint](https://github.com/glaslos/honeyprint) | `2016-01-28` |
| Joss-Steward/honeypotDisplay | [Joss-Steward/honeypotDisplay](https://github.com/Joss-Steward/honeypotDisplay) | `2016-02-05` |
| kingtuna/go-emulators | [kingtuna/go-emulators](https://github.com/kingtuna/go-emulators) | `2016-02-28` |
| omererdem/honeything | [omererdem/honeything](https://github.com/omererdem/honeything) | `2016-03-16` |
| Ziemeck/bifrozt-ansible | [Ziemeck/bifrozt-ansible](https://github.com/Ziemeck/bifrozt-ansible) | `2016-03-17` |
| mushorg/imhoneypot | [mushorg/imhoneypot](https://github.com/mushorg/imhoneypot) | `2016-03-22` |
| CERT-Polska/hsn2-bundle | [CERT-Polska/hsn2-bundle](https://github.com/CERT-Polska/hsn2-bundle) | `2016-05-04` |
| naorlivne/dshp | [naorlivne/dshp](https://github.com/naorlivne/dshp) | `2016-05-31` |
| miguelraulb/spamhat | [miguelraulb/spamhat](https://github.com/miguelraulb/spamhat) | `2016-06-01` |
| xme/dshield-docker | [xme/dshield-docker](https://github.com/xme/dshield-docker) | `2016-06-08` |
| fw42/honeymap | [fw42/honeymap](https://github.com/fw42/honeymap) | `2016-08-09` |
| sec51/honeymail | [sec51/honeymail](https://github.com/sec51/honeymail) | `2016-08-09` |
| andrewmichaelsmith/honeypot-setup-script | [andrewmichaelsmith/honeypot-setup-script](https://github.com/andrewmichaelsmith/honeypot-setup-script) | `2016-11-09` |
| securitygeneration/Honeyport | [securitygeneration/Honeyport](https://github.com/securitygeneration/Honeyport) | `2017-02-22` |
| robertdavidgraham/telnetlogger | [robertdavidgraham/telnetlogger](https://github.com/robertdavidgraham/telnetlogger) | `2017-03-05` |
| Cymmetria/MTPot | [Cymmetria/MTPot](https://github.com/Cymmetria/MTPot) | `2017-03-20` |
| Cymmetria/StrutsHoneypot | [Cymmetria/StrutsHoneypot](https://github.com/Cymmetria/StrutsHoneypot) | `2017-03-24` |
| ashmckenzie/go-sshoney | [ashmckenzie/go-sshoney](https://github.com/ashmckenzie/go-sshoney) | `2017-05-31` |
| tillmannw/honeytrap | [tillmannw/honeytrap](https://github.com/tillmannw/honeytrap) | `2017-06-04` |
| rubenespadas/DionaeaFR | [rubenespadas/DionaeaFR](https://github.com/rubenespadas/DionaeaFR) | `2017-08-07` |
| helospark/tomcat-manager-honeypot | [helospark/tomcat-manager-honeypot](https://github.com/helospark/tomcat-manager-honeypot) | `2017-08-27` |
| sahilm/hived | [sahilm/hived](https://github.com/sahilm/hived) | `2017-08-28` |
| freak3dot/wp-smart-honeypot | [freak3dot/wp-smart-honeypot](https://github.com/freak3dot/wp-smart-honeypot) | `2017-10-13` |
| xlfe/cowrie2neo | [xlfe/cowrie2neo](https://github.com/xlfe/cowrie2neo) | `2017-10-16` |
| fnzv/YAFH | [fnzv/YAFH](https://github.com/fnzv/YAFH) | `2017-12-08` |
| MartinIngesen/HonnyPotter | [MartinIngesen/HonnyPotter](https://github.com/MartinIngesen/HonnyPotter) | `2018-01-18` |
| gfoss/phpmyadmin_honeypot | [gfoss/phpmyadmin_honeypot](https://github.com/gfoss/phpmyadmin_honeypot) | `2018-02-11` |
| blaverick62/SIREN | [blaverick62/SIREN](https://github.com/blaverick62/SIREN) | `2018-03-17` |
| IllusiveNetworks-Labs/WebTrap | [IllusiveNetworks-Labs/WebTrap](https://github.com/IllusiveNetworks-Labs/WebTrap) | `2018-03-28` |
| Marist-Innovation-Lab/DolosHoneypot | [Marist-Innovation-Lab/DolosHoneypot](https://github.com/Marist-Innovation-Lab/DolosHoneypot) | `2018-04-23` |
| Marist-Innovation-Lab/PasitheaHoneypot | [Marist-Innovation-Lab/PasitheaHoneypot](https://github.com/Marist-Innovation-Lab/PasitheaHoneypot) | `2018-04-24` |
| RevengeComing/DemonHunter | [RevengeComing/DemonHunter](https://github.com/RevengeComing/DemonHunter) | `2018-04-29` |
| czardoz/hornet | [czardoz/hornet](https://github.com/czardoz/hornet) | `2018-04-30` |
| magisterquis/sshhipot | [magisterquis/sshhipot](https://github.com/magisterquis/sshhipot) | `2018-05-13` |
| jusafing/pnaf | [jusafing/pnaf](https://github.com/jusafing/pnaf) | `2018-05-17` |
| shbhmsingh72/Honeypot-Research-Papers | [shbhmsingh72/Honeypot-Research-Papers](https://github.com/shbhmsingh72/Honeypot-Research-Papers) | `2018-06-02` |
| ajackal/arctic-swallow | [ajackal/arctic-swallow](https://github.com/ajackal/arctic-swallow) | `2018-07-26` |
| Cymmetria/micros_honeypot | [Cymmetria/micros_honeypot](https://github.com/Cymmetria/micros_honeypot) | `2018-09-25` |
| johestephan/VerySimpleHoneypot | [johestephan/VerySimpleHoneypot](https://github.com/johestephan/VerySimpleHoneypot) | `2018-10-03` |
| aplura/Tango | [aplura/Tango](https://github.com/aplura/Tango) | `2018-10-18` |
| 0x4D31/honeylambda | [0x4D31/honeyLambda](https://github.com/0x4D31/honeylambda) | `2018-10-20` |
| lcashdol/WAPot | [lcashdol/WAPot](https://github.com/lcashdol/WAPot) | `2018-11-14` |
| cymmetria/ciscoasa_honeypot | [Cymmetria/ciscoasa_honeypot](https://github.com/cymmetria/ciscoasa_honeypot) | `2018-11-23` |
| amv42/sshd-honeypot | [amv42/sshd-honeypot](https://github.com/amv42/sshd-honeypot) | `2018-12-20` |
| mkishere/sshsyrup | [victpork/sshsyrup](https://github.com/mkishere/sshsyrup) | `2019-02-25` |
| stamparm/hontel | [stamparm/hontel](https://github.com/stamparm/hontel) | `2019-03-05` |
| graneed/bwpot | [graneed/bwpot](https://github.com/graneed/bwpot) | `2019-03-10` |
| 0x4D31/honeybits | [0x4D31/honeybits](https://github.com/0x4D31/honeybits) | `2019-03-20` |
| 0x4D31/honeyku | [0x4D31/honeyku](https://github.com/0x4D31/honeyku) | `2019-04-24` |
| Cryptix720/HUDINX | [Cryptix720/HUDINX](https://github.com/Cryptix720/HUDINX) | `2019-04-30` |
| kryptoslogic/rdppot | [kryptoslogic/rdppot](https://github.com/kryptoslogic/rdppot) | `2019-06-06` |
| Masood-M/yalih | [Masood-M/yalih](https://github.com/Masood-M/yalih) | `2019-06-18` |
| d1str0/drupot | [d1str0/drupot](https://github.com/d1str0/drupot) | `2019-07-14` |
| magisterquis/vnclowpot | [magisterquis/vnclowpot](https://github.com/magisterquis/vnclowpot) | `2019-08-10` |
| Mojachieee/go-HoneyPot | [Mojachieee/go-HoneyPot](https://github.com/Mojachieee/go-HoneyPot) | `2019-10-05` |
| ppacher/honeyssh | [ppacher/honeyssh](https://github.com/ppacher/honeyssh) | `2019-10-18` |
| run41/honey_ports | [run41/honey_ports](https://github.com/run41/honey_ports) | `2019-10-26` |
| lanjelot/twisted-honeypots | [lanjelot/twisted-honeypots](https://github.com/lanjelot/twisted-honeypots) | `2019-12-27` |
| MalwareTech/CitrixHoneypot | [MalwareTech/CitrixHoneypot](https://github.com/MalwareTech/CitrixHoneypot) | `2020-01-15` |
| magisterquis/sshlowpot | [magisterquis/sshlowpot](https://github.com/magisterquis/sshlowpot) | `2020-02-02` |
| traetox/sshForShits | [traetox/sshForShits](https://github.com/traetox/sshForShits) | `2020-04-08` |
| Cymmetria/weblogic_honeypot | [Cymmetria/weblogic_honeypot](https://github.com/Cymmetria/weblogic_honeypot) | `2020-04-25` |
| rshipp/slipm-honeypot | [rshipp/slipm-honeypot](https://github.com/rshipp/slipm-honeypot) | `2020-06-14` |
| lnslbrty/potd | [utoni/potd](https://github.com/lnslbrty/potd) | `2020-07-12` |
| mzweilin/ipv6-attack-detector | [mzweilin/IPv6-Attack-Detector](https://github.com/mzweilin/ipv6-attack-detector) | `2020-07-30` |
| darkarnium/kako | [darkarnium/kako](https://github.com/darkarnium/kako) | `2020-08-26` |
| ciscocsirt/dhp | [ciscocsirt/dhp](https://github.com/ciscocsirt/dhp) | `2020-10-06` |
| kungfuguapo/HoneyPress | [kungfuguapo/HoneyPress](https://github.com/kungfuguapo/HoneyPress) | `2020-11-19` |
| aelth/ddospot | [aelth/ddospot](https://github.com/aelth/ddospot) | `2020-12-27` |
| r0hi7/HoneySMB | [rosehgal/HoneySMB](https://github.com/r0hi7/HoneySMB) | `2021-03-28` |
| cypwnpwnsocute/RedisHoneyPot | [cypwnpwnsocute/RedisHoneyPot](https://github.com/cypwnpwnsocute/RedisHoneyPot) | `2021-04-23` |
| UHH-ISS/honeygrove | [UHH-ISS/honeygrove](https://github.com/UHH-ISS/honeygrove) | `2021-06-07` |
| citronneur/rdpy | [citronneur/rdpy](https://github.com/citronneur/rdpy) | `2021-06-28` |

</details>

## Broken / inaccessible GitHub links

See [`CLEANUP-PR.md`](CLEANUP-PR.md) for the upstream PR draft.

