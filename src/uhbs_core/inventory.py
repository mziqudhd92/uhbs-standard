"""Load benchmark targets from inventory YAML or CLI overrides (UHBS v4)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .models import TargetSpec
from .tps import apply_tps, load_tps, resolve_tps_path

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None


def _site_to_spec(name: str, raw: dict[str, Any]) -> TargetSpec:
    ports = raw.get("ports") or {}
    ssh_port = raw.get("ssh_port", ports.get("ssh"))
    smtp_port = raw.get("smtp_port", ports.get("smtp"))
    http_port = raw.get("http_port", ports.get("http"))
    primary = int(raw.get("port", ssh_port or 2222))
    ports_map = {str(k).lower(): int(v) for k, v in ports.items()}
    if ssh_port is not None:
        ports_map.setdefault("ssh", int(ssh_port))
    if smtp_port is not None:
        ports_map.setdefault("smtp", int(smtp_port))
    if http_port is not None:
        ports_map.setdefault("http", int(http_port))
    if "ssh" not in ports_map:
        ports_map["ssh"] = primary

    protocols = raw.get("protocols") or []
    if isinstance(protocols, str):
        protocols = [protocols]
    protocol = raw.get("protocol")
    if not protocols and protocol:
        protocols = [protocol]
    if not protocols:
        protocols = list(ports_map.keys())

    t = TargetSpec(
        name=name,
        kind=str(raw.get("kind", "generic")),
        source_root=raw.get("source_root"),
        host=raw.get("host"),
        port=primary,
        user=str(raw.get("user", "root")),
        password=str(raw.get("password", "root")),
        telemetry_dir=raw.get("telemetry_dir"),
        profile=raw.get("profile"),
        baseline_native_host=raw.get("baseline_native_host"),
        container_image=raw.get("container_image"),
        ssh_port=int(ssh_port) if ssh_port is not None else primary,
        smtp_port=int(smtp_port) if smtp_port is not None else None,
        http_port=int(http_port) if http_port is not None else None,
        tps_path=raw.get("tps") or raw.get("tps_path"),
        protocol=str(protocol or (protocols[0] if protocols else "ssh")),
        protocols=[str(p) for p in protocols],
        profile_class=str(raw.get("class") or raw.get("profile_class") or "POSIX-Shell"),
        ports_map=ports_map,
    )

    tps_ref = t.tps_path or raw.get("tps")
    path = resolve_tps_path(tps_ref) if tps_ref else None
    if path:
        apply_tps(t, load_tps(path))
        t.tps_path = str(path)
        # Keep explicit inventory ports authoritative
        t.ports_map.update(ports_map)
    return t


def load_inventory(path: Path) -> dict[str, TargetSpec]:
    if yaml is None:
        raise RuntimeError("PyYAML required: pip install pyyaml")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    sites = data.get("sites") or {}
    return {name: _site_to_spec(name, raw or {}) for name, raw in sites.items()}


def resolve_target(
    inventory: dict[str, TargetSpec],
    name_or_addr: str,
    *,
    kind: str | None = None,
    source_root: str | None = None,
    port: int | None = None,
    protocol: str | None = None,
    tps: str | None = None,
    profile_class: str | None = None,
) -> TargetSpec:
    if name_or_addr in inventory:
        t = inventory[name_or_addr]
        if kind:
            t.kind = kind
        if source_root:
            t.source_root = source_root
        if port:
            t.port = port
            t.ports_map["ssh"] = port
            t.ssh_port = port
        if protocol:
            t.protocol = protocol
            t.protocols = [protocol]
        if profile_class:
            t.profile_class = profile_class
        if tps:
            path = resolve_tps_path(tps)
            if path:
                apply_tps(t, load_tps(path))
                t.tps_path = str(path)
        return t

    kind_part = kind
    hostport = name_or_addr
    if "@" in name_or_addr and not name_or_addr.startswith("@"):
        kind_part, hostport = name_or_addr.split("@", 1)
    host = hostport
    p = port or 2222
    if ":" in hostport:
        host, _, ps = hostport.rpartition(":")
        if ps.isdigit():
            p = int(ps)
        else:
            host = hostport
    proto = protocol or "ssh"
    t = TargetSpec(
        name=name_or_addr,
        kind=kind_part or "generic",
        source_root=source_root,
        host=host,
        port=p,
        protocol=proto,
        protocols=[proto],
        ports_map={proto: p},
        ssh_port=p if proto == "ssh" else None,
        profile_class=profile_class or "POSIX-Shell",
    )
    if tps:
        path = resolve_tps_path(tps)
        if path:
            apply_tps(t, load_tps(path))
            t.tps_path = str(path)
    return t
