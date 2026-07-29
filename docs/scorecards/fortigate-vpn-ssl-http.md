# Scorecard: FortiGate VPN-SSL Honeypot — http

**Status:** Informative · evaluation proof (not an endorsement)  
**UHBS:** **4.2.2** · **Class:** Web-API · **Protocol / surface:** `http`  
**Target id (lab):** `fortigate-vpn-ssl-http` · **Evaluation date:** 2026-07-29

| Run | UHQS | Grade | δ_C | Proof artifacts |
| --- | ---: | --- | --- | --- |
| Quick | see report hub | — | 0.5625 | Report hub quick artifacts |
| **Full (authoritative)** | **46.78** | **F** | **0.5625** | Verbatim SCORECARD below |

**Report hub:** [../conformance/reports/fortigate-vpn-ssl/http/index.md](../conformance/reports/fortigate-vpn-ssl/http/index.md)

## Proof: module scores (full run)

| Module | Score | Weight | Status | Notes |
| --- | ---: | --- | --- | --- |
| Module A | 70.6 | 0.25 | PASSED | status=200 |
| Module B | 82.5 | 0.20 | PASSED | survived binary blast |
| Module C | 100.0 | 0.20 | PASSED | telemetry_dir missing — set TPS/inventory telemetry_dir for C1 schema gates |
| Module D | 75.0 | 100 | GATE | PASSED (UHBS_AIRGAP_ATTESTED=1 (operator attestation; not a substitute for shell probes on SSH decoys |
| Module E | 100.0 | 0.15 | PASSED | service alive after load (connect 0.2ms |
| Module F | 70.0 | 0.20 | PASSED | POSIX coverage 0% (0/104 |

## Verbatim full SCORECARD

```text
====================================================================================
                  UNIVERSAL HONEYPOT BENCHMARK SCORECARD v4.2.2
====================================================================================
Target System         : fortigate-vpn-ssl-http
System Profile Class  : Web-API
Protocols             : http
Evaluation Date       : 2026-07-29
Evaluation Type       : Full-Spectrum (Static Audit + Dynamic Sandbox)
Environment           : Isolated Sandbox
MCP Surface Depth     : unknown
------------------------------------------------------------------------------------
EVALUATION MODULE                     SCORE (0-100)    WEIGHT    STATUS
------------------------------------------------------------------------------------
Module A: Protocol Fidelity         :  70.6/100       0.25     PASSED (status=200)
Module B: Behavioral Realism        :  82.5/100       0.20     PASSED (survived binary blast)
Module C: Telemetry Quality         : 100.0/100       0.20     PASSED (telemetry_dir missing — set TPS/inventory telemetry_dir for C1 schema gates)
Module D: Safety & Containment (C)  :  75.0/100       GATE     PASSED (UHBS_AIRGAP_ATTESTED=1 (operator attestation; not a substitute for shell probes on SSH decoys))
Module E: Scalability & Latency     : 100.0/100       0.15     PASSED (service alive after load (connect 0.2ms))
Module F: Static Code Audit         :  70.0/100       0.20     PASSED (POSIX coverage 0% (0/104))
------------------------------------------------------------------------------------
SAFETY GATE MULTIPLIER                : δ_C = 0.5625 (C = 75.0 < 95 — exponential penalty)
FINAL COMPOSITE SCORE (UHQS 4.2.2)      : 46.78 / 100
OVERALL EVALUATION GRADE              : GRADE F (Fail)
====================================================================================
```

## Replication

See [tutorial](../conformance/reports/fortigate-vpn-ssl/TUTORIAL.md) and [methodology](../conformance/reports/fortigate-vpn-ssl/METHODOLOGY.md).
