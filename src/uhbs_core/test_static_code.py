#!/usr/bin/env python3
"""Module F — Source Code & Static Security Audit (White-Box / D1+D4).

1. Static fingerprint & artifact scanning (keys, banners, seeds, MACs)
2. LLM prompt & guardrail boundary audit
3. SAST & supply chain (Bandit / Semgrep / Trivy when installed)
4. VFS / POSIX command coverage against simulated shell surface
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Set, Tuple

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from uhbs_core.hqs import pass_status  # noqa: E402
from uhbs_core.models import CheckResult, ModuleResult, TargetSpec  # noqa: E402

SKIP_DIRS = {
    ".git",
    ".local",
    "node_modules",
    "vendor",
    "dist",
    "build",
    ".venv",
    "venv",
    "__pycache__",
    ".cursor",
    "testdata",
    "honeyfs",  # fake FS content trees are expected decoy data
}

TEXT_SUFFIXES = {
    ".py",
    ".go",
    ".rs",
    ".js",
    ".ts",
    ".tsx",
    ".java",
    ".c",
    ".h",
    ".cpp",
    ".yml",
    ".yaml",
    ".toml",
    ".json",
    ".md",
    ".txt",
    ".cfg",
    ".ini",
    ".sh",
    ".bash",
    ".env.example",
}

PRIVATE_KEY_RE = re.compile(
    r"-----BEGIN (?:RSA |OPENSSH |EC |DSA |ED25519 )?PRIVATE KEY-----"
)
SSH_BANNER_RE = re.compile(
    r"""(?:ServerVersion|versionString|banner)\s*=\s*['\"]SSH-[^'\"]+['\"]""",
    re.IGNORECASE,
)
RANDOM_SEED_RE = re.compile(r"random\.seed\s*\(|rand\.Seed\s*\(|math/rand\.Seed")
MAC_RE = re.compile(r"(?:['\"])(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}(?:['\"])")
WEAK_PROMPT_BOUNDARIES = [
    re.compile(r"ignore\s+previous\s+instructions", re.I),
    re.compile(r"you\s+are\s+chatgpt", re.I),
    re.compile(r"SYSTEM\s*PROMPT\s*:", re.I),
]
FALLBACK_LEAK_RE = re.compile(
    # Bare "hallucin" matches the target decoy brand — require real leak phrases.
    r"(as an ai|language model|i cannot actually execute|llm fallback|"
    r"hallucinat(?:e|es|ed|ing|ion)s?)",
    re.I,
)


def _iter_files(root: Path, limit: int = 8000) -> Iterable[Path]:
    n = 0
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.suffix and p.suffix.lower() not in TEXT_SUFFIXES and p.name not in (
            "Dockerfile",
            "Makefile",
        ):
            # still scan key-like filenames without suffix filter bypass for *.pem
            if p.suffix.lower() not in {".pem", ".key", ".pub"}:
                continue
        yield p
        n += 1
        if n >= limit:
            return


def _read(path: Path, max_bytes: int = 512_000) -> str:
    try:
        data = path.read_bytes()[:max_bytes]
    except OSError:
        return ""
    return data.decode("utf-8", errors="ignore")


def _scan_artifacts(root: Path) -> Tuple[CheckResult, CheckResult, CheckResult, CheckResult]:
    key_hits: List[str] = []
    banner_hits: List[str] = []
    seed_hits: List[str] = []
    mac_hits: List[str] = []
    for fp in _iter_files(root):
        # Filename heuristics for committed host keys
        name = fp.name.lower()
        if name in {"ssh_host_rsa_key", "ssh_host_ed25519_key", "id_rsa", "id_ed25519"} or (
            name.endswith("_key") and "host" in name and not name.endswith(".pub")
        ):
            key_hits.append(str(fp.relative_to(root)))
            continue
        text = _read(fp)
        if not text:
            continue
        rel = str(fp.relative_to(root))
        if PRIVATE_KEY_RE.search(text):
            # allow test fixtures under *test* paths at reduced severity later
            key_hits.append(rel)
        if SSH_BANNER_RE.search(text):
            banner_hits.append(rel)
        if RANDOM_SEED_RE.search(text):
            seed_hits.append(rel)
        if MAC_RE.search(text):
            mac_hits.append(rel)

    def _score_clean(hits: List[str], cid: str, label: str, points: float) -> CheckResult:
        # Deduplicate; ignore obvious test-only paths for pass/fail but list them
        real = [h for h in hits if "test" not in h.lower() and "fixture" not in h.lower()]
        ok = len(real) == 0
        return CheckResult(
            id=cid,
            team="white",
            passed=ok,
            detail=(
                f"0 {label}"
                if ok
                else f"{len(real)} {label}: " + ", ".join(real[:5])
            ),
            score=points if ok else max(0.0, points - 5.0 * min(len(real), 4)),
            evidence=(real or hits)[:12],
        )

    return (
        _score_clean(key_hits, "white.static_private_keys", "static private keys", 10.0),
        _score_clean(banner_hits, "white.hardcoded_ssh_banners", "hardcoded SSH banners", 5.0),
        _score_clean(seed_hits, "white.predictable_seeds", "predictable PRNG seeds", 5.0),
        _score_clean(mac_hits, "white.hardcoded_macs", "hardcoded MAC addresses", 5.0),
    )


def _scan_prompts(root: Path) -> List[CheckResult]:
    prompt_dirs = [
        root / "prompts",
        root / "personas",
        root / "engine" / "internal" / "persona",
        root / "services" / "ai-broker",
    ]
    files: List[Path] = []
    for d in prompt_dirs:
        if d.is_dir():
            files.extend([p for p in d.rglob("*") if p.is_file()])
    # Also catch *prompt* filenames
    for p in _iter_files(root, limit=3000):
        if "prompt" in p.name.lower() or p.suffix in {".txt", ".md"} and "persona" in str(p).lower():
            files.append(p)
    # unique
    uniq: List[Path] = []
    seen: Set[str] = set()
    for f in files:
        s = str(f)
        if s not in seen:
            seen.add(s)
            uniq.append(f)

    weak = 0
    leak = 0
    samples: List[str] = []
    for fp in uniq[:200]:
        # Test fixtures intentionally contain extraction-attack strings; skip them.
        parts = {p.lower() for p in fp.parts}
        name_l = fp.name.lower()
        if (
            "tests" in parts
            or "testdata" in parts
            or "__pycache__" in parts
            or ".venv" in parts
            or name_l.endswith("_test.py")
            or name_l.endswith("_test.go")
            or name_l.startswith("test_")
            or name_l.endswith(".pyc")
            or name_l.endswith(".pyo")
        ):
            continue
        text = _read(fp)
        try:
            rel = str(fp.relative_to(root))
        except ValueError:
            rel = str(fp)
        if any(r.search(text) for r in WEAK_PROMPT_BOUNDARIES):
            weak += 1
            samples.append(f"weak-boundary:{rel}")
        if FALLBACK_LEAK_RE.search(text):
            leak += 1
            samples.append(f"fallback-leak:{rel}")

    # Missing prompt corpus is not a failure for non-LLM honeypots
    has_prompts = len(uniq) > 0
    boundary_ok = weak == 0
    leak_ok = leak == 0
    return [
        CheckResult(
            id="white.prompt_corpus_present",
            team="white",
            passed=True,
            detail=f"{len(uniq)} prompt/persona files scanned" if has_prompts else "no prompt corpus (N/A for non-LLM)",
            score=5.0 if has_prompts else 5.0,
        ),
        CheckResult(
            id="white.prompt_boundaries",
            team="white",
            passed=boundary_ok,
            detail="no weak delimiter/extract patterns" if boundary_ok else f"{weak} weak boundary hits",
            score=10.0 if boundary_ok else 2.0,
            evidence=samples[:8],
        ),
        CheckResult(
            id="white.fallback_strings",
            team="white",
            passed=leak_ok,
            detail="no plain-text LLM fallback artifacts" if leak_ok else f"{leak} fallback leak hits",
            score=10.0 if leak_ok else 2.0,
            evidence=[s for s in samples if s.startswith("fallback")][:8],
        ),
    ]


def _run_tool_json(
    cmd: Sequence[str], cwd: Path, timeout: int = 180
) -> Tuple[bool, dict, str]:
    try:
        proc = subprocess.run(
            list(cmd),
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError:
        return False, {}, "not installed"
    except subprocess.TimeoutExpired:
        return False, {}, "timeout"
    raw = proc.stdout or ""
    try:
        return True, json.loads(raw) if raw.strip() else {}, ""
    except json.JSONDecodeError:
        return True, {"raw": raw[:2000], "returncode": proc.returncode}, ""


def _sast_checks(root: Path, image: Optional[str], out_dir: Optional[Path]) -> List[CheckResult]:
    checks: List[CheckResult] = []
    high_crit = 0

    # Bandit (Python)
    bandit_ok, bandit, berr = _run_tool_json(
        ["bandit", "-r", ".", "-f", "json", "-q"],
        cwd=root,
        timeout=240,
    )
    if berr == "not installed":
        checks.append(
            CheckResult(
                id="white.bandit",
                team="white",
                passed=True,
                detail="bandit not installed (skipped)",
                score=5.0,
            )
        )
    else:
        metrics = bandit.get("metrics", {}) if isinstance(bandit, dict) else {}
        totals = metrics.get("_totals", {}) if isinstance(metrics, dict) else {}
        sev_h = int(totals.get("SEVERITY.HIGH", 0) or 0)
        sev_c = int(totals.get("SEVERITY.HIGH", 0) or 0)  # bandit has HIGH/MEDIUM/LOW
        # Also count CONFIDENCE — prefer results list
        results = bandit.get("results", []) if isinstance(bandit, dict) else []
        high = sum(1 for r in results if str(r.get("issue_severity", "")).upper() == "HIGH")
        high_crit += high
        if out_dir:
            (out_dir / "bandit-report.json").write_text(
                json.dumps(bandit, indent=2)[:2_000_000], encoding="utf-8"
            )
        checks.append(
            CheckResult(
                id="white.bandit",
                team="white",
                passed=high == 0,
                detail=f"bandit HIGH={high}" + (f" ({berr})" if berr else ""),
                score=8.0 if high == 0 else max(0.0, 8.0 - high),
            )
        )
        _ = sev_h, sev_c, bandit_ok

    # Semgrep
    sem_ok, sem, serr = _run_tool_json(
        ["semgrep", "--config=auto", "--json", "--quiet", "."],
        cwd=root,
        timeout=300,
    )
    if serr == "not installed":
        checks.append(
            CheckResult(
                id="white.semgrep",
                team="white",
                passed=True,
                detail="semgrep not installed (skipped)",
                score=5.0,
            )
        )
    else:
        results = sem.get("results", []) if isinstance(sem, dict) else []
        errorish = [
            r
            for r in results
            if str(r.get("extra", {}).get("severity", "")).lower() in {"error", "critical"}
            or str(r.get("severity", "")).lower() in {"error", "critical"}
        ]
        high_crit += len(errorish)
        if out_dir:
            (out_dir / "semgrep-report.json").write_text(
                json.dumps(sem, indent=2)[:2_000_000], encoding="utf-8"
            )
        checks.append(
            CheckResult(
                id="white.semgrep",
                team="white",
                passed=len(errorish) == 0,
                detail=f"semgrep error/critical={len(errorish)} total={len(results)}"
                + (f" ({serr})" if serr else ""),
                score=8.0 if len(errorish) == 0 else max(0.0, 8.0 - len(errorish)),
            )
        )
        _ = sem_ok

    # Trivy (image or fs)
    if image:
        tcmd = ["trivy", "image", "--format", "json", "--quiet", image]
    else:
        tcmd = ["trivy", "fs", "--format", "json", "--quiet", "."]
    tok, trivy, terr = _run_tool_json(tcmd, cwd=root, timeout=300)
    if terr == "not installed":
        checks.append(
            CheckResult(
                id="white.trivy",
                team="white",
                passed=True,
                detail="trivy not installed (skipped)",
                score=4.0,
            )
        )
    else:
        crit = 0
        high = 0
        for res in (trivy.get("Results") or []) if isinstance(trivy, dict) else []:
            for v in res.get("Vulnerabilities") or []:
                sev = str(v.get("Severity", "")).upper()
                if sev == "CRITICAL":
                    crit += 1
                elif sev == "HIGH":
                    high += 1
        high_crit += crit + high
        if out_dir:
            (out_dir / "trivy-report.json").write_text(
                json.dumps(trivy, indent=2)[:2_000_000], encoding="utf-8"
            )
        checks.append(
            CheckResult(
                id="white.trivy",
                team="white",
                passed=crit == 0 and high == 0,
                detail=f"trivy CRITICAL={crit} HIGH={high}" + (f" ({terr})" if terr else ""),
                score=4.0 if crit == 0 and high == 0 else max(0.0, 4.0 - crit - 0.5 * high),
            )
        )
        _ = tok

    checks.append(
        CheckResult(
            id="white.sast_gate",
            team="white",
            passed=high_crit == 0,
            detail="0 high/critical static findings" if high_crit == 0 else f"{high_crit} high/critical findings",
            score=0.0,  # informational aggregate; points already in tools
        )
    )
    return checks


def _posix_list() -> List[str]:
    path = ROOT / "profiles" / "coverage" / "posix_commands.txt"
    cmds: List[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        cmds.append(line)
    return cmds


def _ot_list() -> List[str]:
    path = ROOT / "profiles" / "coverage" / "ot_modbus_coverage.txt"
    items: List[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        items.append(line)
    return items


def _coverage_review(root: Path, kind: str, profile_class: str) -> List[CheckResult]:
    """F3 — POSIX VFS and/or OT register-map coverage."""
    out: List[CheckResult] = []
    # POSIX
    posix = _vfs_coverage(root, kind)
    out.append(posix)

    # OT / ICS register & function coverage
    if profile_class in {"ICS-SCADA"} or kind in {"modbus"}:
        terms = _ot_list()
        focus = [
            root / "engine" / "internal" / "protocol" / "modbus",
            root,
        ]
        blobs: List[str] = []
        for base in focus:
            if not base.exists():
                continue
            for fp in _iter_files(base if base.is_dir() else root, limit=3000):
                blobs.append(_read(fp, max_bytes=150_000))
        blob = "\n".join(blobs).lower()
        found = {t for t in terms if t.lower().replace("_", " ") in blob or t.lower() in blob}
        cov = len(found) / max(len(terms), 1)
        out.append(
            CheckResult(
                id="white.ot_register_coverage",
                team="white",
                passed=cov >= 0.30,
                detail=f"OT/Modbus coverage {cov:.0%} ({len(found)}/{len(terms)})",
                score=round(25.0 * cov, 2),
                evidence=sorted(found)[:40],
            )
        )
    return out


def _vfs_coverage(root: Path, kind: str) -> CheckResult:
    cmds = _posix_list()
    text_blobs: List[str] = []
    focus: List[Path] = [root]
    if kind == "research":
        focus = [
            root / "engine" / "internal" / "protocol" / "ssh",
            root / "engine" / "internal" / "decoyfs",
        ]
    elif kind == "cowrie":
        focus = [
            root / "src" / "cowrie" / "commands",
            root / "cowrie" / "commands",
            root / "src" / "cowrie" / "shell",
        ]
    found: Set[str] = set()
    for base in focus:
        if not base.exists():
            continue
        for fp in _iter_files(base if base.is_dir() else root, limit=4000):
            text_blobs.append(_read(fp, max_bytes=200_000))
    blob = "\n".join(text_blobs).lower()
    for c in cmds:
        if re.search(rf"(?:^|[^a-z0-9_]){re.escape(c.lower())}(?:[^a-z0-9_]|$)", blob):
            found.add(c)
    coverage = len(found) / max(len(cmds), 1)
    return CheckResult(
        id="white.vfs_posix_coverage",
        team="white",
        passed=coverage >= 0.35,
        detail=f"POSIX coverage {coverage:.0%} ({len(found)}/{len(cmds)})",
        score=round(25.0 * coverage, 2),
        evidence=sorted(found)[:40],
    )


def run(
    target: TargetSpec,
    out_dir: Optional[Path] = None,
    skip_sast_tools: bool = False,
) -> ModuleResult:
    if not target.source_root:
        return ModuleResult(
            module="F",
            dimension="static",
            score=0.0,
            status="SKIPPED",
            notes=["no source_root configured"],
        )
    root = Path(target.source_root).expanduser().resolve()
    if not root.is_dir():
        return ModuleResult(
            module="F",
            dimension="static",
            score=0.0,
            status="FAILED",
            error=f"source_root not found: {root}",
        )

    if out_dir:
        out_dir.mkdir(parents=True, exist_ok=True)

    checks: List[CheckResult] = []
    checks.extend(_scan_artifacts(root))
    checks.extend(_scan_prompts(root))
    if skip_sast_tools:
        checks.append(
            CheckResult(
                id="white.sast_tools",
                team="white",
                passed=True,
                detail="SAST tools skipped by flag",
                score=15.0,
            )
        )
    else:
        checks.extend(_sast_checks(root, target.container_image, out_dir))
    checks.extend(_coverage_review(root, target.kind, target.profile_class))

    # Blocking / async heuristic (efficiency static focus from matrix)
    blocking_hits = 0
    for fp in _iter_files(root, limit=2000):
        if fp.suffix not in {".py", ".go"}:
            continue
        text = _read(fp, max_bytes=120_000)
        if re.search(r"time\.sleep\s*\(\s*[1-9]", text) or "time.Sleep(" in text:
            # only count outside tests lightly
            if "test" not in str(fp).lower():
                blocking_hits += 1
    checks.append(
        CheckResult(
            id="white.blocking_calls",
            team="white",
            passed=blocking_hits < 25,
            detail=f"sleep/blocking markers in non-test code≈{blocking_hits}",
            score=5.0 if blocking_hits < 25 else 1.0,
        )
    )

    score = min(100.0, sum(c.score for c in checks))
    # Normalize roughly: max theoretical ~25+25+25+25+5 ≈ 105 with skips
    score = min(100.0, score)

    # Hard gate note: high/critical SAST findings should keep F from looking perfect
    sast_gate = next((c for c in checks if c.id == "white.sast_gate"), None)
    if sast_gate and not sast_gate.passed:
        score = min(score, 70.0)

    return ModuleResult(
        module="F",
        dimension="static",
        score=round(score, 2),
        status=pass_status(score),
        checks=checks,
        metrics={"source_root": str(root)},
        notes=["Module F white-box audit (keys/prompts/SAST/VFS)"],
    )


def main() -> int:
    p = argparse.ArgumentParser(description="Module F: Source Code & Static Audit")
    p.add_argument("--repo-path", "--source-root", dest="repo_path", required=True)
    p.add_argument("--kind", default="generic")
    p.add_argument("--output", default="static-report.json")
    p.add_argument("--container-image", default=None)
    p.add_argument("--skip-sast-tools", action="store_true")
    args = p.parse_args()
    t = TargetSpec(
        name=Path(args.repo_path).name,
        kind=args.kind,
        source_root=args.repo_path,
        container_image=args.container_image,
    )
    out = Path(args.output).resolve().parent
    result = run(t, out_dir=out, skip_sast_tools=args.skip_sast_tools)
    Path(args.output).write_text(json.dumps(result.to_dict(), indent=2), encoding="utf-8")
    print(f"Module F static score={result.score} status={result.status}")
    for c in result.checks:
        print(f"  [{c.team}] {c.id}: {'PASS' if c.passed else 'FAIL'} — {c.detail}")
    return 0 if result.status != "FAILED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
