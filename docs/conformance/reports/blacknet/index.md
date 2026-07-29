# blacknet — evaluation skipped (UHBS 4.2.2)

**Status:** Skipped · no UHQS numbers  
**Upstream:** [morian/blacknet](https://github.com/morian/blacknet)

This honeypot was queued for batch A grading but did not complete a reproducible lab run within the batch time box. Blacknet 2 is a distributed SSH sensor architecture: each honeypot (`blacknet-sensor`) expects TLS to a `blacknet-master`, MySQL schema initialization, and PKI material. Standing that stack up reliably exceeds the ~20 minute lab budget without inventing scores, so no UHBS run was executed.

Analysts should not cite UHQS, letter grades, or δ_C for this product until a successful `uhbs-lab` run produces `SCORECARD.txt` and `report.json` under `docs/conformance/reports/blacknet/`.

## Why skips still matter

Documenting skip reasons preserves vendor-neutral honesty: UHBS conformance entries are evaluation proofs, not catalog marketing. When dependencies or architecture block a fair dynamic sandbox (MySQL masters, PKI, Python 2 EOL stacks), we record the blocker instead of fabricating scores.

## Next steps for operators

If you operate this software in production, run your own isolated lab once the upstream install path is modernized or once you accept the operational cost of the full dependency stack. Then replay the tutorial pattern from a graded sibling product (for example heralding SSH or datatrap telnet) with inventory/TPS files adjusted to your listener.

- [Tutorial](TUTORIAL.md) · [Methodology](METHODOLOGY.md)

> Named product appears only under conformance — not a UHBS requirement or endorsement.
