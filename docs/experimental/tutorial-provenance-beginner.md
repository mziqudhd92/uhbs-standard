# Beginner tutorial: host provenance

```bash
pip install 'uhbs[experimental]'
uhbs provenance example beginner --out prov-beginner
uhbs provenance summarize prov-beginner/events.jsonl \
  --collector prov-beginner/collector.json --out summary.json
uhbs provenance validate summary.json
```

For rate-limit demos:

```bash
uhbs provenance example advanced --out prov-advanced
uhbs provenance summarize prov-advanced/events.jsonl --max-events 10 --out capped.json
```

Expect `dropped > 0` and `overflow: true`. Digests cover filtered data only.
