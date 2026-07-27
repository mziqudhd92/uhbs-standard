"""Plugin-author SDK — thin, additive helpers for third-party UHBS plugins.

This module does **not** duplicate anything in ``uhbs_core.netutil`` — the
low-level transport helpers (``tcp_transact``, ``udp_transact``,
``sample_udp_latencies``) already live there and continue to be the single
source of truth. This module simply **re-exports/wraps** them with
docstrings, defaults, and naming aimed at a third-party plugin author
writing a new ``ProtocolPlugin`` from scratch, so they don't have to read
``uhbs_core.netutil``'s internals to get started. If you're maintaining a
built-in plugin inside this repo, keep using ``uhbs_core.netutil`` directly
— this module is for external/new plugin code.

It also adds a couple of genuinely new, small, low-risk builder utilities
that did not exist anywhere else in the codebase yet:

- :class:`PktLineBuilder` — git-style pkt-line framing (see
  ``uhbs_core.protocols.git`` for the exact hand-rolled inline logic this
  factors out; ``git.py`` itself is intentionally **not** changed to use
  this helper in this pass — see the class docstring for why).

See ``docs/plugin-authoring.md`` for the full third-party plugin walkthrough.
"""

from __future__ import annotations

from uhbs_core.netutil import sample_udp_latencies as _sample_udp_latencies
from uhbs_core.netutil import tcp_transact as _tcp_transact
from uhbs_core.netutil import udp_transact as _udp_transact

__all__ = [
    "PktLineBuilder",
    "sample_udp_latencies",
    "tcp_transact",
    "udp_transact",
]


def tcp_transact(
    host: str,
    port: int,
    payload: bytes = b"",
    *,
    timeout: float = 4.0,
    recv_first: bool = False,
) -> tuple[bytes, float, str]:
    """Open a TCP connection, optionally send ``payload``, and read one reply.

    This is the primary building block for a protocol plugin's
    ``probe_fsm``/``probe_negotiation``/``probe_state`` hooks. Returns
    ``(data, rtt_ms, err)`` — ``err`` is a non-empty string on any
    ``OSError`` (connection refused, timeout, etc.); ``data`` is ``b""`` on
    error rather than raising, so a plugin can build a ``CheckResult`` with
    ``passed=False`` instead of needing its own try/except around every call.

    Set ``recv_first=True`` for protocols where the server sends a banner
    before you send anything (e.g. SSH, SMTP, FTP); leave it ``False`` for
    protocols where the client speaks first (e.g. HTTP, most RPC-style
    binary protocols).
    """
    return _tcp_transact(host, port, payload, timeout=timeout, recv_first=recv_first)


def udp_transact(
    host: str,
    port: int,
    payload: bytes,
    *,
    timeout: float = 2.0,
) -> tuple[bytes, float, str]:
    """Send one UDP datagram and wait (briefly) for a reply.

    Returns ``(reply_or_empty, rtt_ms, err)``. Many honeypot/canary UDP
    listeners are alert-only and never reply — an empty ``reply`` with no
    ``err`` is a normal, successful send, not a failure; only a non-empty
    ``err`` indicates the datagram could not be sent at all.
    """
    return _udp_transact(host, port, payload, timeout=timeout)


def sample_udp_latencies(
    host: str,
    port: int,
    samples: int,
    payload: bytes = b"\x00",
    timeout: float = 1.5,
) -> tuple[list[float], int]:
    """Collect ``samples`` UDP round-trip-time measurements, in milliseconds.

    Intended for a plugin's timing/jitter probe (see
    ``uhbs_core.protocols.base.ProtocolPlugin.probe_timing`` for the TCP
    equivalent pattern used by built-in plugins). A send that times out with
    no reply still counts as a successful sample — see the return value's
    second element (``errors``) for the count of genuine send failures.
    """
    return _sample_udp_latencies(host, port, samples, payload=payload, timeout=timeout)


class PktLineBuilder:
    """Build/parse git-style "pkt-line" framed messages.

    Format (see the git ``protocol-common`` documentation): each line is a
    4-hex-digit ASCII length prefix — counting itself — followed by the line
    body; a bare ``"0000"`` is the special "flush-pkt" with no body.

    ``uhbs_core.protocols.git`` already hand-rolls exactly this framing
    inline (see its private ``_pkt_line()`` helper) because it predates this
    SDK module. It is intentionally **not** modified to use this class in
    this pass — that plugin already has passing test coverage and this is a
    behavior-preserving refactor opportunity, not a bug fix, so it's safer
    left for a dedicated follow-up rather than bundled here. New plugins
    (git-protocol-adjacent or otherwise pkt-line-framed) should use this
    class instead of re-implementing the same four lines themselves.
    """

    @staticmethod
    def encode(body: bytes) -> bytes:
        """Encode one pkt-line: ``len(body) + 4`` as 4 hex digits, then body."""
        total = len(body) + 4
        return f"{total:04x}".encode("ascii") + body

    @staticmethod
    def flush() -> bytes:
        """The pkt-line "flush-pkt" — a bare ``0000`` with no body."""
        return b"0000"

    @staticmethod
    def decode_length(raw: bytes) -> int | None:
        """Parse a pkt-line's 4-hex-digit length prefix from ``raw[:4]``.

        Returns ``None`` if ``raw`` is too short or not valid hex (e.g. the
        peer sent something that isn't pkt-line framed at all) rather than
        raising, so callers can treat it as "not a pkt-line reply".
        """
        if len(raw) < 4:
            return None
        try:
            return int(raw[:4], 16)
        except ValueError:
            return None
