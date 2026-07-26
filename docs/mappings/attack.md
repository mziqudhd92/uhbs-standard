# ATT&CK Technique Mapping (Informative)

**Status:** Informative  
Maps UHBS evaluation modules to [MITRE ATT&CK](https://attack.mitre.org/) techniques
commonly exercised or observed during decoy evaluation. This does **not** redefine
ATT&CK; it helps GRC and detection engineering teams place UHBS results in existing
taxonomies.

| UHBS module / step | ATT&CK technique(s) | Notes |
| --- | --- | --- |
| A1 Protocol FSM | T1040, T1595 | Network sniffing / scanning against protocol state |
| A2 Negotiation / fingerprint | T1082, T1016 | System / network discovery via banners & fingerprints |
| A3 Timing side-channel | T1595 | Active scanning with statistical timing |
| B1 Cross-session state | T1059, T1105 | Command execution / ingress tool transfer analogs |
| B2 Payload handling | T1203, T1059 | Exploitation / interpreter abuse against decoy handlers |
| B3 Input fuzzing | T1499 | Endpoint DoS / resource exhaustion via malformed input |
| C1 Schema / ATT&CK mapping in logs | T1071, TA0011 | C2 channel realism in telemetry quality |
| C2 Log injection | T1565, T1070 | Data manipulation / indicator removal via log poison |
| D1 OOB egress | T1041, T1572, T1090 | Exfiltration / tunneling / proxy from compromised shell |
| D2 Container escape / LPE | T1611, T1068 | Escape to host / privilege escalation |
| D3 Prompt injection (GenAI) | T1059 (adjacent) | LLM boundary bypass — map per org GenAI threat model |
| E1 Connection saturation | T1498, T1499 | Network / endpoint DoS under load |
| E2 Resource exhaustion | T1499 | Resource hijacking / crash loops |
| F1 SAST / vulns | T1190, T1195 | Exploit public-facing app / supply chain |
| F2 Secrets in source | T1552 | Unsecured credentials |
| F3 Coverage gaps | T1083 | File/command discovery of unhandled stubs |

## Using this mapping

1. When publishing a UHBS scorecard, **MAY** attach ATT&CK IDs for failed checks.
2. Module C **SHOULD** emit MITRE technique IDs in CTI when `mitre_attack_mapping: true`.
3. Mappings are **Informative**; UHQS math does not depend on them.
