# glastopf — skipped (legacy image unbuildable)

**Status:** Informative · **not graded**  
**Upstream:** [https://github.com/mushorg/glastopf](https://github.com/mushorg/glastopf)

Glastopf’s published `Dockerfile` targets **`ubuntu:14.04.1`**, whose registry manifest uses deprecated Docker schema 1. Modern Docker Desktop (2026) rejects that base with: *“manifest version 2, schema 1 has been removed.”* A rebuild would require rewriting the image (new base, Python 2.7/PHP sandbox migration, BFR extension build) — well beyond the ~20 minute lab budget for this batch.

Because no runnable container could be produced, UHBS does **not** publish UHQS for glastopf here. Re-queue after a maintained lab Dockerfile (similar to other mushorg stacks) or an official multi-arch image exists.

See [TUTORIAL.md](TUTORIAL.md) · [METHODOLOGY.md](METHODOLOGY.md).

## Trust

Informative UHBS 4.2.2 gap note — [READING-UHQS.md](../READING-UHQS.md)
