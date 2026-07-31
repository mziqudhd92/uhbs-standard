# AEP Metrics (Informative)

These definitions are **informative**. They must not be converted into UHQS
module scores or letter grades. Status is `valid | inconclusive | control_failed |
not_computed`.

## Value of Deception (VoD)

\[
\mathrm{VoD} = \overline{U_D}(\mathrm{decoy}) - \overline{U_D}(\mathrm{reference})
\]

| Item | Rule |
| --- | --- |
| Inputs | Explicit `utility.weights` in the experiment manifest; observed defender outcomes / costs on trials |
| Units | Utility delta (study-defined) |
| Invalid uses | Substituting UHQS or `delta_uhqs`; omitting the utility model |
| Interpretation | Positive VoD means higher mean defender utility on the decoy arm under the declared model |

**Worked synthetic example:** weights `{detection: 1.0, intelligence_yield: 0.5,
defender_infra_cost: -0.1}` with mean utilities 1.4 (decoy) and 0.9 (reference)
⇒ VoD = 0.5.

## Fingerprinting Susceptibility Vector (FSV)

Report **per layer** (network, protocol, system, state):

- Confusion counts (TP/FP/TN/FN)
- TPR, FPR, balanced accuracy
- Bootstrap intervals when sample size allows

| Item | Rule |
| --- | --- |
| Inputs | `detector.layer`, `predicted_decoy`, `actual_is_decoy` on decoy/reference trials |
| Invalid uses | Collapsing to one global FSV scalar without meeting all control requirements (AEP never emits a global scalar today) |

## Dwell-Time Distortion Ratio (DTDR)

\[
\mathrm{DTDR} = \frac{\mathrm{median\_time}(\mathrm{decoy})}{\mathrm{median\_time}(\mathrm{reference})}
\]

When any trial is right-censored, AEP uses a **Kaplan–Meier** median estimator
and does not pretend an uncensored mean is valid.

| Item | Rule |
| --- | --- |
| Units | Ratio (dimensionless) |
| Invalid uses | Comparing against production assets; ignoring censoring |
| Tarpits | DTDR > 1 may be desirable even when Module E latency looks “worse” |

**Worked synthetic example:** decoy median 210 s, reference median 92.5 s ⇒
DTDR ≈ 2.27.

## Exploit Exhaustion Rate (EER)

Mean unique controlled capabilities expended on the decoy per session, as a
**fraction of the declared experiment budget** (`budget.max_unique_capabilities`).
Category counts (tools, credentials, payload families, ATT&CK IDs) are preserved.

| Item | Rule |
| --- | --- |
| Invalid uses | Treating EER as universal attacker cost outside the declared budget |

## Uncertainty

Bootstrap intervals use the analysis `--seed` for determinism. Low sample size,
high censoring, missing controls, and missing utility weights produce warnings
or `inconclusive` / `not_computed` statuses.
