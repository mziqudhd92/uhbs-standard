"""Protocol-agnostic TPS / target binding tests."""

from __future__ import annotations

import pytest

from uhbs_core.inventory import resolve_target
from uhbs_core.models import TargetSpec
from uhbs_core.test_safety import run as run_safety
from uhbs_core.tps import (
    ProtocolConflictError,
    apply_tps,
    load_tps,
    resolve_tps_path,
)


def test_low_interaction_is_class_only() -> None:
    path = resolve_tps_path("low_interaction")
    assert path is not None
    tps = load_tps(path)
    assert tps.profile_class == "Low-Interaction"
    assert tps.protocol_list() == []


def test_low_interaction_ssh_declares_shell_protocols() -> None:
    path = resolve_tps_path("low_interaction_ssh")
    assert path is not None
    tps = load_tps(path)
    assert set(tps.protocol_list()) == {"ssh", "telnet"}


def test_apply_tps_preserves_explicit_protocol() -> None:
    t = TargetSpec(
        name="printer",
        host="miniprint-lab",
        port=9100,
        protocol="pjl",
        protocols=["pjl"],
        ports_map={"pjl": 9100},
    )
    tps = load_tps(resolve_tps_path("low_interaction"))  # type: ignore[arg-type]
    apply_tps(t, tps)
    assert t.protocol_list() == ["pjl"]
    assert t.profile_class == "Low-Interaction"
    assert t.shell_exec_port() is None


def test_apply_tps_conflict_ssh_profile_vs_pjl() -> None:
    t = TargetSpec(
        name="printer",
        host="miniprint-lab",
        port=9100,
        protocol="pjl",
        protocols=["pjl"],
        ports_map={"pjl": 9100},
    )
    tps = load_tps(resolve_tps_path("low_interaction_ssh"))  # type: ignore[arg-type]
    with pytest.raises(ProtocolConflictError, match="conflict"):
        apply_tps(t, tps)


def test_shell_exec_port_never_uses_application_port() -> None:
    t = TargetSpec(
        name="es",
        host="espot-lab",
        port=9200,
        protocol="http",
        protocols=["http"],
        ports_map={"http": 9200},
    )
    # Even if someone later sets protocol=ssh without ports.ssh, do not Paramiko :9200
    t.protocol = "ssh"
    t.protocols = ["ssh"]
    assert t.shell_exec_port() is None
    assert t.port_for("ssh") is None
    assert t.port_for("http") == 9200


def test_module_d_skips_paramiko_without_ssh_listener() -> None:
    t = TargetSpec(
        name="printer",
        host="127.0.0.1",
        port=9100,
        protocol="pjl",
        protocols=["pjl"],
        ports_map={"pjl": 9100},
    )
    result = run_safety(t)
    assert result.metrics.get("shell_exec") is False
    ids = {c.id for c in result.checks}
    assert "d1.shell_exec_unavailable" in ids
    assert result.score <= 90.0


def test_resolve_target_requires_protocol_or_tps_protocols() -> None:
    t = resolve_target({}, "127.0.0.1", port=9100, protocol="pjl")
    assert t.protocol_list() == ["pjl"]
    assert t.ports_map["pjl"] == 9100
    assert t.shell_exec_port() is None

    bare = resolve_target({}, "127.0.0.1", port=9100)
    assert bare.protocol_list() == []
