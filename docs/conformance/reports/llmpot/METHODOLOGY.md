# Methodology: LLMPot UHBS lab

**Status:** Informative  
**UHBS:** 4.2.2  
**Upstream commit:** `9568b5ffe6f3626c70078e53eacaac4a9fcf1b9e`

## What LLMPot speaks vs what UHBS can grade

| LLMPot surface | UHBS plugin | Graded? | Notes |
| --- | --- | --- | --- |
| Modbus TCP (ByT5) | `modbus` | **yes** | Upstream `modbus_app.py` needs unpublished Lightning `last.ckpt` + CUDA. Lab uses HF [`cv43/llmpot`](https://huggingface.co/cv43/llmpot) via `docs/conformance/labs/llmpot/modbus_hf_server.py` on CPU |
| S7comm | `s7comm` | **yes** | No public ByT5 S7 weights. Lab uses Snap7 `NoLogicServer`-equivalent (`s7_snap7_server.py`) — the same gold PLC LLMPot’s dataset generator trains against |
| WAGO web (Flask) | `http` | **yes** | Lab X-Forwarded-For fallback patch |
| Honeyd WAGO (`docker/`) | ssh/http/modbus mix | no | Not stood up in this lab |

## Environment

- Web: `compose.lab.yaml` → mongo + `web_app` on host `127.0.0.1:18081`
- Modbus: `llmpot-modbus:uhbs-lab` on `127.0.0.1:15020`
- S7comm: `llmpot-s7:uhbs-lab` on `127.0.0.1:1102`
- No NVIDIA GPU on the grading host — Modbus uses CPU HF inference; S7 uses Snap7

## Limitations

- HF sample model ≠ full Lightning checkpoints from the paper’s `honeypot/` tree
- S7 grades the **dataset gold PLC** (Snap7), not a live ByT5 S7 emulator
- Module B Modbus write/read round-trip often fails (model hallucinated / empty replies)
- Module C partial without STIX/OTel
- Evaluation proof only — not certification
