# Universal Scoring Methodology (UHQS 4.0)

## Composite Score Formula

The **Universal Honeypot Quality Score (UHQS)** produces a normalized value from **0 to 100**:

\[
\mathrm{UHQS} = \delta_C \cdot (w_A \cdot S_A + w_B \cdot S_B + w_C \cdot S_C + w_E \cdot S_E + w_F \cdot S_F)
\]

| Symbol | Meaning |
| --- | --- |
| \(S_A, S_B, S_C, S_E, S_F\) | Normalized scores (0–100) for Modules A, B, C, E, and F |
| \(w_A, w_B, w_C, w_E, w_F\) | Dimension weights assigned by profile class |
| \(\delta_C\) | Safety Gate multiplier derived from Module D containment score \(C\) |

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

## Profile-Adaptive Weight Distributions

Weights adjust according to the honeypot profile class defined in the TPS. All rows sum to **1.00**.

| Target Profile Category | \(w_A\) Protocol | \(w_B\) Behavior | \(w_C\) Telemetry | \(w_E\) Scale | \(w_F\) Static |
| --- | ---: | ---: | ---: | ---: | ---: |
| POSIX / Interactive Shells | 0.20 | 0.25 | 0.20 | 0.15 | 0.20 |
| Low-Interaction Emulators | 0.30 | 0.15 | 0.25 | 0.10 | 0.20 |
| Industrial / OT / SCADA | 0.35 | 0.20 | 0.15 | 0.10 | 0.20 |
| Web & Cloud APIs | 0.25 | 0.20 | 0.20 | 0.15 | 0.20 |

Industrial/OT/SCADA profiles assign the highest protocol fidelity weight (**0.35**), reflecting the criticality of exact protocol emulation in operational technology environments.

## Letter Grades (Recommended Banding)

| UHQS | Grade | Label |
| ---: | :---: | --- |
| 90 – 100 | A | Enterprise Grade |
| 80 – 89.9 | B | Production Candidate |
| 70 – 79.9 | C | Conditional |
| 60 – 69.9 | D | Needs Remediation |
| &lt; 60 | F | Fail |

Bands are advisory for communication; the normative result is the numeric UHQS and Safety Gate outcome.
