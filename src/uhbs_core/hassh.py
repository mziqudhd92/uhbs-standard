"""Minimal SSH server HASSH-like fingerprint from KEXINIT (RFC 4253)."""

from __future__ import annotations

import hashlib
import socket
import struct


def _read_name_list(buf: bytes, off: int) -> tuple[str, int]:
    if off + 4 > len(buf):
        return "", off
    (n,) = struct.unpack(">I", buf[off : off + 4])
    off += 4
    if off + n > len(buf):
        return "", off
    raw = buf[off : off + n].decode("ascii", errors="replace")
    return raw, off + n


def parse_server_hassh(host: str, port: int, timeout: float = 5.0) -> tuple[str, str, str]:
    """Return (hassh_md5, kex_algos, banner). Empty hassh on failure."""
    try:
        with socket.create_connection((host, port), timeout=timeout) as s:
            s.settimeout(timeout)
            banner = b""
            while b"\n" not in banner and len(banner) < 256:
                chunk = s.recv(64)
                if not chunk:
                    break
                banner += chunk
            # Client identification
            s.sendall(b"SSH-2.0-UHBS_HASSH_1.0\r\n")
            data = b""
            # Read until we likely have a full KEXINIT
            while len(data) < 1500:
                try:
                    chunk = s.recv(4096)
                except TimeoutError:
                    break
                if not chunk:
                    break
                data += chunk
                if len(data) > 64 and data[5:6] == b"\x14":
                    # may still need rest of packet
                    if len(data) >= 8:
                        plen = struct.unpack(">I", data[0:4])[0]
                        if len(data) >= 4 + plen:
                            break
    except OSError:
        return "", "", ""

    ban = banner.split(b"\n", 1)[0].decode("utf-8", "replace").strip()
    # Find SSH_MSG_KEXINIT (20) — may follow banner CR LF
    payload = data
    if b"\r\n" in data[:128]:
        payload = data.split(b"\r\n", 1)[1]
    # Walk binary packets for msg type 20
    off = 0
    body = b""
    while off + 6 <= len(payload):
        plen = struct.unpack(">I", payload[off : off + 4])[0]
        if plen < 2 or off + 4 + plen > len(payload) + 1024:
            # heuristic scan
            idx = payload.find(b"\x14", off)
            if idx < 0 or idx + 17 > len(payload):
                break
            body = payload[idx + 1 :]  # after msg type? actually msg at pad+1
            # Better: standard layout packet_len|pad_len|msg|...
            break
        pad = payload[off + 4]
        msg = payload[off + 5]
        if msg == 20:
            body = payload[off + 6 : off + 4 + plen]  # after msg type byte... wait
            # Structure: [4 plen][1 pad][1 msg=20][16 cookie][name-lists...]
            body = payload[off + 6 : off + 4 + plen]
            break
        off += 4 + plen

    if not body:
        # Fallback search for cookie+namelist pattern after 0x14
        idx = payload.find(b"\x14")
        if idx >= 0 and idx + 17 < len(payload):
            body = payload[idx + 1 :]
        else:
            return "", "", ban

    # body starts at cookie (16) if we stripped msg byte; if body includes cookie after msg
    # Our body = after msg type → cookie at [0:16]
    if len(body) < 20:
        return "", "", ban
    o = 16  # skip cookie
    kex, o = _read_name_list(body, o)
    _hostkey, o = _read_name_list(body, o)
    enc_c2s, o = _read_name_list(body, o)
    _enc_s2c, o = _read_name_list(body, o)
    mac_c2s, o = _read_name_list(body, o)
    _mac_s2c, o = _read_name_list(body, o)
    comp_c2s, o = _read_name_list(body, o)
    if not kex:
        return "", "", ban
    # Server HASSH set: kex;enc_c2s;mac_c2s;comp_c2s (common convention)
    algo = f"{kex};{enc_c2s};{mac_c2s};{comp_c2s}"
    hassh = hashlib.md5(algo.encode("utf-8")).hexdigest()
    return hassh, algo, ban
