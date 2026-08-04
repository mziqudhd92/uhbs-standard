# Experimental matrix — beginner

Offline synthetic fixture for `uhbs matrix`.

```bash
uhbs matrix example beginner --out matrix-beginner
cd matrix-beginner
uhbs matrix validate matrix-input.json
uhbs matrix analyze matrix-input.json --out matrix-report.json
uhbs matrix report matrix-report.json --format markdown
```

Does **not** change UHQS.
