# Writing a third-party UHBS protocol plugin

> **Status:** Phase 1 / experimental extension point. UHBS is a personal
> open-source beta framework (see [`AGENTS.md`](https://github.com/mziqudhd92/uhbs-standard/blob/main/AGENTS.md) and
> [`GOVERNANCE.md`](https://github.com/mziqudhd92/uhbs-standard/blob/main/GOVERNANCE.md)) — this page describes what the code
> does today, not a certified or committee-reviewed plugin API.

UHBS ships 18+ built-in protocol plugins under `src/uhbs_core/protocols/`
(ssh, http, **mcp**, ftp, redis, modbus, **s7comm**, smb, smtp, **pop3**, telnet, mysql,
**postgres**, rdp, sip, snmp, ntp, tftp, vnc, git, generic). As of this note, the registry
(`src/uhbs_core/protocols/registry.py`) can **also** load plugins from an
installed third-party Python package via
[`importlib.metadata` entry points](https://packaging.python.org/en/latest/specifications/entry-points/) —
you do not need to fork this repository to add a protocol.

## 1. Implement a plugin class

A plugin is any class implementing the `uhbs_core.protocols.base.ProtocolPlugin`
interface (`probe_fsm` and `probe_negotiation` are required; `probe_timing`,
`probe_state`, `probe_payload`, `probe_fuzz`, and `probe_load_once` have
sane defaults you may override). See `src/uhbs_core/protocols/generic.py`
for the smallest working example, and
`src/uhbs_core/contract_validation.py`'s `UHBSProtocolPlugin` structural
`Protocol` for a documented method-signature reference you can type-check
against without subclassing anything.

```python
# my_uhbs_coap_plugin/plugin.py
from uhbs_core.models import CheckResult, TargetSpec
from uhbs_core.protocols.base import ProtocolPlugin
from uhbs_core.tps import TPS


class CoAPPlugin(ProtocolPlugin):
    name = "coap"
    families = ("iot",)

    def probe_fsm(self, host: str, port: int, target: TargetSpec, tps: TPS | None):
        ...  # return list[CheckResult]

    def probe_negotiation(self, host: str, port: int, target: TargetSpec, tps: TPS | None):
        ...  # return list[CheckResult]
```

`src/uhbs_core/plugin_sdk.py` re-exports the low-level `netutil` transport
helpers (`tcp_transact`, `udp_transact`, `sample_udp_latencies`) with
plugin-author-facing docstrings/defaults, plus a couple of small new
framing helpers (e.g. `PktLineBuilder`) — prefer it over reaching into
`uhbs_core.netutil` directly so your plugin keeps working if internal
helper names change.

## 2. Register it via a Python entry point

In **your own package's** `pyproject.toml` (not this repository's), declare
an entry point under the `uhbs.plugins` group pointing at your plugin class:

```toml
[project.entry-points."uhbs.plugins"]
coap = "my_uhbs_coap_plugin.plugin:CoAPPlugin"
```

When your package is `pip install`-ed alongside `uhbs`, the registry
automatically discovers and instantiates it the next time UHBS starts —
no changes to this repository are required. Internally, this repo's own
`pyproject.toml` documents the same group (as a **comment**, since there
are no first-party third-party plugins to register yet):

```toml
# Third-party plugin authors register here in *their own* project, not here:
# [project.entry-points."uhbs.plugins"]
# coap = "my_uhbs_coap_plugin.plugin:CoAPPlugin"
```

## 3. Failure isolation

`load_external_plugins()` loads every discovered entry point independently,
inside a `try/except`. If your plugin's module fails to import, its class
fails to instantiate, or it doesn't actually implement `ProtocolPlugin`,
UHBS logs a `logging.warning(...)` and continues bootstrapping the
built-in plugins — a broken third-party package cannot crash the core
harness. See `tests/test_entry_point_plugins.py` for the exact contract
being tested (including the "broken plugin doesn't crash discovery" case).

## 4. Maturity expectations

Per [`GOVERNANCE.md`](https://github.com/mziqudhd92/uhbs-standard/blob/main/GOVERNANCE.md), a plugin registered only via an
entry point is **`Experimental`** by default — UHBS performs basic
presence/type checks on load, not a security or protocol-fidelity audit.
See `GOVERNANCE.md`'s plugin maturity lifecycle section for what it takes
to be considered for `Standard` recognition in this repository's own
`docs/conformance/` fixtures, and
[`docs/architecture/plugin-contracts.md`](architecture/plugin-contracts.md)
for the (opt-in, advisory) `CheckResult` contract validator plugin authors
can run against their own output.

## What this is *not* (yet)

- Not a plugin marketplace or curated registry — there is no discovery UI.
- Not a security sandbox — an entry-point plugin runs with the same
  privileges as the harness process. Only install plugin packages you trust.
- Not schema/Pydantic-enforced at the interface boundary yet — see
  `docs/architecture/plugin-contracts.md` for the current (dataclass +
  advisory validator) state and the tracked Pydantic v2 follow-up in
  [`ROADMAP.md`](https://github.com/mziqudhd92/uhbs-standard/blob/main/ROADMAP.md).
