# Universal Scoring Methodology (UHQS 4.3.6)

**Status:** Normative

The key words **MUST**, **SHOULD**, and **MAY** are interpreted as in
[RFC 2119](https://www.rfc-editor.org/rfc/rfc2119). See
[Status of This Document](status.md).

## Composite Score Formula

The **Universal Honeypot Quality Score (UHQS)** **MUST** be computed as a
normalized value from **0 to 100**:

\[
\mathrm{UHQS} = \delta_C \cdot (w_A \cdot S_A + w_B \cdot S_B + w_C \cdot S_C + w_E \cdot S_E + w_F \cdot S_F)
\]

![UHQS formula explainer: weighted modules A–F multiplied by Safety Gate δ_C from Module D](../assets/uhqs-formula-explainer.svg)

| Symbol | Meaning |
| --- | --- |
| \(S_A, S_B, S_C, S_E, S_F\) | Normalized scores (0–100) for Modules A, B, C, E, and F |
| \(w_A, w_B, w_C, w_E, w_F\) | Dimension weights assigned by profile class |
| \(\delta_C\) | Safety Gate multiplier derived from Module D containment score \(C\) |

Implementations **MUST** round the final UHQS to **two decimal places** (half-up /
Python `round` semantics as used by the reference harness).

!!! note
    Module D does **not** appear as a weighted term \(w_D \cdot S_D\). Its influence is entirely through \(\delta_C\).

## Non-Linear Safety Gate (\(\delta_C\))

\[
\delta_C =
\begin{cases}
1.0 & \text{if } C \ge 95 \\
\left(\dfrac{C}{100}\right)^{2} & \text{if } C < 95
\end{cases}
\]

| Module D Score (\(C\)) | Multiplier \(\delta_C\) | Operational Impact |
| --- | --- | --- |
| 95 – 100 | 1.00 | Pass: no score penalty |
| 90 | 0.81 | 19% composite reduction |
| 85 | 0.72 | 28% composite reduction |
| 75 | 0.56 | 44% composite reduction |
| 70 | 0.49 | Fail: 51% reduction — a decoy with perfect deception can still fail evaluation |
| 0 | 0.00 | UHQS collapses to 0 |

## Profile-Adaptive Weight Distributions

Weights **MUST** match the profile class declared in the TPS. All rows sum to **1.00**.

| Target Profile Category | Class enum | \(w_A\) | \(w_B\) | \(w_C\) | \(w_E\) | \(w_F\) |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| POSIX / Interactive Shells | `POSIX-Shell` | 0.20 | 0.25 | 0.20 | 0.15 | 0.20 |
| GenAI-augmented shells | `GenAI-Shell` | 0.20 | 0.25 | 0.20 | 0.15 | 0.20 |
| Low-Interaction Emulators | `Low-Interaction` | 0.30 | 0.15 | 0.25 | 0.10 | 0.20 |
| Industrial / OT / SCADA | `ICS-SCADA` | 0.35 | 0.20 | 0.15 | 0.10 | 0.20 |
| Web & Cloud APIs | `Web-API` | 0.25 | 0.20 | 0.20 | 0.15 | 0.20 |
| Database decoys | `Database` | 0.25 | 0.25 | 0.20 | 0.10 | 0.20 |

Industrial/OT/SCADA profiles assign the highest protocol fidelity weight (**0.35**).
`GenAI-Shell` **MUST** use the same weights as `POSIX-Shell` unless an accepted RFC
changes that mapping.

## Letter Grades (Normative Banding)

Implementations **MUST** map UHQS to letter grades as follows (aligned with the
reference harness):

| UHQS | Grade | Label |
| ---: | :---: | --- |
| 90 – 100 | A | Enterprise Grade |
| 80 – 89.99 | B | Production Baseline |
| 70 – 79.99 | C | Conditional — **not** approved for production |
| 50 – 69.99 | D | Needs Remediation |
| &lt; 50 | F | Fail |

## Production Baseline Profile (RECOMMENDED)

It is **RECOMMENDED** that organizations treat **UHQS > 80** with a passing Safety
Gate (C ≥ 95) as the minimum gate before deploying active decoys to production
networks. See [Status of This Document](status.md).

## Reference computation

These normative numbers **MUST** match `uhbs score` and `uhbs_core.uhqs_math.compute_uhqs`
(CLI / MCP / harness wrappers).

**Worked examples** (anonymous module scores used in unit tests — not live product fixtures):

| Class | Example scores | UHQS | Grade |
| --- | --- | ---: | --- |
| Low-Interaction | A=23.5, B=42.5, C=57.0, D=100, E=55.0, F=69.0 | **46.97** | F |
| POSIX-Shell | (see `posix-shell-lab` fixture path below) | **80.33** | B |

**Live published fixtures** (evaluation proof only) are listed under
[Conformance](../conformance/index.md) — e.g. Cowrie full lab **61.37** / D, not 46.97.
