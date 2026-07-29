# Terminal demo assets

- `uhbs-lab-demo.cast` — asciinema v2 recording (source)
- `uhbs-lab-demo.gif` — README embed (rendered with [`agg`](https://docs.asciinema.org/manual/agg/))
- `build_quickstart_cast.py` — regenerates the cast (install → start → full grades)

The cast must use **CRLF** (`\r\n`) line endings. Raw LF alone causes a
staircase layout in `agg` / asciinema (no tty `ONLCR`). Keep lines shorter than
the cast `width`.

Regenerate:

```bash
python docs/assets/build_quickstart_cast.py
agg --cols 100 --rows 32 --font-size 13 --speed 0.9 \
  docs/assets/uhbs-lab-demo.cast /tmp/uhbs-lab-demo-raw.gif
gifsicle -O3 --lossy=80 --colors 64 \
  -o docs/assets/uhbs-lab-demo.gif /tmp/uhbs-lab-demo-raw.gif
```

Play: `asciinema play docs/assets/uhbs-lab-demo.cast`
