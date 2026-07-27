"""Userspace-only TCP/IP + TLS stack fingerprint auditing (new, opt-in probe).

Architecture-review item 1 (2026-07-27): p0f-style stack fingerprinting and
JA3S/JA4S-style TLS fingerprinting, implemented **without raw sockets and
without root**, because UHBS's lab harness runs as an unprivileged process.

READ THIS BEFORE TRUSTING ANY VALUE THIS MODULE RETURNS
=========================================================

True p0f fingerprints are built from the raw IP/TCP header of the SYN-ACK:
initial TTL, exact advertised window size *before* any OS-level clamping,
TCP option order (MSS, SACK, timestamps, window-scale — in the order the
peer sent them), and IP ID behavior. **None of that is obtainable from
Python's ``socket`` module on an unprivileged connect() on any platform
this harness targets** — the kernel's TCP stack has already consumed the
SYN-ACK by the time userspace code sees a connected socket. Achieving the
real thing requires either raw sockets (``SOCK_RAW``, needs root/
``CAP_NET_RAW``) or a packet-capture library such as ``scapy``/libpcap.
This module does **not** pretend otherwise: every TTL/exact-window/
option-order field p0f would normally use is intentionally absent here,
not stubbed with a fake value.

What *is* honestly obtainable from userspace and is implemented below:

  - TCP connect() latency (multiple samples → median + jitter) — a weak but
    real timing signal.
  - ``SO_RCVBUF``/``SO_SNDBUF`` as configured on *our own* local socket —
    informative only insofar as it reflects the local OS/Python defaults,
    NOT the peer's advertised window. Documented as such below.
  - ``TCP_NODELAY`` set/query round-trip (confirms the local stack accepted
    the option; says nothing about the peer).
  - On Linux only: ``getsockopt(IPPROTO_TCP, TCP_INFO, ...)``, a **kernel**
    sockopt (constant ``11``, stable across the range of Linux kernels this
    project cares about) that *does* expose real post-handshake telemetry —
    measured RTT/RTT-variance, the negotiated window-scale option, current
    congestion window, retransmit count — without needing raw sockets or
    root. This is the one genuinely p0f-adjacent signal we can get for
    free on Linux. It is unavailable on macOS/BSD (different, non-portable
    struct — ``TCP_CONNECTION_INFO`` — deliberately not reverse-engineered
    here) and is parsed defensively: if the returned bytes don't look like
    a plausible ``tcp_info`` struct (sane TCP state, bounded RTT), we
    report "unavailable" rather than surface a mis-parsed number that
    *looks* precise but isn't. TCP_INFO's exact struct layout has drifted
    slightly across kernel versions, so this must be treated as
    best-effort supplementary telemetry, never a scored gate on its own.

JA3S/JA4S — TLS ServerHello fingerprinting
===========================================

Real JA3S/JA4S hashes are built from the *raw bytes* of the ServerHello
message: negotiated cipher, TLS version, and the **exact order** of
extensions as the server sent them. Python's ``ssl`` module does not
expose raw handshake bytes — it terminates the TLS session and gives you
already-negotiated, already-reordered-by-openssl metadata
(``cipher()``, ``version()``, ``selected_alpn_protocol()``). Genuine
JA3S/JA4S therefore requires packet capture (e.g. scapy/tshark) and is
**out of scope for a userspace-only implementation** — this module does
not claim to produce a JA3S/JA4S hash. What it does instead is a
best-effort *approximation*: it records what ``ssl`` will tell us about a
single default handshake, and — for a little more signal without a full
capture — makes a couple of additional handshake attempts with a
restricted client cipher policy to see whether the server will accept
something outside a modern default set. That tells us "does this server's
TLS stack accept X" via repeated client-driven probing, not "what order
did the server list its ciphers in" — a materially different, weaker
signal that is labelled as such throughout.

Everything below is designed to be **opt-in**: :func:`fingerprint_host`
returns a single ``CheckResult``-shaped dict that a protocol plugin *could*
choose to call, but nothing here is wired into any plugin's default probe
path. That integration is deliberately left as follow-up work so this
module cannot silently change any existing pass/fail outcome.
"""

from __future__ import annotations

import contextlib
import socket
import ssl
import statistics
import struct
import sys
import time
from dataclasses import dataclass, field

from .models import CheckResult

# Linux getsockopt(IPPROTO_TCP, TCP_INFO, ...) — sockopt number 11 has been
# stable across the Linux kernel versions this project targets. Not exposed
# as socket.TCP_INFO by CPython on every platform/build, so we use the
# literal here rather than depending on the attribute existing.
_LINUX_TCP_INFO = 11
# First 8 fields are single bytes (state, ca_state, retransmits, probes,
# backoff, options, then a byte packing snd_wscale:rcv_wscale nibbles, then
# a delivery_rate_app_limited bitfield byte on newer kernels) — this exact
# 8-bytes-then-24-uint32 layout is the widely used minimal decode for Linux
# tcp_info and is treated as best-effort: we sanity-check before trusting it.
_TCP_INFO_FMT = "B" * 8 + "I" * 24
_TCP_INFO_SIZE = struct.calcsize(_TCP_INFO_FMT)
_TCP_INFO_FIELDS = (
    "state",
    "ca_state",
    "retransmits",
    "probes",
    "backoff",
    "options",
    "wscale_byte",  # low nibble = rcv_wscale, high nibble = snd_wscale
    "delivery_rate_app_limited",
    "rto",
    "ato",
    "snd_mss",
    "rcv_mss",
    "unacked",
    "sacked",
    "lost",
    "retrans",
    "fackets",
    "last_data_sent",
    "last_ack_sent",
    "last_data_recv",
    "last_ack_recv",
    "pmtu",
    "rcv_ssthresh",
    "rtt",
    "rttvar",
    "snd_ssthresh",
    "snd_cwnd",
    "advmss",
    "reordering",
    "rcv_rtt",
    "rcv_space",
    "total_retrans",
)
# Plausible TCP_ESTABLISHED range for the leading `state` byte (RFC793-ish
# Linux enum tcp_state_t is 1..11); used purely as a sanity gate before we
# trust the rest of the struct decode.
_TCP_STATE_MAX = 12


@dataclass
class TCPStackSignature:
    """Best-effort, userspace-obtainable TCP-stack signal set.

    See module docstring for exactly which p0f-grade fields are
    intentionally absent (TTL, exact advertised window, option order).
    """

    host: str
    port: int
    samples_requested: int
    connect_latencies_ms: list[float] = field(default_factory=list)
    connect_errors: int = 0
    median_connect_ms: float | None = None
    connect_jitter_ms: float | None = None
    so_rcvbuf: int | None = None
    so_sndbuf: int | None = None
    tcp_nodelay_ok: bool | None = None
    linux_tcp_info: dict[str, float] | None = None
    linux_tcp_info_note: str = ""

    @property
    def reachable(self) -> bool:
        return len(self.connect_latencies_ms) > 0


def _decode_linux_tcp_info(raw: bytes) -> dict[str, float] | None:
    """Best-effort decode of Linux ``tcp_info``; ``None`` if implausible."""
    if len(raw) < _TCP_INFO_SIZE:
        return None
    try:
        values = struct.unpack(_TCP_INFO_FMT, raw[:_TCP_INFO_SIZE])
    except struct.error:
        return None
    decoded = dict(zip(_TCP_INFO_FIELDS, values, strict=False))
    state = decoded.get("state", 0)
    rtt = decoded.get("rtt", 0)
    # Sanity gate: refuse to report a decode that doesn't look like a real
    # tcp_info struct rather than silently surfacing garbage as "data".
    if not (0 < state <= _TCP_STATE_MAX):
        return None
    if rtt > 60_000_000:  # >60s RTT in microseconds is not plausible
        return None
    wscale_byte = int(decoded.pop("wscale_byte", 0))
    decoded["rcv_wscale"] = wscale_byte & 0x0F
    decoded["snd_wscale"] = (wscale_byte >> 4) & 0x0F
    decoded["rtt_ms"] = decoded["rtt"] / 1000.0
    decoded["rttvar_ms"] = decoded.get("rttvar", 0) / 1000.0
    return decoded


def probe_tcp_stack(
    host: str, port: int, samples: int = 5, timeout: float = 4.0
) -> TCPStackSignature:
    """Collect the userspace-obtainable TCP-stack signature described above.

    Opens ``samples`` independent TCP connections (each closed immediately)
    to measure connect-latency jitter, then on the last connection attempts
    the Linux-only ``TCP_INFO`` sockopt read before closing.
    """
    sig = TCPStackSignature(host=host, port=port, samples_requested=max(1, samples))
    for i in range(sig.samples_requested):
        t0 = time.perf_counter()
        try:
            with socket.create_connection((host, port), timeout=timeout) as s:
                sig.connect_latencies_ms.append((time.perf_counter() - t0) * 1000.0)
                if i == 0:
                    try:
                        sig.so_rcvbuf = s.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
                        sig.so_sndbuf = s.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
                    except OSError:
                        pass
                    try:
                        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                        sig.tcp_nodelay_ok = (
                            s.getsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY) == 1
                        )
                    except OSError:
                        sig.tcp_nodelay_ok = False
                if i == sig.samples_requested - 1:
                    if sys.platform.startswith("linux"):
                        try:
                            raw = s.getsockopt(
                                socket.IPPROTO_TCP, _LINUX_TCP_INFO, _TCP_INFO_SIZE
                            )
                            decoded = _decode_linux_tcp_info(raw)
                            if decoded is not None:
                                sig.linux_tcp_info = decoded
                            else:
                                sig.linux_tcp_info_note = (
                                    "TCP_INFO read but did not decode to a plausible "
                                    "struct — treated as unavailable, not reported"
                                )
                        except OSError as exc:
                            sig.linux_tcp_info_note = f"TCP_INFO unavailable: {exc}"
                    else:
                        sig.linux_tcp_info_note = (
                            f"TCP_INFO is Linux-only (platform={sys.platform!r}); "
                            "p0f-grade window/RTT telemetry not obtainable here"
                        )
        except OSError:
            sig.connect_errors += 1

    if sig.connect_latencies_ms:
        sig.median_connect_ms = statistics.median(sig.connect_latencies_ms)
        sig.connect_jitter_ms = (
            statistics.pstdev(sig.connect_latencies_ms)
            if len(sig.connect_latencies_ms) > 1
            else 0.0
        )
    return sig


# --- TLS / JA3S-ish approximation -------------------------------------------

# Illustrative "typical real daemon" defaults — NOT captured JA3S/JA4S
# hashes (those need ServerHello byte order, which `ssl` never exposes).
# These are coarse, common-knowledge shapes of what widely-deployed TLS
# stacks tend to negotiate by default, used only to flag "looks unusual"
# vs "looks unremarkable" — never a hard pass/fail signal on its own.
KNOWN_TLS_PROFILES: tuple[dict, ...] = (
    {
        "name": "modern_tls13_default",
        "tls_versions": {"TLSv1.3"},
        "cipher_prefixes": ("TLS_AES_", "TLS_CHACHA20_"),
    },
    {
        "name": "openssl_tls12_default",
        "tls_versions": {"TLSv1.2"},
        "cipher_prefixes": ("ECDHE-", "DHE-"),
    },
)

# Cipher-name substrings considered legacy/weak enough to be a mild anomaly
# signal if a server accepts them outside a deliberate legacy-compat test.
_WEAK_CIPHER_MARKERS = ("RC4", "3DES", "DES-", "NULL", "EXPORT", "MD5")

# Certificate CN/SAN substrings that read as obvious lab/placeholder values
# rather than a real hostname — a soft anomaly signal only.
_PLACEHOLDER_CERT_MARKERS = (
    "example.com",
    "localhost",
    "test",
    "placeholder",
    "changeme",
    "invalid",
)


@dataclass
class TLSFingerprint:
    host: str
    port: int
    ok: bool
    tls_version: str | None = None
    cipher_name: str | None = None
    alpn_protocol: str | None = None
    cert_subject: str | None = None
    cert_issuer: str | None = None
    cert_self_signed: bool | None = None
    accepts_weak_cipher_probe: bool | None = None
    anomaly_flags: list[str] = field(default_factory=list)
    matched_known_profile: str | None = None
    error: str = ""
    note: str = (
        "best-effort ssl-module introspection; NOT a captured JA3S/JA4S hash "
        "(no ServerHello byte/extension order available in userspace)"
    )


def _match_known_profile(tls_version: str | None, cipher_name: str | None) -> str | None:
    for profile in KNOWN_TLS_PROFILES:
        if (
            tls_version in profile["tls_versions"]
            and cipher_name
            and any(cipher_name.startswith(p) for p in profile["cipher_prefixes"])
        ):
            return profile["name"]
    return None


def _cert_fields_from_der(der: bytes) -> tuple[str | None, str | None]:
    """Best-effort subject/issuer CN extraction from a DER cert.

    Uses ``cryptography`` (already a transitive dependency via paramiko's
    ``lab`` extra) if importable; otherwise returns ``(None, None)`` rather
    than guessing at ASN.1 by hand.
    """
    try:
        from cryptography import x509  # type: ignore
        from cryptography.hazmat.backends import default_backend  # type: ignore
    except ImportError:
        return None, None
    try:
        cert = x509.load_der_x509_certificate(der, default_backend())
        subject = cert.subject.rfc4514_string()
        issuer = cert.issuer.rfc4514_string()
        return subject, issuer
    except Exception:  # noqa: BLE001 — best-effort parse, never raise
        return None, None


def probe_tls(
    host: str,
    port: int,
    timeout: float = 5.0,
    server_hostname: str | None = None,
) -> TLSFingerprint:
    """Negotiate one TLS handshake and record what ``ssl`` will tell us.

    Does not validate the peer certificate (honeypots commonly present
    self-signed certs) — we want to *observe* the cert, not reject it.
    """
    fp = TLSFingerprint(host=host, port=port, ok=False)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with contextlib.suppress(NotImplementedError, ssl.SSLError):
        ctx.set_alpn_protocols(["h2", "http/1.1"])
    try:
        with (
            socket.create_connection((host, port), timeout=timeout) as raw_sock,
            ctx.wrap_socket(raw_sock, server_hostname=server_hostname or host) as tls_sock,
        ):
            fp.ok = True
            fp.tls_version = tls_sock.version()
            cipher = tls_sock.cipher()
            fp.cipher_name = cipher[0] if cipher else None
            fp.alpn_protocol = tls_sock.selected_alpn_protocol()
            der = tls_sock.getpeercert(binary_form=True)
            if der:
                subject, issuer = _cert_fields_from_der(der)
                fp.cert_subject = subject
                fp.cert_issuer = issuer
                if subject and issuer:
                    fp.cert_self_signed = subject == issuer
                if subject and any(m in subject.lower() for m in _PLACEHOLDER_CERT_MARKERS):
                    fp.anomaly_flags.append(f"placeholder-looking cert subject: {subject!r}")
    except (OSError, ssl.SSLError) as exc:
        fp.error = str(exc)
        return fp

    fp.matched_known_profile = _match_known_profile(fp.tls_version, fp.cipher_name)
    if fp.matched_known_profile is None and fp.tls_version:
        fp.anomaly_flags.append(
            f"negotiated {fp.tls_version}/{fp.cipher_name} did not match any known-profile "
            "shape in KNOWN_TLS_PROFILES (illustrative table, not exhaustive)"
        )
    if fp.cert_self_signed:
        fp.anomaly_flags.append("self-signed certificate (subject == issuer)")

    # Best-effort weak-cipher acceptance probe: a handful of additional
    # handshakes with a client cipher list restricted to legacy/weak names.
    # This tells us "does the server's TLS stack accept legacy crypto when
    # offered," which is weaker than and different from a captured
    # ServerHello cipher-order fingerprint — see class docstring `note`.
    try:
        weak_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        weak_ctx.check_hostname = False
        weak_ctx.verify_mode = ssl.CERT_NONE
        weak_ctx.set_ciphers("ALL:@SECLEVEL=0")
        weak_ctx.minimum_version = ssl.TLSVersion.MINIMUM_SUPPORTED
        with (
            socket.create_connection((host, port), timeout=timeout) as raw_sock2,
            weak_ctx.wrap_socket(raw_sock2, server_hostname=server_hostname or host) as weak_sock,
        ):
            weak_cipher = weak_sock.cipher()
            name = weak_cipher[0] if weak_cipher else ""
            fp.accepts_weak_cipher_probe = any(m in name.upper() for m in _WEAK_CIPHER_MARKERS)
    except (OSError, ssl.SSLError, ValueError):
        fp.accepts_weak_cipher_probe = False

    if fp.accepts_weak_cipher_probe:
        fp.anomaly_flags.append(
            "server accepted a legacy/weak cipher when explicitly offered "
            "(observational only — real hardened daemons vary widely here too)"
        )

    return fp


def fingerprint_host(
    host: str,
    port: int,
    use_tls: bool = False,
    *,
    tcp_samples: int = 5,
    timeout: float = 4.0,
) -> dict:
    """Run the TCP-stack probe (+ optional TLS probe) and return one
    ``CheckResult``-shaped dict any plugin *could* opt into calling.

    ``passed`` here means "we could reach the host and collect a
    signature," not "this proves a honeypot." Anomalies are surfaced in
    ``evidence``/``detail`` for a human (or a later, explicitly-designed
    scoring rule) to interpret — this probe intentionally does not gate
    pass/fail on any single heuristic above, per this module's honesty
    requirement.
    """
    tcp_sig = probe_tcp_stack(host, port, samples=tcp_samples, timeout=timeout)
    evidence: list[str] = []
    notes: list[str] = []

    if not tcp_sig.reachable:
        return CheckResult(
            id="fingerprint.tcp_stack",
            team="blue",
            passed=False,
            detail=f"{host}:{port} unreachable ({tcp_sig.connect_errors} connect errors)",
            score=0.0,
        ).to_dict()

    notes.append(
        f"median_connect={tcp_sig.median_connect_ms:.2f}ms "
        f"jitter={tcp_sig.connect_jitter_ms:.2f}ms n={len(tcp_sig.connect_latencies_ms)}"
    )
    if tcp_sig.linux_tcp_info:
        info = tcp_sig.linux_tcp_info
        notes.append(
            f"linux_tcp_info: rtt={info['rtt_ms']:.2f}ms rttvar={info['rttvar_ms']:.2f}ms "
            f"snd_wscale={info['snd_wscale']} rcv_wscale={info['rcv_wscale']} "
            f"cwnd={info['snd_cwnd']} retrans={info['total_retrans']}"
        )
    else:
        notes.append(f"linux_tcp_info: unavailable ({tcp_sig.linux_tcp_info_note})")
    evidence.append(
        f"so_rcvbuf={tcp_sig.so_rcvbuf} so_sndbuf={tcp_sig.so_sndbuf} "
        f"tcp_nodelay_ok={tcp_sig.tcp_nodelay_ok} "
        "(local-socket-only signals — not the peer's advertised window)"
    )

    tls_fp: TLSFingerprint | None = None
    if use_tls:
        tls_fp = probe_tls(host, port, timeout=timeout)
        if tls_fp.ok:
            notes.append(
                f"tls={tls_fp.tls_version} cipher={tls_fp.cipher_name} "
                f"alpn={tls_fp.alpn_protocol} known_profile={tls_fp.matched_known_profile}"
            )
            if tls_fp.anomaly_flags:
                evidence.extend(tls_fp.anomaly_flags)
        else:
            notes.append(f"tls probe failed: {tls_fp.error}")

    return CheckResult(
        id="fingerprint.tcp_stack" + (".tls" if use_tls else ""),
        team="blue",
        passed=True,
        detail=" | ".join(notes),
        score=100.0,
        evidence=evidence[:10],
    ).to_dict()
