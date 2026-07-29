#!/usr/bin/env python3
"""Calculate UHQS 4.3.0 from report.json or explicit module scores."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from uhbs_core.models import compute_uhqs


def main() -> int:
    p = argparse.ArgumentParser(description="UHQS 4.3.0 composite score")
    p.add_argument("--input", help="report.json with modules[] or scores{}")
    p.add_argument("--output", default="report.json")
    p.add_argument("--protocol", type=float, dest="s_a", help="Module A score")
    p.add_argument("--behavior", type=float, dest="s_b", help="Module B score")
    p.add_argument("--telemetry", type=float, dest="s_c")
    p.add_argument("--containment", type=float, dest="c")
    p.add_argument("--scale", type=float, dest="s_e")
    p.add_argument("--static", type=float, dest="s_f")
    p.add_argument("--class", dest="profile_class", default="POSIX-Shell")
    p.add_argument("--target", default="target")
    args = p.parse_args()

    scores = {}
    payload = {}
    if args.input:
        payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
        if "scores" in payload:
            scores = {k: float(v) for k, v in payload["scores"].items()}
        elif "modules" in payload:
            for m in payload["modules"]:
                if m.get("status") == "SKIPPED":
                    continue
                dim = m.get("dimension")
                if dim:
                    scores[dim] = float(m.get("score", 0))
        if payload.get("uhqs", {}).get("profile_class"):
            args.profile_class = payload["uhqs"]["profile_class"]

    for key, val in (
        ("protocol", args.s_a),
        ("behavior", args.s_b),
        ("telemetry", args.s_c),
        ("containment", args.c),
        ("scale", args.s_e),
        ("static", args.s_f),
    ):
        if val is not None:
            scores[key] = val

    if not scores:
        print("no scores provided", file=sys.stderr)
        return 2

    uhqs = compute_uhqs(scores, target=args.target, profile_class=args.profile_class)
    out = {**payload, "scores": scores, "uhqs": uhqs.to_dict()}
    Path(args.output).write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(
        f"UHQS 4.3.0 = {uhqs.uhqs}  grade={uhqs.grade}  δ_C={uhqs.delta_c}  "
        f"A={uhqs.S_A} B={uhqs.S_B} C_telem={uhqs.S_C} C_gate={uhqs.C} "
        f"E={uhqs.S_E} F={uhqs.S_F} class={uhqs.profile_class}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
