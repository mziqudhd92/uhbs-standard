from __future__ import annotations

import contextlib
import re
import time

from uhbs_core.protocols.base import ProtocolPlugin

from ..hassh import parse_server_hassh
from ..models import CheckResult, TargetSpec
from ..rfc_probes import probe_ssh_rfc4253
from ..ssh_session import run_ssh_command
from ..tps import TPS

# Architecture-review item 2 (2026-07-27): read-only recon commands real
# attackers run within seconds of landing an SSH shell. Kept as a module
# constant so both the probe and its tests reference the same battery.
_RECON_COMMANDS = (
    "uname -a",
    "cat /proc/version",
    "cat /proc/cpuinfo",
    "id",
    "echo $PATH",
    "cat /etc/os-release",
)

# Generic, vendor-neutral placeholder markers that a templated/canned
# low-interaction shell might leak into recon output. Deliberately does
# NOT name any specific honeypot product (AGENTS.md: vendor-neutral outside
# docs/conformance/) — this is an illustrative, non-exhaustive heuristic,
# not a fingerprint database.
_GENERIC_PLACEHOLDER_MARKERS = (
    "REPLACE_ME",
    "FIXME",
    "TODO_",
    "SAMPLE_CPU",
    "PLACEHOLDER",
    "FAKE_HONEYPOT",
)

_ARCH_TOKENS = ("x86_64", "aarch64", "armv7l", "arm64", "i686", "i386")
_X86_CPUINFO_MARKERS = ("vendor_id", "flags", "model name", "GenuineIntel", "AuthenticAMD")
_ARM_CPUINFO_MARKERS = ("CPU architecture", "Features", "model name", "Hardware")


def _run_recon_shell(
    host: str, port: int, user: str, password: str, timeout: float = 20.0
) -> dict:
    """Open one interactive shell channel, run the recon battery with a
    unique per-command marker (so outputs can be split reliably even
    though paramiko's channel is a raw byte stream), then exercise a
    clear-screen ANSI escape and a tab-completion trigger on the same PTY.

    Self-contained here (does not modify ``ssh_session.py``) — returns a
    plain dict rather than a new dataclass to keep this additive change
    small: ``{"ok", "error", "outputs": {cmd: text}, "pty_ok", "pty_detail"}``.
    """
    try:
        import paramiko  # type: ignore
    except ImportError:
        return {
            "ok": False,
            "error": "paramiko not installed (pip install paramiko)",
            "outputs": {},
            "pty_ok": False,
            "pty_detail": "",
        }

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    outputs: dict[str, str] = {}
    pty_ok = True
    pty_detail = ""
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
            chan.recv(65535)  # discard MOTD/prompt banner

        per_cmd_timeout = min(6.0, max(1.0, timeout / 2))
        for i, cmd in enumerate(_RECON_COMMANDS):
            marker = f"UHBS_RECON_{i}_DONE"
            chan.send(f"{cmd}\n")
            time.sleep(0.05)
            chan.send(f"echo {marker}\n")
            buf = b""
            deadline = time.monotonic() + per_cmd_timeout
            while marker.encode() not in buf and time.monotonic() < deadline:
                if chan.recv_ready():
                    buf += chan.recv(65535)
                else:
                    time.sleep(0.05)
            outputs[cmd] = buf.decode("utf-8", errors="replace")

        # (c) PTY / terminal-control realism: clear-screen escape + a
        # tab-completion trigger. We only check the channel survives
        # without a protocol violation (exception/close) — we are not
        # attempting to validate real readline completion semantics.
        try:
            chan.send("\x1b[2J")
            time.sleep(0.2)
            if chan.recv_ready():
                chan.recv(65535)
            chan.send("ech\t")
            time.sleep(0.3)
            tab_echo = chan.recv(65535).decode("utf-8", errors="replace") if chan.recv_ready() else ""
            chan.send("\n")
            time.sleep(0.1)
            if chan.recv_ready():
                chan.recv(65535)
            pty_detail = f"tab_echo={tab_echo[:60]!r}"
        except Exception as exc:  # noqa: BLE001 — PTY probe must not abort recon
            pty_ok = False
            pty_detail = str(exc)
        chan.close()
        return {"ok": True, "error": "", "outputs": outputs, "pty_ok": pty_ok, "pty_detail": pty_detail}
    except Exception as exc:  # noqa: BLE001
        return {
            "ok": False,
            "error": str(exc),
            "outputs": outputs,
            "pty_ok": False,
            "pty_detail": pty_detail,
        }
    finally:
        with contextlib.suppress(Exception):
            client.close()


def _looks_templated(text: str) -> bool:
    """Best-effort, illustrative-only templated-output heuristic.

    We do not maintain (and should not maintain, per vendor-neutrality) a
    database of real low-interaction honeypot canned strings — this only
    catches obvious lab/placeholder leakage, not a specific product.
    """
    if not text.strip():
        return False
    upper = text.upper()
    return any(marker in upper for marker in _GENERIC_PLACEHOLDER_MARKERS)


def _check_recon_consistency(outputs: dict[str, str]) -> tuple[bool, str]:
    """(a) Cross-check the recon outputs for internal consistency.

    Heuristic and intentionally loose: real systems vary widely (containers,
    chroots, minimal distros), so we only flag combinations that would be
    genuinely contradictory on any real Linux box, not merely unusual.
    """
    uname = outputs.get("uname -a", "")
    cpuinfo = outputs.get("cat /proc/cpuinfo", "")
    osrelease = outputs.get("cat /etc/os-release", "")
    version = outputs.get("cat /proc/version", "")

    notes: list[str] = []
    ok = True

    uname_arch = next((a for a in _ARCH_TOKENS if a in uname), None)
    if uname_arch is None:
        notes.append("uname -a did not report a recognizable architecture token")
    elif (
        uname_arch in ("x86_64", "i686", "i386")
        and cpuinfo.strip()
        and not any(m in cpuinfo for m in _X86_CPUINFO_MARKERS)
    ):
        ok = False
        notes.append(f"uname reports {uname_arch} but /proc/cpuinfo lacks x86 markers")
    elif (
        uname_arch in ("aarch64", "armv7l", "arm64")
        and cpuinfo.strip()
        and not any(m in cpuinfo for m in _ARM_CPUINFO_MARKERS)
    ):
        ok = False
        notes.append(f"uname reports {uname_arch} but /proc/cpuinfo lacks ARM markers")

    if version.strip() and uname.strip():
        ver_nums = re.findall(r"\d+\.\d+\.\d+", uname)
        if ver_nums and ver_nums[0] not in version:
            ok = False
            notes.append("uname -a kernel version not echoed in /proc/version")

    if osrelease.strip() and "ID=" not in osrelease and "NAME=" not in osrelease:
        ok = False
        notes.append("/etc/os-release output missing NAME=/ID= fields")

    return ok, ("; ".join(notes) if notes else "recon outputs internally consistent")


class SSHPlugin(ProtocolPlugin):
    name = "ssh"
    families = ("it", "posix", "genai")

    def probe_fsm(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        suite = probe_ssh_rfc4253(host, port)
        if suite.skipped:
            return [
                CheckResult(
                    id="ssh.fsm.skipped",
                    team="blue",
                    passed=False,
                    detail=suite.skip_reason,
                    score=0.0,
                )
            ]
        return [c for c in suite.checks if c.id.startswith("rfc4253.")]

    def probe_negotiation(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        checks: list[CheckResult] = []
        suite = probe_ssh_rfc4253(host, port)
        checks.extend([c for c in suite.checks if "kex" in c.id or "identification" in c.id])

        hassh, algo, banner = parse_server_hassh(host, port)
        checks.append(
            CheckResult(
                id="ssh.nego.hassh",
                team="blue",
                passed=bool(hassh),
                detail=(f"HASSH={hassh} banner={banner}" if hassh else "HASSH parse failed"),
                score=100.0 if hassh else 0.0,
                evidence=[algo[:200]] if algo else [],
            )
        )
        # Optional gold baseline HASSH compare
        gold = (tps.gold_baseline_host if tps else None) or target.baseline_native_host
        if gold and hassh:
            gport = port
            if tps and tps.gold_baseline_port:
                gport = int(tps.gold_baseline_port)
            g_hassh, _, g_ban = parse_server_hassh(gold, gport)
            match = bool(g_hassh) and g_hassh == hassh
            checks.append(
                CheckResult(
                    id="ssh.nego.hassh_vs_gold",
                    team="blue",
                    passed=match,
                    detail=(
                        f"decoy={hassh} gold={g_hassh} banner_gold={g_ban}"
                        if g_hassh
                        else f"gold {gold}:{gport} HASSH unavailable"
                    ),
                    # Algo-offer match is informative; decoy may intentionally differ.
                    score=100.0 if match else (50.0 if g_hassh else 25.0),
                )
            )
        return checks

    def probe_shell_realism(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        """Architecture-review item 2 (2026-07-27): deeper interactive-shell
        realism, opt-in and NOT wired into ``test_realism.py``'s default
        Module B loop — callers (a future harness change, or ad-hoc
        analysis) invoke this explicitly.

        Runs the read-only recon battery attackers actually run first
        (``uname -a``, ``/proc/version``, ``/proc/cpuinfo``, ``id``,
        ``$PATH``, ``/etc/os-release``), then scores:

          (a) internal consistency across those outputs,
          (b) whether outputs look templated/generic vs plausible real
              kernel artifacts (byte-identical output across genuinely
              distinct commands is the strongest, most vendor-neutral tell
              and is the one check here marked ``critical=True``),
          (c) basic PTY realism — does the shell survive a clear-screen
              ANSI escape and a tab-completion trigger without a protocol
              violation.
        """
        result = _run_recon_shell(host, port, target.user, target.password)
        if not result["ok"]:
            return [
                CheckResult(
                    id="ssh.realism.shell_recon.unreachable",
                    team="blue",
                    passed=False,
                    detail=result["error"] or "shell recon failed",
                    score=0.0,
                )
            ]

        outputs: dict[str, str] = result["outputs"]
        checks: list[CheckResult] = []

        non_empty_values = [v.strip() for v in outputs.values() if v.strip()]
        empty_cmds = [c for c, v in outputs.items() if not v.strip()]
        # Byte-identical output across two *distinct* recon commands (e.g.
        # `id` and `uname -a` returning the same text) is not something a
        # real shell running real commands can produce — a genuine,
        # vendor-neutral "this isn't actually executing commands" tell.
        duplicate_signal = len(non_empty_values) >= 2 and len(set(non_empty_values)) < len(
            non_empty_values
        )
        placeholder_hits = [c for c, v in outputs.items() if _looks_templated(v)]
        templated = duplicate_signal or bool(placeholder_hits) or len(empty_cmds) >= 2
        checks.append(
            CheckResult(
                id="ssh.realism.shell_recon.generic_output",
                team="red",
                critical=duplicate_signal,
                passed=not templated,
                detail=(
                    f"duplicate_outputs={duplicate_signal} "
                    f"placeholder_hits={placeholder_hits} empty_cmds={empty_cmds}"
                ),
                score=0.0 if templated else 100.0,
                evidence=[v[:120] for v in non_empty_values[:3]],
            )
        )

        consistent, consistency_detail = _check_recon_consistency(outputs)
        checks.append(
            CheckResult(
                id="ssh.realism.shell_recon.consistency",
                team="red",
                passed=consistent,
                detail=consistency_detail,
                score=100.0 if consistent else 30.0,
            )
        )

        checks.append(
            CheckResult(
                id="ssh.realism.shell_recon.pty_controls",
                team="blue",
                passed=bool(result["pty_ok"]),
                detail=result["pty_detail"] or "clear-screen/tab probes completed",
                score=100.0 if result["pty_ok"] else 20.0,
            )
        )
        return checks

    def probe_state(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        # B1: cross-session persistence — write in session 1, read in session 2
        marker = "UHBS_CROSS_SESSION_OK"
        path = "/tmp/uhbs_cross_session_marker"
        s1 = run_ssh_command(
            host,
            port,
            target.user,
            target.password,
            f"mkdir -p /tmp && echo {marker} > {path} && cat {path}",
        )
        s2 = run_ssh_command(
            host,
            port,
            target.user,
            target.password,
            f"cat {path}",
        )
        ok = s1.ok and s2.ok and marker in s2.stdout
        return [
            CheckResult(
                id="ssh.state.cross_session",
                team="blue",
                passed=ok,
                detail=(
                    "state persisted across independent SSH sessions"
                    if ok
                    else (s2.error or s1.error or "marker missing across sessions")
                ),
                score=100.0 if ok else 0.0,
                evidence=[(s1.stdout or "")[:80], (s2.stdout or "")[:80]],
            )
        ]

    def probe_payload(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        out = run_ssh_command(host, port, target.user, target.password, "echo PAYLOAD_OK")
        ok = out.ok and "PAYLOAD_OK" in out.stdout
        return [
            CheckResult(
                id="ssh.payload.echo",
                team="red",
                passed=ok,
                detail="echo path ok" if ok else (out.error or "failed"),
                score=100.0 if ok else 0.0,
            )
        ]

    def probe_fuzz(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> list[CheckResult]:
        out = run_ssh_command(
            host, port, target.user, target.password, "head -c 1000 /dev/urandom | wc -c"
        )
        ok = out.ok and any(ch.isdigit() for ch in out.stdout)
        return [
            CheckResult(
                id="ssh.fuzz.non_utf8",
                team="red",
                passed=ok,
                detail=(out.stdout.strip() or out.error or "failed")[:160],
                score=100.0 if ok else 25.0,
            )
        ]

    def probe_load_once(
        self, host: str, port: int, target: TargetSpec, tps: TPS | None
    ) -> float:
        out = run_ssh_command(host, port, target.user, target.password, "true", timeout=20)
        if not out.ok:
            raise RuntimeError(out.error or "ssh failed")
        return out.latency_ms
