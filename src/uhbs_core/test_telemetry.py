#!/usr/bin/env python3
"""Module C — Telemetry Quality & Pipeline Resilience (UHBS v4.4.4).

C1: STIX 2.1 / OpenTelemetry / ECS schema conformance
C2: Log injection & parser fuzzing
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from uhbs_core.hqs import pass_status  # noqa: E402
from uhbs_core.models import CheckResult, ModuleResult, TargetSpec  # noqa: E402
from uhbs_core.protocols import get_plugin  # noqa: E402
from uhbs_core.ssh_session import run_ssh_command  # noqa: E402
from uhbs_core.tps import TPS  # noqa: E402

_STIX_ID = re.compile(r"^[a-z0-9-]+--[0-9a-fA-F-]{36}$")
_STIX_TYPES = {
    "indicator",
    "malware",
    "attack-pattern",
    "identity",
    "observed-data",
    "bundle",
    "relationship",
    "sighting",
    "tool",
    "campaign",
    "intrusion-set",
    "threat-actor",
    "vulnerability",
    "file",
    "ipv4-addr",
    "domain-name",
    "url",
    "network-traffic",
}


def _iter_jsonl_lines(text: str, *, limit: int, rows: list[Any]) -> None:
    """Append JSON objects parsed from newline-delimited JSON text."""
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            rows.append({"__malformed__": line[:120]})
        if len(rows) >= limit:
            return


def _iter_records(path: Path, limit: int = 800) -> List[Any]:
    """Load telemetry records from a file or directory.

    Accepts ``*.jsonl`` (one JSON object per line) and ``*.json``. Many
    honeypot daemons write JSONL into a file named ``*.json``; when a
    whole-file JSON parse fails with trailing data, we fall back to
    line-delimited parsing so schema gates see real events instead of a
    single false ``malformed`` row.
    """
    rows: List[Any] = []
    files: List[Path]
    if path.is_file():
        files = [path]
    elif path.is_dir():
        files = sorted(path.rglob("*.jsonl")) + sorted(path.rglob("*.json"))
    else:
        return rows
    for fp in files[:60]:
        try:
            text = fp.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if fp.suffix == ".json":
            try:
                rows.append(json.loads(text))
            except json.JSONDecodeError:
                # Common honeypot layout: JSONL content in a ``.json`` path.
                before = len(rows)
                _iter_jsonl_lines(text, limit=limit, rows=rows)
                if len(rows) == before:
                    rows.append({"__malformed__": str(fp)})
            if len(rows) >= limit:
                return rows
            continue
        _iter_jsonl_lines(text, limit=limit, rows=rows)
        if len(rows) >= limit:
            return rows
    return rows


def _flatten(obj: Any) -> List[Any]:
    if isinstance(obj, list):
        out: List[Any] = []
        for x in obj:
            out.extend(_flatten(x))
        return out
    if isinstance(obj, dict):
        if "objects" in obj and isinstance(obj["objects"], list):
            return _flatten(obj["objects"]) + [obj]
        return [obj]
    return []


def _validate_stix(obj: Dict[str, Any]) -> Tuple[bool, str]:
    t = str(obj.get("type", ""))
    if t == "bundle":
        if "objects" not in obj:
            return False, "bundle missing objects"
        return True, "bundle"
    if t not in _STIX_TYPES and not t:
        return False, "missing/unknown type"
    if "id" in obj and not _STIX_ID.match(str(obj["id"])):
        # allow non-UUID lab ids but prefer STIX shape
        if "--" not in str(obj["id"]):
            return False, f"id not STIX-shaped: {obj.get('id')}"
    spec = str(obj.get("spec_version", obj.get("specVersion", "")))
    if spec and not spec.startswith("2."):
        return False, f"spec_version={spec}"
    return True, t or "ok"


def _validate_otel(obj: Dict[str, Any]) -> bool:
    keys = set(obj.keys())
    if "resourceSpans" in keys or "resourceMetrics" in keys or "resourceLogs" in keys:
        return True
    if "attributes" in obj and ("traceId" in obj or "spanId" in obj or "name" in obj):
        return True
    blob = json.dumps(obj).lower()
    return "otel" in blob or "honeypot." in blob


def _validate_ecs(obj: Dict[str, Any]) -> bool:
    if "@timestamp" in obj or "event" in obj or "ecs" in obj:
        return True
    return "message" in obj and ("source" in obj or "destination" in obj)


def _walk_strings(obj: Any) -> List[str]:
    out: List[str] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.append(str(k))
            out.extend(_walk_strings(v))
    elif isinstance(obj, list):
        for v in obj:
            out.extend(_walk_strings(v))
    else:
        out.append(str(obj))
    return out


def run(target: TargetSpec, tps: Optional[TPS] = None) -> ModuleResult:
    checks: List[CheckResult] = []

    # C2 — injection via primary protocol (SSH shell inject or generic fuzz)
    protos = target.protocol_list()
    proto = protos[0] if protos else "generic"
    port = target.port_for(proto) or (target.port if target.host else None)
    if target.host and proto == "ssh" and target.shell_exec_port():
        port = target.shell_exec_port()
        payloads = [
            r'echo -e "ANSI:\x1b[31mRED\x1b[0m"',
            "echo 'json-break: {\"a\": \"unterminated'",
            "printf 'null\\x00byte\\n'",
            "echo 'newline\rinjection'",
        ]
        survived = 0
        for i, cmd in enumerate(payloads):
            out = run_ssh_command(
                target.host, port, target.user, target.password, cmd, timeout=15
            )
            if out.ok:
                survived += 1
            checks.append(
                CheckResult(
                    id=f"c2.inject_{i}",
                    team="red",
                    passed=out.ok,
                    detail=(out.error or "accepted")[:160],
                    score=8.0 if out.ok else 0.0,
                )
            )
        checks.append(
            CheckResult(
                id="c2.parser_survival",
                team="red",
                passed=survived == len(payloads),
                detail=f"{survived}/{len(payloads)} injections survived without client crash",
                score=20.0 if survived == len(payloads) else 4.0 * survived,
            )
        )
    elif target.host and port:
        # Generic binary fuzz as injection stand-in
        fuzz = get_plugin(proto).probe_fuzz(target.host, port, target, tps)
        checks.extend(fuzz)

    # C1 — schema conformance
    tdir = Path(target.telemetry_dir).expanduser() if target.telemetry_dir else None
    if tdir and tdir.exists():
        rows = _iter_records(tdir)
        flat = []
        malformed = 0
        for r in rows:
            if isinstance(r, dict) and "__malformed__" in r:
                malformed += 1
            else:
                flat.extend(_flatten(r))

        total = max(len(rows), 1)
        checks.append(
            CheckResult(
                id="c1.json_parse_clean",
                team="blue",
                passed=malformed == 0,
                detail=f"{malformed} malformed / {len(rows)} records",
                score=20.0 * (1.0 - malformed / total),
            )
        )

        stix_ok = stix_n = 0
        otel_n = ecs_n = 0
        for obj in flat:
            if not isinstance(obj, dict):
                continue
            ok, _ = _validate_stix(obj)
            if obj.get("type") or obj.get("spec_version") or obj.get("objects"):
                stix_n += 1
                if ok:
                    stix_ok += 1
            if _validate_otel(obj):
                otel_n += 1
            if _validate_ecs(obj):
                ecs_n += 1

        if stix_n:
            ratio = stix_ok / stix_n
            checks.append(
                CheckResult(
                    id="c1.stix_2_1",
                    team="blue",
                    passed=ratio >= 0.95,
                    detail=f"STIX-shaped objects ok={stix_ok}/{stix_n} ({ratio:.0%})",
                    score=25.0 * ratio,
                )
            )
        else:
            checks.append(
                CheckResult(
                    id="c1.stix_2_1",
                    team="blue",
                    passed=False,
                    detail="no STIX objects found",
                    score=0.0,
                )
            )

        checks.append(
            CheckResult(
                id="c1.otel_or_ecs",
                team="blue",
                passed=(otel_n + ecs_n) > 0,
                detail=f"otel_docs={otel_n} ecs_docs={ecs_n}",
                score=15.0 if (otel_n + ecs_n) > 0 else 5.0,
            )
        )

        blob = " ".join(_walk_strings(flat)[:8000]).lower()
        has_hash = "sha256" in blob or "md5" in blob
        has_mitre = bool(re.search(r"\bt1\d{3,}|\bmitre\b|\battack\b", blob))
        checks.append(
            CheckResult(
                id="c1.payload_hashes",
                team="blue",
                passed=has_hash,
                detail="hash fields present" if has_hash else "no md5/sha256 fields",
                score=10.0 if has_hash else 0.0,
            )
        )
        checks.append(
            CheckResult(
                id="c1.mitre_mapping",
                team="blue",
                passed=has_mitre,
                detail="MITRE-like tags present" if has_mitre else "no MITRE tags",
                score=10.0 if has_mitre else 0.0,
            )
        )
    else:
        checks.append(
            CheckResult(
                id="c1.telemetry_dir",
                team="blue",
                passed=False,
                detail="telemetry_dir missing — set TPS/inventory telemetry_dir for C1 schema gates",
                score=0.0,
            )
        )

    score = min(100.0, sum(c.score for c in checks))
    # If only C2 ran, scale
    if not (tdir and tdir.exists()) and any(c.id.startswith("c2.") for c in checks):
        c2 = sum(c.score for c in checks if c.id.startswith("c2.") or c.id.startswith("red."))
        score = min(100.0, c2 * (100.0 / 52.0))

    # When telemetry_dir is present but no STIX/OTel/ECS schema evidence exists,
    # do not let C2 fuzz-survival alone claim an excellent Module C score.
    if tdir and tdir.exists():
        schema_ok = any(
            c.id in {"c1.stix_2_1", "c1.otel_or_ecs"} and c.passed for c in checks
        )
        if not schema_ok:
            score = min(score, 55.0)

    return ModuleResult(
        module="C",
        dimension="telemetry",
        score=round(score, 2),
        status=pass_status(score),
        checks=checks,
        notes=["UHBS C1 schema: STIX 2.1 / OTel / ECS best-effort validators"],
    )


def main() -> int:
    p = argparse.ArgumentParser(description="UHBS Module C: Telemetry Quality")
    p.add_argument("--target", default="")
    p.add_argument("--port", type=int, default=2222)
    p.add_argument("--user", default="root")
    p.add_argument("--password", default="root")
    p.add_argument("--telemetry-dir", default=None)
    args = p.parse_args()
    t = TargetSpec(
        name=args.target or "telemetry-only",
        kind="generic",
        host=args.target or None,
        port=args.port,
        user=args.user,
        password=args.password,
        telemetry_dir=args.telemetry_dir,
        protocol="ssh",
        protocols=["ssh"],
        ports_map={"ssh": args.port},
    )
    result = run(t)
    print(f"Module C telemetry score={result.score} status={result.status}")
    for c in result.checks:
        print(f"  [{c.team}] {c.id}: {'PASS' if c.passed else 'FAIL'} — {c.detail}")
    return 0 if result.status != "FAILED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
