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
    ports_map = {str(k).lower(): int(v) for k, v in ports.items()}
    if ssh_port is not None:
        ports_map.setdefault("ssh", int(ssh_port))
    if smtp_port is not None:
        ports_map.setdefault("smtp", int(smtp_port))
    if http_port is not None:
        ports_map.setdefault("http", int(http_port))

    protocols = raw.get("protocols") or []
    if isinstance(protocols, str):
        protocols = [protocols]
    protocol = raw.get("protocol")
    if not protocols and protocol:
        protocols = [protocol]
    if not protocols:
        protocols = list(ports_map.keys())
    protocols = [str(p) for p in protocols]
    proto_l = {p.lower() for p in protocols}

    # Prefer explicit port, then protocol-native ports — never invent SSH for HTTP-only.
    if raw.get("port") is not None:
        primary = int(raw["port"])
    elif "http" in proto_l and ports_map.get("http") is not None:
        primary = int(ports_map["http"])
    elif "ssh" in proto_l and ports_map.get("ssh") is not None:
        primary = int(ports_map["ssh"])
    elif ports_map:
        primary = int(next(iter(ports_map.values())))
    else:
        primary = 2222

    if "ssh" not in ports_map and "ssh" in proto_l:
        ports_map["ssh"] = primary

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
        ssh_port=int(ssh_port) if ssh_port is not None else ports_map.get("ssh"),
        smtp_port=int(smtp_port) if smtp_port is not None else ports_map.get("smtp"),
        http_port=int(http_port) if http_port is not None else ports_map.get("http"),
        tps_path=raw.get("tps") or raw.get("tps_path"),
        protocol=str(protocol or (protocols[0] if protocols else "")) or None,
        protocols=protocols,
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
        if protocol:
            t.protocol = protocol
            t.protocols = [protocol]
        if port:
            t.port = port
            proto = (protocol or t.protocol or "").lower()
            if proto:
                t.ports_map[proto] = port
                if proto == "ssh":
                    t.ssh_port = port
                elif proto in {"http", "https"}:
                    t.http_port = port
                elif proto == "smtp":
                    t.smtp_port = port
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
    # Do not default to ssh — require --protocol or a TPS that declares protocols.
    proto = protocol
    ports_map = {proto: p} if proto else {}
    t = TargetSpec(
        name=name_or_addr,
        kind=kind_part or "generic",
        source_root=source_root,
        host=host,
        port=p,
        protocol=proto,
        protocols=[proto] if proto else [],
        ports_map=ports_map,
        ssh_port=p if proto == "ssh" else None,
        http_port=p if proto in {"http", "https"} else None,
        smtp_port=p if proto == "smtp" else None,
        profile_class=profile_class or "POSIX-Shell",
    )
    if tps:
        path = resolve_tps_path(tps)
        if path:
            apply_tps(t, load_tps(path))
            t.tps_path = str(path)
    return t
