"""Protocol plugin registry — extend UHBS by registering new plugins."""

from __future__ import annotations

from uhbs_core.protocols.base import ProtocolPlugin

from .ftp import FTPPlugin
from .generic import GenericTCPPlugin
from .http import HTTPPlugin
from .modbus import ModbusPlugin
from .redis import RedisPlugin
from .smb import SMBPlugin
from .smtp import SMTPPlugin
from .ssh import SSHPlugin
from .telnet import TelnetPlugin

_REGISTRY: dict[str, ProtocolPlugin] = {}


def register(plugin: ProtocolPlugin) -> None:
    _REGISTRY[plugin.name.lower()] = plugin


def get_plugin(name: str) -> ProtocolPlugin:
    key = (name or "generic").lower()
    if key in {"https"}:
        key = "http"
    if key in _REGISTRY and key != "generic":
        return _REGISTRY[key]
    if key == "generic" and "generic" in _REGISTRY:
        return _REGISTRY["generic"]
    return GenericTCPPlugin(name=key)


def list_protocols() -> list[str]:
    return sorted(_REGISTRY.keys())


def _bootstrap() -> None:
    if _REGISTRY:
        return
    for p in (
        SSHPlugin(),
        SMTPPlugin(),
        HTTPPlugin(),
        TelnetPlugin(),
        ModbusPlugin(),
        FTPPlugin(),
        RedisPlugin(),
        SMBPlugin(),
        GenericTCPPlugin(),
    ):
        register(p)


_bootstrap()
