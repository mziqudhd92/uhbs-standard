# Core Principles & Isolation Requirements

## Executive Mandate

This is the **mandatory** enterprise and academic standard before deploying any active decoys to production networks. Failure to meet baseline scores (**UHQS > 80**) exposes internal networks to lateral movement risks from compromised containment shells.

## 1. Objective & Scope

### 1.1 Purpose

UHBS provides an objective, repeatable, quantitative methodology for deception technology evaluation — a non-biased baseline for comparing and grading honeypots and decoy systems. It measures:

- Deception realism
- Security safety / containment
- Operational scale
- Telemetry quality

…**before** deploying decoys to production.

### 1.2 Universal Applicability

Framework **v4.0** is 100% protocol-agnostic, architecture-neutral, and **vendor-neutral**. It provides standard testing procedures for:

| Domain | Examples |
| --- | --- |
| **Standard IT Services** | SSH, Telnet, HTTP/S, RDP, SMB, FTP, database RPCs |
| **Industrial & OT/ICS** | Modbus TCP, DNP3, EtherNet/IP, BACnet, S7comm |
| **Next-Gen AI & Generative Decoys** | LLM-driven interactive shells, synthetic file systems, agentic decoys |
| **Cloud & SaaS** | Public-cloud control-plane APIs, container orchestration management interfaces, OAuth / identity endpoints |

## 2. Dual-Plane Audit Philosophy

To prevent decoy compromise via source exposure (open-source repositories, leaked container images, or supply-chain compromises), evaluation requires **two distinct testing planes**:

### White-Box Static Audit

Codebase analysis covering static credentials, logic flaws, prompt leaks, and dependency vulnerabilities. *(Primarily Module F, executed before live probing.)*

### Dynamic Adversarial Probing

Network-level, protocol-level, and execution-level attacks executed against a live target inside an **isolated sandbox**. *(Modules A–E.)*

## 3. Standard Test Bed Prerequisites

### Air-Gapped Sandbox

Target honeypots must be deployed in an isolated VLAN or container runtime with all external outbound connectivity blocked except through an auditing egress gateway.

### Gold Baseline System

Dynamic metrics must be compared against a true native baseline (e.g., standard general-purpose OS kernel, genuine industrial controller, un-emulated database engine) running under identical resource constraints.

## 4. Five-Phase Audit Workflow

| Phase | Name | Description |
| --- | --- | --- |
| 1 | Configuration & Profile Setup | Define `profile.yaml`, protocol expectations, register baselines |
| 2 | Static Audit Execution | Analyze repository code, container build manifests, and system prompts |
| 3 | Sandbox Environment Provisioning | Spin up the target with network egress monitors attached |
| 4 | Dynamic Adversarial Execution | Run Modules A–E via automated harnesses |
| 5 | Score Computation & Reporting | Apply Safety Gate \(\delta_C\) and emit the standardized scorecard |

!!! important "TPS is mandatory"
    The Target Profile Specification (`profile.yaml`) is a mandatory prerequisite. All module weights, latency thresholds, and safety boundaries are derived from the declared profile class — **no evaluation may proceed without a completed TPS**.

!!! danger "Production gate"
    Decoys with **UHQS ≤ 80** must not be deployed to production networks under this standard.
