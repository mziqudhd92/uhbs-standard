"""Kubernetes API discovery probes (HTTPS/HTTP over TCP).

Exercises ``/version``, ``/api``, and ``/apis`` discovery shapes per upstream
API conventions. Uses plain HTTP suitable for lab decoys; TLS is not required.
"""

from __future__ import annotations

import json
import re

from uhbs_core.protocols.base import ProtocolPlugin

from ..models import CheckResult, TargetSpec
from ..rfc_probes import _transact
from ..tps import TPS

_HTTP_STATUS = re.compile(rb"^HTTP/1\.[01] (\d{3})", re.MULTILINE)

_NONSENSE_PATH = "/uhbs-nonsense-not-a-k8s-resource"


def _http_get(path: str, host_header: str = "uhbs.invalid") -> bytes:
    return (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host_header}\r\n"
        f"Accept: application/json\r\n"
        f"Connection: close\r\n\r\n"
    ).encode("ascii")


def _http_status_code(raw: bytes) -> int | None:
    m = _HTTP_STATUS.search(raw)
    return int(m.group(1)) if m else None


def _http_body(raw: bytes) -> bytes:
    if b"\r\n\r\n" in raw:
        return raw.split(b"\r\n\r\n", 1)[1]
    if b"\n\n" in raw:
        return raw.split(b"\n\n", 1)[1]
    return b""


def _try_json(body: bytes) -> dict | None:
    text = body.decode("utf-8", errors="replace").strip()
    if not text:
        return None
    try:
        obj = json.loads(text)
    except json.JSONDecodeError:
        return None
    return obj if isinstance(obj, dict) else None


def looks_like_version_info(obj: dict | None) -> bool:
    if not isinstance(obj, dict):
        return False
    major = obj.get("major")
    minor = obj.get("minor")
    return major is not None and minor is not None


def looks_like_api_versions(obj: dict | None) -> bool:
    if not isinstance(obj, dict):
        return False
    return obj.get("kind") == "APIVersions" and isinstance(obj.get("versions"), list)


def version_fingerprint(obj: dict | None) -> tuple[str, str, str]:
    if not isinstance(obj, dict):
        return ("", "", "")
    return (
        str(obj.get("major", "")),
        str(obj.get("minor", "")),
        str(obj.get("gitVersion", "")),
    )


def _score_fsm(code: int | None, body: bytes) -> tuple[float, str, bool]:
    """Return (score, detail, passed-derived ok)."""
    obj = _try_json(_http_body(body))
    kube_shaped_200 = code == 200 and looks_like_version_info(obj)
    if kube_shaped_200:
        return 0.0, "200 on nonsense path with /version-shaped JSON", False
    if code is not None and 400 <= code < 500:
        return 100.0, f"status={code}", True
    if code == 404:
        return 100.0, "status=404", True
    if code is not None and code >= 500:
        return 70.0, f"status={code} (server error, not kube discovery spoof)", True
    if code == 200:
        return 40.0, "status=200 on unknown path without version JSON", False
    if code is None:
        return 60.0, "no HTTP status (closed or non-HTTP)", True
    return 30.0, f"status={code}", False


class KubernetesPlugin(ProtocolPlugin):
    name = "kubernetes"
    families = ("it", "api", "orchestration")

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        checks: list[CheckResult] = []

        raw, _, err = _transact(host, port, _http_get(_NONSENSE_PATH), recv_first=False)
        code = _http_status_code(raw)
        score, detail, _ = _score_fsm(code, raw)
        if code is None and err:
            detail = err[:120]
            score = 0.0
        checks.append(
            CheckResult(
                id="kubernetes.fsm.nonsense_path",
                team="blue",
                passed=score >= 70.0,
                detail=detail,
                score=score,
            )
        )

        bad_method = (
            b"TRACE /version HTTP/1.1\r\n"
            b"Host: uhbs.invalid\r\n"
            b"Connection: close\r\n\r\n"
        )
        raw_m, _, err_m = _transact(host, port, bad_method, recv_first=False)
        code_m = _http_status_code(raw_m)
        obj_m = _try_json(_http_body(raw_m))
        if code_m == 200 and looks_like_version_info(obj_m):
            score_m = 0.0
            detail_m = "TRACE /version returned version JSON with 200"
        elif code_m in (404, 405, 400, 401, 403) or (code_m is not None and 400 <= code_m < 500):
            score_m = 100.0
            detail_m = f"status={code_m}"
        elif code_m is None and err_m:
            score_m = 0.0
            detail_m = err_m[:120]
        elif code_m == 200:
            score_m = 50.0
            detail_m = "status=200 on unsupported method"
        else:
            score_m = 80.0 if (code_m is None or code_m >= 400) else 25.0
            detail_m = f"status={code_m}" if code_m is not None else "no HTTP status"
        checks.append(
            CheckResult(
                id="kubernetes.fsm.bad_method",
                team="blue",
                passed=score_m >= 70.0,
                detail=detail_m,
                score=score_m,
            )
        )
        return checks

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        checks: list[CheckResult] = []

        raw_v, _, err_v = _transact(host, port, _http_get("/version"), recv_first=False)
        code_v = _http_status_code(raw_v)
        ver = _try_json(_http_body(raw_v))
        ver_ok = code_v == 200 and looks_like_version_info(ver)
        checks.append(
            CheckResult(
                id="kubernetes.nego.version",
                team="blue",
                passed=ver_ok,
                detail=(
                    f"major={ver.get('major')} minor={ver.get('minor')}"
                    if ver_ok and ver
                    else (err_v or f"status={code_v}")[:120]
                ),
                score=100.0 if ver_ok else 0.0,
            )
        )

        raw_a, _, err_a = _transact(host, port, _http_get("/api"), recv_first=False)
        code_a = _http_status_code(raw_a)
        api = _try_json(_http_body(raw_a))
        api_ok = code_a == 200 and looks_like_api_versions(api)
        checks.append(
            CheckResult(
                id="kubernetes.nego.api",
                team="blue",
                passed=api_ok,
                detail=(
                    f"kind=APIVersions versions={len(api.get('versions', []))}"
                    if api_ok and api
                    else (err_a or f"status={code_a}")[:120]
                ),
                score=100.0 if api_ok else 0.0,
            )
        )
        return checks

    def probe_state(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        raw1, _, err1 = _transact(host, port, _http_get("/version"), recv_first=False)
        raw2, _, err2 = _transact(host, port, _http_get("/version"), recv_first=False)
        v1 = _try_json(_http_body(raw1))
        v2 = _try_json(_http_body(raw2))
        fp1 = version_fingerprint(v1)
        fp2 = version_fingerprint(v2)
        ok = (
            looks_like_version_info(v1)
            and looks_like_version_info(v2)
            and fp1 == fp2
            and fp1 != ("", "", "")
        )
        detail = (
            f"fingerprint stable {fp1}"
            if ok
            else (
                f"mismatch {fp1} vs {fp2}"
                if looks_like_version_info(v1) or looks_like_version_info(v2)
                else (err1 or err2 or "no version JSON")[:120]
            )
        )
        return [
            CheckResult(
                id="kubernetes.state.version_stable",
                team="blue",
                passed=ok,
                detail=detail,
                score=100.0 if ok else 20.0,
            )
        ]
