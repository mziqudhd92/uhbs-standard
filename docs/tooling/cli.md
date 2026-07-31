# CLI & Validator Guide

**Status:** Normative (CLI behavior for UHBS-Core)

The `uhbs` CLI validates Target Profile Specifications and scorecards against the
official JSON Schemas, enforces class→weight tables, and recomputes UHQS.

For the full executable Modules A–F harness, see
[Reference Implementation](../reference-implementation.md).

When a command runs, the CLI prints this notice on **stderr** (stdout stays clean
for JSON / machine output):

```text
NOTICE: UHBS/AEP are for lab/sandbox evaluation of decoys. Do not run them against production or unauthorized real services.
```

Human-facing lines (NOTICE / OK / ERROR) use ANSI colors when stderr/stdout is a
TTY. Disable with `NO_COLOR=1`; force with `FORCE_COLOR=1`. No extra color
library is required (Click is already a dependency; styling is in
`uhbs_core.termui`).

## Install

```bash
git clone https://github.com/mziqudhd92/uhbs-standard.git
cd uhbs-standard
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uhbs --help
```

### UHBS-Lab harness

```bash
pip install -e ".[lab]"
uhbs lab --list-protocols
uhbs-lab --help
# Grade an MCP honeypot (HTTP/SSE JSON-RPC):
# uhbs-lab --inventory … --protocol mcp --tps …/mcp_server.yaml --out ./reports/mcp
```

Built-in protocols in v4.3.5 (**36**): `bluetooth`, `dhcp`, `dns`, `ftp`,
`generic`, `git`, `http`, `httpproxy`, `imap`, `ipp`, `irc`, `kubernetes`,
`ldap`, `mcp`, `memcache`, `modbus`, `mongodb`, `mssql`, `mysql`, `ntp`,
`oracle`, `pjl`, `pop3`, `postgres`, `rdp`, `redis`, `s7comm`, `sip`, `smb`,
`smtp`, `snmp`, `socks5`, `ssh`, `telnet`, `tftp`, `vnc` (plus registry aliases
such as `postgresql`, `pop`, `s7`, …).

MCP honeypot grading is part of `uhbs[lab]` (protocol plugin `mcp`). The separate `uhbs[mcp]` / `uhbs-mcp` entry point is only for AI-host scorecard tools — see [MCP honeypot grading](../architecture/mcp-honeypot-grading.md).

### MCP server (AI hosts)

For Cursor / Claude Desktop / VS Code agents that speak the
[Model Context Protocol](https://modelcontextprotocol.io/):

```bash
pip install -e ".[mcp]"
# then configure the host — see tooling/mcp.md
uhbs-mcp   # stdio JSON-RPC (or: python -m uhbs_mcp)
```

Full guide: [MCP server](mcp.md) · registry metadata: repo-root `server.json`.

### Optional Advanced Evidence Profile (AEP)

Offline analysis of **local** controlled-trial evidence. Does **not** change UHQS
and never launches attacks, probes, containers, or network connections.

```bash
pip install -e ".[aep]"   # or: pip install 'uhbs[aep]'
uhbs aep --help
uhbs aep example beginner --out aep-beginner   # packaged synthetic fixture
uhbs aep init --class Web-API --out aep-experiment/
uhbs aep validate aep-experiment/experiment.yaml
uhbs aep validate-trials aep-experiment/trials.jsonl --experiment aep-experiment/experiment.yaml
uhbs aep analyze --experiment aep-experiment/experiment.yaml \
  --trials aep-experiment/trials.jsonl --out advanced-evidence.json
uhbs aep report advanced-evidence.json --format markdown --out ADVANCED-EVIDENCE.md
```

Extras at a glance: `uhbs[lab]` (live harness) · `uhbs[mcp]` (AI-host tools) ·
`uhbs[aep]` (offline evidence). Full guide:
[AEP CLI](../advanced-evidence/cli.md) ·
[Beginner tutorial](../advanced-evidence/tutorial-beginner.md) ·
[Advanced tutorial](../advanced-evidence/tutorial-advanced.md).

### Docker image

Build once from the repository root:

```bash
docker build -t uhbs:4.3.5 .
```

The image entrypoint is `uhbs`. Mount your project at `/work`:

```bash
docker run --rm -v "$PWD:/work" -w /work uhbs:4.3.5 --help
docker run --rm -v "$PWD:/work" -w /work uhbs:4.3.5 \
  validate-scorecard ./docs/conformance/fixtures/cowrie-low-interaction.scorecard.json
docker run --rm -v "$PWD:/work" -w /work uhbs:4.3.5 lab --list-protocols
```

For live Modules A–E probes, point `--target` at a host reachable from the
container (`host.docker.internal` on Docker Desktop, or a shared compose
network). Prefer an isolated lab; do not point the harness at production.

Optional compose wrapper: `docker compose run --rm uhbs <command>…`.

Published honeypot lab reports (quick + full artifacts, tutorials):  
[docs/conformance/reports/](../conformance/reports/index.md).

Schema discovery inside the image uses `UHBS_ROOT` / `UHBS_SCHEMA_DIR`
(defaults set in the Dockerfile).

### Protocol-agnostic lab tips

- Always pass `--protocol <id>` (or inventory `protocols`) for the decoy’s real
  listener (`http`, `pjl`, `ssh`, `modbus`, …).
- Builtin `low_interaction` is **class-only** (weights). Use `low_interaction_ssh`
  only for SSH/Telnet decoys.
- Mixing an SSH TPS with `--protocol pjl` (etc.) fails fast with
  `ProtocolConflictError` instead of hanging on Paramiko.
- Module D shell probes run only when `ports.ssh` / `ssh_port` is explicit.

## Commands

### Validate a profile

```bash
uhbs validate-profile templates/profile.yaml
uhbs validate-profile templates/profiles/low-interaction.yaml
```

Checks:

- JSON Schema conformance (`schemas/profile.schema.json`)
- Module weights sum to \(1.00 \pm 0.001\)
- Class→weight table match (strict mode, default on)

### Validate a scorecard (with integrity)

```bash
uhbs validate-scorecard docs/conformance/fixtures/cowrie-low-interaction.scorecard.json
uhbs validate-scorecard docs/conformance/fixtures/posix-shell-lab.scorecard.json
```

Strict mode (default) **recomputes** UHQS, δ_C, and letter grade and **MUST** fail
if declared values diverge from the normative formula.

Conformance fixtures may name specific products as **evaluation proof** only;
see [Conformance](../conformance/index.md).

### Validate an evidence pack

```bash
uhbs validate-evidence path/to/evidence-pack.json
```

### Compute UHQS

```bash
uhbs score --class Low-Interaction --scores scores.json
uhbs score --profile templates/profile.yaml --scores scores.json
```

Where `scores.json` contains module scores:

```json
{
  "A": 23.5,
  "B": 42.5,
  "C": 57.0,
  "D": 100,
  "E": 55.0,
  "F": 69.0
}
```

Expected for this **worked example** under Low-Interaction weights: **UHQS = 46.97**
(Grade F). That is **not** the live Cowrie fixture (UHQS **61.37** — see
[`docs/conformance/fixtures/cowrie-low-interaction.scorecard.json`](../conformance/fixtures/cowrie-low-interaction.scorecard.json)).

## CI Integration

`.github/workflows/ci-validate.yml` runs schema validation and conformance
fixtures on every push and pull request.
