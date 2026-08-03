"""UHBS Advanced Evidence Profile (AEP) — offline analysis only.

This module parses local experiment manifests and trial JSONL, computes
informative metrics (VoD, FSV, DTDR, EER), and renders addenda. It must never
import sockets, HTTP clients, SSH libraries, subprocess, Docker SDKs, protocol
plugins, or uhbs-lab.
"""

from __future__ import annotations

import json
import math
import os
import random
import re
import shutil
import statistics
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from uhbs_cli import __version__

AEP_VERSION = "1.0.0"
UHBS_VERSION = "4.4.3"
ARMS = ("decoy", "reference", "evaluator_control")
FSV_LAYERS = ("network", "protocol", "system", "state")

_FORBIDDEN_ARG_PATTERNS = (
    re.compile(r"^https?://", re.I),
    re.compile(r"^ftp://", re.I),
    re.compile(r"^ssh://", re.I),
    re.compile(r"^s3://", re.I),
    re.compile(r"^gs://", re.I),
    re.compile(r"^\\\\"),  # UNC
)

_FORBIDDEN_FIELD_KEYS = frozenset(
    {
        "host",
        "hostname",
        "port",
        "url",
        "uri",
        "endpoint",
        "target_host",
        "target_port",
        "executable",
        "command",
        "script",
        "hook",
        "callback",
        "container",
        "docker",
        "kubernetes",
        "kubeconfig",
        "api_key",
        "password",
        "private_key",
        "ssh_key",
        "credential",
        "credentials",
        "agent",
        "plugin",
        "subprocess",
    }
)


class AepError(Exception):
    """User-facing AEP validation or analysis error."""


def _schema_dir() -> Path:
    env = os.environ.get("UHBS_SCHEMA_DIR")
    if env:
        return Path(env)
    packaged = Path(__file__).resolve().parent / "schemas"
    if (packaged / "aep-experiment.schema.json").is_file():
        return packaged
    return Path(__file__).resolve().parents[2] / "schemas"


def packaged_data_dir() -> Path:
    """Directory of packaged AEP examples/templates inside uhbs_cli."""
    return Path(__file__).resolve().parent / "data" / "advanced-evidence"


def load_schema(name: str) -> dict[str, Any]:
    path = _schema_dir() / name
    if not path.is_file():
        raise AepError(f"AEP schema not found: {path}")
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def load_yaml(path: Path) -> Any:
    _assert_local_path(path)
    with path.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if data is None:
        raise AepError(f"{path}: empty or null YAML document")
    return data


def load_json(path: Path) -> Any:
    _assert_local_path(path)
    with path.open(encoding="utf-8") as fh:
        data = json.load(fh)
    if data is None:
        raise AepError(f"{path}: JSON null root is not allowed")
    return data


def _assert_local_path(path: Path) -> None:
    text = str(path)
    for pat in _FORBIDDEN_ARG_PATTERNS:
        if pat.search(text):
            raise AepError(
                f"AEP accepts local filesystem paths only; refused remote-looking path: {path}"
            )
    if path.is_absolute() and not path.exists() and "://" in text:
        raise AepError(f"AEP accepts local filesystem paths only: {path}")


def reject_forbidden_cli_values(*values: str | None) -> None:
    """Reject URL / host:port style CLI string values."""
    for value in values:
        if value is None:
            continue
        text = str(value).strip()
        for pat in _FORBIDDEN_ARG_PATTERNS:
            if pat.search(text):
                raise AepError(
                    "AEP commands refuse URL/remote inputs. "
                    "Provide local experiment and trial files only."
                )
        if re.fullmatch(r"[A-Za-z0-9.-]+:\d{1,5}", text):
            raise AepError(
                "AEP commands refuse host:port inputs. "
                "Provide local experiment and trial files only."
            )


def _walk_forbidden_keys(obj: Any, path: str = "") -> list[str]:
    hits: list[str] = []
    if isinstance(obj, dict):
        for key, val in obj.items():
            loc = f"{path}.{key}" if path else str(key)
            if str(key).lower() in _FORBIDDEN_FIELD_KEYS:
                hits.append(loc)
            hits.extend(_walk_forbidden_keys(val, loc))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            hits.extend(_walk_forbidden_keys(item, f"{path}[{i}]"))
    return hits


def validate_schema(data: Any, schema_name: str) -> list[str]:
    schema = load_schema(schema_name)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
    return [
        f"{'.'.join(str(p) for p in err.path) or '(root)'}: {err.message}" for err in errors
    ]


def validate_experiment(data: Any, *, strict: bool = True) -> list[str]:
    if not isinstance(data, dict):
        return ["(root): experiment must be a mapping/object"]
    errors = validate_schema(data, "aep-experiment.schema.json")
    errors.extend(f"forbidden field: {loc}" for loc in _walk_forbidden_keys(data))
    if strict:
        attest = data.get("attestations") or {}
        for key in (
            "sandbox_only",
            "no_production_assets",
            "local_evidence_only",
            "informative_only",
        ):
            if attest.get(key) is not True:
                errors.append(f"attestations.{key}: must be true")
        utility = data.get("utility") or {}
        weights = utility.get("weights") or {}
        if not weights:
            errors.append("utility.weights: required for VoD (explicit utility model)")
        reps = data.get("repetitions") or {}
        if reps.get("minimum_per_arm", 0) > reps.get("planned_per_arm", 0):
            errors.append("repetitions: minimum_per_arm cannot exceed planned_per_arm")
    return errors


def load_trials_jsonl(path: Path) -> list[dict[str, Any]]:
    _assert_local_path(path)
    trials: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, start=1):
            text = line.strip()
            if not text or text.startswith("#"):
                continue
            try:
                obj = json.loads(text)
            except json.JSONDecodeError as exc:
                raise AepError(f"{path}:{lineno}: invalid JSON — {exc}") from exc
            if not isinstance(obj, dict):
                raise AepError(f"{path}:{lineno}: trial must be a JSON object")
            trials.append(obj)
    if not trials:
        raise AepError(f"{path}: no trial objects found (empty JSONL)")
    return trials


def validate_trials(
    trials: list[dict[str, Any]],
    experiment: dict[str, Any] | None = None,
    *,
    strict: bool = True,
) -> list[str]:
    errors: list[str] = []
    seen_ids: set[str] = set()
    exp_id = (experiment or {}).get("experiment_id")
    for idx, trial in enumerate(trials):
        prefix = f"trial[{idx}]"
        schema_errs = validate_schema(trial, "aep-trial.schema.json")
        errors.extend(f"{prefix}.{e}" for e in schema_errs)
        errors.extend(f"{prefix} forbidden field: {loc}" for loc in _walk_forbidden_keys(trial))
        tid = trial.get("trial_id")
        if isinstance(tid, str):
            if tid in seen_ids:
                errors.append(f"{prefix}.trial_id: duplicate {tid}")
            seen_ids.add(tid)
        if exp_id and trial.get("experiment_id") != exp_id:
            errors.append(
                f"{prefix}.experiment_id: {trial.get('experiment_id')!r} "
                f"!= experiment {exp_id!r}"
            )
        started = trial.get("started_at")
        ended = trial.get("ended_at")
        if isinstance(started, str) and isinstance(ended, str):
            try:
                t0 = datetime.fromisoformat(started.replace("Z", "+00:00"))
                t1 = datetime.fromisoformat(ended.replace("Z", "+00:00"))
                if t1 < t0:
                    errors.append(f"{prefix}: ended_at before started_at")
            except ValueError:
                errors.append(f"{prefix}: invalid timestamp")
    if strict and experiment is not None:
        arms_present = {t.get("arm") for t in trials}
        if "decoy" not in arms_present or "reference" not in arms_present:
            errors.append("strict: trials must include both decoy and reference arms")
        min_n = int((experiment.get("repetitions") or {}).get("minimum_per_arm", 1))
        for arm in ("decoy", "reference"):
            n = sum(1 for t in trials if t.get("arm") == arm)
            if n < min_n:
                errors.append(f"strict: arm {arm} has {n} trials; minimum_per_arm={min_n}")
    return errors


def _percentile(sorted_vals: list[float], p: float) -> float | None:
    if not sorted_vals:
        return None
    if len(sorted_vals) == 1:
        return sorted_vals[0]
    k = (len(sorted_vals) - 1) * p
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return sorted_vals[int(k)]
    return sorted_vals[f] * (c - k) + sorted_vals[c] * (k - f)


def bootstrap_ci(
    values: list[float],
    *,
    statistic: Any,
    n_samples: int,
    confidence: float,
    seed: int,
) -> tuple[float | None, float | None]:
    if not values or n_samples <= 0:
        return None, None
    rng = random.Random(seed)
    stats: list[float] = []
    n = len(values)
    for _ in range(n_samples):
        sample = [values[rng.randrange(n)] for _ in range(n)]
        try:
            stats.append(float(statistic(sample)))
        except (statistics.StatisticsError, ZeroDivisionError, ValueError):
            continue
    if not stats:
        return None, None
    stats.sort()
    alpha = 1.0 - confidence
    return _percentile(stats, alpha / 2), _percentile(stats, 1 - alpha / 2)


def kaplan_meier_median(durations: list[float], censored: list[bool]) -> float | None:
    """Estimate median duration with right-censoring via Kaplan–Meier."""
    if not durations:
        return None
    events = sorted(zip(durations, censored, strict=True), key=lambda x: x[0])
    n = len(events)
    survival = 1.0
    at_risk = n
    last_t = 0.0
    for t, is_censored in events:
        if at_risk <= 0:
            break
        if not is_censored:
            survival *= (at_risk - 1) / at_risk
            if survival <= 0.5:
                return float(t)
        at_risk -= 1
        last_t = float(t)
    # Median not reached — return None (inconclusive) rather than optimistic mean
    if survival > 0.5:
        return None
    return last_t


def _arm_durations(
    trials: list[dict[str, Any]], arm: str
) -> tuple[list[float], list[bool]]:
    durs: list[float] = []
    cens: list[bool] = []
    for t in trials:
        if t.get("arm") != arm:
            continue
        durs.append(float(t.get("session_duration_seconds", 0)))
        cens.append(bool(t.get("censored", False)))
    return durs, cens


def compute_dtdr(
    trials: list[dict[str, Any]],
    *,
    bootstrap_samples: int,
    confidence: float,
    seed: int,
) -> dict[str, Any]:
    decoy_d, decoy_c = _arm_durations(trials, "decoy")
    ref_d, ref_c = _arm_durations(trials, "reference")
    details: dict[str, Any] = {
        "decoy_n": len(decoy_d),
        "reference_n": len(ref_d),
        "decoy_censoring_rate": (sum(decoy_c) / len(decoy_c)) if decoy_c else 0.0,
        "reference_censoring_rate": (sum(ref_c) / len(ref_c)) if ref_c else 0.0,
        "estimator": "kaplan_meier_median_ratio",
    }
    if len(decoy_d) < 2 or len(ref_d) < 2:
        return {
            "value": None,
            "unit": "ratio",
            "n": len(decoy_d) + len(ref_d),
            "interval": {"low": None, "high": None, "confidence": confidence},
            "status": "inconclusive",
            "details": details,
            "notes": "Need at least 2 trials per arm for DTDR",
        }

    any_censored = any(decoy_c) or any(ref_c)
    if any_censored:
        decoy_med = kaplan_meier_median(decoy_d, decoy_c)
        ref_med = kaplan_meier_median(ref_d, ref_c)
        details["decoy_median_seconds"] = decoy_med
        details["reference_median_seconds"] = ref_med
        if decoy_med is None or ref_med is None or ref_med == 0:
            return {
                "value": None,
                "unit": "ratio",
                "n": len(decoy_d) + len(ref_d),
                "interval": {"low": None, "high": None, "confidence": confidence},
                "status": "inconclusive",
                "details": details,
                "notes": "Censoring-aware median undefined (survival never crossed 0.5)",
            }
        value = decoy_med / ref_med
    else:
        decoy_med = statistics.median(decoy_d)
        ref_med = statistics.median(ref_d)
        details["decoy_median_seconds"] = decoy_med
        details["reference_median_seconds"] = ref_med
        details["estimator"] = "median_ratio"
        if ref_med == 0:
            return {
                "value": None,
                "unit": "ratio",
                "n": len(decoy_d) + len(ref_d),
                "interval": {"low": None, "high": None, "confidence": confidence},
                "status": "inconclusive",
                "details": details,
                "notes": "Reference median duration is zero",
            }
        value = decoy_med / ref_med

    # Bootstrap on uncensored medians when no censoring; otherwise skip parametric CI
    low = high = None
    if not any_censored:
        rng = random.Random(seed)
        ratios: list[float] = []
        for _ in range(bootstrap_samples):
            d_s = [decoy_d[rng.randrange(len(decoy_d))] for _ in range(len(decoy_d))]
            r_s = [ref_d[rng.randrange(len(ref_d))] for _ in range(len(ref_d))]
            rm = statistics.median(r_s)
            if rm == 0:
                continue
            ratios.append(statistics.median(d_s) / rm)
        ratios.sort()
        if ratios:
            alpha = 1.0 - confidence
            low = _percentile(ratios, alpha / 2)
            high = _percentile(ratios, 1 - alpha / 2)
    else:
        details["interval_note"] = (
            "Bootstrap CI omitted when right-censoring is present; "
            "report KM medians and sample sizes."
        )

    return {
        "value": float(value),
        "unit": "ratio",
        "n": len(decoy_d) + len(ref_d),
        "interval": {"low": low, "high": high, "confidence": confidence},
        "status": "valid",
        "details": details,
        "notes": "DTDR > 1 means longer dwell on decoy than matched reference",
    }


def _unique_capability_count(trial: dict[str, Any]) -> int:
    bags = (
        trial.get("unique_tools") or [],
        trial.get("unique_credentials") or [],
        trial.get("unique_payload_families") or [],
        trial.get("attack_technique_ids") or [],
    )
    return len({str(x) for bag in bags for x in bag})


def compute_eer(
    trials: list[dict[str, Any]],
    experiment: dict[str, Any],
    *,
    bootstrap_samples: int,
    confidence: float,
    seed: int,
) -> dict[str, Any]:
    budget = int((experiment.get("budget") or {}).get("max_unique_capabilities", 1))
    decoy_trials = [t for t in trials if t.get("arm") == "decoy"]
    if len(decoy_trials) < 2:
        return {
            "value": None,
            "unit": "fraction_of_budget",
            "n": len(decoy_trials),
            "interval": {"low": None, "high": None, "confidence": confidence},
            "status": "inconclusive",
            "details": {"budget_max_unique_capabilities": budget},
            "notes": "Need at least 2 decoy trials for EER",
        }
    per_session = [_unique_capability_count(t) for t in decoy_trials]
    fractions = [c / budget for c in per_session]
    mean_frac = statistics.fmean(fractions)
    low, high = bootstrap_ci(
        fractions,
        statistic=statistics.fmean,
        n_samples=bootstrap_samples,
        confidence=confidence,
        seed=seed,
    )
    # Category tallies
    tools: set[str] = set()
    creds: set[str] = set()
    payloads: set[str] = set()
    techniques: set[str] = set()
    for t in decoy_trials:
        tools.update(str(x) for x in (t.get("unique_tools") or []))
        creds.update(str(x) for x in (t.get("unique_credentials") or []))
        payloads.update(str(x) for x in (t.get("unique_payload_families") or []))
        techniques.update(str(x) for x in (t.get("attack_technique_ids") or []))
    return {
        "value": float(mean_frac),
        "unit": "fraction_of_budget",
        "n": len(decoy_trials),
        "interval": {"low": low, "high": high, "confidence": confidence},
        "status": "valid",
        "details": {
            "budget_max_unique_capabilities": budget,
            "mean_unique_capabilities_per_session": statistics.fmean(per_session),
            "category_counts": {
                "tools": len(tools),
                "credentials": len(creds),
                "payload_families": len(payloads),
                "attack_technique_ids": len(techniques),
            },
            "per_session_unique_capabilities": per_session,
        },
        "notes": "EER uses the declared experiment budget; not universal attacker cost",
    }


def _utility_value(trial: dict[str, Any], weights: dict[str, float]) -> float:
    outcomes = trial.get("defender_outcomes") or {}
    costs = trial.get("costs") or {}
    mapping = {
        "prevented_compromise": 1.0 if outcomes.get("prevented_compromise") else 0.0,
        "detection": 1.0 if outcomes.get("detection") else 0.0,
        "intelligence_yield": float(outcomes.get("intelligence_yield") or 0.0),
        "attacker_time_seconds": float(costs.get("attacker_time_seconds") or 0.0),
        "defender_time_seconds": float(costs.get("defender_time_seconds") or 0.0),
        "attacker_token_cost": float(costs.get("attacker_token_cost") or 0.0),
        "defender_infra_cost": float(costs.get("defender_infra_cost") or 0.0),
        "session_duration_seconds": float(trial.get("session_duration_seconds") or 0.0),
        "exchanges": float(trial.get("exchanges") or 0.0),
    }
    total = 0.0
    for key, weight in weights.items():
        if key not in mapping:
            raise AepError(
                f"utility.weights key {key!r} is not an observed trial field. "
                "Declare outcomes/costs in trials or adjust the utility model. "
                "Never substitute UHQS or delta_uhqs for VoD."
            )
        total += float(weight) * mapping[key]
    return total


def compute_vod(
    trials: list[dict[str, Any]],
    experiment: dict[str, Any],
    *,
    bootstrap_samples: int,
    confidence: float,
    seed: int,
) -> dict[str, Any]:
    utility = experiment.get("utility") or {}
    weights = utility.get("weights") or {}
    if not weights:
        return {
            "value": None,
            "unit": "utility_delta",
            "n": 0,
            "interval": {"low": None, "high": None, "confidence": confidence},
            "status": "not_computed",
            "details": {},
            "notes": "Missing utility.weights — refuse VoD (never use delta_uhqs)",
        }
    decoy_u = [_utility_value(t, weights) for t in trials if t.get("arm") == "decoy"]
    ref_u = [_utility_value(t, weights) for t in trials if t.get("arm") == "reference"]
    details = {
        "utility_name": utility.get("name"),
        "formula": utility.get("formula"),
        "weights": weights,
        "mean_u_decoy": statistics.fmean(decoy_u) if decoy_u else None,
        "mean_u_reference": statistics.fmean(ref_u) if ref_u else None,
        "delta_uhqs_forbidden": True,
    }
    if len(decoy_u) < 2 or len(ref_u) < 2:
        return {
            "value": None,
            "unit": "utility_delta",
            "n": len(decoy_u) + len(ref_u),
            "interval": {"low": None, "high": None, "confidence": confidence},
            "status": "inconclusive",
            "details": details,
            "notes": "Need at least 2 trials per arm for VoD",
        }
    value = statistics.fmean(decoy_u) - statistics.fmean(ref_u)
    # Bootstrap difference of means
    rng = random.Random(seed)
    diffs: list[float] = []
    for _ in range(bootstrap_samples):
        d_s = [decoy_u[rng.randrange(len(decoy_u))] for _ in range(len(decoy_u))]
        r_s = [ref_u[rng.randrange(len(ref_u))] for _ in range(len(ref_u))]
        diffs.append(statistics.fmean(d_s) - statistics.fmean(r_s))
    diffs.sort()
    alpha = 1.0 - confidence
    low = _percentile(diffs, alpha / 2) if diffs else None
    high = _percentile(diffs, 1 - alpha / 2) if diffs else None
    return {
        "value": float(value),
        "unit": "utility_delta",
        "n": len(decoy_u) + len(ref_u),
        "interval": {"low": low, "high": high, "confidence": confidence},
        "status": "valid",
        "details": details,
        "notes": "VoD = mean U_D(decoy) - mean U_D(reference); not delta_uhqs",
    }


def compute_fsv(
    trials: list[dict[str, Any]],
    *,
    bootstrap_samples: int,
    confidence: float,
    seed: int,
) -> dict[str, Any]:
    layers: dict[str, Any] = {}
    for layer in FSV_LAYERS:
        rows = [
            t
            for t in trials
            if (t.get("detector") or {}).get("layer") == layer
            and t.get("arm") in ("decoy", "reference")
            and (t.get("detector") or {}).get("predicted_decoy") is not None
            and (t.get("detector") or {}).get("actual_is_decoy") is not None
        ]
        tp = fp = tn = fn = 0
        for t in rows:
            pred = bool(t["detector"]["predicted_decoy"])
            actual = bool(t["detector"]["actual_is_decoy"])
            if pred and actual:
                tp += 1
            elif pred and not actual:
                fp += 1
            elif (not pred) and (not actual):
                tn += 1
            else:
                fn += 1
        n = tp + fp + tn + fn
        if n < 4 or (tp + fn) == 0 or (tn + fp) == 0:
            layers[layer] = {
                "n": n,
                "tp": tp,
                "fp": fp,
                "tn": tn,
                "fn": fn,
                "tpr": None,
                "fpr": None,
                "balanced_accuracy": None,
                "interval_tpr": {"low": None, "high": None, "confidence": confidence},
                "interval_fpr": {"low": None, "high": None, "confidence": confidence},
                "status": "inconclusive" if n else "not_computed",
            }
            continue
        tpr = tp / (tp + fn)
        fpr = fp / (fp + tn)
        bal = 0.5 * (tpr + (tn / (tn + fp)))
        # Bootstrap TPR/FPR by resampling rows
        rng = random.Random(seed + sum(ord(c) for c in layer))
        tprs: list[float] = []
        fprs: list[float] = []
        for _ in range(bootstrap_samples):
            sample = [rows[rng.randrange(len(rows))] for _ in range(len(rows))]
            stp = sfp = stn = sfn = 0
            for t in sample:
                pred = bool(t["detector"]["predicted_decoy"])
                actual = bool(t["detector"]["actual_is_decoy"])
                if pred and actual:
                    stp += 1
                elif pred and not actual:
                    sfp += 1
                elif (not pred) and (not actual):
                    stn += 1
                else:
                    sfn += 1
            if stp + sfn and stn + sfp:
                tprs.append(stp / (stp + sfn))
                fprs.append(sfp / (sfp + stn))
        tprs.sort()
        fprs.sort()
        alpha = 1.0 - confidence
        layers[layer] = {
            "n": n,
            "tp": tp,
            "fp": fp,
            "tn": tn,
            "fn": fn,
            "tpr": tpr,
            "fpr": fpr,
            "balanced_accuracy": bal,
            "interval_tpr": {
                "low": _percentile(tprs, alpha / 2) if tprs else None,
                "high": _percentile(tprs, 1 - alpha / 2) if tprs else None,
                "confidence": confidence,
            },
            "interval_fpr": {
                "low": _percentile(fprs, alpha / 2) if fprs else None,
                "high": _percentile(fprs, 1 - alpha / 2) if fprs else None,
                "confidence": confidence,
            },
            "status": "valid",
        }
    return {
        "layers": layers,
        "global_scalar_emitted": False,
        "notes": "FSV is reported per layer; no global scalar",
    }


@dataclass
class AnalyzeConfig:
    bootstrap_samples: int = 1000
    confidence: float = 0.95
    seed: int = 42
    experiment_path: str | None = None
    trials_path: str | None = None
    scorecard_ref: str | None = None


def _control_status(
    trials: list[dict[str, Any]], experiment: dict[str, Any]
) -> tuple[str, list[str]]:
    warnings: list[str] = []
    controls = [t for t in trials if t.get("arm") == "evaluator_control"]
    primary = experiment.get("primary_outcome")
    needs_control = primary in ("vod", "eer", "fsv")
    if not controls:
        if needs_control:
            warnings.append(
                "evaluator_control arm missing; capability-dependent claims are weakened"
            )
            return "missing", warnings
        return "not_required", warnings
    failed = [t for t in controls if t.get("evaluator_control_passed") is False]
    if failed:
        warnings.append(
            f"evaluator_control failed on {len(failed)}/{len(controls)} trials"
        )
        return "failed", warnings
    unknown = [t for t in controls if "evaluator_control_passed" not in t]
    if unknown:
        warnings.append("evaluator_control trials lack evaluator_control_passed")
        return "missing", warnings
    return "passed", warnings


def analyze(
    experiment: dict[str, Any],
    trials: list[dict[str, Any]],
    *,
    config: AnalyzeConfig | None = None,
) -> dict[str, Any]:
    cfg = config or AnalyzeConfig()
    warnings: list[str] = []
    arms_present = {t.get("arm") for t in trials}
    if "decoy" not in arms_present or "reference" not in arms_present:
        raise AepError("Analysis refused: both decoy and reference arms are required")

    control_status, ctrl_warnings = _control_status(trials, experiment)
    warnings.extend(ctrl_warnings)

    min_n = int((experiment.get("repetitions") or {}).get("minimum_per_arm", 1))
    per_arm: dict[str, dict[str, int]] = {}
    for arm in ARMS:
        arm_trials = [t for t in trials if t.get("arm") == arm]
        cens = sum(1 for t in arm_trials if t.get("censored"))
        per_arm[arm] = {"n": len(arm_trials), "censored": cens}
        if arm in ("decoy", "reference") and len(arm_trials) < min_n:
            warnings.append(f"low sample size for {arm}: n={len(arm_trials)} < {min_n}")

    total = sum(v["n"] for v in per_arm.values())
    cens_total = sum(v["censored"] for v in per_arm.values())
    censoring_rate = (cens_total / total) if total else 0.0
    if censoring_rate >= 0.5:
        warnings.append(f"high censoring rate: {censoring_rate:.2f}")

    bs = cfg.bootstrap_samples
    conf = cfg.confidence
    seed = cfg.seed

    metrics: dict[str, Any] = {
        "vod": compute_vod(
            trials, experiment, bootstrap_samples=bs, confidence=conf, seed=seed
        ),
        "dtdr": compute_dtdr(
            trials, bootstrap_samples=bs, confidence=conf, seed=seed + 1
        ),
        "eer": compute_eer(
            trials, experiment, bootstrap_samples=bs, confidence=conf, seed=seed + 2
        ),
        "fsv": compute_fsv(
            trials, bootstrap_samples=bs, confidence=conf, seed=seed + 3
        ),
    }

    if control_status == "failed":
        status = "control_failed"
        for key in ("vod", "dtdr", "eer"):
            if metrics[key].get("status") == "valid":
                metrics[key]["status"] = "control_failed"
        for layer in metrics["fsv"]["layers"].values():
            if layer.get("status") == "valid":
                layer["status"] = "control_failed"
    else:
        primary = experiment.get("primary_outcome", "dtdr")
        primary_status = "valid"
        if primary == "fsv":
            layer_statuses = [
                layer.get("status") for layer in metrics["fsv"]["layers"].values()
            ]
            if any(s == "valid" for s in layer_statuses):
                primary_status = "valid"
            elif any(s == "inconclusive" for s in layer_statuses):
                primary_status = "inconclusive"
            else:
                primary_status = "not_computed"
        else:
            primary_status = metrics.get(primary, {}).get("status", "inconclusive")
        status = "valid" if primary_status == "valid" else "inconclusive"
        if primary_status == "not_computed":
            status = "inconclusive"
            warnings.append(f"primary outcome {primary} was not computed")

    if per_arm["decoy"]["n"] < 5 or per_arm["reference"]["n"] < 5:
        warnings.append("n < 5 per arm — treat results as exploratory")

    # Only record scorecard_ref when the CLI validated it via --scorecard.
    # Do not promote an unverified experiment.scorecard_ref into provenance.
    scorecard_ref = cfg.scorecard_ref
    declared_ref = experiment.get("scorecard_ref")
    if scorecard_ref is None and declared_ref:
        warnings.append(
            "experiment.scorecard_ref is declared but was not validated; "
            "pass --scorecard <path> to link and verify the scorecard JSON"
        )

    interpretation = (
        "AEP evidence observed under the declared controlled conditions. "
        "This addendum does not change UHQS, δ_C, or letter grade."
    )
    limitations = [
        "Informative research metrics only — not a UHBS grade or certification.",
        "Results apply to the declared task, budget, timeout, and evaluator tier.",
        "Never equate delta_uhqs with Value of Deception (VoD).",
    ]

    result = {
        "aep_version": AEP_VERSION,
        "uhbs_version": UHBS_VERSION,
        "experiment_id": experiment["experiment_id"],
        "status": status,
        "control_status": control_status,
        "metrics": metrics,
        "sample": {
            "per_arm": per_arm,
            "censoring_rate": censoring_rate,
            "exclusions": [],
        },
        "provenance": {
            "tool": "uhbs aep",
            "tool_version": __version__,
            "analysis_seed": seed,
            "generated_at": datetime.now(UTC)
            .replace(microsecond=0)
            .isoformat()
            .replace("+00:00", "Z"),
            "experiment_path": cfg.experiment_path,
            "trials_path": cfg.trials_path,
            "scorecard_ref": scorecard_ref,
            "bootstrap_samples": bs,
            "confidence": conf,
        },
        "uhqs_unchanged": True,
        "interpretation": interpretation,
        "limitations": limitations,
        "warnings": warnings,
    }
    return result


def render_markdown(evidence: dict[str, Any], *, include_methodology: bool = True) -> str:
    lines = [
        "# Advanced Evidence Addendum",
        "",
        "> **Informative only · lab / sandbox evidence.** This document does "
        "**not** change UHQS, δ_C, weights, or letter grade. Status values are "
        "`valid | inconclusive | control_failed` — not pass/fail grades. "
        "UHBS/AEP are laboratory evaluation tools — not real-world production testing.",
        "",
        f"- Experiment ID: `{evidence.get('experiment_id')}`",
        f"- AEP status: **{evidence.get('status')}**",
        f"- Control status: **{evidence.get('control_status')}**",
        f"- UHQS unchanged: **{evidence.get('uhqs_unchanged')}**",
        "",
    ]
    if include_methodology:
        lines += [
            "## Methodology (summary)",
            "",
            "Three-arm controlled **lab** design (decoy, matched lab reference, "
            "optional evaluator control). Metrics use local trial evidence only. "
            "Bootstrap intervals use the declared analysis seed.",
            "",
            "## Academic credit",
            "",
            "AEP design vocabulary draws on Zhu (2019) DOI 10.1145/3314058.3314067; "
            "Collins, Xu & Brown (2024) arXiv:2401.13815; Ersok et al. (2022) "
            "DOI 10.1109/ICCC202255925.2022.9922853; Li et al. (2020) "
            "DOI 10.1109/OJCS.2020.3030825. Citation does not imply endorsement. "
            "See UHBS docs: advanced-evidence/research-foundations.",
            "",
        ]
    lines += ["## Metrics", ""]
    metrics = evidence.get("metrics") or {}
    for name in ("vod", "dtdr", "eer"):
        block = metrics.get(name) or {}
        lines.append(f"### {name.upper()}")
        lines.append("")
        lines.append(f"- Value: `{block.get('value')}` {block.get('unit', '')}")
        lines.append(f"- Status: `{block.get('status')}`")
        lines.append(f"- n: `{block.get('n')}`")
        interval = block.get("interval") or {}
        lines.append(
            f"- Interval ({interval.get('confidence')}): "
            f"[{interval.get('low')}, {interval.get('high')}]"
        )
        if block.get("notes"):
            lines.append(f"- Notes: {block['notes']}")
        lines.append("")
    fsv = metrics.get("fsv") or {}
    lines += ["### FSV (per layer)", ""]
    for layer, block in (fsv.get("layers") or {}).items():
        lines.append(
            f"- **{layer}**: TPR=`{block.get('tpr')}` FPR=`{block.get('fpr')}` "
            f"bal_acc=`{block.get('balanced_accuracy')}` "
            f"status=`{block.get('status')}` n=`{block.get('n')}`"
        )
    lines += ["", "## Sample", ""]
    sample = evidence.get("sample") or {}
    for arm, counts in (sample.get("per_arm") or {}).items():
        lines.append(f"- {arm}: n={counts.get('n')} censored={counts.get('censored')}")
    lines.append(f"- Censoring rate: {sample.get('censoring_rate')}")
    lines += ["", "## Warnings", ""]
    warnings = evidence.get("warnings") or []
    if warnings:
        for w in warnings:
            lines.append(f"- {w}")
    else:
        lines.append("- (none)")
    lines += [
        "",
        "## Interpretation",
        "",
        evidence.get("interpretation")
        or "AEP evidence observed under the declared controlled conditions.",
        "",
        "## Limitations",
        "",
    ]
    for lim in evidence.get("limitations") or []:
        lines.append(f"- {lim}")
    lines += [
        "",
        "## Provenance",
        "",
        f"- Tool: `{((evidence.get('provenance') or {}).get('tool'))}` "
        f"{((evidence.get('provenance') or {}).get('tool_version'))}",
        f"- Analysis seed: `{(evidence.get('provenance') or {}).get('analysis_seed')}`",
        f"- Scorecard ref: `{(evidence.get('provenance') or {}).get('scorecard_ref')}`",
        "",
    ]
    return "\n".join(lines) + "\n"


def default_experiment_template(
    *,
    name: str,
    profile_class: str,
    trials: int,
    seed: int,
) -> dict[str, Any]:
    exp_id = re.sub(r"[^A-Za-z0-9._:-]+", "-", name.strip())[:64] or "aep-experiment"
    return {
        "aep_version": AEP_VERSION,
        "uhbs_version": UHBS_VERSION,
        "experiment_id": exp_id,
        "name": name,
        "hypothesis": (
            "Under matched task/budget/timeout, the decoy changes dwell time "
            "and/or defender utility relative to a matched reference."
        ),
        "primary_outcome": "dtdr",
        "secondary_outcomes": ["vod", "eer", "fsv"],
        "profile_class": profile_class,
        "arms": {
            "decoy": {"name": "decoy-under-test", "version": "0.0.0", "digest": ""},
            "reference": {
                "name": "matched-reference",
                "version": "0.0.0",
                "digest": "",
            },
            "evaluator_control": {
                "name": "capability-check",
                "version": "0.0.0",
                "digest": "",
            },
        },
        "attacker_capability_tier": "scripted",
        "task": {
            "description": "Complete the declared recon/exploitation task.",
            "starting_knowledge": "Shared starter brief for all arms.",
            "success_criteria": "Task completion or timeout.",
        },
        "budget": {
            "max_attempts": 20,
            "max_unique_capabilities": 10,
            "currency_unit": "USD",
        },
        "timeout_seconds": 600,
        "randomization": {
            "method": "shuffled_blocks",
            "seed": seed,
            "notes": "Declare the seed used when assigning trial order.",
        },
        "repetitions": {
            "planned_per_arm": trials,
            # Keep minimum ≤ planned so `uhbs aep init --trials N` is immediately valid.
            "minimum_per_arm": max(1, min(trials, 5)),
        },
        "utility": {
            "name": "simple-defender-utility",
            "formula": (
                "U_D = w_detection*detection + w_intel*intelligence_yield "
                "- w_def_cost*defender_infra_cost"
            ),
            "weights": {
                "detection": 1.0,
                "intelligence_yield": 0.5,
                "defender_infra_cost": -0.1,
            },
            "notes": "Replace with study-specific utilities. Never use UHQS.",
        },
        "ethics": {
            "human_subjects": False,
            "consent_attested": False,
            "privacy_minimization": "Use subject pseudonyms only.",
        },
        "attestations": {
            "sandbox_only": True,
            "no_production_assets": True,
            "local_evidence_only": True,
            "informative_only": True,
            "notes": "AEP analyzes local files only; it never launches attacks.",
        },
        "notes": "Fill digests and versions before publishing results.",
    }


def example_trial_line(
    *,
    experiment_id: str,
    trial_id: str,
    arm: str,
    duration: float,
    censored: bool = False,
) -> dict[str, Any]:
    row: dict[str, Any] = {
        "aep_version": AEP_VERSION,
        "experiment_id": experiment_id,
        "trial_id": trial_id,
        "subject_pseudonym": "synth-01",
        "arm": arm,
        "started_at": "2026-01-01T00:00:00Z",
        "ended_at": "2026-01-01T00:10:00Z",
        "censored": censored,
        "session_duration_seconds": duration,
        "exchanges": 5,
        "attempts": 3,
        "unique_tools": ["nmap"],
        "unique_credentials": [],
        "unique_payload_families": [],
        "attack_technique_ids": ["T1595"],
        "detector": {
            "layer": "protocol",
            "predicted_decoy": arm == "decoy",
            "actual_is_decoy": arm == "decoy",
            "confidence": 0.8,
        },
        "defender_outcomes": {
            "prevented_compromise": True,
            "detection": True,
            "intelligence_yield": 1.0,
        },
        "costs": {
            "attacker_time_seconds": duration,
            "defender_time_seconds": 30,
            "attacker_token_cost": 0,
            "defender_infra_cost": 1.0,
            "currency_unit": "USD",
        },
        "raw_evidence_sha256": "0" * 64,
        "notes": "Template row — replace with measured values.",
    }
    if arm == "evaluator_control":
        row["evaluator_control_passed"] = True
    return row


def write_init_bundle(
    out_dir: Path,
    *,
    name: str,
    profile_class: str,
    trials: int,
    seed: int,
    force: bool = False,
) -> dict[str, Path]:
    out_dir = Path(out_dir)
    exp_path = out_dir / "experiment.yaml"
    trials_path = out_dir / "trials.jsonl"
    readme = out_dir / "README.md"
    if not force and (exp_path.exists() or trials_path.exists()):
        raise AepError(
            f"Refusing to overwrite existing AEP files in {out_dir}. "
            "Pass force=True / --force to replace them."
        )
    out_dir.mkdir(parents=True, exist_ok=True)
    experiment = default_experiment_template(
        name=name, profile_class=profile_class, trials=trials, seed=seed
    )
    with exp_path.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(experiment, fh, sort_keys=False, allow_unicode=True)

    trial_rows: list[dict[str, Any]] = []
    exp_id = experiment["experiment_id"]
    for arm in ("decoy", "reference", "evaluator_control"):
        for i in range(trials):
            row = example_trial_line(
                experiment_id=exp_id,
                trial_id=f"{arm}-{i+1:03d}",
                arm=arm,
                duration=120.0 if arm == "decoy" else 60.0,
                censored=False,
            )
            if arm != "evaluator_control":
                row.pop("evaluator_control_passed", None)
            trial_rows.append(row)
    with trials_path.open("w", encoding="utf-8") as fh:
        for row in trial_rows:
            fh.write(json.dumps(row, separators=(",", ":")) + "\n")

    readme.write_text(
        "# AEP experiment bundle\n\n"
        "Offline Advanced Evidence Profile inputs. Fill digests/versions, "
        "replace synthetic trial rows with measured local evidence, then run:\n\n"
        "```bash\n"
        "uhbs aep validate experiment.yaml\n"
        "uhbs aep validate-trials trials.jsonl --experiment experiment.yaml\n"
        "uhbs aep analyze --experiment experiment.yaml --trials trials.jsonl "
        "--out advanced-evidence.json\n"
        "uhbs aep report advanced-evidence.json --format markdown "
        "--out ADVANCED-EVIDENCE.md\n"
        "```\n\n"
        "AEP never launches attacks and never changes UHQS.\n",
        encoding="utf-8",
    )
    return {"experiment": exp_path, "trials": trials_path, "readme": readme}


EXAMPLE_BUNDLES = ("beginner", "advanced", "template")


def export_example_bundle(
    name: str,
    out_dir: Path,
    *,
    force: bool = False,
) -> Path:
    """Copy a packaged AEP example/template bundle to a local directory."""
    if name not in EXAMPLE_BUNDLES:
        raise AepError(
            f"Unknown AEP example {name!r}. Choose one of: {', '.join(EXAMPLE_BUNDLES)}"
        )
    src = packaged_data_dir() / name
    if not src.is_dir():
        raise AepError(
            f"Packaged AEP example missing from install: {src}. "
            "Reinstall uhbs[aep] or use a git checkout."
        )
    out_dir = Path(out_dir)
    marker = out_dir / "experiment.yaml"
    if out_dir.exists() and any(out_dir.iterdir()) and not force:
        if marker.exists() or (out_dir / "trials.jsonl").exists():
            raise AepError(
                f"Refusing to overwrite existing files in {out_dir}. Use --force."
            )
        raise AepError(
            f"Output directory {out_dir} is not empty. Choose an empty path or use --force."
        )
    out_dir.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        dest = out_dir / item.name
        if item.is_dir():
            if dest.exists() and force:
                shutil.rmtree(dest)
            shutil.copytree(item, dest, dirs_exist_ok=force)
        else:
            if dest.exists() and not force:
                raise AepError(f"Refusing to overwrite {dest}. Use --force.")
            shutil.copy2(item, dest)
    return out_dir
