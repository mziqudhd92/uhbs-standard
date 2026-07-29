"""Internet Printing Protocol (IPP/1.1) over HTTP — RFC 8010 / RFC 8011."""

from __future__ import annotations

import struct

from uhbs_core.models import CheckResult, TargetSpec
from uhbs_core.protocols.base import ProtocolPlugin
from uhbs_core.rfc_probes import _transact
from uhbs_core.tps import TPS

# IPP/1.1
_IPP_VERSION = (1, 1)
_OP_GET_PRINTER_ATTRIBUTES = 0x000B

_TAG_OPERATION_ATTRIBUTES = 0x01
_TAG_END_OF_ATTRIBUTES = 0x03

_VAL_CHARSET = 0x47
_VAL_NATURAL_LANGUAGE = 0x48
_VAL_URI = 0x45
_VAL_KEYWORD = 0x44

_DEFAULT_PATHS = ("/ipp/print", "/", "/printers/ipp")


def _encode_attribute(name: str, value_tag: int, value: bytes) -> bytes:
    name_b = name.encode("utf-8")
    return (
        struct.pack("!B", value_tag)
        + struct.pack("!H", len(name_b))
        + name_b
        + struct.pack("!H", len(value))
        + value
    )


def build_ipp_message(
    *,
    major: int = 1,
    minor: int = 1,
    operation_or_status: int,
    request_id: int,
    attribute_groups: bytes,
) -> bytes:
    """Build an IPP request or response (attribute groups include group tags)."""
    head = struct.pack("!BBHI", major, minor, operation_or_status, request_id)
    if attribute_groups and not attribute_groups.endswith(bytes([_TAG_END_OF_ATTRIBUTES])):
        attribute_groups += bytes([_TAG_END_OF_ATTRIBUTES])
    elif not attribute_groups:
        attribute_groups = bytes([_TAG_END_OF_ATTRIBUTES])
    return head + attribute_groups


def build_get_printer_attributes_request(
    printer_uri: str = "ipp://127.0.0.1/ipp/print",
    *,
    request_id: int = 1,
    attributes: tuple[str, ...] = ("printer-name", "document-format-supported"),
) -> bytes:
    """RFC 8011 Get-Printer-Attributes (operation 0x000B)."""
    group = bytes([_TAG_OPERATION_ATTRIBUTES])
    group += _encode_attribute("attributes-charset", _VAL_CHARSET, b"utf-8")
    group += _encode_attribute("attributes-natural-language", _VAL_NATURAL_LANGUAGE, b"en")
    group += _encode_attribute("printer-uri", _VAL_URI, printer_uri.encode("utf-8"))
    for attr in attributes:
        group += _encode_attribute("requested-attributes", _VAL_KEYWORD, attr.encode("utf-8"))
    return build_ipp_message(
        major=_IPP_VERSION[0],
        minor=_IPP_VERSION[1],
        operation_or_status=_OP_GET_PRINTER_ATTRIBUTES,
        request_id=request_id,
        attribute_groups=group,
    )


def build_malformed_ipp_request() -> bytes:
    """IPP/2.0 Get-Printer-Attributes — version not supported on IPP/1.1 stacks."""
    group = bytes([_TAG_OPERATION_ATTRIBUTES, _TAG_END_OF_ATTRIBUTES])
    return build_ipp_message(
        major=2,
        minor=0,
        operation_or_status=_OP_GET_PRINTER_ATTRIBUTES,
        request_id=99,
        attribute_groups=group,
    )


def build_http_ipp_post(
    ipp_body: bytes,
    *,
    host: str,
    path: str = "/ipp/print",
) -> bytes:
    host_hdr = host if ":" not in host else host.split(":", 1)[0]
    req = (
        f"POST {path} HTTP/1.1\r\n"
        f"Host: {host_hdr}\r\n"
        "Content-Type: application/ipp\r\n"
        f"Content-Length: {len(ipp_body)}\r\n"
        "Connection: close\r\n"
        "\r\n"
    ).encode("ascii")
    return req + ipp_body


def split_http_response(raw: bytes) -> tuple[int | None, bytes]:
    """Return (HTTP status code or None, message body)."""
    if not raw:
        return None, b""
    header_end = raw.find(b"\r\n\r\n")
    if header_end < 0:
        return None, raw
    header = raw[:header_end].decode("latin-1", "replace")
    body = raw[header_end + 4 :]
    status_code: int | None = None
    first_line = header.split("\r\n", 1)[0]
    parts = first_line.split()
    if len(parts) >= 2 and parts[0].startswith("HTTP/"):
        try:
            status_code = int(parts[1])
        except ValueError:
            status_code = None
    return status_code, body


def ipp_status_code(ipp_body: bytes) -> int | None:
    """Parse IPP status-code (bytes 2–3) from a response body."""
    if len(ipp_body) < 4:
        return None
    return struct.unpack("!H", ipp_body[2:4])[0]


def is_client_error_ipp(status: int | None) -> bool:
    return status is not None and 0x0400 <= status < 0x0500


def is_successful_ipp(status: int | None) -> bool:
    return status is not None and 0x0000 <= status < 0x0100


def _http_ipp_exchange(
    host: str,
    port: int,
    ipp_body: bytes,
    *,
    path: str,
) -> tuple[int | None, int | None, str]:
    """POST application/ipp; return (http_status, ipp_status, detail)."""
    payload = build_http_ipp_post(ipp_body, host=f"{host}:{port}", path=path)
    raw, _, err = _transact(host, port, payload, recv_first=False)
    if err and not raw:
        return None, None, err
    http_status, body = split_http_response(raw)
    ipp_st = ipp_status_code(body)
    if ipp_st is not None:
        detail = f"http={http_status} ipp=0x{ipp_st:04x} path={path}"
    elif http_status is not None:
        detail = f"http={http_status} path={path} body_len={len(body)}"
    else:
        detail = err or f"no HTTP response path={path}"
    return http_status, ipp_st, detail


class IppPlugin(ProtocolPlugin):
    """IPP/1.1 printer attribute exchange over HTTP (typical TCP 631)."""

    name = "ipp"
    families = ("it", "print")

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        checks: list[CheckResult] = []

        # Wrong major/minor — expect client-error or HTTP 4xx (RFC 8010 §4.1.9).
        bad_ver = build_malformed_ipp_request()
        http_st, ipp_st, detail = _http_ipp_exchange(
            host, port, bad_ver, path=_DEFAULT_PATHS[0]
        )
        rejected = (
            is_client_error_ipp(ipp_st)
            or (http_st is not None and 400 <= http_st < 500)
        )
        score_ver = 100.0 if rejected else (40.0 if http_st or ipp_st is not None else 0.0)
        checks.append(
            CheckResult(
                id="ipp.fsm.version_not_supported",
                team="blue",
                passed=score_ver >= 70.0,
                detail=detail,
                score=score_ver,
            )
        )

        # Truncated / non-IPP binary body — still must not accept as valid IPP.
        garbage = b"\xff\xfe\xfd\xfc" + bytes(range(32))
        http_g, ipp_g, detail_g = _http_ipp_exchange(
            host, port, garbage, path=_DEFAULT_PATHS[0]
        )
        rejected_g = (
            is_client_error_ipp(ipp_g)
            or (http_g is not None and 400 <= http_g < 500)
            or (http_g is not None and http_g >= 500)
        )
        # Treat silent close without HTTP as weak but not a hang (score 60).
        if not http_g and not ipp_g and detail_g and "refused" not in detail_g.lower():
            rejected_g = True
            score_g = 60.0
        else:
            score_g = 100.0 if rejected_g else 20.0
        checks.append(
            CheckResult(
                id="ipp.fsm.malformed_body",
                team="blue",
                passed=score_g >= 70.0,
                detail=detail_g,
                score=score_g,
            )
        )
        return checks

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        host_label = host
        best_score = 0.0
        best_detail = "no IPP response"
        best_passed = False
        best_path = _DEFAULT_PATHS[0]

        for path in _DEFAULT_PATHS:
            uri = f"ipp://{host_label}:{port}{path}"
            ipp_req = build_get_printer_attributes_request(printer_uri=uri)
            http_st, ipp_st, detail = _http_ipp_exchange(
                host, port, ipp_req, path=path
            )
            if is_successful_ipp(ipp_st):
                return [
                    CheckResult(
                        id="ipp.nego.get_printer_attributes",
                        team="blue",
                        passed=True,
                        detail=detail,
                        score=100.0,
                    )
                ]
            # Structured client/server IPP status still proves IPP framing.
            if ipp_st is not None and not is_client_error_ipp(ipp_st):
                best_score = max(best_score, 85.0)
                best_passed = True
                best_detail = detail
                best_path = path
            elif ipp_st is not None and is_client_error_ipp(ipp_st):
                best_score = max(best_score, 75.0)
                best_passed = True
                best_detail = detail
                best_path = path
            elif http_st == 200 and ipp_st is None:
                best_score = max(best_score, 50.0)
                best_detail = detail
                best_path = path
            elif http_st is not None and http_st < 500:
                best_score = max(best_score, 40.0)
                best_detail = detail
                best_path = path

        return [
            CheckResult(
                id="ipp.nego.get_printer_attributes",
                team="blue",
                passed=best_passed or best_score >= 70.0,
                detail=f"{best_detail} (tried paths including {best_path})",
                score=best_score,
            )
        ]

    def probe_load_once(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> float:
        uri = f"ipp://{host}:{port}{_DEFAULT_PATHS[0]}"
        ipp_req = build_get_printer_attributes_request(printer_uri=uri)
        payload = build_http_ipp_post(ipp_req, host=f"{host}:{port}", path=_DEFAULT_PATHS[0])
        _, rtt, err = _transact(host, port, payload, recv_first=False)
        if err:
            raise RuntimeError(err)
        return rtt
