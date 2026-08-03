# Related Deception Frameworks (Informative)

**Status:** Informative · evidence-graded comparison  
**UHBS version:** 4.4.4

This page compares UHBS with fourteen deception-evaluation frameworks, taxonomies,
and research model families. Entries are **not** all adopted standards. Each row
states evidence maturity, unit of analysis, and whether UHBS should adopt, experiment
with, map, or leave out of scope for UHQS.

UHBS answers: *how good and safe is this decoy implementation?*  
Many entries answer different questions (program maturity, campaign design, placement
strategy, topology). Their scores must not be merged into UHQS.

See also the optional [Advanced Evidence Profile (AEP)](../advanced-evidence/index.md)
for controlled **lab** comparative experiments that stay outside the normative grade.
UHBS evaluation (including AEP) is for **laboratory / sandbox use**, not real-world
production testing.

## Trust limits

- Mappings are informative. They do not certify frameworks or claim UHBS implements them.
- Prefer peer-reviewed or DOI-linked sources; label preprints and practitioner blogs.
- **Credit:** source authors and venues are acknowledged in the ledger below and in
  [AEP research foundations](../advanced-evidence/research-foundations.md); citation
  does not imply those authors endorse UHBS.
- UHQS, weights, δ_C, and letter grades are unchanged by this page.

## Layer overview

| Layer | Entries | Question |
| --- | --- | --- |
| Asset quality | 5-Dimension, Dynamic MoE, Honeyval, ICS/OT | How good is this decoy? |
| Program / procurement | CDMM, 7-Criteria | Is the org / product ready? |
| Lifecycle / psychology | Cyber-Deception Chain, Belief-Scepticism | How is the campaign designed / perceived? |
| Strategic / formal | Game theory, information theory, ACI/economic | Where to place / how to optimize? |
| System / topology | CLOUDBURST/CAS, MTD, topology camouflage | How to evaluate network/cloud deception systems? |

## Source ledger (evidence maturity)

| Entry | Canonical source(s) | Maturity label |
| --- | --- | --- |
| 5-Dimension honeypot evaluation | Metrics-driven five-dimension proposals (e.g. Acta Polytechnica Hungarica / related surveys) | Proposed metrics framework (not an adopted standard) |
| CDMM | Practitioner maturity models (e.g. Deceptiq / industry blogs) | Practitioner guidance |
| Game-theoretic models | Zhu (2019) HotSoS tutorial DOI `10.1145/3314058.3314067`; Collins et al. (2024) arXiv `2401.13815`; signaling-game literature | Research family |
| Dynamic Honeypot MoE | Pittman et al., arXiv `2005.12969` | Peer-reviewed / preprint taxonomy |
| Cyber-Deception Chain | Heckman et al., *Cyber Denial, Deception and Counter Deception* (Springer) | Book / MITRE-adjacent framework; OODA is an adjacent lens |
| Belief-Scepticism | Descriptive attacker decision models (e.g. arXiv `2512.03641`) | Recent research / preprint |
| CLOUDBURST / CAS | Cloud-native beacon taxonomy (arXiv `2605.12976`) | Recent research / preprint |
| 7-Criteria enterprise | Vendor/practitioner evaluation checklists (e.g. realism, containment, telemetry, integration, adaptability, compliance, ease of use) | Practitioner / procurement guidance |
| Information-theoretic | Z-channel / KL / hypothesis-testing deception analyses | Research family |
| MTD evaluation | MTD-Playground (arXiv `2607.12199`), OpenMTD, PyMTDEvaluator | Research / tooling family |
| Honeyval | Google Research Honeyval (arXiv `2605.29963`) | Recent research / open tooling |
| ICS / OT frameworks | HoneyJudge, PLC interaction-level taxonomies, ICSLure | Research family |
| ACI / economic asymmetry | Cost-imposition / economic-denial / game-theoretic cost models | Research family (not a single named ACI standard) |
| Topology camouflage | NetHide, NetObfu, BottleNet, RDS, TopoSleuth | Research / tooling family |

## Comparison matrix

| Framework / model | Unit of analysis | What it measures | Common with UHBS | Unique vs UHBS | Primary use cases | UHBS improvement opportunity | Adoption |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **5-Dimension Framework** | Decoy deployment | Interaction, data quality, resource use, stealth, fingerprinting resistance | Overlaps A/B/C/E; weighted composite | Soft context indicators; runtime-only view | Academic comparison of deployments | Keep as conceptual mapping; UHBS already operationalizes most axes | Map only |
| **CDMM** | Organization | People/process/tech/coverage/integration/deployment maturity | Little overlap | Org roadmap, not asset grade | CISO deception-program planning | Use UHBS scorecards as evidence inputs to CDMM levels | Map only |
| **Game-theoretic models** | Strategy / placement | Equilibria, value of deception, disguise vs reveal | Detection risk ↔ Module A probes | Placement optimization, PBNE utilities | Research; deployment strategy | Optional VoD research metric in AEP; never substitute UHQS | Experiment (AEP VoD) |
| **Dynamic MoE taxonomy** | Dynamic honeypot | Fingerprinting, data capture, deception (sojourn/command slope), intelligence | Fingerprinting ↔ A; data capture ↔ C | Engagement yield metrics | Live deployment effectiveness | Informative engagement metrics / AEP DTDR | Adopt now (informative) |
| **Cyber-Deception Chain (+ OODA lens)** | Campaign lifecycle | Purpose→collect→plan→prepare→execute→monitor→reinforce→terminate | Safety Gate echoes risk management | Campaign orchestration | D&D campaign design | Evaluation-intent metadata; AEP for post-ops evidence | Map only |
| **Belief-Scepticism model** | Attacker decision | Belief, scepticism, fidelity, recon, experience | Fidelity ↔ A/B | Psychological engage/disengage | Controlled CTF/human studies | Design AEP human/agent experiments | Experiment |
| **CLOUDBURST / CAS** | Cloud honeytokens | Attribution quality, ephemeral decay, IAM depth, detection resistance | Stealth ↔ A | Cloud artifact classes UHBS does not grade | Cloud beacon selection | Coverage map / future decoy-object corpus | Adopt now (coverage map) |
| **7-Criteria enterprise** | Product / vendor | Realism, containment, telemetry, integration, adaptability, compliance, ease of use | Realism/containment/telemetry ↔ A-B/D/C | SOC integration, compliance, TCO | Procurement RFP | Checklist mapping, not UHQS weights | Map only |
| **Information-theoretic models** | Indistinguishability | Entropy/KL / hypothesis-testing distinguishability | A3 timing is informal cousin | Principled distinguishability bounds | Theory; formal detectability | AEP FSV with matched reference + detector TPR/FPR | Experiment |
| **MTD frameworks** | Moving-target systems | Mutation interval, attack success/time, defender advantage | Reproducible composite scoring philosophy | Path randomization / address shuffling | SDN MTD benchmarking | Future MTD-specific profiles only | Out of scope (generic UHQS) |
| **Honeyval** | LLM HTTP honeypots | Engagement, detection rate, cost, latency; agent + honeypot controls | Fidelity/stealth/latency ↔ A/B/E | Agentic attackers; paired control tasks | LLM honeypot R&D | AEP three-arm design; cost metrics | Experiment / adopt controls |
| **ICS / OT frameworks** | PLC / ICS decoys | Memory consistency, physics-aware process, honey system/service/token | ICS-SCADA class + modbus/s7comm | Device-memory anti-honeypot probes | Validating PLC decoys | Protocol state/memory probes (future) | Experiment |
| **ACI / economic asymmetry** | Attacker cost burden | Time/resource burn, cost-benefit break-even | Tarpits touch Module E (today “slow=bad”) | Attacker-cost as success signal | Justify tarpits / edge denial | AEP attacker/defender cost + tarpit interpretation | Adopt now (informative) |
| **Topology camouflage** | Network topology | Fake topologies, honey links, traceroute utility | Deception accuracy vs usability trade-offs | Whole-network obfuscation | LFA / recon defense | Separate topology profiles; not asset UHQS | Out of scope (generic UHQS) |

## Concrete UHBS takeaways

### Adopt now (informative)

1. Evaluation-intent metadata (asset vs program vs campaign vs topology).
2. Engagement-yield metrics where sessions exist (MoE / Honeyval).
3. Attacker- and defender-cost reporting (ACI); tarpit delay may be beneficial in AEP while Module E still reports latency.
4. Cloud / decoy-object coverage gaps (CLOUDBURST + D3FEND).

### Experiment (Advanced Evidence Profile)

1. Paired decoy vs reference + evaluator control (Honeyval-style).
2. Fingerprinting Susceptibility Vector across network/protocol/system/state layers.
3. Dwell-Time Distortion Ratio and Exploit Exhaustion Rate under censored trials.
4. Value of Deception with an explicit utility model (not `delta_uhqs`).
5. ICS memory/register consistency probes.

### Map only / out of scope for UHQS

- CDMM, Cyber-Deception Chain, 7-Criteria, Belief-Scepticism, game-theoretic placement, MTD, and topology camouflage do not redefine Modules A–F.

## Academic foundations for AEP (credited)

Full bibliographic credit, DOIs, and non-claim language:
[AEP Research foundations & credits](../advanced-evidence/research-foundations.md).

| Reference (short) | Role in AEP | Credit link |
| --- | --- | --- |
| Zhu (2019), HotSoS | Signaling/dynamic games vocabulary | [DOI 10.1145/3314058.3314067](https://doi.org/10.1145/3314058.3314067) |
| Collins, Xu & Brown (2024) | Uncertainty / practicality discipline | [arXiv:2401.13815](https://arxiv.org/abs/2401.13815) |
| Ersok et al. (2022), IEEE ICCC | Controlled CTF / log validation patterns | [DOI 10.1109/ICCC202255925.2022.9922853](https://doi.org/10.1109/ICCC202255925.2022.9922853) |
| Li et al. (2020), IEEE OJCS | Anti-honeypot *attacker* threat model (not defender grade) | [DOI 10.1109/OJCS.2020.3030825](https://doi.org/10.1109/OJCS.2020.3030825) |

## Next step

Optional **lab** controlled experiments: [Advanced Evidence Profile](../advanced-evidence/index.md).
