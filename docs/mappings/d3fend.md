# MITRE D3FEND Mapping (Informative)

**Status:** Informative  
Maps UHBS profile classes and graded surfaces to the [MITRE D3FEND](https://d3fend.mitre.org/)
**Deceive** tactic. This does **not** redefine D3FEND, certify coverage of D3FEND
techniques, or change UHQS math. It helps SOC / architecture readers place a
UHBS scorecard in a defender-technique taxonomy.

Primary D3FEND references:

- [Deceive tactic](https://d3fend.mitre.org/tactic/d3f:Deceive/)
- Decoy Environment family (e.g. Standalone / Connected / Integrated Honeynet)
- Decoy Object family (Network Resource, File, Credential, Persona, Session Token, …)

## Decoy Environment (lab topology)

| UHBS lab posture | D3FEND technique | Notes |
| --- | --- | --- |
| Isolated Docker / air-gapped single container | Standalone Honeynet (`D3-SHN`) | Typical UHBS lab with `UHBS_AIRGAP_ATTESTED` |
| Decoy bridged to a monitored segment (no prod data plane) | Connected Honeynet (`D3-CHN`) | Topology claim is operator-attested; Module D measures containment |
| Decoy co-located with production-like services | Integrated Honeynet (`D3-IHN`) | Higher lateral risk — Safety Gate (Module D) is decisive |

UHBS does **not** auto-detect honeynet topology. Operators **MAY** record the
intended D3FEND environment ID under optional scorecard `framework_refs.d3fend`.

## Decoy Object (asset kind)

| UHBS graded surface | Typical D3FEND ID | Notes |
| --- | --- | --- |
| Listening protocol decoy (SSH, HTTP, Modbus, FTP, …) | Decoy Network Resource (`D3-DNR`) | Dominant UHBS corpus today (protocol plugins A/B/E) |
| Web-API / HTTP lure panel | `D3-DNR` | e.g. HellPot, ESPot, HoneyWire WebRouterDecoy |
| ICS/SCADA protocol listener | `D3-DNR` | e.g. Conpot Modbus |
| Low-Interaction shell / tarpit | `D3-DNR` | e.g. Cowrie SSH, Endlessh |
| Canary file / bait document | Decoy File (`D3-DF`) | Thin UHBS coverage today — corpus gap |
| Planted credentials / honey accounts | Decoy User Credential (`D3-DUC`) | Thin coverage — corpus gap |
| Fake identity / social lure | Decoy Persona (`D3-DP`) | Out of band for protocol harness |
| Fake session / auth token | Decoy Session Token (`D3-DST`) | Web-API adjacent; not a first-class UHBS class |

## Profile class → D3FEND (default reading)

| UHBS profile class | Default D3FEND tags | Reading |
| --- | --- | --- |
| Low-Interaction | `D3-DNR`, often `D3-SHN` | Network lure with limited post-connect depth |
| POSIX-Shell / GenAI-Shell | `D3-DNR` | Interactive shell lure; Module B realism dominates |
| Web-API | `D3-DNR` | HTTP(S) decoy / tarpit / fake panel |
| ICS-SCADA | `D3-DNR` | OT protocol lure |
| Database | `D3-DNR` | DB wire-protocol lure |

## Using this mapping

1. When publishing a UHBS scorecard, **MAY** set `framework_refs.d3fend` to one or
   more D3FEND technique IDs (e.g. `["D3-DNR", "D3-SHN"]`).
2. Prefer Decoy Object IDs for *what* was graded and Decoy Environment IDs for
   *how* it was deployed.
3. Mappings are **Informative**; UHQS, δ_C, and letter grades do **not** depend
   on them. UHBS does **not** claim D3FEND certification or complete Deceive-tactic coverage.
