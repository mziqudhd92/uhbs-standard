"""Shared TCP/UDP helpers for protocol plugins."""

from __future__ import annotations

import socket
import time


def tcp_transact(
    host: str,
    port: int,
    payload: bytes,
    *,
    timeout: float = 4.0,
    recv_first: bool = False,
) -> tuple[bytes, float, str]:
    """Send optional payload over TCP; return (data, rtt_ms, err)."""
    t0 = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout) as s:
            s.settimeout(timeout)
            if recv_first:
                try:
                    first = s.recv(65535)
                except TimeoutError:
                    first = b""
            else:
                first = b""
            if payload:
                s.sendall(payload)
            try:
                more = s.recv(65535)
            except TimeoutError:
                more = b""
            data = first + more
            return data, (time.perf_counter() - t0) * 1000.0, ""
    except OSError as exc:
        return b"", (time.perf_counter() - t0) * 1000.0, str(exc)


def udp_transact(
    host: str,
    port: int,
    payload: bytes,
    *,
    timeout: float = 2.0,
) -> tuple[bytes, float, str]:
    """Send one UDP datagram; return (reply_or_empty, rtt_ms, err)."""
    t0 = time.perf_counter()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(timeout)
            s.sendto(payload, (host, port))
            try:
                data, _ = s.recvfrom(65535)
            except TimeoutError:
                data = b""
            return data, (time.perf_counter() - t0) * 1000.0, ""
    except OSError as exc:
        return b"", (time.perf_counter() - t0) * 1000.0, str(exc)


def sample_udp_latencies(
    host: str, port: int, samples: int, payload: bytes = b"\x00", timeout: float = 1.5
) -> tuple[list[float], int]:
    """UDP send(+optional recv) RTT samples in milliseconds.

    A timeout with empty reply still counts as a successful send sample
    (many canaries are alert-only / no-response).
    """
    lat: list[float] = []
    errors = 0
    for _ in range(max(1, samples)):
        _, rtt, err = udp_transact(host, port, payload, timeout=timeout)
        if err:
            errors += 1
        else:
            lat.append(rtt)
    return lat, errors
