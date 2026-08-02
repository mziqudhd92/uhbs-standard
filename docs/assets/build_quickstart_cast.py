#!/usr/bin/env python3
"""Build docs/assets/uhbs-lab-demo.cast (CRLF — required for agg/asciinema).

Usage:
  python docs/assets/build_quickstart_cast.py
  agg --cols 100 --rows 32 --font-size 13 --speed 0.9 \\
    docs/assets/uhbs-lab-demo.cast /tmp/uhbs-lab-demo-raw.gif
  gifsicle -O3 --lossy=80 --colors 64 \\
    -o docs/assets/uhbs-lab-demo.gif /tmp/uhbs-lab-demo-raw.gif
"""
from __future__ import annotations

import json
import textwrap
from pathlib import Path

COLS = 100
ROWS = 32
OUT = Path(__file__).resolve().parent / "uhbs-lab-demo.cast"

PLUGINS = (
    "bluetooth, dhcp, dns, ftp, generic, git, http, httpproxy, imap, ipp, "
    "irc, kubernetes, ldap, mcp, memcache, modbus, mongodb, mssql, mysql, ntp, "
    "oracle, pjl, pop3, postgres, rdp, redis, s7comm, sip, smb, smtp, snmp, "
    "socks5, ssh, telnet, tftp, vnc"
)

COWRIE_CARD = """\
====================================================================================
                  UNIVERSAL HONEYPOT BENCHMARK SCORECARD v4.3.6
====================================================================================
Target System         : cowrie-ssh
System Profile Class  : Low-Interaction
Protocols             : ssh
Evaluation Type       : Full-Spectrum (Static Audit + Dynamic Sandbox)
------------------------------------------------------------------------------------
EVALUATION MODULE                     SCORE (0-100)    WEIGHT    STATUS
------------------------------------------------------------------------------------
Module A: Protocol Fidelity         :  57.1/100       0.30     PARTIAL
Module B: Behavioral Realism        :  60.0/100       0.15     PARTIAL
Module C: Telemetry Quality         :  55.0/100       0.25     PARTIAL
Module D: Safety & Containment (C)  : 100.0/100       GATE     PASSED
Module E: Scalability & Latency     :  75.0/100       0.10     PASSED
Module F: Static Code Audit         :  70.0/100       0.20     PASSED
------------------------------------------------------------------------------------
SAFETY GATE MULTIPLIER                : δ_C = 1.0
FINAL COMPOSITE SCORE (UHQS 4.3.6)      : 61.37 / 100
OVERALL EVALUATION GRADE              : GRADE D (Needs Remediation)
===================================================================================="""

CONPOT_CARD = """\
====================================================================================
                  UNIVERSAL HONEYPOT BENCHMARK SCORECARD v4.3.6
====================================================================================
Target System         : conpot
System Profile Class  : ICS-SCADA
Protocols             : modbus
Evaluation Type       : Full-Spectrum (Static Audit + Dynamic Sandbox)
------------------------------------------------------------------------------------
EVALUATION MODULE                     SCORE (0-100)    WEIGHT    STATUS
------------------------------------------------------------------------------------
Module A: Protocol Fidelity         :  79.0/100       0.35     PASSED
Module B: Behavioral Realism        :  42.5/100       0.20     PARTIAL
Module C: Telemetry Quality         :  55.0/100       0.15     PARTIAL
Module D: Safety & Containment (C)  :  90.0/100       GATE     PASSED
Module E: Scalability & Latency     : 100.0/100       0.10     PASSED
Module F: Static Code Audit         :  70.0/100       0.20     PASSED
------------------------------------------------------------------------------------
SAFETY GATE MULTIPLIER                : δ_C = 0.81
FINAL COMPOSITE SCORE (UHQS 4.3.6)      : 55.4 / 100
OVERALL EVALUATION GRADE              : GRADE D (Needs Remediation)
===================================================================================="""

HELLPOT_CARD = """\
====================================================================================
                  UNIVERSAL HONEYPOT BENCHMARK SCORECARD v4.3.6
====================================================================================
Target System         : HellPot-http
System Profile Class  : Web-API
Protocols             : http
Evaluation Type       : Full-Spectrum (Static Audit + Dynamic Sandbox)
------------------------------------------------------------------------------------
EVALUATION MODULE                     SCORE (0-100)    WEIGHT    STATUS
------------------------------------------------------------------------------------
Module A: Protocol Fidelity         :  86.8/100       0.25     PASSED
Module B: Behavioral Realism        :  82.5/100       0.20     PASSED
Module C: Telemetry Quality         :  55.0/100       0.20     PARTIAL
Module D: Safety & Containment (C)  :  75.0/100       GATE     PASSED
Module E: Scalability & Latency     : 100.0/100       0.15     PASSED
Module F: Static Code Audit         :  69.0/100       0.20     PARTIAL
------------------------------------------------------------------------------------
SAFETY GATE MULTIPLIER                : δ_C = 0.5625
FINAL COMPOSITE SCORE (UHQS 4.3.6)      : 43.87 / 100
OVERALL EVALUATION GRADE              : GRADE F (Fail)
===================================================================================="""


class Cast:
    def __init__(self) -> None:
        self.t = 0.0
        self.events: list[tuple[float, str, str]] = []

    def emit(self, s: str, dt: float = 0.02) -> None:
        self.t += dt
        self.events.append((round(self.t, 3), "o", s))

    def nl(self, dt: float = 0.05) -> None:
        self.emit("\r\n", dt)

    def out_line(self, line: str = "", dt: float = 0.04) -> None:
        if len(line) >= COLS:
            raise SystemExit(f"line too long ({len(line)}): {line!r}")
        self.emit(line + "\r\n", dt)

    def out_block(self, text: str, line_dt: float = 0.08) -> None:
        # Emit 2–3 lines per event to cut GIF frames without looking jumpy.
        buf: list[str] = []
        for line in text.splitlines():
            if len(line) >= COLS:
                raise SystemExit(f"line too long ({len(line)}): {line!r}")
            buf.append(line)
            if len(buf) >= 3:
                self.emit("\r\n".join(buf) + "\r\n", line_dt)
                buf = []
        if buf:
            self.emit("\r\n".join(buf) + "\r\n", line_dt)

    def wrap_out(self, text: str, *, indent: str = "", dt: float = 0.04) -> None:
        width = COLS - 1 - len(indent)
        for line in textwrap.wrap(
            text, width=width, break_long_words=False, break_on_hyphens=False
        ):
            self.out_line(indent + line, dt)

    def type_cmd(self, lines: list[str], *, char_dt: float = 0.07) -> None:
        """Type commands in small bursts (readable, fewer GIF frames)."""
        for i, line in enumerate(lines):
            if i == 0:
                self.emit("$ ", 0.55)
                body = line
            else:
                self.emit("> ", 0.28)
                body = line[2:] if line.startswith("  ") else line
            if len(("$ " if i == 0 else "> ") + body) >= COLS:
                raise SystemExit(f"cmd too long: {body!r}")
            j = 0
            while j < len(body):
                n = 1 if j < 3 else 4
                self.emit(body[j : j + n], char_dt)
                j += n
            self.nl(0.22)

    def pause(self, seconds: float) -> None:
        self.emit("", seconds)


def build() -> None:
    c = Cast()

    c.out_line("# UHBS — install honeypots, then full UHQS (Cowrie · Conpot · HellPot)", 0.7)
    c.nl(0.35)

    c.type_cmd(["python3 -m venv .venv && source .venv/bin/activate"], char_dt=0.05)
    c.nl(0.25)

    c.type_cmd(["pip install -q 'uhbs[lab]'"], char_dt=0.055)
    c.pause(1.1)
    c.nl(0.2)

    c.out_line("# Install Cowrie (SSH) + Conpot (ICS / Modbus) from PyPI", 0.55)
    c.type_cmd(["pip install cowrie conpot"], char_dt=0.06)
    c.pause(0.4)
    c.out_line("Collecting cowrie", 0.08)
    c.out_line("  Downloading cowrie-3.0.10-py3-none-any.whl (9.0 kB)", 0.07)
    c.out_line("Collecting conpot", 0.08)
    c.out_line("  Downloading conpot-0.6.0-py3-none-any.whl (7.9 kB)", 0.07)
    c.out_line("Collecting twisted==26.4.0 (from cowrie)", 0.07)
    c.out_line("Collecting gevent>=1.0 (from conpot)", 0.07)
    c.out_line("Collecting pysnmp (from conpot)", 0.07)
    c.out_line("Building wheels for collected packages: crc16, hpfeeds3, pycrypto", 0.08)
    c.pause(0.9)
    c.wrap_out(
        "Successfully installed cowrie-3.0.10 conpot-0.6.0 twisted-26.4.0 "
        "gevent-26.7.0 pysnmp-7.1.27 bcrypt-5.0.0 cryptography-49.0.0 ...",
        dt=0.06,
    )
    c.nl(0.35)

    c.out_line("# Start Cowrie (SSH :2222)", 0.55)
    c.type_cmd(["cowrie init && cowrie start"], char_dt=0.06)
    c.out_line("Wrote etc/cowrie.cfg", 0.1)
    c.out_line("Created var/log/cowrie, var/lib/cowrie, var/run", 0.1)
    c.pause(0.7)
    c.out_line("cowrie is running (PID: 18421).", 0.2)
    c.nl(0.3)

    c.out_line("# Start Conpot Modbus (:5020) — lab Docker image (pkg_resources-safe)", 0.6)
    c.type_cmd(
        [
            "docker run -d --name conpot-lab \\",
            "  -p 5020:5020 conpot:lab-fixed",
        ],
        char_dt=0.05,
    )
    c.out_line("5e38ec39badf912353351b7790abe4df9c9da0a7d8a811eeba53c8f9f3deb5d0", 0.25)
    c.nl(0.25)

    c.out_line("# Start HellPot HTTP tarpit (:18080)", 0.55)
    c.type_cmd(
        [
            "docker run -d --name HellPot-lab \\",
            "  -p 18080:8080 hellpot:uhbs-lab",
        ],
        char_dt=0.05,
    )
    c.out_line("b184c7a3226f3f2321da836dfccda0fe67388d6b245498ed6723274bc6c7f4eb", 0.25)
    c.nl(0.4)

    def grade(
        title: str,
        cmd: list[str],
        target_line: str,
        card: str,
        wrote: str,
    ) -> None:
        c.out_line(title, 0.65)
        c.type_cmd(cmd, char_dt=0.048)
        c.pause(0.65)
        c.wrap_out(target_line, dt=0.1)
        c.wrap_out(f"plugins available: {PLUGINS}", indent="    ", dt=0.05)
        c.pause(2.0)
        c.out_line("    phase=profile+static+sandbox+dynamic+score  modules=A–F", 0.25)
        c.pause(2.8)
        c.out_block(card, line_dt=0.1)
        c.out_line(f"Wrote {wrote}/report.json", 0.12)
        c.out_line(f"Wrote {wrote}/manifest.json", 0.12)
        c.nl(0.45)

    grade(
        "# Full UHQS — Cowrie SSH",
        [
            "UHBS_AIRGAP_ATTESTED=1 uhbs-lab \\",
            "  --inventory docs/conformance/labs/cowrie/inventory.yaml \\",
            "  --target cowrie-ssh \\",
            "  --tps docs/conformance/labs/cowrie/low_interaction_ssh_full.yaml \\",
            "  --phases profile,static,sandbox,dynamic,score \\",
            "  --modules A,B,C,D,E,F --out ./out-cowrie-full",
        ],
        "==> UHBS v4 target=cowrie-ssh class=Low-Interaction "
        "protocols=['ssh'] phases=['profile', 'static', 'sandbox', 'dynamic', 'score']",
        COWRIE_CARD,
        "./out-cowrie-full",
    )

    grade(
        "# Full UHQS — Conpot Modbus",
        [
            "UHBS_AIRGAP_ATTESTED=1 uhbs-lab \\",
            "  --inventory docs/conformance/labs/conpot/inventory.yaml \\",
            "  --target conpot \\",
            "  --tps docs/conformance/labs/conpot/ics_modbus_full.yaml \\",
            "  --phases profile,static,sandbox,dynamic,score \\",
            "  --modules A,B,C,D,E,F --out ./out-conpot-full",
        ],
        "==> UHBS v4 target=conpot class=ICS-SCADA "
        "protocols=['modbus'] phases=['profile', 'static', 'sandbox', 'dynamic', 'score']",
        CONPOT_CARD,
        "./out-conpot-full",
    )

    grade(
        "# Full UHQS — HellPot HTTP",
        [
            "UHBS_AIRGAP_ATTESTED=1 uhbs-lab \\",
            "  --inventory docs/conformance/labs/HellPot/inventory.yaml \\",
            "  --target HellPot-http \\",
            "  --tps docs/conformance/labs/HellPot/web_api_http_full.yaml \\",
            "  --phases profile,static,sandbox,dynamic,score \\",
            "  --modules A,B,C,D,E,F --out ./out-hellpot-full",
        ],
        "==> UHBS v4 target=HellPot-http class=Web-API "
        "protocols=['http'] phases=['profile', 'static', 'sandbox', 'dynamic', 'score']",
        HELLPOT_CARD,
        "./out-hellpot-full",
    )

    c.out_line("# Summary", 0.5)
    c.out_line("  Cowrie   UHQS 61.37   GRADE D   δ_C=1.0", 0.18)
    c.out_line("  Conpot   UHQS 55.40   GRADE D   δ_C=0.81", 0.18)
    c.out_line("  HellPot  UHQS 43.87   GRADE F   δ_C=0.5625", 0.18)
    c.nl(0.25)
    c.out_line("# Docs: https://uhbs.github.io/uhbs-standard/", 0.4)
    c.nl(0.2)
    c.pause(2.5)

    header = {
        "version": 2,
        "width": COLS,
        "height": ROWS,
        "timestamp": 1785334800,
        "env": {"SHELL": "/bin/bash", "TERM": "xterm-256color"},
        "title": "UHBS: install Cowrie/Conpot + full UHQS grades",
    }
    lines = [json.dumps(header, separators=(",", ":"))]
    for ts, kind, data in c.events:
        lines.append(
            json.dumps([ts, kind, data], ensure_ascii=False, separators=(",", ":"))
        )
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    text = "".join(e[2] for e in c.events)
    bare = sum(
        1
        for i, ch in enumerate(text)
        if ch == "\n" and (i == 0 or text[i - 1] != "\r")
    )
    print(f"wrote {OUT}")
    print(f"events={len(c.events)} duration={c.t:.1f}s bare_LF={bare} cols={COLS}")


if __name__ == "__main__":
    build()
