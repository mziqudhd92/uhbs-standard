# Plugin interface contracts — phase 1 (advisory)

> Companion to [`docs/plugin-authoring.md`](../plugin-authoring.md) and
> [`GOVERNANCE.md`](https://github.com/mziqudhd92/uhbs-standard/blob/main/GOVERNANCE.md). Describes the *current* state of the
> `CheckResult` / `ProtocolPlugin` contract, not an aspirational future one.

## What exists today

- `uhbs_core.models.CheckResult` is a plain `@dataclass` (`id`, `team`,
  `passed`, `detail`, `score`, `evidence`, `critical`). It is **not**
  Pydantic. There is no runtime schema validation on construction — a
  plugin can (and, per an architecture review, occasionally did) return a
  `CheckResult` where `passed` and `score` disagree, or a `score` outside
  `[0, 100]`.
- `uhbs_core.protocols.base.ProtocolPlugin` is a plain `ABC`. Third-party
  plugins registered via `uhbs.plugins` entry points (see
  `uhbs_core.protocols.registry.load_external_plugins`) are only checked
  with `isinstance(plugin, ProtocolPlugin)` — a presence/inheritance check,
  not a structural or type-level audit of every probe method's signature.
- `uhbs_core.contract_validation` adds an **additive, opt-in** advisory
  layer on top of the above, without changing either type:
  - `validate_check_result()` / `validate_module_result()` — plain
    functions you can call by hand (or from your own test suite / CI step)
    against already-constructed `CheckResult`/`ModuleResult` objects (or
    dict-shaped data loaded from a scorecard JSON) to catch the
    passed/score-disagreement, out-of-range-score, and
    missing-required-field bug classes an architecture review flagged.
    An empty list means compliant; nothing is enforced automatically.
  - `UHBSProtocolPlugin` — a `typing.Protocol` (`@runtime_checkable`)
    documenting the `probe_fsm` / `probe_negotiation` / `probe_state`
    method shape. It is satisfied **structurally**: every existing
    built-in plugin already passes `isinstance(plugin, UHBSProtocolPlugin)`
    without inheriting from it or changing a single line. Third-party
    plugin authors can use it purely for their own static type-checking.

## Why not just migrate to Pydantic v2 now

A full migration of `CheckResult`/`ModuleResult`/`ProtocolPlugin` to
Pydantic v2 models would give real, always-on schema enforcement (coercion,
`ge=0, le=100` field constraints, etc.) instead of an opt-in lint. It was
**intentionally deferred** for this pass because:

1. `models.py` was being edited concurrently by another workstream in this
   same session (adding the `critical: bool` field used above) — a
   simultaneous structural rewrite of the same file is unsafe.
2. All 17+ built-in protocol plugins construct `CheckResult` positionally/by
   keyword today; a Pydantic migration touching every call site is a
   large, separate effort that deserves its own focused review, not a
   drive-by change bundled with unrelated work.

This is tracked as a follow-up in [`ROADMAP.md`](https://github.com/mziqudhd92/uhbs-standard/blob/main/ROADMAP.md) — **not
done**, not started as code, just written down so it isn't lost.

## Honest status

| Claim | Reality today |
| --- | --- |
| `CheckResult`/`ModuleResult` schema-validated on construction | **No** — plain dataclasses |
| `ProtocolPlugin` interface enforced structurally at registration | **No** — `isinstance` (inheritance) check only |
| Advisory lint you can run by hand against check output | **Yes** — `uhbs_core.contract_validation` |
| Third-party plugins statically type-checkable against a documented shape | **Yes** — `UHBSProtocolPlugin` Protocol |
| Pydantic v2 migration of the core contract | **Not started** — tracked in `ROADMAP.md` |

See [`docs/architecture/ci-baseline.md`](ci-baseline.md) for the related,
also-phase-1, golden-baseline CI note.
