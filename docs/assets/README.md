# Terminal demo assets

- `uhbs-quickstart.cast` — asciinema v2 recording (source)
- `uhbs-quickstart.gif` — README embed (rendered with [`agg`](https://docs.asciinema.org/manual/agg/))
- `build_quickstart_cast.py` — regenerates the cast (install → start → full grades)

The cast must use **CRLF** (`\r\n`) line endings. Raw LF alone causes a
staircase layout in `agg` / asciinema (no tty `ONLCR`). Keep lines shorter than
the cast `width`.

Regenerate:

```bash
python docs/assets/build_quickstart_cast.py
agg --cols 100 --rows 32 --font-size 13 --speed 0.9 \
  docs/assets/uhbs-quickstart.cast /tmp/uhbs-quickstart-raw.gif
gifsicle -O3 --lossy=55 --colors 128 \
  -o docs/assets/uhbs-quickstart.gif /tmp/uhbs-quickstart-raw.gif
```

Play: `asciinema play docs/assets/uhbs-quickstart.cast`
