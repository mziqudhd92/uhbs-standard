# Tutorial: glastopf (not graded — Docker build failed)

**Upstream:** [mushorg/glastopf](https://github.com/mushorg/glastopf)

```bash
docker build -f .local/labs/glastopf/Dockerfile -t glastopf:uhbs-lab .local/labs/glastopf
# fails: ubuntu:14.04.1 schema 1 manifest removed
```

Modernize base image and Python/PHP dependencies before re-attempting HTTP grading on `127.0.0.1:17082`.

## What this skip means for analysts

This tutorial cannot reproduce a UHBS UHQS grade for this product in the current lab environment. The product hub explains the blocker. Do **not** invent scores. When the blocker is cleared (API keys, backend dependency, or buildable image), re-queue with the same proof pattern as graded labs: `SCORECARD.txt`, `report.json`, protocol hub with verbatim modules, and CTI/blue-team reading via [READING-UHQS.md](../READING-UHQS.md).

## Trust limits

UHBS 4.2.2 evaluation notes are informative only — not certifications or endorsements. Product names appear only under conformance as survey/evaluation evidence.
