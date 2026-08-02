# Golden-baseline CI — today vs. intended end state

> Companion to [`.github/workflows/golden-baseline.yml`](https://github.com/uhbs/uhbs-standard/blob/main/.github/workflows/golden-baseline.yml)
> and [`docs/architecture/plugin-contracts.md`](plugin-contracts.md).

## Intended end state (aspirational — not implemented today)

A protocol plugin should be required to score **100/100** (or some
explicitly documented near-100 floor) when run against a **genuine,
standards-compliant reference implementation** of its own protocol — a real
Redis server, a real Samba daemon, a real OpenSSH server, etc. — not a
honeypot. If a plugin can't recognize ground truth, its scores against
honeypots are not trustworthy either. Reaching this bar for every plugin,
enforced as a **required, blocking** CI check, is the goal.

## Actual state today

- [`tests/test_plugin_baseline_live.py`](https://github.com/uhbs/uhbs-standard/blob/main/tests/test_plugin_baseline_live.py)
  implements this pattern for exactly **two** of 17+ built-in plugins today
  (`redis.py` against `redis:7-alpine`, `smb.py` against `dperson/samba`) —
  see that file's module docstring for the honest, up-to-date coverage list
  and explicit list of protocols with **no** live baseline yet.
- [`.github/workflows/golden-baseline.yml`](https://github.com/uhbs/uhbs-standard/blob/main/.github/workflows/golden-baseline.yml)
  runs those tests in CI with `RUN_LIVE_BASELINE=1`, but as an
  **informational, non-blocking** job (`continue-on-error: true`). A
  failure here is currently a *signal to investigate*, not a merge blocker.
- This workflow was added in the same work session as the test file it
  runs, so it has **zero production run history** as of this writing.
  There is no basis yet to trust it as a required check.

## Why it isn't blocking yet

1. `tests/test_plugin_baseline_live.py` spins up real Docker containers on
   the runner (image pulls, port binding, readiness polling). That kind of
   test is inherently more flaky than a pure-Python unit test until it has
   a track record on hosted CI infrastructure specifically (not just a
   local dev machine).
2. Making a brand-new, never-run-in-CI test suite a required check on day
   one risks blocking unrelated PRs on infrastructure noise rather than
   real protocol regressions — which would erode trust in CI faster than
   just leaving it informational for now.

## Path to blocking

Once `golden-baseline.yml` has run green (or with clearly-understood,
non-flaky failures) across several consecutive `main`-branch runs:

1. Remove `continue-on-error: true` from the job (or set it to `false`).
2. Add the job as a required status check in branch protection.
3. Expand `tests/test_plugin_baseline_live.py` coverage toward the other
   15 plugins, one protocol at a time, each backed by an official
   (non-honeypot) reference image.
4. Only then update this document and the workflow's comments to describe
   the check as enforcing "100/100 against a real reference daemon or the
   build fails" — not before.

**Do not** describe the current workflow as already enforcing that bar in
any other doc, README, or marketing copy. As of this writing it does not.
