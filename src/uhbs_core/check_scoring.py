"""Shared check-list aggregation for UHBS Module A/B (v4.0.0 architecture fix).

Prior behavior (pre-2026-07-27): a check-list was reduced to a plain
arithmetic mean of scores. This let a single catastrophic failure (score
0.0) sit next to two superficial passes (100.0, 100.0) and net ~33.3 —
diluting a severe protocol/behavioral defect into a passing-looking number.

This module implements the architecture-review remediation:

1. **Circuit breaker.** Any check marked ``critical=True`` (see
   :class:`uhbs_core.models.CheckResult`) that has ``passed=False`` hard-caps
   the aggregate to ``0.0``, regardless of every other check in the list.
   Security gatekeepers — "does the FTP canary reject RETR before auth?",
   "does SMB actually negotiate a real dialect?", "does Modbus really hold
   the value it was told to write?" — MUST be marked critical in the plugin
   so a benchmark cannot average its way past a real failure.

2. **Integrity gate (2026-07-27 code-review follow-up).** Any check whose
   own ``passed`` boolean and ``score`` number *disagree* — per
   :func:`uhbs_core.contract_validation.has_passed_score_disagreement` —
   ALSO hard-caps the aggregate to ``0.0``, exactly like a failed critical
   gate. This closes a real loophole found in this module's own prior
   version: a single-check list with ``passed=True, score=0.0`` (e.g. a
   plugin bug that forgot to set ``score``, which defaults to ``0.0`` on
   ``CheckResult``) used to fall through to the "legacy pass-rate fallback"
   below and silently score ``100.0`` — precisely the "boolean says pass,
   number says fail" bug class the whole review was about, and it bypassed
   even the ``critical=True`` circuit breaker in gate #1 above (that gate
   only ever looks at ``critical and not passed``, never at whether
   ``passed`` and ``score`` actually agree). A check that contradicts
   itself cannot be trusted at all, so — same reasoning as a critical-gate
   failure — the whole list is zeroed rather than silently averaged/
   pass-rated past the contradiction.

3. **Geometric mean, not arithmetic mean, for the remainder.** Geometric
   mean punishes a low outlier far harder than an arithmetic mean does
   (e.g. gmean(0.5, 100, 100) ≈ 17 vs mean(0, 100, 100) ≈ 33), so a single
   weak-but-not-gating check still visibly drags the module score down
   instead of nearly vanishing.

4. **Legacy pass-rate fallback.** If every check in the list has an
   explicit ``score == 0.0`` (i.e. no plugin populated a real score, only
   ``passed``/``failed`` booleans) AND none of them tripped gate #2 above,
   fall back to ``pass_rate * 100``. Note that, by construction, any
   ``passed=True`` check with ``score == 0.0`` always trips gate #2 first
   (0.0 is always below the pass floor) — so this fallback is now only
   reachable when every check in the list is ``passed=False`` with
   ``score == 0.0``, which trivially evaluates to ``0.0`` anyway. It is
   kept (rather than deleted) purely so the formula stays self-documenting
   for that degenerate-but-correct case — no currently-shipped plugin
   exercises a non-zero result from this path, and none should.

``uhbs_core.test_stealth`` (Module A) and ``uhbs_core.test_realism``
(Module B) both delegate to :func:`score_checks` so the math stays in one
place, per the repository's "single source of truth" rule for scoring.
"""

from __future__ import annotations

import math
from collections.abc import Sequence

from uhbs_core.contract_validation import has_passed_score_disagreement
from uhbs_core.models import CheckResult

# Floor used in place of a literal 0.0 before taking log() — keeps a single
# exact-zero score from making the *entire* geometric mean collapse to zero
# via a math domain error, while still contributing an extremely low value.
_LOG_FLOOR = 0.5


def score_checks(checks: Sequence[CheckResult]) -> float:
    """Aggregate a Module A/B check list into one 0-100 score.

    See module docstring for the circuit-breaker + geometric-mean rationale.
    """
    if not checks:
        return 0.0

    # 1) Circuit breaker — a failed critical gate zeroes the whole list.
    if any(c.critical and not c.passed for c in checks):
        return 0.0

    # 2) Integrity gate — a self-contradictory check (passed/score disagree)
    # zeroes the whole list too. See module docstring for why this can't be
    # left to the legacy fallback below.
    if any(has_passed_score_disagreement(c) for c in checks):
        return 0.0

    # 3) Geometric mean over real scores.
    if any(c.score > 0 for c in checks):
        vals = [max(float(c.score), _LOG_FLOOR) for c in checks]
        log_mean = sum(math.log(v) for v in vals) / len(vals)
        return round(min(100.0, math.exp(log_mean)), 4)

    # 4) Legacy fallback — booleans only, no scores populated. Reachable
    # only when every check is passed=False/score=0.0 (see docstring).
    return 100.0 * sum(1 for c in checks if c.passed) / len(checks)
