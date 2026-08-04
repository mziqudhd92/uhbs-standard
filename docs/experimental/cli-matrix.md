# Matrix CLI (`uhbs matrix`)

Experimental. Offline. Does not change UHQS.

```bash
pip install 'uhbs[experimental]'
uhbs matrix example beginner --out matrix-beginner
uhbs matrix validate matrix-beginner/matrix-input.json
uhbs matrix analyze matrix-beginner/matrix-input.json --out matrix-report.json
uhbs matrix report matrix-report.json --format markdown
```
