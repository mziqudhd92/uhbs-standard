"""Protocol plugin registry — extend UHBS by registering new plugins."""

from __future__ import annotations

import logging
from importlib import metadata as _importlib_metadata

from uhbs_core.protocols.base import ProtocolPlugin

from .ftp import FTPPlugin
from .generic import GenericTCPPlugin
from .git import GitPlugin
from .http import HTTPPlugin
from .mcp import MCPPlugin
from .modbus import ModbusPlugin
from .mysql import MySQLPlugin
from .ntp import NTPPlugin
from .postgres import PostgresPlugin
from .rdp import RDPPlugin
from .redis import RedisPlugin
from .s7comm import S7commPlugin
from .sip import SIPPlugin
from .smb import SMBPlugin
from .smtp import SMTPPlugin
from .snmp import SNMPPlugin
from .ssh import SSHPlugin
from .telnet import TelnetPlugin
from .tftp import TFTPPlugin
from .vnc import VNCPlugin

_REGISTRY: dict[str, ProtocolPlugin] = {}
_LOG = logging.getLogger(__name__)

#: Entry-point group third-party packages should register plugin classes under,
#: e.g. in a plugin package's ``pyproject.toml``:
#:
#:   [project.entry-points."uhbs.plugins"]
#:   coap = "uhbs_coap_plugin:CoAPPlugin"
#:
#: See ``docs/plugin-authoring.md`` for the full contract.
ENTRY_POINT_GROUP = "uhbs.plugins"


def register(plugin: ProtocolPlugin) -> None:
    """Register (or silently replace) the plugin for ``plugin.name``.

    2026-07-27 code-review fix: replacing an already-registered name used
    to be completely silent — no log line anywhere — which is a real
    observability gap for a benchmark harness whose entire value
    proposition is "you can trust this scorecard." A third-party
    ``uhbs.plugins`` entry point (typosquat, supply-chain compromise, or
    just an honest mistake) that declares ``name = "ssh"`` would silently
    take over every subsequent SSH scorecard in that environment with zero
    trace in the output. This does not forbid overriding (that remains a
    deliberate, documented capability — see ``load_external_plugins``) but
    it can no longer happen invisibly.
    """
    existing = _REGISTRY.get(plugin.name.lower())
    if existing is not None and type(existing) is not type(plugin):
        _LOG.warning(
            "plugin name '%s' is being re-registered: %s -> %s "
            "(scorecards for this protocol will now come from the new implementation)",
            plugin.name.lower(),
            type(existing).__name__,
            type(plugin).__name__,
        )
    _REGISTRY[plugin.name.lower()] = plugin


def get_plugin(name: str) -> ProtocolPlugin:
    key = (name or "generic").lower()
    if key in {"https"}:
        key = "http"
    if key in {"postgresql"}:
        key = "postgres"
    if key in {"s7", "iso-tsap", "isotp", "iso_on_tcp"}:
        key = "s7comm"
    if key in _REGISTRY and key != "generic":
        return _REGISTRY[key]
    if key == "generic" and "generic" in _REGISTRY:
        return _REGISTRY["generic"]
    return GenericTCPPlugin(name=key)


def list_protocols() -> list[str]:
    return sorted(_REGISTRY.keys())


def load_external_plugins(group: str = ENTRY_POINT_GROUP) -> list[str]:
    """Discover and register third-party plugins via Python entry points.

    Third-party packages advertise ``ProtocolPlugin`` subclasses under the
    ``uhbs.plugins`` entry-point group (see ``docs/plugin-authoring.md``).
    Each discovered entry point is loaded and instantiated independently;
    a broken/raising third-party package MUST NOT be able to crash the core
    harness, so every step is wrapped in try/except and logged as a warning.

    Returns the list of plugin ``name`` keys that were newly registered
    (empty list if no external packages are installed, or all failed).
    """
    registered: list[str] = []
    try:
        eps = _importlib_metadata.entry_points(group=group)
    except Exception as exc:  # pragma: no cover — defensive: metadata API failure
        _LOG.warning("uhbs.plugins entry-point discovery failed: %s", exc)
        return registered

    for ep in eps:
        try:
            plugin_cls = ep.load()
            plugin = plugin_cls()
            if not isinstance(plugin, ProtocolPlugin):
                _LOG.warning(
                    "external plugin '%s' (%s) does not subclass ProtocolPlugin — skipped",
                    ep.name,
                    ep.value,
                )
                continue
            register(plugin)
            registered.append(plugin.name.lower())
        except Exception as exc:  # noqa: BLE001 — a broken external plugin must not crash core
            _LOG.warning(
                "failed to load external uhbs.plugins entry point '%s' (%s): %s",
                ep.name,
                getattr(ep, "value", "?"),
                exc,
            )
            continue
    return registered


def _bootstrap() -> None:
    if _REGISTRY:
        return
    for p in (
        SSHPlugin(),
        SMTPPlugin(),
        HTTPPlugin(),
        MCPPlugin(),
        TelnetPlugin(),
        ModbusPlugin(),
        S7commPlugin(),
        FTPPlugin(),
        RedisPlugin(),
        SMBPlugin(),
        MySQLPlugin(),
        PostgresPlugin(),
        RDPPlugin(),
        SIPPlugin(),
        SNMPPlugin(),
        NTPPlugin(),
        TFTPPlugin(),
        VNCPlugin(),
        GitPlugin(),
        GenericTCPPlugin(),
    ):
        register(p)
    # Third-party plugins register last so they can override a built-in name
    # if a plugin author intentionally does so; failures never abort bootstrap.
    load_external_plugins()


_bootstrap()
