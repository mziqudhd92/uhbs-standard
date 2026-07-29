# Methodology: pyrdp UHBS lab

**UHBS:** 4.2.2 · Graded **rdp** Low-Interaction decoy.  
Quick **33.93 / F**, full **33.93 / F**.

## Analyst trust notes

- **Role:** RDP MITM listener graded as a decoy surface; slim image runs pyrdp-mitm on 3389 with loopback relay target for lab containment.
- **Evidence primary sources:** `full/SCORECARD.txt`, `full/report.json`, this methodology, and the tutorial commands.
- **Air-gap / Safety:** lab runs used `UHBS_AIRGAP_ATTESTED=1`; still isolate honeypot networks in real deployments.
- **Not in scope:** UHBS does not certify detection content packs, MITRE mappings, or production SIEM pipelines.
- **Reading guide:** [READING-UHQS.md](../READING-UHQS.md)

## Environment & containment

Labs use Docker network `uhbs-lab` with `127.0.0.1` host binds only. Module F uses `source_root` pointing at the cloned upstream tree under `.local/labs/pyrdp`.

## Evidence hierarchy

1. `full/SCORECARD.txt` (human-readable proof)
2. `full/report.json` (machine-readable)
3. This methodology (class, protocol scope, known limits)
4. Tutorial commands (replication)

Quick runs are for iteration speed. Prefer **full** when publishing or comparing products.

## What UHBS does not claim

Not a vulnerability assessment of every dependency CVE, not a guarantee of Internet engagement volume, not a SIEM content pack, and not an endorsement of the named open-source project.
