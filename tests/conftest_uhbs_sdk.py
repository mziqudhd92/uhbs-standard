"""Optional pytest fixtures for third-party UHBS plugin test suites.

No root-level ``tests/conftest.py`` existed in this repository at the time
this module was added, and several other in-flight edits in this session
also add test files under ``tests/`` — rather than create a root
``conftest.py`` (which would apply globally and risk colliding with
concurrent work), fixtures here are opt-in: import what you need directly
into your test module, e.g.::

    from conftest_uhbs_sdk import uhbs_target_mock  # noqa: F401

Third-party plugin authors testing their own ``ProtocolPlugin`` subclass
outside this repository can copy this pattern (or this file) directly —
``uhbs_core`` does not need to be modified to use it.
"""

from __future__ import annotations

from collections.abc import Callable

import pytest

from uhbs_core.models import TargetSpec
from uhbs_core.tps import TPS

#: Loopback port deliberately unlikely to have a real listener — mirrors the
#: "connect to something that will refuse/time out" pattern already used
#: throughout tests/test_new_protocol_plugins.py and tests/test_uhbs_core.py.
UNREACHABLE_PORT = 1


@pytest.fixture
def uhbs_target_mock() -> Callable[..., TargetSpec]:
    """Factory fixture returning throwaway ``TargetSpec`` instances.

    Usage in a plugin author's own test::

        def test_my_plugin_handles_unreachable_target(uhbs_target_mock):
            target = uhbs_target_mock(protocol="coap", port=1)
            plugin = CoAPPlugin()
            checks = plugin.probe_negotiation("127.0.0.1", 1, target, None)
            assert checks and not checks[0].passed

    Defaults to ``host="127.0.0.1"``, ``port=1`` (i.e. no live listener
    required) and ``protocol="generic"`` so tests exercising a plugin's
    error/timeout handling don't need a running server. Pass any
    ``TargetSpec`` field as a keyword to override it.
    """

    def _make(
        *,
        name: str = "uhbs-sdk-mock-target",
        host: str = "127.0.0.1",
        port: int = UNREACHABLE_PORT,
        protocol: str = "generic",
        **kwargs: object,
    ) -> TargetSpec:
        protocols = kwargs.pop("protocols", None)
        if protocols is None:
            protocols = [protocol] if protocol else []
        return TargetSpec(
            name=name,
            host=host,
            port=port,
            protocol=protocol,
            protocols=protocols,  # type: ignore[arg-type]
            **kwargs,  # type: ignore[arg-type]
        )

    return _make


@pytest.fixture
def uhbs_tps_mock() -> Callable[..., TPS]:
    """Factory fixture returning a throwaway ``TPS`` (Target Profile Spec).

    Companion to :func:`uhbs_target_mock` for plugin tests that also need a
    ``TPS`` object (e.g. to exercise ``probe_timing``'s gold-baseline path).
    Defaults to a class-only, no-gold-baseline TPS so it never accidentally
    triggers a live KS-compare against a real host in a unit test.
    """

    def _make(*, profile_class: str = "POSIX-Shell", **kwargs: object) -> TPS:
        return TPS(name="uhbs-sdk-mock-tps", profile_class=profile_class, **kwargs)  # type: ignore[arg-type]

    return _make
