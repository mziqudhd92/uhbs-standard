# UHBS Protocol Plugin Audit — Compliance & Design Rationale

**Scope:** all 17 built-in `uhbs_core.protocols.*` plugins + the shared scoring
engine, as of 2026-07-27 (post code-review remediation).
**Audience:** external auditors, architects, and CI/CD gate reviewers
deciding whether a given plugin's grading result can be trusted.
**Status key:** 🟢 Tier 1 (audited, critical-gated, mostly baseline/FSM-verified) ·
🟡 Tier 2 (real gate, not yet baseline-verified) · 🟠 Tier 3 (functional, no
critical gate yet — documented gap, not a false claim).

---

## 0. Scoring engine — how a plugin's checks become a number

Every probe hook (`probe_fsm`, `probe_negotiation`, `probe_state`, …) returns
a `list[CheckResult]`. `CheckResult` (`uhbs_core/models.py`) has: `id`,
`team` (`blue`=defender signal, `red`=attacker-view signal, `white`=neutral),
`passed: bool`, `score: float` (0–100), `evidence: list[str]`, and
`critical: bool`.

`uhbs_core.check_scoring.score_checks()` — the single aggregator used by
both Module A (`test_stealth.py`) and Module B (`test_realism.py`) — reduces
a check list to one 0–100 number via, **in order**:

1. **Circuit breaker.** Any `critical=True` check with `passed=False` →
   whole list scores `0.0`. Reserved for genuine security gates (auth
   rejection, protocol header validation, data-plane integrity) — not every
   check is critical.
2. **Integrity gate.** Any check whose `passed` and `score` *contradict*
   each other (e.g. `passed=True` at `score=5`) → whole list scores `0.0`.
   A self-contradictory check cannot be trusted, so it's treated the same
   as a critical-gate failure.
3. **Geometric mean** over the remaining scores (not arithmetic) — a single
   weak check drags the aggregate down hard instead of being diluted by
   unrelated passes (`gmean(0.5, 100, 100) ≈ 17` vs `mean ≈ 33`).
4. **Legacy pass-rate fallback** — reachable only in the degenerate case
   where every check is `passed=False, score=0.0` (trivially evaluates to
   `0.0`); kept for formula self-documentation, not exercised by any
   shipped plugin.

**Dual evaluation mode.** Most TCP plugins accept a `tps.strict_rfc_enforcement`
flag (from the target's Target Profile Specification): `True` (default,
every shipped TPS file) makes the protocol's core negotiation gate
`critical=True` (a hard 0); `False` treats the same missing signal as
explicit, non-critical partial credit (`score≈35`) for genuinely alert-only,
log-only decoys that never claim to speak the full protocol.

**Score scale (2026-07-27):** every `CheckResult.score` in RFC suites and
shared timing probes is on a **0–100** scale. Older partial-point layouts
(e.g. SSH `25+25+20+30`) were designed to *sum* to 100 and silently capped a
perfect suite at ~25 under geometric mean — that structural bug is fixed.
When `gold_baseline_host` is unset, the KS timing check is **omitted**
(not recorded as `passed=False`). Module E P95 defaults are class/protocol
aware (`ssh` → 3000 ms) so interactive shell decoys are not failed for
missing a 100 ms bar.

---

## 1. SSH — `protocols/ssh.py` 🟢 Tier 1

- **Standards:** RFC 4253 (SSH Transport Layer), HASSH client/server fingerprinting.
- **A1 (`probe_fsm`):** Reuses `rfc_probes.probe_ssh_rfc4253` — validates
  malformed-KEX-init handling and other RFC 4253 negative cases.
- **A2 (`probe_negotiation`):** KEX/identification-string checks from the
  same RFC suite, plus `ssh.nego.hassh` — computes the server's HASSH
  (MD5 of ordered KEX/cipher/MAC/compression algorithm lists) and, if
  `tps.gold_baseline_host` is set, compares it against a known-good
  reference daemon's HASSH.
- **B1 (`probe_state`):** Cross-session persistence — writes a marker file
  in one SSH session, reads it back in an independent second session.
- **B2 (`probe_payload`):** Echo-path sanity, plus (Module B runner only,
  when a compiled probe binary is present) drops and executes a real ELF
  binary over the shell and checks its arithmetic output — proves genuine
  code execution, not a canned response.
- **Live regrade (2026-07-27, post 0–100 score-scale + P95 defaults) against
  `cowrie/cowrie:latest`:** Module A quick **70.64**, full **57.07**; Module E
  benefits from SSH P95 **3000 ms**. Full composite UHQS **61.37 / D** (was
  **47.49** under the prior partial-point layout). See
  `docs/conformance/reports/cowrie/ssh/{quick,full}/`.
- **New, opt-in — `probe_shell_realism`** (not wired into any default run):
  runs a read-only recon battery real attackers run first (`uname -a`,
  `/proc/version`, `/proc/cpuinfo`, `id`, `$PATH`, `/etc/os-release`), then
  scores (a) cross-output consistency (does the claimed arch/kernel/distro
  agree across all five outputs), (b) generic/templated-output detection —
  **critical-gated** on byte-identical output across genuinely distinct
  commands, a vendor-neutral tell that a shell isn't actually executing
  anything, (c) PTY survival of a clear-screen escape + tab-completion
  trigger.
- **Why it's good:** the ELF-execution payload check and cross-session
  state check are hard to fake without a real, stateful POSIX shell behind
  the SSH listener — this is the strongest plugin in the suite specifically
  *because* it demands genuine command execution, not banner matching.
- **Disclosed limitation:** `probe_shell_realism` is real but not yet wired
  into any scored run (deliberately, to avoid silently changing existing
  scorecards) — treat it as available-but-inactive today.

## 2. HTTP — `protocols/http.py` 🟢 Tier 1

- **Standards:** RFC 9110/9112 (HTTP Semantics/Message Syntax).
- **A1:** `rfc_probes.probe_http_rfc9110`'s reject/invalid/unknown-method/
  bare-LF checks — validates the server correctly rejects malformed
  request lines rather than accepting anything.
- **A2:** The same suite's `valid_get` check — a well-formed request must
  get a well-formed response.
- **B1:** Two independent `GET /uhbs-marker` requests must both return an
  `HTTP/` status line — consistency, not just a single lucky reply.
- **Why it's good:** built on a real conformance test suite (shared with
  any other RFC 9110 consumer in this repo) rather than a bespoke,
  protocol-specific hand check.
- **Disclosed limitation:** no header-ordering, HTTP/2 upgrade, or cookie-
  handling checks yet (noted gap, not claimed).

## 3. SMTP — `protocols/smtp.py` 🟢 Tier 1

- **Standards:** RFC 5321 (SMTP).
- **A1:** `rfc_probes.probe_smtp_rfc5321`'s bad-sequence/unknown/bare-LF checks.
- **A2:** Greeting (220) + EHLO capability-list checks from the same suite.
- **B1:** `MAIL FROM` → `RSET` → `MAIL FROM` again — session-state reset is
  a real behavioral signal (a canary that doesn't actually track SMTP
  transaction state can't do this correctly).
- **Why it's good:** same "real RFC suite, not ad hoc" rationale as HTTP;
  the RSET-then-reuse check specifically targets stateful realism, not just
  banner correctness.

## 4. FTP — `protocols/ftp.py` 🟢 Tier 1 (this round)

- **Standards:** RFC 959 (FTP).
- **Named FSM sequence:** `Connect → Banner(220) → Unauthenticated RETR
  rejected → USER → PASS → PWD`, spread fail-fast across the three hooks.
- **A1 (`probe_fsm`) — `ftp.fsm.retr_before_auth` (critical=True):** an
  unauthenticated `RETR` **must** be rejected with 530/503/550. This is the
  canonical FTP security gate — a canary that lets an anonymous client pull
  files is a real security failure, not a cosmetic one, and is hard-gated
  so it can't be averaged away by a correct banner elsewhere.
- **A2:** Banner must start with `220`.
- **B1 (`probe_state`):** Walks `USER → PASS → PWD` on one connection with
  an explicit expected-reply-code check at each step and an early return on
  the first mismatch (rather than firing all three blind and grepping the
  combined output for "230 or 331 anywhere," which risks a coincidental
  substring false-positive).
- **Why it's good:** the pre-auth security gate is the single highest-value
  check a benchmark can run against an FTP canary, and it's now hard-gated
  rather than diluted.
- **Disclosed limitation:** no PASV data-channel or file-upload simulation yet.

## 5. Telnet — `protocols/telnet.py` 🟢 Tier 1 (this round)

- **Standards:** RFC 854 (Telnet).
- **A1/A2 (`telnet.fsm.iac_negotiation`, critical in Strict mode):** strictly
  requires a literal `IAC` (`0xFF`) byte in the response. **Fixed this
  round:** the prior version accepted `has_iac or len(data) > 0` — any
  non-empty TCP reply (an HTTP banner, an SSH banner, plain echo) used to
  pass as "Telnet." Now a target must produce a real IAC byte, or (Canary/
  Alert mode only) the miss is scored as explicit partial credit, not a
  disguised pass.
- **B1 (`probe_state`):** After real IAC negotiation (using a purpose-built
  `_negate_options` helper that replies `DO→WONT`/`WILL→DONT` so a server
  waiting for negotiation to settle will actually proceed), checks for a
  login/username prompt — a realism signal, not a security gate (a valid
  Telnet stack could legitimately skip a banner), so it is **not** critical.
- **Why it's good:** closes a real false-positive vector (bare open port ≠
  Telnet) with the cheapest possible fix — one literal-byte assertion — and
  the login-prompt check adds a genuine behavioral-realism signal on top.
- **Live regrade (2026-07-27) against real `cowrie/cowrie:latest`:**
  Module A effectively unchanged (77.5 → 77.4 quick; 75.5 → 77.4 full,
  within normal timing-sample noise) — the renamed, now-critical
  `telnet.fsm.iac_negotiation` check still passes, confirming Cowrie
  genuinely negotiates IAC rather than benefiting from the old tautology.
  Module B **62.5 → 82.5** (quick and full) — a real capability gain, not a
  formula artifact: the new `telnet.state.login_prompt` probe_state check
  replaces a flat `50`-point "no probe implemented" stub with a live
  detection of Cowrie's real `login:` prompt, scoring `100`. Full composite
  UHQS **64.90** (Telnet full, post scale fix). See
  `docs/conformance/reports/cowrie/telnet/{quick,full}/`.

## 6. Modbus — `protocols/modbus.py` 🟢 Tier 1 (this round)

- **Standards:** Modbus TCP / MBAP framing.
- **Named FSM sequence (`probe_state`, `modbus.state.write_read`, critical=True):**
  `Connect → Write register 0 = 0x1234 (FC 0x06) → Read holding register 0
  (FC 0x03) → Assert read_value == 0x1234`, fail-fast at each step with a
  named checkpoint in the failure detail. **Fixed this round:** the prior
  version only checked that *a* plausible-length response arrived — a
  static memory stub that ignores writes and always echoes a fixed dummy
  value would have scored 100/100 for "data-plane statefulness" it doesn't
  have. Real value-equality is now asserted and hard-gated.
- **A1/A2:** illegal-function-code exception handling; valid Read Holding
  Registers.
- **Encoding backend:** requests are built via `scapy.contrib.modbus` when
  the optional `uhbs[scapy]` extra is installed (byte-identical output,
  verified against the hand-rolled bytes for the same inputs), with an
  automatic, silent fallback to hand-rolled `struct.pack` bytes otherwise —
  scapy is **not** a hard dependency of this package or its Docker images.
- **Why it's good:** a real ICS/OT canary must now prove it actually
  persists a written value, the single most meaningful behavioral check
  available for this protocol class.

## 6b. S7comm — `protocols/s7comm.py` 🟡 Tier 1

- **Standards:** ISO-on-TCP (RFC 1006 TPKT) + COTP (ISO 8073) + S7comm Setup
  Communication. Aliases: `s7`, `iso-tsap`, `isotp`, `iso_on_tcp`.
- **A1 (`s7comm.fsm.truncated_tpkt`):** truncated TPKT length claim must not hang.
- **A2 (`s7comm.nego.cotp_cc`, critical in Strict mode):** COTP Connection
  Request → Connection Confirm (PDU type `0xD0`).
- **B1 (`s7comm.state.setup_communication`, critical in Strict mode):** after
  COTP CC, S7 Setup Communication (`0xF0`) must yield an S7 (`0x32`) ack.
  Dual-engine: Canary mode soft-scores COTP-only decoys.
- **Why it's good:** covers the other major ICS wire UHBS lists in
  `core-principles.md` alongside Modbus; COTP CC is the minimal proof of an
  ISO-TSAP stack before any PLC memory ops.
- **Disclosed limitation:** no Read/Write Var or SZL identity probing yet.

## 7. Redis — `protocols/redis.py` 🟡 Tier 1 (live-baseline verified)

- **Standards:** RESP (REdis Serialization Protocol).
- **A1 (`redis.fsm.invalid_verb`):** an unknown RESP verb must get a real
  `-ERR` reply. **Fixed this round:** `passed` is now derived directly from
  the score band (`passed = score >= 70`) rather than being set
  independently — the prior version could return `passed=True` at
  `score=40`, a boolean/numeric contract violation for any downstream
  consumer (dashboards, CI gates, other agents).
- **A2:** `PING` → `PONG`/`+` reply.
- **B1:** `SET`/`GET` round trip on a marker key.
- **Why it's good:** live-verified this round via
  `tests/test_plugin_baseline_live.py` against the real, official
  `redis:7-alpine` image (score ≥ 90/100), proving the plugin recognizes
  ground truth, not just "not a honeypot."

## 8. SMB — `protocols/smb.py` 🟢 Tier 1 (this round)

- **Standards:** MS-SMB2 (SMB1/SMB2/SMB3 dialect negotiation + Direct TCP transport).
- **Named FSM sequence:** `Connect → Negotiate (Direct-TCP-framed SMB1 PDU
  offering real dialects incl. "SMB 2.???") → Assert SMB1 (`\xffSMB`) or
  SMB2/3 (`\xfeSMB`) magic bytes in the unwrapped reply`.
- **A2 (`smb.nego.dialect_header`, critical=True):** **Fixed this round,
  twice.** Round 1: the plugin previously hardcoded `passed=True`
  unconditionally — it measured "TCP port 445 is open," not SMB
  negotiation, and could never fail. Round 2 (same day): the first fix
  still got an empty response from a real Samba daemon — root-caused to a
  missing mandatory 4-byte Direct TCP transport length header (MS-SMB2
  §2.1) that wraps *every* SMB message even without a legacy NBSS
  handshake; without it, Samba read the raw `\xffSMB` magic bytes as a
  bogus ~5MB length field and closed without replying. Both directions
  (`_direct_tcp_wrap`/`_direct_tcp_unwrap`) are now handled correctly.
- **B1:** negotiates twice on independent connections and asserts the same
  dialect family both times (consistency, non-critical).
- **Why it's good:** live-verified via `tests/test_plugin_baseline_live.py`
  against a real Samba (`dperson/samba`) daemon (score ≥ 90/100) — this is
  the plugin with the most thoroughly-documented root-cause history in the
  suite, specifically because it was the most broken.

## 9. MySQL — `protocols/mysql.py` 🟡 Tier 1

- **Standards:** MySQL client/server wire protocol (HandshakeV10).
- **A1:** truncated post-greeting packet must not hang/crash the connection.
- **A2:** greeting must start with protocol version `0x0A` or contain a
  `mysql`/`mariadb` banner substring (**fixed this round:** both substrings
  are now checked case-insensitively — the prior version checked `"MariaDB"`
  case-sensitively only, missing a lowercase banner variant).
- **B1 (`mysql.state.auth_deny`, critical in Strict mode):** sends a
  HandshakeResponse41 for an unrecognized user and requires an ERR packet
  (auth denial) — same security-gate rationale as FTP's pre-auth check.
  Dual-engine aware: Canary/Alert mode treats a missing deny as partial
  credit, not a hard fail, for log-only decoys that don't implement a real
  auth-deny error packet.
- **Why it's good:** auth rejection is the one MySQL check that actually
  matters for security fidelity, and it's hard-gated with an honest
  leniency path for canaries that were never designed to enforce it.
- **Disclosed limitation:** no SQL-syntax parsing or dynamic error-code testing yet.

## 9b. PostgreSQL — `protocols/postgres.py` 🟡 Tier 1

- **Standards:** PostgreSQL frontend/backend protocol v3 (StartupMessage /
  SSLRequest / Authentication* / ErrorResponse). Alias: `postgresql` → `postgres`.
- **A1 (`postgres.fsm.truncated_startup`):** truncated Startup length claim must
  not hang the harness (ErrorResponse, clean close, or non-timeout survival).
- **A2a (`postgres.nego.ssl_request`):** SSLRequest → single-byte `N` (refuse) or
  `S` (accept).
- **A2b (`postgres.nego.startup`):** StartupMessage → Authentication* (`R`) or
  ErrorResponse (`E`).
- **B1 (`postgres.state.auth_deny`, critical in Strict mode):** after
  AuthenticationCleartextPassword (or MD5), a bad password must yield
  ErrorResponse (typically SQLSTATE `28P01`). Dual-engine: Canary/Alert mode
  soft-scores decoys that AuthOk any password (common honeypot pattern).
- **Why it's good:** mirrors the MySQL auth-deny security gate for the other
  major database wire protocol UHBS grades; client-speaks-first framing is
  covered (unlike MySQL's server-first greeting).
- **Disclosed limitation:** no extended-query / COPY / cancel-request coverage yet.

## 10. RDP — `protocols/rdp.py` 🟢 Tier 1 (this round)

- **Standards:** RDP / X.224 connection request-confirm (ITU-T T.123 / RFC 1006 TPKT framing).
- **A1 (`rdp.fsm.truncated`):** **Fixed this round.** The prior check was
  `ok = not err` — a bare "the TCP connect didn't throw" tautology, true
  for almost any open port regardless of protocol. Now requires either a
  clean, error-free close, or a genuinely TPKT-shaped (`\x03\x00`-prefixed)
  reply.
- **A2 (`rdp.nego.x224`, now critical in Strict mode):** requires a
  TPKT-shaped reply or the specific OpenCanary-observed Connection Confirm
  bytes (`\x0e\xd0`). Newly critical-gated this round (was previously
  never gated).
- **B1 (`rdp.state.nla_fail`):** **Fixed this round.** The prior check
  (`bool(raw1) or bool(raw2) or not (err1 and err2)`) was true unless
  *both* independent connection attempts errored — now requires at least
  one of the two replies to be genuinely TPKT-shaped.
- **Why it's good:** live re-verified this round against the real
  `thinkst/opencanary` RDP module (all three checks still pass, aggregate
  ≈82/100) and confirmed to correctly fail (score 0.0) against a mismatched
  port serving HTTP instead.
- **Disclosed limitation:** does not probe TLS/NLA (CredSSP) yet — still Tier 1 for FSM/negotiation rigor, not for full RDP security-layer coverage.

## 11. SIP — `protocols/sip.py` 🟠 Tier 3 (UDP, alert-only aware)

- **Standards:** SIP (RFC 3261-family OPTIONS request).
- **A1/A2:** sends a garbage datagram / a real `OPTIONS` request; scores
  100 if a genuine `SIP/2.0` reply arrives, partial credit (35–60) if the
  UDP send itself succeeded with no reply (an intentionally-lenient
  "alert-only canary, not penalized as broken" stance — OpenCanary's SIP
  module is log-only by design).
- **Why the leniency is deliberate, not a bug:** UDP is connectionless —
  "no reply" and "actively malicious/broken" are indistinguishable at the
  transport layer for a fire-and-forget canary; `udp_base.py`'s dedicated
  timing probe (below) is where actual responsiveness gets measured
  properly, so these per-hook checks don't need to (and shouldn't)
  over-penalize silence.
- **Disclosed limitation:** `ok = not err` in `probe_fsm`/`probe_negotiation`
  is a weak signal for an *active* SIP responder (it mostly just confirms
  the datagram was sent) — acceptable for the documented alert-only use
  case, not yet critical-gated for a target claiming full SIP compliance.

## 12. SNMP — `protocols/snmp.py` 🟠 Tier 3 (UDP, alert-only aware)

- **Standards:** SNMPv1 GET (BER/ASN.1 encoding).
- **A1/A2:** same alert-only-aware pattern as SIP — a real SNMP GET for
  `sysDescr.0` gets full credit if a BER-`SEQUENCE`-shaped (`0x30`-prefixed)
  reply arrives, partial credit for silent-but-successful send.
- **Encoding backend:** built via `scapy.layers.snmp` when the optional
  `uhbs[scapy]` extra is present, hand-rolled BER-bytes fallback otherwise
  (mirrors OpenCanary's own optional-scapy pattern for its SNMP module).
- **Disclosed limitation:** same weak-signal caveat as SIP.

## 13. NTP — `protocols/ntp.py` 🟠 Tier 3 (UDP, alert-only aware)

- **Standards:** NTPv3 client mode + the CVE-2013-5211 `monlist` amplification probe.
- **A1/A2:** client-mode request scored on a full 48-byte reply.
- **B1 (`ntp.state.monlist`):** deliberately sends the classic `monlist`
  amplification-attack trigger and checks the canary survives the send —
  this is a security-relevant probe by design (does the target expose a
  known DDoS-amplification vector), not just a functionality check.
- **Disclosed limitation:** same alert-only weak-signal caveat as SIP/SNMP.

## 14. TFTP — `protocols/tftp.py` 🟠 Tier 3 (UDP, alert-only aware)

- **Standards:** TFTP (RFC 1350) RRQ/WRQ opcodes.
- **A1/A2:** bad-opcode survival; RRQ scored on a real DATA(3)/ERROR(5)/OACK(6) reply.
- **B1:** WRQ (write request) send survival.
- **Disclosed limitation:** same alert-only weak-signal caveat as SIP/SNMP/NTP.

## 15. VNC — `protocols/vnc.py` 🟢 Tier 1 (this round)

- **Standards:** RFB (Remote Framebuffer Protocol) 3.x handshake.
- **A1 (`vnc.fsm.bad_client_ver`):** **Fixed this round.** The prior check
  (`b"RFB" in raw or (not err)`) had the identical tautology shape already
  fixed in Telnet — *any* non-erroring reply passed as "VNC." Now requires
  a literal `RFB` banner or a clean, error-free close.
- **A2 (`vnc.nego.rfb_banner`, now critical in Strict mode):** requires the
  reply to start with `RFB `. Newly critical-gated this round.
- **B1 (`vnc.state.security`):** **Fixed this round.** Dropped a redundant
  `or not err` fallback; now requires concrete evidence of a security-type
  list (plausible reply length, or the VNC-Authentication type byte `0x02`
  actually present) rather than banner-presence alone.
- **Why it's good:** live re-verified this round against the real
  `thinkst/opencanary` VNC module (all three checks still pass, aggregate
  ≈89/100) and confirmed to correctly fail against a mismatched port.

## 16. Git — `protocols/git.py` 🟢 Tier 1 (this round)

- **Standards:** git daemon pkt-line wire protocol.
- **A1/A2/B1:** **Fixed this round.** All three hooks previously accepted
  "any non-empty reply" (`not err` alone; `text.startswith("00")` — true
  for most short replies, pkt-line or not; a bare `bool(raw)` fallback) as
  sufficient. All three now validate the reply is *syntactically*
  pkt-line-shaped via a real 4-hex-digit length-prefix decode
  (`plugin_sdk.PktLineBuilder.decode_length`), not a loose string prefix.
  `git.nego.upload_pack` is now critical-gated in Strict mode.
- **Why it's good:** live re-verified this round against the real
  `thinkst/opencanary` git module (all three checks still pass, aggregate
  ≈93/100 — the highest of the three protocols fixed this round) and
  confirmed to correctly fail against a mismatched port.

## 17. Generic fallback — `protocols/generic.py` 🟠 Tier 3 (by design)

- **Purpose:** the catch-all for any protocol identifier without a
  dedicated plugin — connect, capture whatever banner arrives, done. This
  is intentionally the floor of the suite, not a gap: it exists so an
  unrecognized protocol degrades to "we could reach it and got some bytes"
  rather than crashing the harness or silently skipping the target.

---

## Supporting infrastructure (not protocol-specific, but part of this audit)

- **`netutil.py`** — single source of truth for raw TCP/UDP transact/sample
  helpers; every plugin above uses this rather than hand-rolling sockets.
- **`udp_base.py`** — shared UDP timing base class: samples with a short
  per-attempt timeout, separates "genuinely replied" from "silently
  timed out" latency distributions rather than conflating them, and treats
  total silence as a measurement limitation (not a fidelity verdict either
  way) — the correct move given SIP/SNMP/NTP/TFTP's alert-only design.
- **`contract_validation.py`** — advisory lint (`validate_check_result`) plus
  the now load-bearing `has_passed_score_disagreement` helper wired directly
  into `check_scoring.score_checks`'s integrity gate (see §0).
- **`fingerprint.py` / `honeytoken.py` / `jitter.py`** — new, honestly-scoped,
  **opt-in, not-yet-wired** capabilities (TCP/TLS stack signals, OOB
  honeytoken plumbing, timing-jitter scoring). None of these affect any
  scored run today — flagged explicitly so this audit doesn't overstate
  current coverage.
- **`registry.py`** — `load_external_plugins()` discovers third-party
  `uhbs.plugins` entry points; a broken external package cannot crash the
  harness (try/except-wrapped), and overriding an existing plugin name now
  logs a `WARNING` (fixed this round — previously silent).
- **`tests/test_plugin_baseline_live.py`** — live verification against real
  (non-honeypot) reference daemons. **Current coverage: `redis`, `smb`
  only.** The other 15 plugins do not have live-daemon baseline coverage
  yet — stated plainly so this audit cannot be mistaken for a claim that
  it does.

---

## 2026-07-27 code-review fixes applied in this pass

| # | Finding | Fix |
|---|---|---|
| 1 (High) | `score_checks`'s legacy fallback let a `passed=True, score=0.0` check silently score `100.0`, bypassing even the critical-gate circuit breaker | New integrity gate (§0, step 2), reusing `contract_validation.has_passed_score_disagreement`; regression tests added |
| 2 (High) | Third-party entry-point plugins could silently override a built-in plugin name with zero logging | `registry.register()` now logs a `WARNING` on any type-changing override; regression test added |
| 3 (Medium) | `rdp.py`/`vnc.py`/`git.py` still had "port didn't error = pass" tautologies | Tightened all three to require real protocol-shaped evidence; added critical gates to each protocol's core negotiation check; live re-verified against real OpenCanary, no regression |
| 4 (Medium) | `contract_validation.py` built but never wired into anything | Wired into `check_scoring.score_checks` (also fixes #1) |
| 5 (Medium) | `mysql.py` checked `"mysql"` case-insensitively but `"MariaDB"` case-sensitively | Both now case-insensitive |
| 9–10 (missing tests) | No regression tests for the #1/#2 loopholes | Added to `tests/test_check_scoring.py` / `tests/test_entry_point_plugins.py` |

Verification after all fixes: `pytest -q` → **140 passed, 2 skipped**; `ruff check` → the same 5 pre-existing, untouched findings in `hassh.py`/`rfc_probes.py`; RDP/VNC/Git live-re-verified against the real `thinkst/opencanary` lab (all three still score well and now correctly fail against a mismatched port).
