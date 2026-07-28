"""HTTP / SSE JSON-RPC helpers for MCP honeypot grading (UHBS P0).

Supports streamable HTTP POST and MCP SSE (GET → endpoint event → POST).
Notifications are sent without a JSON-RPC ``id`` field.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any

DEFAULT_TIMEOUT_S = 5.0


@dataclass
class JsonRpcResponse:
    http_status: int
    headers: dict[str, str]
    body: bytes
    parsed: dict[str, Any] | None = None
    rtt_ms: float = 0.0
    error: str = ""
    session_id: str | None = None


@dataclass
class McpSession:
    """Resolved POST endpoint + optional session id for a target."""

    post_url: str
    session_id: str | None = None
    sse_url: str | None = None
    transport: str = "streamable_http"


def _header_map(headers: Any) -> dict[str, str]:
    out: dict[str, str] = {}
    try:
        for k, v in headers.items():
            out[str(k).lower()] = str(v)
    except Exception:
        pass
    return out


def _extract_session(headers: dict[str, str]) -> str | None:
    for key in ("mcp-session-id", "mcp_session_id", "x-mcp-session-id"):
        if key in headers and headers[key].strip():
            return headers[key].strip()
    return None


def _parse_json_body(body: bytes) -> dict[str, Any] | None:
    text = body.decode("utf-8", errors="replace").strip()
    if not text:
        return None
    if "data:" in text and ("event:" in text or text.lstrip().startswith("data:")):
        last: dict[str, Any] | None = None
        for line in text.splitlines():
            line = line.strip()
            if line.startswith(":"):
                continue  # ping / comment
            if line.startswith("data:"):
                payload = line[5:].strip()
                if not payload or payload == "[DONE]":
                    continue
                try:
                    obj = json.loads(payload)
                except json.JSONDecodeError:
                    continue
                if isinstance(obj, dict):
                    last = obj
        return last
    try:
        obj = json.loads(text)
    except json.JSONDecodeError:
        return None
    return obj if isinstance(obj, dict) else None


def _http_exchange(
    url: str,
    *,
    method: str = "POST",
    body: bytes | None = None,
    headers: dict[str, str] | None = None,
    timeout: float = DEFAULT_TIMEOUT_S,
) -> JsonRpcResponse:
    hdrs = {"Accept": "application/json, text/event-stream"}
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, data=body, headers=hdrs, method=method)
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            rtt = (time.perf_counter() - t0) * 1000.0
            hmap = _header_map(resp.headers)
            return JsonRpcResponse(
                http_status=int(getattr(resp, "status", 200) or 200),
                headers=hmap,
                body=raw,
                parsed=_parse_json_body(raw),
                rtt_ms=rtt,
                session_id=_extract_session(hmap),
            )
    except urllib.error.HTTPError as exc:
        raw = exc.read() if hasattr(exc, "read") else b""
        rtt = (time.perf_counter() - t0) * 1000.0
        hmap = _header_map(getattr(exc, "headers", {}) or {})
        return JsonRpcResponse(
            http_status=int(exc.code),
            headers=hmap,
            body=raw or b"",
            parsed=_parse_json_body(raw or b""),
            rtt_ms=rtt,
            session_id=_extract_session(hmap),
            error=f"HTTPError {exc.code}",
        )
    except Exception as exc:  # noqa: BLE001 — probe path must not raise
        rtt = (time.perf_counter() - t0) * 1000.0
        return JsonRpcResponse(
            http_status=0,
            headers={},
            body=b"",
            rtt_ms=rtt,
            error=str(exc)[:200],
        )


def build_base_url(host: str, port: int, path: str = "/mcp") -> str:
    if not path.startswith("/"):
        path = "/" + path
    return f"http://{host}:{int(port)}{path}"


def open_sse_session(
    host: str,
    port: int,
    *,
    sse_path: str = "/sse",
    timeout: float = DEFAULT_TIMEOUT_S,
) -> McpSession:
    """GET SSE stream, parse ``event: endpoint``, return POST URL. Closes GET body."""
    url = build_base_url(host, port, sse_path)
    req = urllib.request.Request(url, method="GET", headers={"Accept": "text/event-stream"})
    endpoint: str | None = None
    session_id: str | None = None
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            hmap = _header_map(resp.headers)
            session_id = _extract_session(hmap)
            deadline = time.time() + timeout
            buf = b""
            while time.time() < deadline and endpoint is None:
                chunk = resp.read(256)
                if not chunk:
                    break
                buf += chunk
                text = buf.decode("utf-8", errors="replace")
                event_name = ""
                for line in text.splitlines():
                    if line.startswith(":"):
                        continue
                    if line.startswith("event:"):
                        event_name = line[6:].strip()
                    elif line.startswith("data:") and event_name == "endpoint":
                        endpoint = line[5:].strip()
                        break
                    elif line.startswith("data:") and not event_name:
                        data = line[5:].strip()
                        if data.startswith("/") or data.startswith("http"):
                            endpoint = data
                            break
            # stream closed via context manager (finally hygiene)
    except Exception:
        return McpSession(
            post_url=build_base_url(host, port, "/messages"),
            transport="sse",
            sse_url=url,
            session_id=None,
        )

    if not endpoint:
        post = build_base_url(host, port, "/messages")
    elif endpoint.startswith("http://") or endpoint.startswith("https://"):
        post = endpoint
    else:
        post = build_base_url(host, port, endpoint if endpoint.startswith("/") else f"/{endpoint}")
    qs = urllib.parse.urlparse(post).query
    q = urllib.parse.parse_qs(qs)
    if "sessionId" in q and q["sessionId"]:
        session_id = session_id or q["sessionId"][0]
    return McpSession(post_url=post, session_id=session_id, sse_url=url, transport="sse")


def resolve_session(
    host: str,
    port: int,
    *,
    transport: str = "streamable_http",
    path: str = "/mcp",
    sse_path: str = "/sse",
    timeout: float = DEFAULT_TIMEOUT_S,
) -> McpSession:
    transport = (transport or "streamable_http").lower()
    if transport in {"sse", "http_sse"}:
        return open_sse_session(host, port, sse_path=sse_path, timeout=timeout)
    return McpSession(
        post_url=build_base_url(host, port, path),
        transport="streamable_http",
    )


def jsonrpc_request(
    session: McpSession,
    method: str,
    params: dict[str, Any] | None = None,
    *,
    req_id: int | str = 1,
    timeout: float = DEFAULT_TIMEOUT_S,
    content_type: str = "application/json",
    extra_headers: dict[str, str] | None = None,
) -> JsonRpcResponse:
    payload: dict[str, Any] = {"jsonrpc": "2.0", "id": req_id, "method": method}
    if params is not None:
        payload["params"] = params
    body = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": content_type}
    if session.session_id:
        headers["Mcp-Session-Id"] = session.session_id
    if extra_headers:
        headers.update(extra_headers)
    resp = _http_exchange(
        session.post_url, method="POST", body=body, headers=headers, timeout=timeout
    )
    if resp.session_id and not session.session_id:
        session.session_id = resp.session_id
    return resp


def jsonrpc_notification(
    session: McpSession,
    method: str,
    params: dict[str, Any] | None = None,
    *,
    timeout: float = DEFAULT_TIMEOUT_S,
) -> JsonRpcResponse:
    """JSON-RPC notification — **must not** include ``id``."""
    payload: dict[str, Any] = {"jsonrpc": "2.0", "method": method}
    if params is not None:
        payload["params"] = params
    assert "id" not in payload
    body = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if session.session_id:
        headers["Mcp-Session-Id"] = session.session_id
    return _http_exchange(
        session.post_url, method="POST", body=body, headers=headers, timeout=timeout
    )


def rpc_error_code(resp: JsonRpcResponse) -> int | None:
    if not resp.parsed or "error" not in resp.parsed:
        return None
    err = resp.parsed["error"]
    if isinstance(err, dict) and "code" in err:
        try:
            return int(err["code"])
        except (TypeError, ValueError):
            return None
    return None


def rpc_has_result(resp: JsonRpcResponse) -> bool:
    return bool(resp.parsed and "result" in resp.parsed and "error" not in resp.parsed)
