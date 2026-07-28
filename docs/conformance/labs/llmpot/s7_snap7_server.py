#!/usr/bin/env python3
"""UHBS lab S7 listener using Snap7 — same stack LLMPot trains against.

LLMPot's published ByT5 S7 Lightning weights are not in the public tree
(HF sample cv43/llmpot is Modbus-only). Dataset generation uses
``dataset_generation.s7comm.no_logic_server.NoLogicServer`` (python-snap7).
This runner is that gold PLC surface for UHBS ``s7comm`` grading.
"""
from __future__ import annotations

import argparse
import logging
import time
from ctypes import c_ubyte

from snap7.server import Server
from snap7.type import SrvArea


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--host", default="0.0.0.0")
    p.add_argument("--port", type=int, default=102)
    p.add_argument("--db-count", type=int, default=40)
    p.add_argument("--db-size", type=int, default=100)
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    server = Server()
    try:
        from snap7.type import Parameter
        server.set_param(Parameter.MaxClients, 256)
    except Exception:
        pass
    dbs = []
    for index in range(args.db_count):
        buf = (c_ubyte * args.db_size)()
        dbs.append(buf)  # keep refs alive
        server.register_area(SrvArea.DB, index, buf)

    server.start_to(args.host, args.port)
    print(f"listening S7comm on {args.host}:{args.port}", flush=True)
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        server.stop()
        server.destroy()


if __name__ == "__main__":
    main()
