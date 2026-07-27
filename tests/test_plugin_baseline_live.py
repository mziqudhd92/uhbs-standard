"""Live baseline verification against REAL reference daemons (not honeypots).

Architecture review round 2, item 2 (2026-07-27): every earlier test in this
repo runs plugins against *honeypots* (Cowrie, OpenCanary) or raw byte
fixtures. That proves a plugin can tell a decoy apart from something else,
but it never proves the plugin correctly recognizes a genuine,
standards-compliant implementation of its own protocol. If ``smb.py`` gave
a real Samba server 40/100, that would be a bug in the *plugin*, not a
finding about the target — and nothing in the existing suite would catch
it. This file closes that gap for the protocols listed below.

Design:
  - Each test spins up one lightweight, official-ish Docker image of a real
    (non-honeypot) implementation of the protocol, on a throwaway
    ``docker run --rm -d -p <host>:<container> ...`` container with a
    randomised/ephemeral host port, waits for the port to accept TCP
    connections, runs the plugin's ``probe_negotiation``/``probe_state``
    hooks against it, and asserts the aggregate score (via
    ``uhbs_core.check_scoring.score_checks``, the same aggregator Module
    A/B use) is >= 90/100 — i.e. "the plugin recognizes ground truth."
  - Skipped by default (``pytest.mark.skipif``) unless BOTH:
      1. the ``RUN_LIVE_BASELINE=1`` environment variable is set, and
      2. a local Docker daemon is reachable (``docker version``).
    This keeps plain ``pytest -q`` fast, offline, and CI-safe — no network
    pulls or containers on a normal run.
  - Containers are best-effort torn down in a ``finally`` block even if the
    assertion fails, so a failed baseline run doesn't leak containers.

Coverage as of 2026-07-27 (round 2 architecture review) — BE HONEST ABOUT
GAPS, do not assume any protocol not listed here has been baseline-tested:

  IMPLEMENTED and verified live in this session:
    * redis.py -> ``redis:7-alpine``   (official image, RESP protocol, :6379)
    * smb.py   -> ``dperson/samba``    (real Samba daemon — the exact same
      image already deployed in this lab session as ``opencanary-smb``;
      hand-verified earlier this session to answer a properly Direct-TCP-
      framed SMB1 NEGOTIATE request with a genuine ``\\xfeSMB`` SMB2/3
      response)

  NOT implemented — explicitly deferred, known gap:
    * ftp.py    — candidate images (``delfer/alpine-ftp-server``,
      ``fauria/vsftpd``) were not spun up/verified in this round; no
      baseline coverage exists yet.
    * ssh.py    — ``linuxserver/openssh-server`` was suggested but not
      spun up/verified in this round.
    * mysql.py, telnet.py, modbus.py, http.py, smtp.py, rdp.py, vnc.py,
      git.py, sip.py, snmp.py, ntp.py, tftp.py — no live reference-daemon
      baseline exists for any of these yet. Adding one is mechanically the
      same pattern as the two below (``_LiveContainer`` + a plugin probe
      call + a score assertion); this was not done for all 17 plugins in
      the time available for this round.

Do not read the *absence* of a test here as "the plugin is unverified" in
general — offline unit/regression coverage for every plugin already exists
in ``tests/test_new_protocol_plugins.py`` and ``tests/test_uhbs_core.py``.
This file specifically closes the "plugin vs a genuine, non-honeypot
implementation" gap, and only for the two protocols listed above.
"""

from __future__ import annotations

import os
import shutil
import socket
import subprocess
import time
import uuid

import pytest

from uhbs_core.check_scoring import score_checks
from uhbs_core.models import TargetSpec
from uhbs_core.protocols import get_plugin


def _docker_available() -> bool:
    if shutil.which("docker") is None:
        return False
    try:
        subprocess.run(
            ["docker", "version"],
            check=True,
            capture_output=True,
            timeout=5,
        )
        return True
    except (OSError, subprocess.SubprocessError):
        return False


_RUN_LIVE = os.environ.get("RUN_LIVE_BASELINE", "").strip() in {"1", "true", "yes"}

pytestmark = pytest.mark.skipif(
    not (_RUN_LIVE and _docker_available()),
    reason=(
        "live baseline tests require RUN_LIVE_BASELINE=1 and a reachable "
        "Docker daemon; skipped by default so `pytest -q` stays fast/offline"
    ),
)


class _LiveContainer:
    """Best-effort throwaway ``docker run`` wrapper for one baseline daemon."""

    def __init__(self, image: str, container_port: int, extra_args: list[str] | None = None):
        self.image = image
        self.container_port = container_port
        self.extra_args = extra_args or []
        self.host_port = self._free_port()
        self.name = f"uhbs-baseline-{uuid.uuid4().hex[:8]}"
        self._started = False

    @staticmethod
    def _free_port() -> int:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", 0))
            return s.getsockname()[1]

    def __enter__(self) -> _LiveContainer:
        subprocess.run(
            [
                "docker",
                "run",
                "-d",
                "--rm",
                "--name",
                self.name,
                "-p",
                f"127.0.0.1:{self.host_port}:{self.container_port}",
                *self.extra_args,
                self.image,
            ],
            check=True,
            capture_output=True,
            timeout=60,
        )
        self._started = True
        self._wait_for_port(timeout=30.0)
        return self

    def _wait_for_port(self, timeout: float) -> None:
        # A bare TCP connect can succeed the instant the kernel accepts the
        # SYN into the listen backlog — slightly *before* the daemon's own
        # accept()/handshake loop inside the container is actually
        # servicing requests. Observed live (redis:7-alpine and
        # dperson/samba both hit this): the very first post-connect
        # protocol round trip got no reply even though the TCP connect
        # itself succeeded immediately. Requiring two consecutive
        # successful raw connects with a short gap, then a warm-up pause
        # before returning, made both baselines reliable.
        deadline = time.monotonic() + timeout
        last_err: Exception | None = None
        consecutive_ok = 0
        while time.monotonic() < deadline:
            try:
                with socket.create_connection(("127.0.0.1", self.host_port), timeout=1.0):
                    consecutive_ok += 1
            except OSError as exc:
                last_err = exc
                consecutive_ok = 0
            if consecutive_ok >= 2:
                time.sleep(1.5)  # let the daemon's own accept loop warm up
                return
            time.sleep(0.5)
        raise TimeoutError(f"{self.image} never opened {self.host_port}: {last_err}")

    def __exit__(self, *exc_info: object) -> None:
        if self._started:
            subprocess.run(
                ["docker", "rm", "-f", self.name],
                check=False,
                capture_output=True,
                timeout=15,
            )


def test_redis_plugin_scores_high_against_real_redis() -> None:
    """redis.py vs the official redis:7-alpine image (RESP protocol, real server)."""
    plugin = get_plugin("redis")
    with _LiveContainer("redis:7-alpine", 6379) as c:
        target = TargetSpec(name="baseline-redis", host="127.0.0.1", port=c.host_port)
        checks = [
            *plugin.probe_negotiation("127.0.0.1", c.host_port, target, None),
            *plugin.probe_state("127.0.0.1", c.host_port, target, None),
        ]
        score = score_checks(checks)
        detail = "; ".join(f"{ch.id}={ch.score}" for ch in checks)
        assert score >= 90.0, f"expected >=90 vs real redis, got {score} ({detail})"


def test_smb_plugin_scores_high_against_real_samba() -> None:
    """smb.py vs a real Samba daemon (dperson/samba — same image as opencanary-smb).

    Uses a throwaway instance on an ephemeral host port (NOT the running
    ``opencanary-smb`` lab container) so this test doesn't depend on / dial
    into the shared ``uhbs-lab`` docker network or disturb that container.
    """
    plugin = get_plugin("smb")
    with _LiveContainer(
        "dperson/samba",
        445,
        extra_args=["-e", "USERID=1000", "-e", "GROUPID=1000"],
    ) as c:
        target = TargetSpec(name="baseline-smb", host="127.0.0.1", port=c.host_port)
        checks = [
            *plugin.probe_negotiation("127.0.0.1", c.host_port, target, None),
            *plugin.probe_state("127.0.0.1", c.host_port, target, None),
        ]
        score = score_checks(checks)
        detail = "; ".join(f"{ch.id}={ch.score}" for ch in checks)
        assert score >= 90.0, f"expected >=90 vs real samba, got {score} ({detail})"
