"""Minimal SSH session helper for execution-phase modules (paramiko optional)."""

from __future__ import annotations

import socket
import time
from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class ExecOutcome:
    ok: bool
    stdout: str
    stderr: str
    latency_ms: float
    error: str = ""


def tcp_connect(host: str, port: int, timeout: float = 5.0) -> Tuple[bool, float, str]:
    t0 = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            pass
        return True, (time.perf_counter() - t0) * 1000.0, ""
    except OSError as exc:
        return False, (time.perf_counter() - t0) * 1000.0, str(exc)


def ssh_banner(host: str, port: int, timeout: float = 5.0) -> Tuple[str, float, str]:
    """Read SSH identification string (pre-auth)."""
    t0 = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout) as s:
            s.settimeout(timeout)
            data = s.recv(256)
        banner = data.decode("utf-8", errors="replace").strip()
        return banner, (time.perf_counter() - t0) * 1000.0, ""
    except OSError as exc:
        return "", (time.perf_counter() - t0) * 1000.0, str(exc)


def run_ssh_command(
    host: str,
    port: int,
    user: str,
    password: str,
    command: str,
    timeout: float = 15.0,
) -> ExecOutcome:
    """Run a remote command over SSH. Requires paramiko.

    Prefers SSH exec; if the peer closes the exec channel (common for
    shell-only / limited-interaction decoys), falls back to an interactive shell.
    """
    try:
        import paramiko  # type: ignore
    except ImportError:
        return ExecOutcome(
            ok=False,
            stdout="",
            stderr="",
            latency_ms=0.0,
            error="paramiko not installed (pip install paramiko)",
        )

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    t0 = time.perf_counter()
    try:
        client.connect(
            hostname=host,
            port=port,
            username=user,
            password=password,
            timeout=timeout,
            allow_agent=False,
            look_for_keys=False,
            banner_timeout=timeout,
            auth_timeout=timeout,
        )
        try:
            _, stdout, stderr = client.exec_command(command, timeout=timeout)
            out = stdout.read().decode("utf-8", errors="replace")
            err = stderr.read().decode("utf-8", errors="replace")
            latency = (time.perf_counter() - t0) * 1000.0
            return ExecOutcome(ok=True, stdout=out, stderr=err, latency_ms=latency)
        except Exception as exec_exc:  # noqa: BLE001
            # Some limited-interaction decoys reject non-interactive exec.
            msg = str(exec_exc).lower()
            if "channel closed" not in msg and "channel open" not in msg:
                raise
            shell = run_ssh_shell_commands(
                host, port, user, password, [command], timeout=timeout
            )
            if shell.ok or shell.stdout:
                return shell
            return ExecOutcome(
                ok=False,
                stdout=shell.stdout,
                stderr=shell.stderr,
                latency_ms=(time.perf_counter() - t0) * 1000.0,
                error=str(exec_exc),
            )
    except Exception as exc:  # noqa: BLE001
        latency = (time.perf_counter() - t0) * 1000.0
        return ExecOutcome(
            ok=False, stdout="", stderr="", latency_ms=latency, error=str(exc)
        )
    finally:
        try:
            client.close()
        except Exception:  # noqa: BLE001
            pass


def run_ssh_shell_commands(
    host: str,
    port: int,
    user: str,
    password: str,
    commands: List[str],
    timeout: float = 20.0,
) -> ExecOutcome:
    """Open an interactive shell channel and send commands sequentially."""
    try:
        import paramiko  # type: ignore
    except ImportError:
        return ExecOutcome(
            ok=False,
            stdout="",
            stderr="",
            latency_ms=0.0,
            error="paramiko not installed (pip install paramiko)",
        )

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    t0 = time.perf_counter()
    chunks: List[str] = []
    try:
        client.connect(
            hostname=host,
            port=port,
            username=user,
            password=password,
            timeout=timeout,
            allow_agent=False,
            look_for_keys=False,
            banner_timeout=timeout,
            auth_timeout=timeout,
        )
        chan = client.invoke_shell(term="xterm", width=120, height=40)
        chan.settimeout(timeout)
        time.sleep(0.4)
        if chan.recv_ready():
            chunks.append(chan.recv(65535).decode("utf-8", errors="replace"))
        for cmd in commands:
            chan.send(cmd + "\n")
            time.sleep(0.5)
            if chan.recv_ready():
                chunks.append(chan.recv(65535).decode("utf-8", errors="replace"))
        time.sleep(0.3)
        if chan.recv_ready():
            chunks.append(chan.recv(65535).decode("utf-8", errors="replace"))
        chan.close()
        latency = (time.perf_counter() - t0) * 1000.0
        return ExecOutcome(ok=True, stdout="".join(chunks), stderr="", latency_ms=latency)
    except Exception as exc:  # noqa: BLE001
        latency = (time.perf_counter() - t0) * 1000.0
        return ExecOutcome(
            ok=False, stdout="".join(chunks), stderr="", latency_ms=latency, error=str(exc)
        )
    finally:
        try:
            client.close()
        except Exception:  # noqa: BLE001
            pass
