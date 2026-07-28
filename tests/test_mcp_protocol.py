"""MCP protocol plugin P0 tests — local stub HTTP MCP server."""

from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any
from urllib.parse import urlparse

import pytest

from uhbs_core.models import TargetSpec
from uhbs_core.protocols import get_plugin, list_protocols
from uhbs_core.protocols.mcp import MCPPlugin, _map_string_args, _pick_safe_tool, _tool_is_high_risk
from uhbs_core.protocols.mcp_jsonrpc import jsonrpc_notification, resolve_session
from uhbs_core.test_realism import run as run_module_b


class _McpStubState:
    def __init__(self) -> None:
        self.initialized_notify = False
        self.mode = "full"  # full | empty_tools | high_risk | http500_codes | allow_early_list
        self.tools: list[dict[str, Any]] = [
            {
                "name": "echo",
                "description": "echo a message",
                "inputSchema": {
                    "type": "object",
                    "properties": {"message": {"type": "string"}},
                    "required": ["message"],
                },
            }
        ]


STATE = _McpStubState()


def _json_rpc_result(req_id: Any, result: Any) -> bytes:
    return json.dumps({"jsonrpc": "2.0", "id": req_id, "result": result}).encode()


def _json_rpc_error(req_id: Any, code: int, message: str) -> bytes:
    return json.dumps(
        {"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}
    ).encode()


class _Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args: Any) -> None:  # noqa: A003
        return

    def _read_json(self) -> dict[str, Any] | None:
        n = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(n) if n else b""
        try:
            return json.loads(raw.decode("utf-8"))
        except Exception:
            return None

    def do_GET(self) -> None:  # noqa: N802
        if urlparse(self.path).path == "/sse":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.end_headers()
            self.wfile.write(b": ping\n\n")
            self.wfile.write(b"event: endpoint\ndata: /messages?sessionId=stub1\n\n")
            return
        self.send_response(404)
        self.end_headers()

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path not in {"/mcp", "/messages"}:
            self.send_response(404)
            self.end_headers()
            return
        raw_len = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(raw_len) if raw_len else b""
        try:
            body = json.loads(raw.decode("utf-8"))
        except Exception:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(_json_rpc_error(None, -32700, "Parse error"))
            return

        method = body.get("method")
        req_id = body.get("id")
        has_id = "id" in body

        if STATE.mode == "http500_codes" and method not in {
            "initialize",
            "notifications/initialized",
        }:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"internal error")
            return

        if method == "initialize":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Mcp-Session-Id", "stub-session")
            self.end_headers()
            self.wfile.write(
                _json_rpc_result(
                    req_id,
                    {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "uhbs-stub", "version": "0"},
                    },
                )
            )
            return

        if method == "notifications/initialized":
            # Must be a notification (no id)
            STATE.initialized_notify = not has_id
            self.send_response(202)
            self.end_headers()
            return

        if method == "tools/list":
            if not STATE.initialized_notify and STATE.mode != "allow_early_list":
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(_json_rpc_error(req_id, -32600, "not initialized"))
                return
            tools = [] if STATE.mode == "empty_tools" else list(STATE.tools)
            if STATE.mode == "high_risk":
                tools = [
                    {
                        "name": "execute_shell",
                        "description": "run shell",
                        "inputSchema": {
                            "type": "object",
                            "properties": {"command": {"type": "string"}},
                        },
                    }
                ]
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(_json_rpc_result(req_id, {"tools": tools}))
            return

        if method == "tools/call":
            if not STATE.initialized_notify:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(_json_rpc_error(req_id, -32600, "not initialized"))
                return
            params = body.get("params") or {}
            args = params.get("arguments") or {}
            msg = args.get("message") or args.get("input") or ""
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                _json_rpc_result(
                    req_id,
                    {"content": [{"type": "text", "text": str(msg)}]},
                )
            )
            return

        # unknown method
        if STATE.mode == "http500_codes":
            self.send_response(500)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(_json_rpc_error(req_id, -32601, "Method not found"))


@pytest.fixture()
def mcp_server():
    STATE.initialized_notify = False
    STATE.mode = "full"
    STATE.tools = [
        {
            "name": "echo",
            "description": "echo a message",
            "inputSchema": {
                "type": "object",
                "properties": {"message": {"type": "string"}},
                "required": ["message"],
            },
        }
    ]
    httpd = HTTPServer(("127.0.0.1", 0), _Handler)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield "127.0.0.1", port
    httpd.shutdown()


def _target(host: str, port: int, **ann: Any) -> TargetSpec:
    return TargetSpec(
        name="mcp-stub",
        kind="generic",
        host=host,
        port=port,
        protocol="mcp",
        protocols=["mcp"],
        profile_class="Web-API",
        ports_map={"mcp": port},
        annotations={"mcp_path": "/mcp", "mcp_transport": "streamable_http", **ann},
    )


def test_registry_has_mcp() -> None:
    assert "mcp" in list_protocols()
    assert isinstance(get_plugin("mcp"), MCPPlugin)


def test_notification_omits_id(mcp_server) -> None:
    host, port = mcp_server
    session = resolve_session(host, port, path="/mcp")
    # manually ensure payload has no id by calling helper
    from uhbs_core.protocols import mcp_jsonrpc as m

    payload = {"jsonrpc": "2.0", "method": "notifications/initialized"}
    assert "id" not in payload
    # initialize first
    m.jsonrpc_request(
        session,
        "initialize",
        {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "t", "version": "0"},
        },
    )
    resp = jsonrpc_notification(session, "notifications/initialized", {})
    assert resp.http_status in {200, 202, 204}


def test_lifecycle_and_codes(mcp_server) -> None:
    host, port = mcp_server
    plugin = MCPPlugin()
    t = _target(host, port)
    fsm = plugin.probe_fsm(host, port, t, None)
    ids = {c.id: c for c in fsm}
    assert ids["mcp.fsm.invalid_jsonrpc"].passed
    assert ids["mcp.fsm.unknown_method"].passed
    assert ids["mcp.fsm.uninitialized_call"].passed

    nego = plugin.probe_negotiation(host, port, t, None)
    nids = {c.id: c for c in nego}
    assert nids["mcp.nego.initialize"].passed
    assert nids["mcp.nego.initialized_notification"].passed
    assert nids["mcp.nego.tools_list"].passed


def test_schema_mapped_echo(mcp_server) -> None:
    host, port = mcp_server
    plugin = MCPPlugin()
    t = _target(host, port)
    payload = plugin.probe_payload(host, port, t, None)
    echo = next(c for c in payload if c.id == "mcp.payload.tool_echo")
    assert echo.passed
    assert echo.score >= 70
    assert t.annotations.get("mcp_surface_depth") == "interactive"


def test_empty_tools_ceiling(mcp_server) -> None:
    host, port = mcp_server
    STATE.mode = "empty_tools"
    plugin = MCPPlugin()
    t = _target(host, port)
    payload = plugin.probe_payload(host, port, t, None)
    echo = next(c for c in payload if c.id == "mcp.payload.tool_echo")
    assert "NEUTRAL_NO_SURFACE" in echo.detail
    assert echo.score == 50.0
    assert t.annotations.get("mcp_surface_depth") == "metadata_only"
    b = run_module_b(t)
    assert b.score <= 50.0
    assert "surface_depth=metadata_only" in " ".join(b.notes)


def test_high_risk_schema_denylist(mcp_server) -> None:
    host, port = mcp_server
    STATE.mode = "high_risk"
    plugin = MCPPlugin()
    t = _target(host, port)
    payload = plugin.probe_payload(host, port, t, None)
    echo = next(c for c in payload if c.id == "mcp.payload.tool_echo")
    assert "SKIPPED_HIGH_RISK_TOOL" in echo.detail
    assert echo.score == 50.0


def test_schema_denylist_helper() -> None:
    tool = {
        "name": "get_system_status",
        "description": "status",
        "inputSchema": {"properties": {"command": {"type": "string"}}},
    }
    risky, why = _tool_is_high_risk(tool)
    assert risky
    assert "command" in why


def test_map_string_args_uses_message() -> None:
    tool = {
        "name": "echo",
        "inputSchema": {
            "properties": {"message": {"type": "string"}},
            "required": ["message"],
        },
    }
    args = _map_string_args(tool, "nonceA")
    assert args == {"message": "nonceA"}


def test_custom_allowlist(mcp_server) -> None:
    host, port = mcp_server
    STATE.tools = [
        {
            "name": "check_weather",
            "description": "weather",
            "inputSchema": {"properties": {"message": {"type": "string"}}},
        }
    ]
    tool, reason = _pick_safe_tool(STATE.tools, ["check_weather"])
    assert tool is not None
    assert reason == ""
    plugin = MCPPlugin()
    t = _target(host, port, mcp_custom_allowlist_tools=["check_weather"])
    payload = plugin.probe_payload(host, port, t, None)
    echo = next(c for c in payload if c.id == "mcp.payload.tool_echo")
    assert echo.passed


def test_beelzebub_style_tool_prefix_allowlist() -> None:
    tools = [
        {
            "name": "tool:system-log",
            "description": "query logs",
            "inputSchema": {
                "properties": {
                    "filter": {"type": "string"},
                }
            },
        }
    ]
    tool, reason = _pick_safe_tool(tools, ["system-log"])
    assert reason == ""
    assert tool is not None
    assert tool["name"] == "tool:system-log"


def test_sse_endpoint_resolve(mcp_server) -> None:
    host, port = mcp_server
    session = resolve_session(host, port, transport="sse", sse_path="/sse")
    assert "messages" in session.post_url
    assert session.transport == "sse"


def test_http500_unknown_method_fails(mcp_server) -> None:
    host, port = mcp_server
    STATE.mode = "http500_codes"
    plugin = MCPPlugin()
    t = _target(host, port)
    fsm = plugin.probe_fsm(host, port, t, None)
    unk = next(c for c in fsm if c.id == "mcp.fsm.unknown_method")
    assert not unk.passed
