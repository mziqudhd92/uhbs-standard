# Methodology: sentrypeer

**Status:** Informative · evaluation proof  
**UHBS version:** 4.2.2  
**Upstream:** [https://github.com/SentryPeer/SentryPeer](https://github.com/SentryPeer/SentryPeer) (`pushed_at` `2026-07-27`)

## Environment

- Docker network `uhbs-lab`; inventory host `127.0.0.1` with published lab port
- Harness: local `uhbs-lab` from editable install (`pip install -e ".[dev,lab,mcp]"`)
- Quick: `UHBS_QUICK=1`, `--skip-sast-tools`
- Full: formal TPS timing samples, `--skip-sast-tools` (SAST optional follow-up)

## Limitations

- Evaluation proof only — not an endorsement
- Single-protocol surface graded where noted in the hub
- Air-gap attested via `UHBS_AIRGAP_ATTESTED=1` for local lab runs
