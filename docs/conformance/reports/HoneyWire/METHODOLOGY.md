# Methodology: HoneyWire UHBS lab

**Graded surface:** official `WebRouterDecoy` sensor (HTTP router-admin lure).  
**Not graded this round:** Hub dashboard, TcpTarpit, FileCanary, ICMP Canary, Network Scan Detector.

## Lab topology

1. HoneyWire **Hub** (`ghcr.io/andreicscs/honeywire-hub:latest`) on Docker network `uhbs-lab`, published at `127.0.0.1:18088`.
2. First-time `POST /api/v2/setup`, dashboard login, `POST /api/v2/nodes` to obtain a node `apiKey`.
3. `WebRouterDecoy` container with `HW_HUB_*` env vars; bind port `8081` published as `127.0.0.1:18081`.
4. `uhbs-lab` against inventory `HoneyWire-http` / class `Web-API` / protocol `http`.

## Module notes

| Module | Observation |
| --- | --- |
| A | HTTP FSM/negotiation/timing all passed (100). |
| B | Survived binary blast; router-login lure is shallow by design. |
| C | Partial — Hub receives Universal Event Standard JSON; harness telemetry dir had no STIX/OTel/ECS objects. |
| D | Air-gap attestation only (`UHBS_AIRGAP_ATTESTED=1`); δ_C = 0.5625. |
| E | Service remained reachable under load. |
| F | Source tree for WebRouterDecoy (+ SDK stubs); SAST tools skipped (`--skip-sast-tools`). |

## Environment caveats

- Published GHCR images are **linux/amd64**; Apple Silicon labs run under emulation.
- Sensors refuse to start without `HW_HUB_ENDPOINT`, `HW_HUB_KEY`, and `HW_SENSOR_ID`.
- Do not treat Hub UI reachability as decoy fidelity — grade the sensor listeners.

Informative only · UHBS 4.3.0 · not an endorsement.
