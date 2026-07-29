# Terminal demo assets

- `uhbs-quickstart.cast` — asciinema v2 recording (source)
- `uhbs-quickstart.gif` — README embed (rendered with [`agg`](https://docs.asciinema.org/manual/agg/))

Regenerate locally (needs a reachable decoy on `:18080` and a built wheel with packaged schemas):

```bash
python -m build -w
# start HellPot or another HTTP decoy on 127.0.0.1:18080
bash .local/demo-record/demo.sh   # capture real output
# then rebuild GIF from docs/assets/uhbs-quickstart.cast via agg
agg --cols 100 --rows 28 --font-size 14 --speed 1.4 \
  docs/assets/uhbs-quickstart.cast docs/assets/uhbs-quickstart.gif
```

Play the cast: `asciinema play docs/assets/uhbs-quickstart.cast`
