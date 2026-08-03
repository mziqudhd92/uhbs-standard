# Evaluation Modules (A–F)

UHBS v4.4.4 defines six evaluation modules. Module **D** is the **Safety Gate**; a containment score below 95 applies an exponential penalty to the composite UHQS.

---

## Module A: Protocol & Syntax Fidelity

**Objective:** Verify that the honeypot accurately implements the targeted protocol and does not reveal its emulated nature through network artifacts or timing side-channels.

| Step | Name | Procedure |
| --- | --- | --- |
| **A1** | Protocol FSM Inspection | Issue valid, out-of-order, and invalid protocol verbs sequentially; verify exact protocol-mandated status codes. |
| **A2** | Header & Negotiation Parity | Query capability negotiation strings, cipher suites, and server headers; compare against standard OS/device fingerprint baselines for the target protocol. |
| **A3** | Statistical Side-Channel Analysis | Measure response timing jitter across 1,000 simple queries; require inter-arrival-time distribution to match the gold baseline using a two-sample goodness-of-fit test. |

---

## Module B: Behavioral & Stateful Realism

**Objective:** Confirm that the honeypot maintains consistent session state, persists dynamic modifications, and handles non-standard attacker inputs.

| Step | Name | Procedure |
| --- | --- | --- |
| **B1** | Cross-Session State Persistence | Modify session state (file create, coil change, DB insert) and re-query; assert 100% of dynamic state changes persist. |
| **B2** | Payload Handling & Execution | Send class-tailored workloads; process realistically or fail gracefully without stack traces or dropped connections. |
| **B3** | Non-UTF8 & Input Stress Fuzzing | Flood with raw binary, null bytes, and improper encodings; confirm zero unhandled exceptions or unexpected resets. |

---

## Module C: Telemetry Quality & Pipeline Resilience

**Objective:** Ensure the decoy produces clean, structured threat intelligence (CTI) that cannot be corrupted or blinded by an attacker.

| Step | Name | Procedure |
| --- | --- | --- |
| **C1** | Schema Conformance | Validate 100% compliance against STIX 2.1, OpenTelemetry, or ECS with accurate MITRE ATT&CK mapping. |
| **C2** | Log Injection & Parser Fuzzing | Inject ANSI escapes, unescaped quotes, nested JSON, newline injections; verify sanitization and SIEM parser stability. |

!!! tip "Force multiplier"
    Telemetry integrity multiplies the value of the entire security stack. Corrupted or injectable logs can blind SIEM/SOAR pipelines — Module C is a critical quality gate independent of deception realism.

---

## Module D: Safety, Containment & Boundary Controls

**Objective:** Guarantee that the honeypot cannot be exploited to breach underlying infrastructure, escalate privileges, or conduct outbound attacks.

| Step | Name | Procedure |
| --- | --- | --- |
| **D1** | Out-of-Band (OOB) Egress Sweeps | Attempt ICMP, DNS tunneling, HTTP/S, and raw TCP/UDP egress; confirm **0%** unauthorized traffic exits the sandbox. |
| **D2** | Container Escape & LPE | Execute standard container breakout checks (runtime control sockets, cgroups abuse, sensitive `/proc` or `/sys` mounts); confirm zero access to underlying host hardware or runtime namespaces. |
| **D3** | GenAI Boundary & Prompt Injection *(if applicable)* | Multi-turn indirect prompt injections and context exhaustion; verify zero system-prompt leaks or guardrail breaches. |

!!! danger "Safety Gate"
    A Module D score **below 95** triggers the exponential multiplier \(\delta_C = (C/100)^2\), degrading the entire UHQS regardless of other module performance.

---

## Module E: Scalability, Latency & Stress Performance

**Objective:** Evaluate performance under sustained, automated attack conditions.

| Step | Name | Procedure |
| --- | --- | --- |
| **E1** | Connection Saturation Stress | Ramp workers to peak capacity; measure P50/P95/P99; ensure P95 remains below the TPS threshold (standard **&lt; 150 ms**). |
| **E2** | Resource Exhaustion & Circuit Breaking | Flood memory-intensive operations; verify clean circuit-breaker engagement with **zero crashes** or thread-blocking loops. |

| Metric | Requirement |
| --- | --- |
| P95 latency | &lt; 150 ms under peak concurrent load (unless TPS overrides) |
| P50 / P99 | Recorded for full latency distribution |
| Crashes | **0** allowed under resource exhaustion |

---

## Module F: White-Box Static Code Audit

**Objective:** Analyze honeypot source and deployment artifacts for vulnerabilities discoverable prior to deployment.

| Step | Name | Procedure |
| --- | --- | --- |
| **F1** | Static Security & SAST | Execute industry-standard SAST and container image scanners across the repository and deployment artifacts; target zero High or Critical vulnerabilities, RCE flaws, or insecure system command wrappers. |
| **F2** | Hardcoded Key & Secret Detection | Scan for embedded keys, static seeds, default SSH host keys, static MACs; target zero deterministic secrets. |
| **F3** | Coverage & Unsupported Command Review | Compare handlers vs. target standards; measure fully handled requests vs. unhandled fallback stubs. |
