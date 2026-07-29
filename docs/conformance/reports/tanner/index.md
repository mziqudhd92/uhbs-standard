# tanner — skipped (analysis backend, not HTTP decoy)

**Status:** Informative · **not graded**  
**Upstream:** [https://github.com/mushorg/tanner](https://github.com/mushorg/tanner)

TANNER is a **remote HTTP analysis and classification service** for [SNARE](https://github.com/mushorg/snare), not a standalone Internet-facing HTTP honeypot. Upstream install docs require Redis, a PHP sandbox (`phpox`), Docker, and typically SNARE as the HTTP front-end. The aiohttp **web UI** exposes operator dashboards, not the vulnerability-emulation surface UHBS HTTP modules probe (paths, auth, error pages, exploit-shaped bodies).

Attempting to grade TANNER’s API/UI would measure a control plane, while grading SNARE without TANNER was already deferred in this conformance round. Standing up Redis + phpox + TANNER + SNARE exceeds the batch time budget and duplicates SNARE’s dependency chain. UHBS records a skip note with **no UHQS** until a documented SNARE+TANNER compose stack exposes a single HTTP listener suitable for `web_api_http` TPS.

See [TUTORIAL.md](TUTORIAL.md) · [METHODOLOGY.md](METHODOLOGY.md).

## Trust

Informative UHBS 4.2.2 gap note — [READING-UHQS.md](../READING-UHQS.md)
