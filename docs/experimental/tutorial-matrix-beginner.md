# Beginner tutorial: five-dimension matrix

Offline, deterministic, **UHQS unchanged**.

## 1. Install

```bash
python -m venv .venv && source .venv/bin/activate
pip install 'uhbs[experimental]'
```

## 2. Export and analyze

```bash
uhbs matrix example beginner --out matrix-beginner
cd matrix-beginner
uhbs matrix validate matrix-input.json
uhbs matrix analyze matrix-input.json --out matrix-report.json
uhbs matrix report matrix-report.json
```

Notice `interaction_depth` is **missing** (not scored as 0) and the composite averages only present dimensions.

## Terms

| Term | Meaning |
| --- | --- |
| Dimension | One of five experimental quality axes |
| Missing | Not collected — never silently filled |
| Composite | Equal-weight mean of *present* scored dimensions only |
