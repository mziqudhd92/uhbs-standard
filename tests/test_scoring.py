"""Unit tests for UHQS scoring."""

from uhbs_cli.scoring import compute_uhqs, letter_grade, safety_gate, validate_weights


def test_posix_weights_sum() -> None:
    weights = {"w_A": 0.20, "w_B": 0.25, "w_C": 0.20, "w_E": 0.15, "w_F": 0.20}
    ok, total = validate_weights(weights)
    assert ok
    assert abs(total - 1.0) < 1e-9


def test_safety_gate_pass() -> None:
    delta, passed = safety_gate(97)
    assert passed
    assert delta == 1.0


def test_safety_gate_fail_quadratic() -> None:
    delta, passed = safety_gate(70)
    assert not passed
    assert abs(delta - 0.49) < 1e-9


def test_cyberhallucinet_uhqs() -> None:
    weights = {"w_A": 0.20, "w_B": 0.25, "w_C": 0.20, "w_E": 0.15, "w_F": 0.20}
    scores = {"A": 88, "B": 94, "C": 98, "D": 97, "E": 88, "F": 91}
    result = compute_uhqs(scores, weights)
    assert result.safety_gate_passed
    assert result.delta_c == 1.0
    # Spec PDF listed 91.8; formula yields 92.1 for these inputs.
    assert result.uhqs == 92.1
    assert letter_grade(result.uhqs) == "A"


def test_safety_gate_penalizes_composite() -> None:
    weights = {"w_A": 0.20, "w_B": 0.25, "w_C": 0.20, "w_E": 0.15, "w_F": 0.20}
    scores = {"A": 100, "B": 100, "C": 100, "D": 70, "E": 100, "F": 100}
    result = compute_uhqs(scores, weights)
    assert result.uhqs == 49.0
    assert letter_grade(result.uhqs) == "F"
