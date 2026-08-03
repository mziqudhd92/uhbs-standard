# HoneyWire (andreicscs)

**Status:** Informative · evaluation proof  
**Upstream:** [https://github.com/andreicscs/HoneyWire](https://github.com/andreicscs/HoneyWire) · GitHub last push `2026-07-19`  
**Runtime:** `ghcr.io/andreicscs/honeywire-hub` + `ghcr.io/andreicscs/honeywire-webrouterdecoy` (amd64 images under emulation on arm64 lab hosts)

HoneyWire is a distributed canary / deception platform (Hub + wizard + sensors). This UHBS round grades the official **Web Router Decoy** sensor (fake Netgear/TP-Link/Cisco admin panel) with the UHBS **http** plugin. The Hub UI itself is management plane, not a decoy surface.

## What this decoy is

A lightweight Go HTTP lure that mimics router admin login pages, captures reconnaissance and credential attempts, and posts Universal Event Standard payloads to the HoneyWire Hub.

## Protocol survey

| Surface | UHBS plugin? | Graded? | Quick | Full |
| --- | --- | --- | --- | --- |
| [HTTP (WebRouterDecoy)](http/index.md) | yes (`http`) | **yes** | [45.84 / F](http/quick/README.md) | [45.84 / F](http/full/README.md) |
| TCP Tarpit | yes (`generic`) | **no** | — | re-queue when hermetic recipe needed |
| FileCanary / ICMP / NetworkScan | no first-class plugin | **no** | — | tripwire / FIM / ICMP surfaces |

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product is evaluation proof only — not a UHBS endorsement.

## For CTI analysts

- WebRouterDecoy attracts internal / LAN recon against fake router admin panels (credential harvesting + path probing).
- Events are designed for the HoneyWire Hub (and optional SIEM via syslog) — not STIX/OTel in the UHBS harness directory by default.

**Primary signals you can expect (when Hub/SIEM is wired):** HTTP request lines, login attempts, User-Agents, sensor node identity.

## For blue teams / detection engineering

- Treat Hub and sensors as separate trust domains (upstream recommends separate hosts).
- Serve Hub over HTTPS in production; node keys authenticate sensor POSTs.
- UHBS Module C reflects harness-visible telemetry schemas — Hub-native events still need your own shipping pipeline.

## Trust & limitations

- This page is **evaluation proof** under UHBS 4.4.1 — not a certification or vendor ranking.
- Prefer **full/** artifacts over **quick/** for operational decisions (scores matched in this run).
- Re-run via [TUTORIAL.md](TUTORIAL.md); environment notes in [METHODOLOGY.md](METHODOLOGY.md).
- How to read modules: [READING-UHQS.md](../READING-UHQS.md)
