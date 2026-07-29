# How to read UHBS lab proof (CTI & blue team)

**Audience:** cyber threat intelligence analysts, detection engineers, and blue-team operators reviewing published UHBS evaluation proof.  
**UHBS version:** 4.2.2 · **Nature of these pages:** informative evaluation proof — **not** product endorsements, certifications, or “best honeypot” rankings.

## What a published grade is

Each lab run produces a **UHQS** score (0–100) and a letter grade under a named **class** (for example Low-Interaction) and **protocol** (SSH, HTTP, …). Scores come from modules **A–F** plus the Safety Gate multiplier **δ_C**:

| Module | Question it answers | Blue-team / CTI use |
| --- | --- | --- |
| **A — Protocol fidelity** | Does the decoy speak the protocol well enough to look like a real service? | Whether scanners and commodity malware will stay engaged long enough to leave telemetry |
| **B — Behavioral realism** | Do post-connect behaviors (auth, sessions, payloads) feel plausible? | Whether interactive attackers / bots continue; weak B often means “credential logger only” |
| **C — Telemetry quality** | Can the harness observe useful session evidence from the lab setup? | Whether *this graded lab* produced analyst-usable logs — not a claim about your production SIEM wiring |
| **D — Safety & containment** | Does the decoy stay contained (Safety Gate)? | Deployment risk: δ_C &lt; 1 collapses UHQS when containment fails |
| **E — Scalability & latency** | Timing vs TPS P95 expectations | Whether the decoy remains responsive under probe load |
| **F — Static code audit** | Source-level signals from the checkout used in the lab | Hygiene / supply-chain posture of **that** tree — not a full CVE audit |

**Prefer `full/`** over `quick/` when making operational judgments. Quick runs are smoke-oriented (fewer timing samples, often SAST skipped).

## Trust checklist (before you cite a grade)

1. Open the **product hub** → protocol page → confirm **full** UHQS and module table.
2. Open [`SCORECARD.txt`](./) and [`report.json`](./) under `full/` — they are the machine/human primary artifacts.
3. Read **Methodology** for lab image, ports, air-gap attestation, and limitations.
4. Read **Tutorial** if you need to re-run the same UHBS-Lab path.
5. Treat product names as **proof labels only** (vendor-neutral UHBS vocabulary is class + protocol).

## How CTI analysts should use these pages

- Map **protocol + interaction depth** to collection strategy (Internet noise vs targeted intrusion).
- Use module notes (auth failed, tarpit, banner quirks) to anticipate **what ATT&CK-ish activity** you will and will not see.
- Do **not** treat UHQS as “threat level” or malware sophistication — it grades the **decoy**, not the attacker.

## How blue teams should use these pages

- Decide whether a decoy is suitable as a **sensor** (telemetry) vs a **delay/tarpit** vs a **credential sink**.
- Check **δ_C / Module D** before exposing anything beyond a lab VLAN.
- Expect to **wire your own** logging/SIEM; Module C reflects the graded lab harness, not your enterprise pipeline.
- Replicate with the tutorial before trusting numbers in change-control or architecture reviews.

## Grade bands (letter)

Approximate UHQS bands used in published proof: **A ≥ 90**, **B ≥ 80**, **C ≥ 70**, **D ≥ 60**, else **F**. An **F** means the composite did not clear the bar for that profile — it does **not** mean “unsafe to study” or “useless as a sensor.” Many credential-only decoys score low on B/C while still producing useful auth attempt telemetry when correctly deployed.
