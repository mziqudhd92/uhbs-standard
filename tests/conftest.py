"""Shared pytest fixtures for UHBS."""

from __future__ import annotations

import pytest

from uhbs_core.notices import reset_lab_sandbox_notice


@pytest.fixture(autouse=True)
def _reset_lab_sandbox_notice() -> None:
    """Allow each test to observe the lab/sandbox NOTICE on stderr."""
    reset_lab_sandbox_notice()
    yield
    reset_lab_sandbox_notice()
