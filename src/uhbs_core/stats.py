"""Statistical helpers for UHBS Module A3 (IAT / gold-baseline matching)."""

from __future__ import annotations

from typing import List, Sequence, Tuple


def ks_2samp(a: Sequence[float], b: Sequence[float]) -> Tuple[float, float]:
    """Two-sample Kolmogorov–Smirnov statistic and asymptotic p-value approx.

    Returns (D, p_approx). p_approx is a rough bound for gating (not scipy-grade).
    """
    x = sorted(float(v) for v in a)
    y = sorted(float(v) for v in b)
    n1, n2 = len(x), len(y)
    if n1 == 0 or n2 == 0:
        return 1.0, 0.0
    i = j = 0
    cdf1 = cdf2 = 0.0
    d = 0.0
    while i < n1 and j < n2:
        if x[i] <= y[j]:
            i += 1
            cdf1 = i / n1
        else:
            j += 1
            cdf2 = j / n2
        d = max(d, abs(cdf1 - cdf2))
    while i < n1:
        i += 1
        cdf1 = i / n1
        d = max(d, abs(cdf1 - cdf2))
    while j < n2:
        j += 1
        cdf2 = j / n2
        d = max(d, abs(cdf1 - cdf2))
    # Massey asymptotic approximation
    en = (n1 * n2) / (n1 + n2)
    import math

    lam = (math.sqrt(en) + 0.12 + 0.11 / math.sqrt(en)) * d
    # Q_KS(lam) ≈ 2 Σ (-1)^{k-1} exp(-2 k^2 lam^2)
    p = 0.0
    for k in range(1, 101):
        p += ((-1) ** (k - 1)) * math.exp(-2.0 * (k * lam) ** 2)
    p = max(0.0, min(1.0, 2.0 * p))
    return d, p


def sample_connect_latencies(
    host: str, port: int, samples: int, timeout: float = 3.0
) -> Tuple[List[float], int]:
    """TCP connect RTT samples in milliseconds."""
    import socket
    import time

    lat: List[float] = []
    errors = 0
    for _ in range(max(1, samples)):
        t0 = time.perf_counter()
        try:
            with socket.create_connection((host, port), timeout=timeout):
                pass
            lat.append((time.perf_counter() - t0) * 1000.0)
        except OSError:
            errors += 1
    return lat, errors
