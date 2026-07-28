# Target Profile Specification (TPS)

Before evaluating a honeypot, the auditor must create a **Target Profile Specification** (`profile.yaml`) that defines expectations for that decoy class.

## Required Sections

### `target_metadata`

| Field | Description |
| --- | --- |
| `name` | Human-readable decoy name |
| `class` | One of: `POSIX-Shell`, `ICS-SCADA`, `Web-API`, `Database`, `GenAI-Shell`, `Low-Interaction` |
| `protocol` | Primary protocol identifier |

### `performance_baseline`

| Field | Description |
| --- | --- |
| `p95_latency_ms` | Expected maximum P95 latency (ms); standard default **150** |
| `strict_rfc_enforcement` | When true, protocol FSM deviations fail Module A hard |

### `safety_boundary`

| Field | Description |
| --- | --- |
| `allowed_outbound` | Allow-list of outbound destinations (empty = deny-all except audit gateway) |
| `allow_local_code_execution` | Whether the decoy intentionally executes attacker-supplied code |

### `module_weights`

Profile-adaptive UHQS weights `w_A` … `w_F` that **must sum to 1.00**.

## Example

See the starter template: [`templates/profile.yaml`](https://github.com/mziqudhd92/uhbs-standard/blob/main/templates/profile.yaml).

```yaml
uhbs_version: "4.2.1"
target_metadata:
  name: "Example POSIX Shell Decoy"
  class: "POSIX-Shell"
  protocol: "ssh"
performance_baseline:
  p95_latency_ms: 150
  strict_rfc_enforcement: true
safety_boundary:
  allowed_outbound: []
  allow_local_code_execution: false
module_weights:
  w_A: 0.20
  w_B: 0.25
  w_C: 0.20
  w_E: 0.15
  w_F: 0.20
```

## Validation

Profiles are validated against [`schemas/profile.schema.json`](https://github.com/mziqudhd92/uhbs-standard/blob/main/schemas/profile.schema.json):

```bash
uhbs validate-profile path/to/profile.yaml
```

!!! important
    The TPS is mandatory. All module weights, latency thresholds, and safety boundaries are derived from the declared profile class — **no evaluation may proceed without a completed TPS**.
