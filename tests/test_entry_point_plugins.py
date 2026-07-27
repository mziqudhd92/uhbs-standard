"""Unit tests for ``uhbs_core.protocols.registry.load_external_plugins()``.

Simulates third-party plugin packages registering under the
``uhbs.plugins`` entry-point group (see ``docs/plugin-authoring.md``)
without requiring an actual installed package — entry points are faked
via monkeypatching ``importlib.metadata.entry_points``, following the
patterns documented in the CPython importlib.metadata test suite.
"""

from __future__ import annotations

import pytest

from uhbs_core.models import CheckResult
from uhbs_core.protocols import registry
from uhbs_core.protocols.base import ProtocolPlugin


class _FakeExternalPlugin(ProtocolPlugin):
    """Minimal third-party-style plugin used only by this test module."""

    name = "uhbs-test-external"
    families = ("test",)

    def probe_fsm(self, host, port, target, tps):
        return [CheckResult(id="fake.fsm", team="blue", passed=True, score=100.0)]

    def probe_negotiation(self, host, port, target, tps):
        return [CheckResult(id="fake.nego", team="blue", passed=True, score=100.0)]


class _GoodEntryPoint:
    """A well-behaved external entry point."""

    name = "uhbs-test-external"
    value = "tests.test_entry_point_plugins:_FakeExternalPlugin"
    group = registry.ENTRY_POINT_GROUP

    @staticmethod
    def load():
        return _FakeExternalPlugin


class _BrokenLoadEntryPoint:
    """Entry point whose ``.load()`` raises — simulates an import-time crash
    in a broken third-party plugin package (e.g. missing dependency)."""

    name = "broken-load"
    value = "uhbs_broken_pkg:BrokenPlugin"
    group = registry.ENTRY_POINT_GROUP

    def load(self):
        raise ImportError("simulated broken third-party plugin package")


class _BrokenInitEntryPoint:
    """Entry point that imports fine but explodes on instantiation."""

    name = "broken-init"
    value = "uhbs_broken_pkg:ExplodingPlugin"
    group = registry.ENTRY_POINT_GROUP

    @staticmethod
    def load():
        class _Exploding(ProtocolPlugin):
            name = "uhbs-test-exploding"

            def __init__(self):
                raise RuntimeError("simulated crash in third-party __init__")

            def probe_fsm(self, host, port, target, tps):
                return []

            def probe_negotiation(self, host, port, target, tps):
                return []

        return _Exploding


class _WrongTypeEntryPoint:
    """Loads a callable whose instance is NOT a ``ProtocolPlugin``."""

    name = "wrong-type"
    value = "uhbs_broken_pkg:NotAPlugin"
    group = registry.ENTRY_POINT_GROUP

    @staticmethod
    def load():
        return dict  # dict() succeeds but isn't a ProtocolPlugin


@pytest.fixture(autouse=True)
def _restore_registry_state():
    """Snapshot/restore the module-level plugin registry around each test
    so these tests can't leak fake plugins into other test modules."""
    original = dict(registry._REGISTRY)
    yield
    registry._REGISTRY.clear()
    registry._REGISTRY.update(original)


def test_load_external_plugins_registers_fake_entry_point(monkeypatch):
    monkeypatch.setattr(
        registry._importlib_metadata,
        "entry_points",
        lambda group=None: [_GoodEntryPoint()],
    )

    registered = registry.load_external_plugins()

    assert "uhbs-test-external" in registered
    plugin = registry.get_plugin("uhbs-test-external")
    assert isinstance(plugin, _FakeExternalPlugin)


def test_load_external_plugins_skips_broken_entry_points_without_raising(monkeypatch):
    monkeypatch.setattr(
        registry._importlib_metadata,
        "entry_points",
        lambda group=None: [
            _BrokenLoadEntryPoint(),
            _BrokenInitEntryPoint(),
            _WrongTypeEntryPoint(),
            _GoodEntryPoint(),
        ],
    )

    # Must not raise even though three of the four entry points are broken —
    # this is the exact "broken external plugin can't crash core harness"
    # guarantee load_external_plugins() is required to provide.
    registered = registry.load_external_plugins()

    assert registered == ["uhbs-test-external"]
    # Broken plugin names must never have made it into the live registry.
    assert "uhbs-test-exploding" not in registry._REGISTRY


def test_load_external_plugins_handles_discovery_failure_gracefully(monkeypatch):
    def _boom(group=None):
        raise RuntimeError("simulated importlib.metadata failure")

    monkeypatch.setattr(registry._importlib_metadata, "entry_points", _boom)

    # Discovery itself failing (e.g. corrupted metadata) must not crash bootstrap.
    assert registry.load_external_plugins() == []


def test_builtin_plugins_still_resolve_after_external_loading_ran():
    # Sanity/regression guard: built-ins registered in ``_bootstrap()`` remain
    # present regardless of what happens during external plugin discovery.
    for name in ("ssh", "http", "git", "generic"):
        assert registry.get_plugin(name).name == name


class _FakeExternalSSHOverride(ProtocolPlugin):
    """Deliberately claims the built-in 'ssh' name to test the override path."""

    name = "ssh"

    def probe_fsm(self, host, port, target, tps):
        return []

    def probe_negotiation(self, host, port, target, tps):
        return []


class _SSHOverrideEntryPoint:
    name = "ssh"
    value = "tests.test_entry_point_plugins:_FakeExternalSSHOverride"
    group = registry.ENTRY_POINT_GROUP

    @staticmethod
    def load():
        return _FakeExternalSSHOverride


def test_overriding_a_builtin_plugin_name_is_logged_not_silent(monkeypatch, caplog):
    """2026-07-27 code-review fix: an external plugin overriding a built-in
    name (here, the real ``ssh`` plugin) must produce a WARNING log line —
    previously this happened with zero observability anywhere."""
    monkeypatch.setattr(
        registry._importlib_metadata,
        "entry_points",
        lambda group=None: [_SSHOverrideEntryPoint()],
    )

    with caplog.at_level("WARNING", logger=registry._LOG.name):
        registered = registry.load_external_plugins()

    assert "ssh" in registered
    assert isinstance(registry.get_plugin("ssh"), _FakeExternalSSHOverride)
    assert any(
        "ssh" in record.message and "re-registered" in record.message
        for record in caplog.records
    ), f"expected an override warning, got: {[r.message for r in caplog.records]}"
