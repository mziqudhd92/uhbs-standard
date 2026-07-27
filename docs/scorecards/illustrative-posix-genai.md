# Illustrative Scorecard: POSIX-Shell / GenAI-Augmented Decoy

**Status:** Synthetic layout sample only — **not** a live UHBS-Lab Docker run.

Vendor-neutral illustrative scorecard demonstrating the UHBS v4.0.1 standard output layout.
For published lab scorecards, see [Official Examples](index.md).

| Field | Value |
| --- | --- |
| Target | Illustrative interactive shell decoy (GenAI-augmented) |
| Class | POSIX-Shell |
| Evaluated | 2026-07-26 |
| Spec | UHBS 4.0.1 |

## Module Results

| Evaluation Module | Score (0–100) | Weight | Status |
| --- | ---: | ---: | --- |
| Module A: Protocol Fidelity | 88/100 | 0.20 | PASSED |
| Module B: Behavioral Realism | 94/100 | 0.25 | PASSED |
| Module C: Telemetry Quality | 98/100 | 0.20 | PASSED |
| Module D: Safety & Containment (\(C\)) | 97/100 | GATE | PASSED (0 Leaks) |
| Module E: Scalability & Latency | 88/100 | 0.15 | PASSED (P95: 110 ms) |
| Module F: Static Code Audit | 91/100 | 0.20 | PASSED (0 Critical) |

## Safety Gate & Composite

| Metric | Value |
| --- | --- |
| Safety Gate Multiplier \(\delta_C\) | 1.0 (\(C = 97 \ge 95\)) |
| **Final Composite Score (UHQS 4.0.1)** | **92.1 / 100** |
| Grade | **A (Enterprise Grade)** |
| Production baseline (UHQS &gt; 80) | **MET** |

Machine-readable artifact: [`examples/illustrative-posix-genai.scorecard.json`](examples/illustrative-posix-genai.scorecard.json).
