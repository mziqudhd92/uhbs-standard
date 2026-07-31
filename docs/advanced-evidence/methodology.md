# AEP Methodology

**Status:** Informative · offline controlled experiments  
**Scope:** Laboratory / sandbox only — never production or unauthorized targets

## Three-arm design

Where applicable, declare:

1. **Decoy under test** — the honeypot / deception surface being studied  
2. **Matched genuine/reference target** — a safe lab reference with comparable
   role (never a production asset)  
3. **Evaluator capability / functional control** — proves the evaluator (human,
   script, or agent) can perform the task on a known-good surface

Refuse analysis without decoy **and** reference. Require evaluator control before
strong claims about attacker capability.

## Design requirements

- Randomize decoy/reference assignment (declare method + seed)
- Stratify humans/agents by capability tier when relevant
- Hold **task**, **budget**, **timeout**, and **starting knowledge** constant
- Repeat trials; pre-register hypothesis and primary outcome
- Record right-censoring (timeouts) explicitly
- Report sample size, medians/quantiles, confidence intervals, effect sizes,
  censoring rate, and multi-run variance
- For human CTF studies: consent, privacy minimization, ethics/IRB where applicable
- For ICS anti-honeypot testing: safe lab fixtures and capability tiers only

## Safe references

Construct references from lab fixtures, synthetic services, or disposable VMs.
Do **not** expose production process-control, customer data, or live attacker
infrastructure to AEP collection. AEP itself never connects to targets — collectors
are a separate, out-of-band step that must emit local trial JSONL.

## Protocol notes

| Class | Notes |
| --- | --- |
| Stateful shells | Session boundary = login→logout/timeout; track command exchanges |
| HTTP / LLM | Pair decoy with matched API surface; record token costs in `costs` |
| Tarpits | Long dwell may be beneficial in AEP while Module E still grades latency |
| ICS/OT | Prefer memory/register consistency probes on lab PLCs; never production OT |

## Evidence manifest (minimum)

- Target / reference versions and digests  
- TPS / profile class  
- Randomization seeds  
- Attacker identity/version or agent build  
- Task description and budget  
- Trial count and timeouts  
- Raw-event hashes (`raw_evidence_sha256`)  
- Analysis tool version and seed  

See also [Runbook](runbook.md) and [Reporting](reporting.md).
