"""Advisory (opt-in) contract validation for UHBS check results — Phase 1.

**What this is.** A lint-style, additive validator that runtime-checks the
*existing* ``CheckResult`` / ``ModuleResult`` dataclasses (see
``uhbs_core.models``) for the exact class of bug an architecture review
flagged: a check whose boolean ``passed`` field and numeric ``score`` field
disagree (e.g. ``passed=True`` with a near-zero score, or ``passed=False``
with a near-100 score), a ``score`` outside the documented ``[0, 100]``
range, or a check missing a required identifying field. Nothing in this
module changes scoring behavior — it is diagnostic only, and nothing in the
harness calls it automatically today. Plugin authors and reviewers can call
it by hand (or wire it into their own CI) while inspecting a plugin's output.

**What this is not (yet).** This is *not* a Pydantic v2 migration of
``CheckResult``/``ProtocolPlugin``. Converting the existing dataclass +
ABC contract to Pydantic models across all 17+ built-in plugins is a
larger, separate effort tracked as a follow-up in ``ROADMAP.md`` — doing it
now, concurrently with other in-flight edits to ``models.py`` and the
plugins themselves, would be unsafe. See
``docs/architecture/plugin-contracts.md`` for the phase framing.

**Update (2026-07-27, code-review follow-up):** :func:`has_passed_score_disagreement`
is no longer purely advisory. ``uhbs_core.check_scoring.score_checks`` now
imports and calls it directly as a hard integrity gate — see that module's
docstring for why. A check whose ``passed``/``score`` fields contradict each
other zeroes the whole check-list aggregate, the same as a failed
``critical=True`` gate. This closes a real loophole: previously, a
single-check list with ``passed=True, score=0.0`` (e.g. a plugin bug that
forgot to set ``score``) fell through to a "legacy boolean-only" fallback
and scored a silent ``100.0`` — exactly the "boolean says pass, number says
fail" bug class this whole module exists to catch. Everything else in this
module remains advisory-only (nothing else here is called automatically).

Three things live here:

1. :func:`has_passed_score_disagreement` — the single-check disagreement
   test, shared by #2 below and by ``check_scoring.score_checks``.
2. :func:`validate_check_result` / :func:`validate_module_result` — plain
   functions that inspect already-constructed result objects and return a
   list of human-readable violation strings (``[]`` means compliant).
3. :class:`UHBSProtocolPlugin` — a ``typing.Protocol`` documenting the
   ``probe_fsm`` / ``probe_negotiation`` / ``probe_state`` method shape a
   third-party plugin author should implement. It is ``@runtime_checkable``
   and used purely **structurally** — the 17+ built-in
   ``uhbs_core.protocols.base.ProtocolPlugin`` subclasses already satisfy it
   without being changed to inherit from it.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

# Sane bounds for the CheckResult.score contract (see uhbs_core.models).
SCORE_MIN = 0.0
SCORE_MAX = 100.0

# Deliberately lenient thresholds: this is an *advisory* lint, not a second
# scoring engine, so defaults are chosen to catch only genuinely inconsistent
# passed/score pairs (e.g. passed=True, score=0.0) without flagging existing
# plugins that legitimately award partial credit on a passing check (see
# uhbs_core.protocols.base.probe_timing for real examples of low-but-nonzero
# passing scores). Callers may tighten these per use case.
DEFAULT_PASS_SCORE_FLOOR = 15.0
DEFAULT_FAIL_SCORE_CEILING = 85.0

_VALID_TEAMS = {"blue", "red", "white"}


def has_passed_score_disagreement(
    result: Any,
    *,
    pass_score_floor: float = DEFAULT_PASS_SCORE_FLOOR,
    fail_score_ceiling: float = DEFAULT_FAIL_SCORE_CEILING,
) -> bool:
    """True iff ``result``'s boolean ``passed`` and numeric ``score`` fields
    contradict each other — the exact bug class an architecture review
    flagged repeatedly (e.g. ``redis.py`` returning ``passed=True`` at
    ``score=40``, or a check that simply forgot to set ``score`` while
    claiming ``passed=True``, silently defaulting to ``score=0.0``).

    Deliberately conservative/duck-typed like :func:`validate_check_result`:
    a missing, malformed, or out-of-range field is judged elsewhere (that
    function reports it as its own violation) — this helper only judges
    disagreement when both fields are present, well-typed, and in range, so
    it can be called from a hot path (see
    ``uhbs_core.check_scoring.score_checks``) without duplicating those
    other checks or risking a false positive on an unrelated defect.
    """
    passed = _get(result, "passed", _MISSING)
    if passed is _MISSING or not isinstance(passed, bool):
        return False
    score = _get(result, "score", _MISSING)
    if score is _MISSING or not isinstance(score, (int, float)) or isinstance(score, bool):
        return False
    score = float(score)
    if not (SCORE_MIN <= score <= SCORE_MAX):
        return False
    if passed:
        return score < pass_score_floor
    return score > fail_score_ceiling


def validate_check_result(
    result: Any,
    *,
    pass_score_floor: float = DEFAULT_PASS_SCORE_FLOOR,
    fail_score_ceiling: float = DEFAULT_FAIL_SCORE_CEILING,
) -> list[str]:
    """Return human-readable contract violations for one check-like object.

    ``result`` is duck-typed on purpose (works for ``CheckResult`` instances,
    dicts loaded from a scorecard JSON, or any other object exposing the
    same attribute names) — it is not required to be an actual
    ``uhbs_core.models.CheckResult`` instance. Missing attributes are treated
    as missing required fields rather than raising ``AttributeError``, so a
    malformed object never crashes the caller.

    Returns an empty list when ``result`` is fully compliant.
    """
    violations: list[str] = []

    check_id = _get(result, "id")
    if not isinstance(check_id, str) or not check_id.strip():
        violations.append("missing required field: id (must be a non-empty string)")

    team = _get(result, "team")
    if not isinstance(team, str) or team.lower() not in _VALID_TEAMS:
        allowed = sorted(_VALID_TEAMS)
        violations.append(
            f"invalid/missing required field: team={team!r} (expected one of {allowed})"
        )

    passed = _get(result, "passed", _MISSING)
    if passed is _MISSING or not isinstance(passed, bool):
        violations.append("missing required field: passed (must be a bool)")
        passed = None

    score = _get(result, "score", _MISSING)
    if score is _MISSING or not isinstance(score, (int, float)) or isinstance(score, bool):
        violations.append("missing required field: score (must be numeric)")
        score = None
    elif not (SCORE_MIN <= float(score) <= SCORE_MAX):
        violations.append(
            f"score={score!r} out of range [{SCORE_MIN}, {SCORE_MAX}] for check id={check_id!r}"
        )

    critical = _get(result, "critical", False)
    if not isinstance(critical, bool):
        violations.append(f"invalid field: critical={critical!r} (must be a bool)")

    # The bug class the architecture review actually flagged: passed/score
    # disagreement. Only evaluated when both fields are present, well-typed,
    # and in range — otherwise the checks above already reported the defect.
    # Delegates to has_passed_score_disagreement() so this module and
    # uhbs_core.check_scoring.score_checks's hard integrity gate can never
    # silently drift out of sync on what counts as a disagreement.
    if (
        passed is not None
        and score is not None
        and SCORE_MIN <= float(score) <= SCORE_MAX
        and has_passed_score_disagreement(
            result, pass_score_floor=pass_score_floor, fail_score_ceiling=fail_score_ceiling
        )
    ):
        if passed:
            violations.append(
                f"passed=True but score={score!r} is below the sane pass floor "
                f"({pass_score_floor}) for check id={check_id!r}"
            )
        else:
            violations.append(
                f"passed=False but score={score!r} is above the sane fail ceiling "
                f"({fail_score_ceiling}) for check id={check_id!r}"
            )

    return violations


def validate_module_result(
    module: Any,
    *,
    pass_score_floor: float = DEFAULT_PASS_SCORE_FLOOR,
    fail_score_ceiling: float = DEFAULT_FAIL_SCORE_CEILING,
) -> list[str]:
    """Return violations for a ``ModuleResult``-like object and its checks.

    Validates the module's own ``score`` range, then delegates to
    :func:`validate_check_result` for every entry in ``module.checks``,
    prefixing each nested violation with the owning check's ``id`` (or its
    list index, if ``id`` is unavailable) so violations remain traceable in
    a module with many checks.
    """
    violations: list[str] = []

    module_score = _get(module, "score", _MISSING)
    if module_score is _MISSING or not isinstance(module_score, (int, float)) or isinstance(
        module_score, bool
    ):
        violations.append("missing required field: score (must be numeric) on ModuleResult")
    elif not (SCORE_MIN <= float(module_score) <= SCORE_MAX):
        violations.append(f"module score={module_score!r} out of range [{SCORE_MIN}, {SCORE_MAX}]")

    checks = _get(module, "checks", []) or []
    for idx, check in enumerate(checks):
        check_id = _get(check, "id", f"#{idx}")
        for v in validate_check_result(
            check, pass_score_floor=pass_score_floor, fail_score_ceiling=fail_score_ceiling
        ):
            violations.append(f"[check {check_id}] {v}")

    return violations


class _Missing:
    def __repr__(self) -> str:  # pragma: no cover — debugging aid only
        return "<missing>"


_MISSING = _Missing()


def _get(obj: Any, name: str, default: Any = _MISSING) -> Any:
    """Attribute-or-mapping getter so this module works on dataclasses, plain
    objects, and dict-shaped data (e.g. JSON loaded from a scorecard)."""
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


@runtime_checkable
class UHBSProtocolPlugin(Protocol):
    """Structural contract for a third-party UHBS protocol plugin.

    This intentionally mirrors ``uhbs_core.protocols.base.ProtocolPlugin``'s
    three core probe hooks, but as a ``typing.Protocol`` rather than an ABC:
    existing/new plugins satisfy it **structurally** just by having methods
    with these names and signatures — no inheritance or code changes are
    required for the 17+ built-in plugins to already conform. Third-party
    plugin authors can use this for static type-checking (``mypy``/``pyright``)
    of their own package without importing or subclassing anything from
    ``uhbs_core.protocols.base``.

    Not enforced at runtime by the registry today — see
    ``docs/architecture/plugin-contracts.md`` for why this is phase 1
    (advisory) rather than a hard interface boundary.
    """

    name: str

    def probe_fsm(self, host: str, port: int, target: Any, tps: Any) -> list[Any]:
        """A1 — out-of-order / invalid verbs vs mandated status codes."""
        ...

    def probe_negotiation(self, host: str, port: int, target: Any, tps: Any) -> list[Any]:
        """A2 — capability / banner / cipher negotiation parity."""
        ...

    def probe_state(self, host: str, port: int, target: Any, tps: Any) -> list[Any]:
        """B — state-machine / stateful realism probe."""
        ...
