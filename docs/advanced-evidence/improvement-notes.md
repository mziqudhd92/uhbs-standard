# Informative UHBS Improvements (No Normative Scoring Change)

**Status:** Informative RFC-style notes · UHBS 4.3.6 unchanged

These improvements are recommended **without** changing UHQS, weights, δ_C, or
letter grades. Normative scoring changes require a separate RFC with corpus
evidence, weight sensitivity, backward compatibility, and independent
reproduction.

## Adopt now (informative)

1. **Evaluation-intent metadata** — label reports as asset quality vs program
   maturity vs campaign vs topology so UHQS is not misused as an org score.
2. **Engagement-yield metrics** — session duration, exchanges, telemetry yield
   (via AEP / future informative `report.json` fields).
3. **Attacker- and defender-cost reporting** — time, tokens, infra cost; tarpit
   delay may be beneficial in AEP while Module E retains latency semantics.
4. **Cloud / decoy-object coverage map** — CLOUDBURST + D3FEND gap analysis for
   IAM tokens, presigned URLs, K8s secrets, decoy files/credentials.

## Experiment (AEP)

1. Paired decoy vs reference + evaluator control  
2. FSV across network/protocol/system/state  
3. DTDR with censoring-aware medians  
4. EER against declared budgets  
5. VoD with explicit utility models (never `delta_uhqs`)  
6. ICS memory/register consistency probes (lab only)

## Map only / out of scope for UHQS

CDMM, Cyber-Deception Chain, 7-Criteria procurement checklists, Belief-Scepticism
psychology models, game-theoretic placement planners, MTD mutation benchmarks,
and topology camouflage systems remain outside generic UHQS.

## Validation gate before any UHQS proposal

For each candidate metric:

- Construct validity and collection method  
- Failure modes and minimum sample size  
- Reproducibility across ≥3 profile classes  
- Variance and correlation with Modules A–F  
- Informative `report.json` field first  
- Separate RFC for any weight/formula change  

See [ROADMAP](../roadmap.md) for maturity sequencing.
