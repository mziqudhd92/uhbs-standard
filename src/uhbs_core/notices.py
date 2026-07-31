"""Shared operator-facing notices for UHBS tooling."""

from __future__ import annotations

import os
import sys

from uhbs_core.termui import format_notice

LAB_SANDBOX_NOTICE = (
    "UHBS/AEP are for lab/sandbox evaluation of decoys. "
    "Do not run them against production or unauthorized real services."
)

_NOTICE_ENV = "UHBS_LAB_NOTICE_EMITTED"


def reset_lab_sandbox_notice() -> None:
    """Clear the once-per-process guard (for tests)."""
    os.environ.pop(_NOTICE_ENV, None)


def print_lab_sandbox_notice(*, stream: object | None = None, force: bool = False) -> None:
    """Print the lab-only scope notice (stderr by default — keeps stdout clean).

    Emits at most once per process unless ``force=True``, so ``uhbs lab`` (CLI
    wrapper + harness) does not print the banner twice.
    """
    if not force and os.environ.get(_NOTICE_ENV) == "1":
        return
    os.environ[_NOTICE_ENV] = "1"
    out = sys.stderr if stream is None else stream
    print(format_notice(LAB_SANDBOX_NOTICE, stream=out), file=out)  # type: ignore[arg-type]
