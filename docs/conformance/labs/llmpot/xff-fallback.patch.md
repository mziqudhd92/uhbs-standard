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
