# HoneyWire — HTTP (WebRouterDecoy)

**Class:** Web-API · **Protocol:** http · **UHBS:** 4.4.5  
**Upstream sensor:** [WebRouterDecoy](https://github.com/andreicscs/HoneyWire/tree/main/Sensors/official/WebRouterDecoy)

This protocol hub collects UHBS-Lab artifacts for HoneyWire’s fake router-admin
HTTP lure (Netgear / TP-Link / Cisco skins). The decoy listens for browser and
scanner traffic, returns a login-style HTML surface, and forwards Universal
Event Standard payloads to the HoneyWire Hub when `HW_HUB_*` credentials are
configured. UHBS grades the **listener** with the built-in `http` plugin — not
the Hub dashboard.

| Mode | UHQS | Grade | δ_C | Artifacts |
| --- | ---: | --- | --- | --- |
| Quick | 45.84 | F | 0.5625 | [quick/](quick/README.md) |
| **Full (authoritative)** | **45.84** | **F** | **0.5625** | [full/](full/README.md) |

Parent hub: [HoneyWire](../index.md) · [Tutorial](../TUTORIAL.md) · [Methodology](../METHODOLOGY.md) · [Scorecard](../../../../scorecards/honeywire-http.md)

> Named product is evaluation proof only — not a UHBS endorsement.
