"""Unit tests for uhbs_core.contract_validation (Phase 1 advisory validator).

Covers:
  - compliant CheckResult/ModuleResult fixtures → no violations
  - the exact passed/score-disagreement bug class the review flagged
  - score-out-of-range and missing/invalid-field violations
  - UHBSProtocolPlugin structural (Protocol) satisfaction by existing,
    unmodified built-in plugins — no inheritance required
"""

from __future__ import annotations

from uhbs_core.contract_validation import (
    UHBSProtocolPlugin,
    validate_check_result,
    validate_module_result,
)
from uhbs_core.models import CheckResult, ModuleResult
from uhbs_core.protocols.generic import GenericTCPPlugin
from uhbs_core.protocols.git import GitPlugin


def _cr(**kwargs) -> CheckResult:
    base = {"id": "t.check", "team": "blue", "passed": True, "score": 100.0}
    base.update(kwargs)
    return CheckResult(**base)


# ---------------------------------------------------------------------------
# Compliant cases
# ---------------------------------------------------------------------------


def test_compliant_passing_check_has_no_violations() -> None:
    assert validate_check_result(_cr(passed=True, score=100.0)) == []


def test_compliant_failing_check_has_no_violations() -> None:
    assert validate_check_result(_cr(passed=False, score=0.0)) == []


def test_compliant_low_but_passing_partial_credit_check_has_no_violations() -> None:
    # Real pattern from uhbs_core.protocols.base.probe_timing: passed=True
    # with a modest, non-zero score is legitimate partial credit, not a bug.
    assert validate_check_result(_cr(passed=True, score=20.0)) == []


def test_compliant_module_result_has_no_violations() -> None:
    module = ModuleResult(
        module="A",
        dimension="protocol",
        score=85.5,
        status="ok",
        checks=[_cr(passed=True, score=90.0), _cr(passed=False, score=10.0)],
    )
    assert validate_module_result(module) == []


# ---------------------------------------------------------------------------
# The flagged bug class: passed/score disagreement
# ---------------------------------------------------------------------------


def test_flags_passed_true_with_near_zero_score() -> None:
    violations = validate_check_result(_cr(passed=True, score=0.0))
    assert any("below the sane pass floor" in v for v in violations)


def test_flags_passed_false_with_near_full_score() -> None:
    violations = validate_check_result(_cr(passed=False, score=100.0))
    assert any("above the sane fail ceiling" in v for v in violations)


def test_thresholds_are_tunable() -> None:
    # With a floor of 0.0, even a passed=True/score=0.0 check is compliant.
    assert validate_check_result(_cr(passed=True, score=0.0), pass_score_floor=0.0) == []


# ---------------------------------------------------------------------------
# Range / missing-field violations
# ---------------------------------------------------------------------------


def test_flags_score_above_100() -> None:
    violations = validate_check_result(_cr(score=150.0))
    assert any("out of range" in v for v in violations)


def test_flags_score_below_0() -> None:
    violations = validate_check_result(_cr(score=-5.0))
    assert any("out of range" in v for v in violations)


def test_flags_missing_id_on_dict_shaped_input() -> None:
    violations = validate_check_result({"team": "blue", "passed": True, "score": 100.0})
    assert any("missing required field: id" in v for v in violations)


def test_flags_invalid_team() -> None:
    violations = validate_check_result(_cr(team="purple"))
    assert any("team" in v for v in violations)


def test_flags_non_bool_critical() -> None:
    violations = validate_check_result(_cr(critical="yes"))  # type: ignore[arg-type]
    assert any("critical" in v for v in violations)


def test_module_result_prefixes_nested_check_violations_with_check_id() -> None:
    module = ModuleResult(
        module="B",
        dimension="behavior",
        score=50.0,
        status="ok",
        checks=[_cr(id="behavior.bad_check", passed=True, score=0.0)],
    )
    violations = validate_module_result(module)
    assert any("[check behavior.bad_check]" in v for v in violations)


def test_module_result_flags_out_of_range_module_score() -> None:
    module = ModuleResult(module="A", dimension="protocol", score=250.0, status="ok", checks=[])
    violations = validate_module_result(module)
    assert any("module score" in v for v in violations)


# ---------------------------------------------------------------------------
# UHBSProtocolPlugin structural typing
# ---------------------------------------------------------------------------


def test_existing_builtin_plugins_satisfy_protocol_structurally_without_inheritance() -> None:
    # Neither plugin class inherits from UHBSProtocolPlugin (a typing.Protocol) —
    # this is exactly the point of structural typing.
    assert isinstance(GenericTCPPlugin(), UHBSProtocolPlugin)
    assert isinstance(GitPlugin(), UHBSProtocolPlugin)
    assert UHBSProtocolPlugin not in type(GenericTCPPlugin()).__mro__


def test_object_missing_probe_methods_does_not_satisfy_protocol() -> None:
    class NotAPlugin:
        name = "nope"

    assert not isinstance(NotAPlugin(), UHBSProtocolPlugin)
