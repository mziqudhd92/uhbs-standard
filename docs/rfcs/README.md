# RFCs

Normative specification changes for UHBS are proposed here as RFCs (request for comments). This process documents **proposed** changes to the evaluation framework — it is not a standards body, steering committee, or consortium process.

## How to use this folder

1. Copy [`0000-template.md`](0000-template.md) to a new numbered file when opening a proposal.
2. Describe the problem, the proposed change to UHQS / schemas / protocols, and migration impact.
3. Keep math truth in `src/uhbs_core/uhqs_math.py` if scoring changes; do not invent a second UHQS implementation.
4. Reference [GOVERNANCE.md](https://github.com/uhbs/uhbs-standard/blob/main/GOVERNANCE.md) in the repository root for maintainer expectations.

## What analysts should know

Published lab grades and scorecards under `docs/conformance/` remain authoritative for evaluation **proof** until an RFC is accepted **and** reflected in a released UHBS version. Do not treat draft RFCs as live scoring rules. UHBS version for current published proof is **4.2.2**.

## Trust

RFC text is discussion material for the beta framework. It does not create mandatory industry requirements or imply multi-party governance that does not exist today.
