"""Kubernetes API plugin — offline helpers and local HTTP stub."""

from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from uhbs_core.models import TargetSpec
from uhbs_core.protocols import registry
from uhbs_core.protocols.kubernetes import (
    KubernetesPlugin,
    looks_like_api_versions,
    looks_like_version_info,
    version_fingerprint,
)


def _register_kubernetes_for_test() -> None:
    plugin = KubernetesPlugin()
    registry.register(plugin)
    for alias in ("k8s", "kube-api", "kubernetes-api"):
        registry._REGISTRY[alias] = plugin  # noqa: SLF001 — mirrors parent registry merge


def test_kubernetes_plugin_resolves_and_aliases() -> None:
    _register_kubernetes_for_test()
    p = registry.get_plugin("kubernetes")
    assert isinstance(p, KubernetesPlugin)
    assert p.name == "kubernetes"
    assert registry.get_plugin("k8s").name == "kubernetes"
    assert registry.get_plugin("kube-api").name == "kubernetes"
    assert registry.get_plugin("kubernetes-api").name == "kubernetes"


def test_version_and_api_shape_helpers() -> None:
    assert looks_like_version_info({"major": "1", "minor": "29", "gitVersion": "v1.29.0"})
    assert not looks_like_version_info({"kind": "APIVersions"})
    assert looks_like_api_versions({"kind": "APIVersions", "versions": ["v1"]})
    assert not looks_like_api_versions({"major": "1", "minor": "1"})
    assert version_fingerprint({"major": "1", "minor": "2", "gitVersion": "v1.2.3"}) == (
        "1",
        "2",
        "v1.2.3",
    )


class _KubeStubHandler(BaseHTTPRequestHandler):
    version_doc = {
        "major": "1",
        "minor": "30",
        "gitVersion": "v1.30.0",
        "gitCommit": "deadbeef",
        "gitTreeState": "clean",
        "buildDate": "2026-01-01T00:00:00Z",
        "goVersion": "go1.22.0",
        "compiler": "gc",
        "platform": "linux/amd64",
    }

    def log_message(self, fmt: str, *args: object) -> None:  # noqa: A003
        return

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/version":
            body = json.dumps(self.version_doc).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == "/api":
            body = json.dumps(
                {"kind": "APIVersions", "versions": ["v1"], "serverAddressByClientCIDRs": []}
            ).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == "/apis":
            body = json.dumps({"kind": "APIGroupList", "groups": [], "apiVersion": "v1"}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self.send_response(404)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"kind":"Status","status":"Failure","code":404}\n')

    def do_TRACE(self) -> None:  # noqa: N802
        self.send_response(405)
        self.send_header("Allow", "GET")
        self.end_headers()


def _start_kube_stub() -> tuple[str, int, threading.Event, HTTPServer]:
    server = HTTPServer(("127.0.0.1", 0), _KubeStubHandler)
    host, port = server.server_address
    stop = threading.Event()

    def _serve() -> None:
        server.timeout = 0.5
        while not stop.is_set():
            server.handle_request()

    thread = threading.Thread(target=_serve, daemon=True)
    thread.start()
    return host, port, stop, server


def test_unreachable_does_not_raise() -> None:
    plugin = KubernetesPlugin()
    target = TargetSpec(name="down", host="127.0.0.1", port=1, protocol="kubernetes")
    for fn in (plugin.probe_fsm, plugin.probe_negotiation, plugin.probe_state):
        results = fn("127.0.0.1", 1, target, None)
        assert isinstance(results, list)
        assert results


def test_kubernetes_probes_against_stub() -> None:
    host, port, stop, server = _start_kube_stub()
    try:
        plugin = KubernetesPlugin()
        target = TargetSpec(name="kube-stub", host=host, port=port, protocol="kubernetes")
        fsm = plugin.probe_fsm(host, port, target, None)
        nego = plugin.probe_negotiation(host, port, target, None)
        state = plugin.probe_state(host, port, target, None)

        fsm_by_id = {c.id: c for c in fsm}
        assert fsm_by_id["kubernetes.fsm.nonsense_path"].passed
        assert fsm_by_id["kubernetes.fsm.nonsense_path"].score >= 70.0
        assert fsm_by_id["kubernetes.fsm.bad_method"].passed

        nego_by_id = {c.id: c for c in nego}
        assert nego_by_id["kubernetes.nego.version"].passed
        assert nego_by_id["kubernetes.nego.api"].passed

        assert len(state) == 1
        assert state[0].id == "kubernetes.state.version_stable"
        assert state[0].passed
    finally:
        stop.set()
        server.server_close()
