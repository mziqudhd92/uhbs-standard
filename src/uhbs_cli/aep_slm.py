"""UHBS AEP Small Language Model evaluator (alpha) — opt-in only.

Generates local AEP trial JSONL from an explicitly unlocked config. Disabled by
default: templates ship with ``enabled: false`` and incomplete activation
attestations. Does not change UHQS.

Trust boundary:
- No honeypot / production probing
- No tool/function calling
- openai_compatible uses loopback-only HTTP, no redirects, size-capped reads
- Default / packaged configs never run model calls until the user edits files
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import random
import re
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import yaml

from uhbs_cli import __version__
from uhbs_cli import aep as aep_mod

AEP_SLM_VERSION = "0.1.0-alpha"
UNLOCK_PHRASE = "I_ENABLE_AEP_SLM_ALPHA"
SCHEMA_NAME = "aep-slm.schema.json"
MAX_MODEL_RESPONSE_BYTES = 256 * 1024

_LOOPBACK_HOSTS = frozenset({"127.0.0.1", "localhost", "::1"})


class AepSlmError(Exception):
    """User-facing AEP SLM configuration or generation error."""


def default_config_template(
    *,
    experiment_path: str = "experiment.yaml",
    output_trials: str = "slm-trials.jsonl",
    output_run: str = "slm-run.json",
) -> dict[str, Any]:
    """Return a **disabled** alpha config. User must edit the file to activate."""
    return {
        "aep_slm_version": AEP_SLM_VERSION,
        "status": "alpha",
        "enabled": False,
        "activation": {
            "unlock_phrase": "CHANGE_ME_SEE_DOCS",
            "acknowledge_alpha": False,
            "lab_sandbox_only": False,
            "no_production_targets": False,
            "no_uhqs_scoring_impact": False,
            "allow_local_model_calls": False,
        },
        "provider": "mock",
        "model": {
            "name": "uhbs-mock-slm",
            "notes": "Deterministic offline mock. Replace only after unlocking.",
        },
        "task": {
            "prompt_id": "aep-slm-alpha-v1",
            "system_prompt": (
                "You are a lab-only honeypot engagement evaluator. "
                "Reply with a single JSON object describing a synthetic trial "
                "outcome. Never suggest contacting production systems."
            ),
            "user_prompt_template": (
                "Arm={arm} trial_index={trial_index} seed={seed}. "
                "Return JSON with keys: session_duration_seconds, exchanges, "
                "attempts, predicted_decoy (bool), confidence (0-1), "
                "evaluator_control_passed (bool)."
            ),
        },
        "generation": {
            "trials_per_arm": 5,
            "seed": 42,
            "temperature": 0.0,
            "max_tokens": 256,
            "arms": ["decoy", "reference", "evaluator_control"],
        },
        "paths": {
            "experiment": experiment_path,
            "output_trials": output_trials,
            "output_run": output_run,
        },
        "safety": {
            "loopback_only": True,
            "forbid_tools": True,
            "forbid_network_targets": True,
            "write_local_files_only": True,
        },
        "notes": (
            "ALPHA / DISABLED BY DEFAULT. To activate, edit this file: set "
            f"enabled=true, unlock_phrase={UNLOCK_PHRASE!r}, and every "
            "activation.* boolean to true (for openai_compatible also set "
            "allow_local_model_calls=true). Then: uhbs aep slm validate && "
            "uhbs aep slm generate. Does not change UHQS."
        ),
    }


def activation_blockers(config: dict[str, Any]) -> list[str]:
    """Return human-readable reasons generation is blocked (empty if unlocked)."""
    blockers: list[str] = []
    if config.get("enabled") is not True:
        blockers.append("enabled is not true (edit config: enabled: true)")
    act = config.get("activation") or {}
    if act.get("unlock_phrase") != UNLOCK_PHRASE:
        blockers.append(
            f"activation.unlock_phrase must be exactly {UNLOCK_PHRASE!r}"
        )
    for key in (
        "acknowledge_alpha",
        "lab_sandbox_only",
        "no_production_targets",
        "no_uhqs_scoring_impact",
    ):
        if act.get(key) is not True:
            blockers.append(f"activation.{key} must be true")
    provider = config.get("provider")
    # Offline recorded/mock do not need model-call attestation.
    if provider == "openai_compatible" and act.get("allow_local_model_calls") is not True:
        blockers.append(
            "activation.allow_local_model_calls must be true for "
            "provider='openai_compatible'"
        )
    return blockers


def validate_config(config: Any, *, require_unlocked: bool = False) -> list[str]:
    """Schema + safety checks. Optionally require full activation."""
    if not isinstance(config, dict):
        return ["(root): config must be a mapping/object"]
    errors = aep_mod.validate_schema(config, SCHEMA_NAME)
    safety = config.get("safety") or {}
    for key in (
        "loopback_only",
        "forbid_tools",
        "forbid_network_targets",
        "write_local_files_only",
    ):
        if safety.get(key) is not True:
            errors.append(f"safety.{key}: must be true (const)")
    provider = config.get("provider")
    if provider == "openai_compatible":
        endpoint = config.get("endpoint") or {}
        base = endpoint.get("base_url")
        if not base:
            errors.append("endpoint.base_url: required for openai_compatible")
        else:
            try:
                _assert_loopback_url(str(base))
            except AepSlmError as exc:
                errors.append(str(exc))
    if provider == "recorded" and not config.get("recorded_responses_path"):
        errors.append("recorded_responses_path: required for provider=recorded")
    if require_unlocked:
        errors.extend(activation_blockers(config))
    return errors


def load_config(path: Path) -> dict[str, Any]:
    aep_mod.reject_forbidden_cli_values(str(path))
    data = aep_mod.load_yaml(path)
    if not isinstance(data, dict):
        raise AepSlmError(f"{path}: config must be a YAML mapping")
    return data


def write_init_config(
    out_path: Path,
    *,
    force: bool = False,
    experiment_path: str = "experiment.yaml",
) -> Path:
    """Write a disabled-by-default alpha SLM config file."""
    aep_mod.reject_forbidden_cli_values(str(out_path), experiment_path)
    out_path = Path(out_path)
    if out_path.exists() and not force:
        raise AepSlmError(
            f"Refusing to overwrite {out_path}. Pass --force to replace it."
        )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cfg = default_config_template(experiment_path=experiment_path)
    with out_path.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(cfg, fh, sort_keys=False, allow_unicode=True)
    return out_path


def _assert_loopback_url(url: str) -> None:
    from urllib.parse import urlparse

    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise AepSlmError(
            f"endpoint.base_url: only http/https loopback URLs allowed, got {url!r}"
        )
    host = (parsed.hostname or "").lower()
    if host not in _LOOPBACK_HOSTS:
        raise AepSlmError(
            f"endpoint.base_url: host must be loopback "
            f"(127.0.0.1 / localhost / ::1), got {host!r}"
        )


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _as_bool(value: Any, *, field: str) -> bool:
    if isinstance(value, bool):
        return value
    raise AepSlmError(
        f"{field}: expected JSON boolean, got {type(value).__name__} ({value!r})"
    )


def _as_float(value: Any, *, field: str) -> float:
    # bool is a subclass of int — reject explicitly.
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise AepSlmError(
            f"{field}: expected JSON number, got {type(value).__name__} ({value!r})"
        )
    return float(value)


def _as_int(value: Any, *, field: str) -> int:
    if isinstance(value, bool):
        raise AepSlmError(
            f"{field}: expected JSON integer, got boolean ({value!r})"
        )
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    raise AepSlmError(
        f"{field}: expected JSON integer, got {type(value).__name__} ({value!r})"
    )


def _as_str_list(value: Any, *, field: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise AepSlmError(
            f"{field}: expected JSON array of strings, got {type(value).__name__}"
        )
    out: list[str] = []
    for i, item in enumerate(value):
        if not isinstance(item, str):
            raise AepSlmError(
                f"{field}[{i}]: expected string, got {type(item).__name__}"
            )
        out.append(item)
    return out


def _render_user_prompt(template: str, *, arm: str, trial_index: int, seed: int) -> str:
    try:
        return template.format(arm=arm, trial_index=trial_index, seed=seed)
    except (KeyError, ValueError, IndexError) as exc:
        raise AepSlmError(
            "task.user_prompt_template format error "
            f"(allowed placeholders: {{arm}}, {{trial_index}}, {{seed}}): {exc}"
        ) from exc


def _mock_response(
    *, arm: str, trial_index: int, seed: int, temperature: float
) -> dict[str, Any]:
    """Deterministic synthetic model JSON — no network."""
    rng = random.Random(f"{seed}:{arm}:{trial_index}:{temperature}")
    if arm == "decoy":
        duration = 80.0 + rng.random() * 40.0
        exchanges = 4 + rng.randint(0, 4)
        predicted = True
        confidence = 0.55 + rng.random() * 0.35
        control_ok = True
    elif arm == "reference":
        duration = 30.0 + rng.random() * 30.0
        exchanges = 1 + rng.randint(0, 2)
        predicted = False
        confidence = 0.50 + rng.random() * 0.40
        control_ok = True
    else:
        duration = 20.0 + rng.random() * 20.0
        exchanges = 2 + rng.randint(0, 2)
        predicted = False
        confidence = 0.70 + rng.random() * 0.25
        control_ok = True
    return {
        "session_duration_seconds": round(duration, 3),
        "exchanges": exchanges,
        "attempts": max(1, exchanges - 1),
        "predicted_decoy": predicted,
        "confidence": round(confidence, 4),
        "evaluator_control_passed": control_ok,
        "unique_tools": ["shell"] if arm != "reference" else [],
        "unique_credentials": [],
        "unique_payload_families": ["recon"],
    }


def _parse_model_json(text: str) -> dict[str, Any]:
    text = text.strip()
    # Tolerate fenced blocks from local models.
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    if fence:
        text = fence.group(1)
    try:
        obj = json.loads(text)
    except json.JSONDecodeError as exc:
        # Last-resort: find first {...}
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end > start:
            try:
                obj = json.loads(text[start : end + 1])
            except json.JSONDecodeError as exc2:
                raise AepSlmError(f"model response is not JSON: {exc2}") from exc2
        else:
            raise AepSlmError(f"model response is not JSON: {exc}") from exc
    if not isinstance(obj, dict):
        raise AepSlmError("model response JSON root must be an object")
    return obj


def _read_limited(resp: Any, *, max_bytes: int = MAX_MODEL_RESPONSE_BYTES) -> bytes:
    # Prefer Content-Length so we refuse before streaming a multi-MiB body
    # (avoids peer ConnectionResetError races when the client aborts mid-read).
    headers = getattr(resp, "headers", None)
    if headers is not None:
        raw_len = headers.get("Content-Length")
        if raw_len is not None:
            try:
                declared = int(raw_len)
            except (TypeError, ValueError):
                declared = -1
            if declared > max_bytes:
                close = getattr(resp, "close", None)
                if callable(close):
                    with contextlib.suppress(OSError):
                        close()
                raise AepSlmError(
                    f"local model response exceeds {max_bytes} bytes "
                    "(refusing unbounded body)"
                )
    chunks: list[bytes] = []
    total = 0
    while True:
        try:
            chunk = resp.read(65536)
        except (ConnectionResetError, BrokenPipeError, TimeoutError) as exc:
            raise AepSlmError(
                f"local model connection failed while reading body: {exc}"
            ) from exc
        if not chunk:
            break
        total += len(chunk)
        if total > max_bytes:
            raise AepSlmError(
                f"local model response exceeds {max_bytes} bytes "
                "(refusing unbounded body)"
            )
        chunks.append(chunk)
    return b"".join(chunks)


def _build_no_redirect_opener() -> Any:
    """HTTP opener that never follows redirects (SSRF guard)."""
    from urllib.error import HTTPError
    from urllib.request import (
        HTTPDefaultErrorHandler,
        HTTPErrorProcessor,
        HTTPHandler,
        HTTPRedirectHandler,
        HTTPSHandler,
        OpenerDirector,
        ProxyHandler,
        UnknownHandler,
    )

    class _RefuseRedirects(HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
            raise AepSlmError(
                f"refusing HTTP redirect from local model endpoint "
                f"({code} -> {newurl})"
            )

        def http_error_302(self, req, fp, code, msg, headers):  # type: ignore[no-untyped-def]
            location = headers.get("Location", "")
            raise HTTPError(
                req.full_url,
                code,
                f"redirect refused -> {location}",
                headers,
                fp,
            )

        http_error_301 = http_error_302
        http_error_303 = http_error_302
        http_error_307 = http_error_302
        http_error_308 = http_error_302

    opener = OpenerDirector()
    # No ProxyHandler entries that could send loopback traffic elsewhere;
    # empty ProxyHandler disables env proxies for this opener.
    for handler in (
        ProxyHandler({}),
        UnknownHandler(),
        HTTPDefaultErrorHandler(),
        HTTPHandler(),
        HTTPSHandler(),
        HTTPErrorProcessor(),
        _RefuseRedirects(),
    ):
        opener.add_handler(handler)
    return opener


def _call_openai_compatible(
    config: dict[str, Any],
    *,
    system_prompt: str,
    user_prompt: str,
) -> str:
    # Lazy import keeps mock/status/validate free of HTTP stack at module import.
    from urllib.error import HTTPError, URLError
    from urllib.request import Request

    endpoint = config.get("endpoint") or {}
    base = str(endpoint.get("base_url") or "").rstrip("/")
    _assert_loopback_url(base)
    api_path = str(endpoint.get("api_path") or "/v1/chat/completions")
    if not api_path.startswith("/"):
        api_path = "/" + api_path
    if "://" in api_path:
        raise AepSlmError(
            "endpoint.api_path must be a path (e.g. /v1/chat/completions), "
            "not an absolute URL"
        )
    url = base + api_path
    # Re-check final URL host after concatenation.
    _assert_loopback_url(url)
    timeout = float(endpoint.get("timeout_seconds") or 60)
    model_name = (config.get("model") or {}).get("name") or "local-model"
    gen = config.get("generation") or {}
    body = {
        "model": model_name,
        "temperature": float(gen.get("temperature") or 0),
        "max_tokens": int(gen.get("max_tokens") or 256),
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    payload = json.dumps(body).encode("utf-8")
    req = Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    opener = _build_no_redirect_opener()
    try:
        with opener.open(req, timeout=timeout) as resp:
            raw_bytes = _read_limited(resp)
            raw = raw_bytes.decode("utf-8")
    except AepSlmError:
        raise
    except HTTPError as exc:
        # Redirect refusals surface as HTTPError from our handler.
        if 300 <= int(exc.code) < 400:
            location = exc.headers.get("Location", "") if exc.headers else ""
            raise AepSlmError(
                f"refusing HTTP redirect from local model endpoint "
                f"({exc.code} -> {location})"
            ) from exc
        raise AepSlmError(f"local model HTTP error: {exc.code} {exc.reason}") from exc
    except URLError as exc:
        raise AepSlmError(f"local model connection failed: {exc.reason}") from exc
    except TimeoutError as exc:
        raise AepSlmError(f"local model timed out after {timeout}s") from exc
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise AepSlmError(f"local model returned non-JSON: {exc}") from exc
    try:
        return str(data["choices"][0]["message"]["content"])
    except (KeyError, IndexError, TypeError) as exc:
        raise AepSlmError(
            "local model response missing choices[0].message.content"
        ) from exc


def _load_recorded(path: Path) -> list[dict[str, Any]]:
    aep_mod.reject_forbidden_cli_values(str(path))
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, start=1):
            text = line.strip()
            if not text or text.startswith("#"):
                continue
            try:
                obj = json.loads(text)
            except json.JSONDecodeError as exc:
                raise AepSlmError(f"{path}:{lineno}: invalid JSON — {exc}") from exc
            if not isinstance(obj, dict):
                raise AepSlmError(f"{path}:{lineno}: recorded row must be an object")
            rows.append(obj)
    if not rows:
        raise AepSlmError(f"{path}: no recorded responses")
    return rows


def _resolve_response(
    config: dict[str, Any],
    *,
    arm: str,
    trial_index: int,
    recorded: list[dict[str, Any]] | None,
    recorded_cursor: list[int],
) -> tuple[dict[str, Any], str]:
    gen = config.get("generation") or {}
    seed = int(gen.get("seed") or 0)
    temperature = float(gen.get("temperature") or 0)
    task = config.get("task") or {}
    provider = config.get("provider")

    if provider == "mock":
        parsed = _mock_response(
            arm=arm, trial_index=trial_index, seed=seed, temperature=temperature
        )
        raw = json.dumps(parsed, sort_keys=True)
        return parsed, raw

    user_prompt = _render_user_prompt(
        str(task.get("user_prompt_template") or ""),
        arm=arm,
        trial_index=trial_index,
        seed=seed,
    )
    system_prompt = str(task.get("system_prompt") or "")

    if provider == "recorded":
        if recorded is None:
            raise AepSlmError("recorded provider requires recorded_responses_path data")
        idx = recorded_cursor[0]
        if idx >= len(recorded):
            raise AepSlmError(
                "recorded_responses_path exhausted before all trials were filled"
            )
        row = recorded[idx]
        recorded_cursor[0] = idx + 1
        if "content" in row:
            raw = str(row["content"])
            parsed = _parse_model_json(raw)
        elif "response" in row and isinstance(row["response"], dict):
            parsed = row["response"]
            raw = json.dumps(parsed, sort_keys=True)
        else:
            raise AepSlmError(
                "recorded row needs 'content' (string) or 'response' (object)"
            )
        return parsed, raw

    if provider == "openai_compatible":
        raw = _call_openai_compatible(
            config, system_prompt=system_prompt, user_prompt=user_prompt
        )
        return _parse_model_json(raw), raw

    raise AepSlmError(f"unsupported provider: {provider!r}")


def _trial_from_response(
    *,
    experiment_id: str,
    arm: str,
    trial_index: int,
    parsed: dict[str, Any],
    raw: str,
    config: dict[str, Any],
) -> dict[str, Any]:
    gen = config.get("generation") or {}
    model = config.get("model") or {}
    task = config.get("task") or {}
    seed = int(gen.get("seed") or 0)

    if "session_duration_seconds" in parsed:
        duration = _as_float(
            parsed["session_duration_seconds"], field="session_duration_seconds"
        )
    else:
        duration = 60.0
    if duration < 0:
        raise AepSlmError("session_duration_seconds: must be >= 0")

    exchanges = (
        _as_int(parsed["exchanges"], field="exchanges")
        if "exchanges" in parsed
        else 1
    )
    if exchanges < 0:
        raise AepSlmError("exchanges: must be >= 0")

    attempts = (
        _as_int(parsed["attempts"], field="attempts")
        if "attempts" in parsed
        else max(1, exchanges)
    )
    if attempts < 0:
        raise AepSlmError("attempts: must be >= 0")

    predicted = (
        _as_bool(parsed["predicted_decoy"], field="predicted_decoy")
        if "predicted_decoy" in parsed
        else arm == "decoy"
    )

    confidence = (
        _as_float(parsed["confidence"], field="confidence")
        if "confidence" in parsed
        else 0.5
    )
    confidence = max(0.0, min(1.0, confidence))

    control_ok = (
        _as_bool(
            parsed["evaluator_control_passed"], field="evaluator_control_passed"
        )
        if "evaluator_control_passed" in parsed
        else True
    )

    unique_tools = _as_str_list(parsed.get("unique_tools"), field="unique_tools")
    unique_credentials = _as_str_list(
        parsed.get("unique_credentials"), field="unique_credentials"
    )
    if "unique_payload_families" in parsed:
        unique_payload_families = _as_str_list(
            parsed["unique_payload_families"], field="unique_payload_families"
        )
    else:
        unique_payload_families = ["recon"]

    started = datetime.now(UTC).replace(microsecond=0)
    ended = started + timedelta(seconds=duration)
    started_s = started.isoformat().replace("+00:00", "Z")
    ended_s = ended.isoformat().replace("+00:00", "Z")

    actual_is_decoy = arm == "decoy"
    trial_id = f"slm-{arm}-{trial_index:03d}"
    row: dict[str, Any] = {
        "aep_version": aep_mod.AEP_VERSION,
        "trial_id": trial_id,
        "experiment_id": experiment_id,
        "arm": arm,
        "started_at": started_s,
        "ended_at": ended_s,
        "censored": False,
        "session_duration_seconds": duration,
        "exchanges": exchanges,
        "attempts": attempts,
        "unique_tools": unique_tools,
        "unique_credentials": unique_credentials,
        "unique_payload_families": unique_payload_families,
        "detector": {
            "layer": "protocol",
            "predicted_decoy": predicted,
            "actual_is_decoy": actual_is_decoy,
            "confidence": confidence,
        },
        "evaluator": {
            "kind": "slm",
            "status": "alpha",
            "provider": config.get("provider"),
            "model_name": model.get("name"),
            "prompt_id": task.get("prompt_id"),
            "seed": seed,
            "temperature": float(gen.get("temperature") or 0),
            "raw_response_sha256": _sha256_text(raw),
        },
        "raw_evidence_sha256": _sha256_text(raw),
        "notes": "Generated by UHBS AEP SLM alpha (lab/sandbox only; not UHQS).",
    }
    digest = model.get("digest")
    if isinstance(digest, str) and digest:
        row["evaluator"]["model_digest"] = digest
    if arm == "evaluator_control":
        row["evaluator_control_passed"] = control_ok
    return row


def generate_trials(
    config: dict[str, Any],
    *,
    config_path: Path | None = None,
    force: bool = False,
) -> dict[str, Any]:
    """Generate trials + run provenance. Requires full activation."""
    errors = validate_config(config, require_unlocked=True)
    if errors:
        raise AepSlmError(
            "AEP SLM generation blocked (alpha is off until you edit the config):\n"
            + "\n".join(f"  - {e}" for e in errors)
        )

    paths = config.get("paths") or {}
    exp_path = Path(str(paths["experiment"]))
    if config_path is not None and not exp_path.is_absolute():
        exp_path = (config_path.parent / exp_path).resolve()
    trials_out = Path(str(paths["output_trials"]))
    run_out = Path(str(paths["output_run"]))
    if config_path is not None:
        if not trials_out.is_absolute():
            trials_out = (config_path.parent / trials_out).resolve()
        if not run_out.is_absolute():
            run_out = (config_path.parent / run_out).resolve()

    aep_mod.reject_forbidden_cli_values(str(exp_path), str(trials_out), str(run_out))
    for p in (trials_out, run_out):
        if p.exists() and not force:
            raise AepSlmError(
                f"Refusing to overwrite {p}. Pass --force to replace outputs."
            )

    experiment = aep_mod.load_yaml(exp_path)
    exp_errors = aep_mod.validate_experiment(experiment, strict=True)
    if exp_errors:
        raise AepSlmError(
            "experiment.yaml invalid:\n" + "\n".join(f"  - {e}" for e in exp_errors)
        )
    experiment_id = str(experiment["experiment_id"])

    gen = config.get("generation") or {}
    arms = list(gen.get("arms") or ["decoy", "reference", "evaluator_control"])
    trials_per_arm = int(gen["trials_per_arm"])
    recorded: list[dict[str, Any]] | None = None
    recorded_cursor = [0]
    if config.get("provider") == "recorded":
        rec_path = Path(str(config["recorded_responses_path"]))
        if config_path is not None and not rec_path.is_absolute():
            rec_path = (config_path.parent / rec_path).resolve()
        recorded = _load_recorded(rec_path)

    trials: list[dict[str, Any]] = []
    for arm in arms:
        for i in range(1, trials_per_arm + 1):
            parsed, raw = _resolve_response(
                config,
                arm=arm,
                trial_index=i,
                recorded=recorded,
                recorded_cursor=recorded_cursor,
            )
            trials.append(
                _trial_from_response(
                    experiment_id=experiment_id,
                    arm=arm,
                    trial_index=i,
                    parsed=parsed,
                    raw=raw,
                    config=config,
                )
            )

    trial_errors = aep_mod.validate_trials(trials, experiment, strict=True)
    if trial_errors:
        raise AepSlmError(
            "generated trials failed validation:\n"
            + "\n".join(f"  - {e}" for e in trial_errors[:20])
        )

    trials_out.parent.mkdir(parents=True, exist_ok=True)
    with trials_out.open("w", encoding="utf-8") as fh:
        for row in trials:
            fh.write(json.dumps(row, separators=(",", ":")) + "\n")

    run_doc = {
        "aep_slm_version": AEP_SLM_VERSION,
        "status": "alpha",
        "uhbs_version": __version__,
        "uhqs_unchanged": True,
        "generated_at": datetime.now(UTC)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "config_path": str(config_path) if config_path else None,
        "experiment_path": str(exp_path),
        "trials_path": str(trials_out),
        "provider": config.get("provider"),
        "model": config.get("model"),
        "prompt_id": (config.get("task") or {}).get("prompt_id"),
        "seed": (config.get("generation") or {}).get("seed"),
        "trial_count": len(trials),
        "arms": arms,
        "lab_sandbox_only": True,
        "notes": (
            "Alpha SLM evaluator provenance. Informative AEP input only; "
            "does not change UHQS."
        ),
    }
    run_out.parent.mkdir(parents=True, exist_ok=True)
    run_out.write_text(json.dumps(run_doc, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return {
        "trials_path": trials_out,
        "run_path": run_out,
        "trial_count": len(trials),
        "run": run_doc,
    }


def status_report(config: dict[str, Any]) -> dict[str, Any]:
    schema_errors = validate_config(config, require_unlocked=False)
    blockers = activation_blockers(config)
    return {
        "aep_slm_version": AEP_SLM_VERSION,
        "status": "alpha",
        "schema_ok": not schema_errors,
        "schema_errors": schema_errors,
        "unlocked": not blockers and not schema_errors,
        "activation_blockers": blockers,
        "enabled": config.get("enabled") is True,
        "provider": config.get("provider"),
        "uhqs_unchanged": True,
        "default_activation": False,
    }
