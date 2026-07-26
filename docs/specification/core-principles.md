# Core Principles & Isolation Requirements

## 1. Objective & Scope

### 1.1 Purpose

UHBS provides an objective, repeatable, and quantitative methodology for benchmarking honeypots, decoys, and deception technology. It serves as an enterprise and academic baseline to measure:

- Deception realism
- Security safety / containment
- Operational scale
- Telemetry quality

…**before** deploying decoys to production.

### 1.2 Universal Applicability

Framework **v4.0** is 100% protocol-agnostic and architecture-neutral. It provides standard testing procedures for:

| Domain | Examples |
| --- | --- |
| **Standard IT Services** | SSH, Telnet, HTTP/S, RDP, SMB, FTP, Database RPCs (SQL, Redis) |
| **Industrial & OT/ICS** | Modbus TCP, DNP3, EtherNet/IP, BACnet, Siemens S7 |
| **Next-Gen AI & Generative Decoys** | LLM-driven interactive shells, synthetic file systems, agentic decoys |
| **Cloud & SaaS** | AWS/Azure/GCP API endpoints, Kubernetes management interfaces, OAuth endpoints |

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

Dynamic metrics must be compared against a true native baseline (e.g., standard Linux kernel, genuine SCADA PLC, un-emulated database engine) running under identical resource constraints.

## 4. Five-Phase Audit Workflow

| Phase | Name | Description |
| --- | --- | --- |
| 1 | Configuration & Profile Setup | Define `profile.yaml`, protocol expectations, register baselines |
| 2 | Static Audit Execution | Analyze repository code, Dockerfiles, and system prompts |
| 3 | Sandbox Environment Provisioning | Spin up the target with network egress monitors attached |
| 4 | Dynamic Adversarial Execution | Run Modules A–E via automated harnesses |
| 5 | Score Computation & Reporting | Apply Safety Gate \(\delta_C\) and emit the standardized scorecard |

!!! important "TPS is mandatory"
    The Target Profile Specification (`profile.yaml`) is a mandatory prerequisite. All module weights, latency thresholds, and safety boundaries are derived from the declared profile class — **no evaluation may proceed without a completed TPS**.
