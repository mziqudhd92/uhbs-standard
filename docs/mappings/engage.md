# MITRE Engage Mapping (Informative)

**Status:** Informative  
Maps UHBS evaluation modules to [MITRE Engage](https://engage.mitre.org/) adversary
engagement goals. This does **not** redefine Engage, certify Engage operations, or
change UHQS math. It helps operators answer “what was this decoy *for*?” when
reading a scorecard.

Engage frames deception as a **process** (Prepare → Expose / Affect / Elicit →
Understand), not a fire-and-forget appliance. UHBS grades the *asset and harness
evidence*; Engage goals describe the *operational intent*.

## Module → Engage goals

| UHBS module | Engage goal(s) | Notes |
| --- | --- | --- |
| A — Protocol Fidelity | **Elicit** (Reassurance) | Believable protocol speak keeps the adversary in the engagement environment |
| B — Behavioral Realism | **Elicit** (Motivation / Reassurance) | Post-connect depth encourages richer TTPs without collapsing the lure |
| C — Telemetry Quality | **Expose**, **Understand** | High-fidelity logs / CTI turn contact into detection and intel |
| D — Safety & Containment | Prepare / Affect constraint | Engagement stays on **defender-controlled** ground (no hack-back); Safety Gate δ_C |
| E — Scalability & Latency | **Expose** / **Affect** | Survives load so the lure remains available under scan / abuse |
| F — Static Code Audit | Prepare | Hygiene of the decoy codebase before deployment |

Engage’s **Affect** activities (raise adversary cost, lower value of stolen bait)
are only meaningful when Module D containment holds. A high A/B score with a
failing Safety Gate is not a successful engagement environment under Engage’s
defender-network boundary.

## Checklist: which Engage goal is this decoy for?

Copy into a lab `METHODOLOGY.md` when publishing proof. Mark one primary goal.

- [ ] **Expose** — primary outcome is high-fidelity alert / presence signal when the adversary touches the lure
- [ ] **Affect** — primary outcome is to waste adversary time / divert from real assets (tarpits, dead-end panels)
- [ ] **Elicit** — primary outcome is richer TTP / malware / tool use inside a controlled environment
- [ ] **Understand** — primary outcome is analyst-usable intel from Module C telemetry (STIX / structured logs)

Supporting notes (optional):

- Intended Engage activities (e.g. Lures): ________________
- ATT&CK techniques expected in telemetry: ________________
- D3FEND Decoy Object / Environment IDs: see [d3fend.md](d3fend.md)

## Using this mapping

1. When publishing a UHBS scorecard, **MAY** set `framework_refs.engage_goals` to
   one or more of `Prepare`, `Expose`, `Affect`, `Elicit`, `Understand`.
2. Prefer a **primary** goal in methodology prose; list secondary goals in
   `framework_refs` only when they were explicit lab design intent.
3. Mappings are **Informative**; UHQS math does **not** depend on them. UHBS does
   **not** claim Engage certification or that a scorecard proves a completed
   Engage operation.
