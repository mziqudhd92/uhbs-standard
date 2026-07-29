# Lab patch: tolerate missing X-Forwarded-For

Upstream `emulator/server/persistence_decorator_web.py` requires
`HTTP_X_FORWARDED_FOR` (HAProxy). Direct lab access to `:8080` falls back to
`REMOTE_ADDR`.

```diff
-            client_ip = environment["HTTP_X_FORWARDED_FOR"]
+            client_ip = environment.get("HTTP_X_FORWARDED_FOR") or environment.get(
+                "REMOTE_ADDR", "0.0.0.0"
+            )
```

## Why this patch note exists

LLMPot lab grading required an XFF / reverse-proxy fallback adjustment so the harness could reach the HTTP surface consistently in the isolated Docker network. This note documents that lab-only change for replication. It is **not** a recommendation to patch production honeypots without review. Prefer upstream configuration when available; keep Module F source trees honest about what was graded. See the LLMPot methodology and tutorial under `docs/conformance/reports/llmpot/` for the full evaluation context and SCORECARD proof links.

## Analyst / replication checklist

- Apply only in the lab checkout used for Module F / dynamic runs described in the tutorial.
- Confirm HTTP probes still hit the graded listener after the change.
- Cite UHQS from `full/SCORECARD.txt`, not from this patch note alone.
- UHBS 4.2.2 proof remains informative evaluation evidence — not an endorsement of LLMPot.
