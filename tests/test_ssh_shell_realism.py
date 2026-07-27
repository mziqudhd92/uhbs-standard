"""Tests for SSHPlugin.probe_shell_realism (architecture-review item 2).

Offline-safe: exercises the pure consistency/templated-output heuristics
directly, plus the plugin method's graceful failure path against an
unreachable port (no live SSH daemon required).
"""

from __future__ import annotations

from uhbs_core.models import TargetSpec
from uhbs_core.protocols.ssh import (
    SSHPlugin,
    _check_recon_consistency,
    _looks_templated,
    _run_recon_shell,
)


def test_probe_shell_realism_is_registered_and_opt_in() -> None:
    plugin = SSHPlugin()
    assert hasattr(plugin, "probe_shell_realism")
    # Not part of the ABC's required probe_fsm/probe_negotiation contract —
    # confirms this is additive, not a forced override of existing hooks.
    assert callable(plugin.probe_shell_realism)


def test_probe_shell_realism_unreachable_host_fails_gracefully() -> None:
    plugin = SSHPlugin()
    t = TargetSpec(name="x", host="127.0.0.1", port=1, user="root", password="root")
    checks = plugin.probe_shell_realism("127.0.0.1", 1, t, None)
    assert isinstance(checks, list)
    assert checks
    assert checks[0].id == "ssh.realism.shell_recon.unreachable"
    assert checks[0].passed is False
    assert checks[0].score == 0.0


def test_run_recon_shell_reports_missing_paramiko_or_connect_failure() -> None:
    # Regardless of whether paramiko is installed in this environment, an
    # unreachable port on localhost must produce a clean failure dict, never
    # raise.
    result = _run_recon_shell("127.0.0.1", 1, "root", "root", timeout=1.0)
    assert result["ok"] is False
    assert result["error"]
    assert result["outputs"] == {}


def test_looks_templated_flags_obvious_placeholder_text() -> None:
    assert _looks_templated("model name : SAMPLE_CPU\n") is True
    assert _looks_templated("REPLACE_ME with real value") is True


def test_looks_templated_accepts_plausible_real_output() -> None:
    real_uname = "Linux uhbs-lab 6.1.0-13-amd64 #1 SMP x86_64 GNU/Linux"
    assert _looks_templated(real_uname) is False
    assert _looks_templated("") is False


def test_check_recon_consistency_passes_on_plausible_x86_output() -> None:
    outputs = {
        "uname -a": "Linux box 6.1.0-13-amd64 #1 SMP x86_64 GNU/Linux",
        "cat /proc/version": "Linux version 6.1.0-13-amd64 (build@host) ...",
        "cat /proc/cpuinfo": (
            "vendor_id\t: GenuineIntel\nmodel name\t: Intel(R) Xeon\nflags\t: fpu vme"
        ),
        "id": "uid=0(root) gid=0(root) groups=0(root)",
        "echo $PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
        "cat /etc/os-release": 'NAME="Debian GNU/Linux"\nID=debian\nVERSION_ID="12"',
    }
    ok, detail = _check_recon_consistency(outputs)
    assert ok is True
    assert "consistent" in detail


def test_check_recon_consistency_flags_arch_mismatch() -> None:
    outputs = {
        "uname -a": "Linux box 6.1.0-13-amd64 #1 SMP x86_64 GNU/Linux",
        "cat /proc/version": "Linux version 6.1.0-13-amd64 (build@host) ...",
        # No x86 markers at all -> contradicts uname's x86_64 claim.
        "cat /proc/cpuinfo": "CPU architecture: 8\nFeatures\t: fp asimd",
        "id": "uid=0(root) gid=0(root) groups=0(root)",
        "echo $PATH": "/usr/bin:/bin",
        "cat /etc/os-release": 'NAME="Debian GNU/Linux"\nID=debian',
    }
    ok, detail = _check_recon_consistency(outputs)
    assert ok is False
    assert "x86" in detail


def test_check_recon_consistency_flags_missing_os_release_fields() -> None:
    outputs = {
        "uname -a": "Linux box 6.1.0-13-amd64 #1 SMP x86_64 GNU/Linux",
        "cat /proc/version": "",
        "cat /proc/cpuinfo": "",
        "id": "uid=0(root)",
        "echo $PATH": "/usr/bin",
        "cat /etc/os-release": "totally unstructured junk with no fields",
    }
    ok, detail = _check_recon_consistency(outputs)
    assert ok is False
    assert "os-release" in detail


def test_duplicate_outputs_would_be_flagged_as_generic(monkeypatch) -> None:
    """Simulates a canned shell that echoes the same text for every
    command — the strongest, vendor-neutral "not a real shell" tell —
    by monkeypatching the recon-shell runner directly (no live daemon)."""

    def _fake_recon(host, port, user, password, timeout=20.0):
        same_text = "CANNED OUTPUT\n"
        return {
            "ok": True,
            "error": "",
            "outputs": {cmd: same_text for cmd in (
                "uname -a",
                "cat /proc/version",
                "cat /proc/cpuinfo",
                "id",
                "echo $PATH",
                "cat /etc/os-release",
            )},
            "pty_ok": True,
            "pty_detail": "tab_echo=''",
        }

    import uhbs_core.protocols.ssh as ssh_mod

    monkeypatch.setattr(ssh_mod, "_run_recon_shell", _fake_recon)
    plugin = ssh_mod.SSHPlugin()
    t = TargetSpec(name="x", host="127.0.0.1", port=2222, user="root", password="root")
    checks = plugin.probe_shell_realism("127.0.0.1", 2222, t, None)

    generic = next(c for c in checks if c.id == "ssh.realism.shell_recon.generic_output")
    assert generic.passed is False
    assert generic.critical is True
    assert generic.score == 0.0
