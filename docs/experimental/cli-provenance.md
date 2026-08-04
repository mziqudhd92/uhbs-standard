# Provenance CLI (`uhbs provenance`)

Experimental. Collector-neutral. Rate-limits before hashing. Does not change UHQS.

```bash
pip install 'uhbs[experimental]'
uhbs provenance example beginner --out prov-beginner
uhbs provenance summarize prov-beginner/events.jsonl \
  --collector prov-beginner/collector.json --out provenance-summary.json
uhbs provenance validate provenance-summary.json
uhbs provenance attach provenance-summary.json --manifest MANIFEST.json
```

Use `--max-events` / `--max-bytes` to bound artifact size. Non-Linux platforms report `not_applicable`.
