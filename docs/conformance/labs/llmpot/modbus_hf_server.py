#!/usr/bin/env python3
"""UHBS lab Modbus TCP front-end for LLMPot HF weights (cv43/llmpot).

Upstream emulator/server/modbus_app.py expects Lightning last.ckpt under a
non-published honeypot/ path and hard-codes CUDA. This adapter uses the
public Hugging Face sample model on CPU so UHBS can grade Modbus TCP locally.
"""
from __future__ import annotations

import argparse
import os
import socketserver

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


class Handler(socketserver.BaseRequestHandler):
    tokenizer = None
    model = None

    def handle(self) -> None:
        try:
            data = self.request.recv(4096)
            if not data:
                return
            incoming = data.hex()
            tok = Handler.tokenizer
            model = Handler.model
            assert tok is not None and model is not None
            inputs = tok(incoming, return_tensors="pt")
            outs = model.generate(**inputs, max_new_tokens=128)
            out = tok.decode(outs[0], skip_special_tokens=True)
            try:
                raw = bytes.fromhex(out.strip())
            except ValueError:
                raw = data[:7] + b"\x83\x01" if len(data) >= 7 else data
            self.request.sendall(raw)
        except Exception:
            try:
                self.request.close()
            except OSError:
                pass


class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--host", default="0.0.0.0")
    p.add_argument("--port", type=int, default=5020)
    p.add_argument("--model", default=os.environ.get("LLMPOT_MODEL", "cv43/llmpot"))
    args = p.parse_args()
    print(f"loading model {args.model} (CPU)…", flush=True)
    Handler.tokenizer = AutoTokenizer.from_pretrained(args.model)
    Handler.model = AutoModelForSeq2SeqLM.from_pretrained(args.model)
    Handler.model.eval()
    print(f"listening Modbus TCP on {args.host}:{args.port}", flush=True)
    with ThreadedServer((args.host, args.port), Handler) as srv:
        srv.serve_forever()


if __name__ == "__main__":
    main()
