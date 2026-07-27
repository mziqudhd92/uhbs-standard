"""Tests for uhbs_core.fingerprint (TCP-stack + TLS auditing, new module).

Offline-safe unit tests exercise the pure-Python decode/anomaly logic.
One live test spins up a real local TCP listener (loopback only, no
external network dependency) and is skipped if loopback binding is
unavailable in the sandbox.
"""

from __future__ import annotations

import socket
import ssl
import sys
import threading

import pytest

from uhbs_core.fingerprint import (
    TCPStackSignature,
    _decode_linux_tcp_info,
    _match_known_profile,
    fingerprint_host,
    probe_tcp_stack,
    probe_tls,
)


def _loopback_available() -> bool:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("127.0.0.1", 0))
        s.close()
        return True
    except OSError:
        return False


_LOOPBACK_OK = _loopback_available()


# --- offline / pure-logic tests ---------------------------------------------


def test_tcp_stack_signature_reports_unreachable_when_no_connects_succeed() -> None:
    sig = probe_tcp_stack("127.0.0.1", 1, samples=2, timeout=0.2)
    assert isinstance(sig, TCPStackSignature)
    assert sig.reachable is False
    assert sig.connect_errors >= 1


def test_decode_linux_tcp_info_rejects_garbage_bytes() -> None:
    # Random bytes will almost never decode to a plausible tcp_info state.
    assert _decode_linux_tcp_info(b"\x00" * 4) is None  # too short
    assert _decode_linux_tcp_info(bytes([255] * 200)) is None  # implausible state


def test_match_known_profile_recognizes_modern_tls13_shape() -> None:
    name = _match_known_profile("TLSv1.3", "TLS_AES_256_GCM_SHA384")
    assert name == "modern_tls13_default"


def test_match_known_profile_returns_none_for_unrecognized_combo() -> None:
    assert _match_known_profile("TLSv1.0", "SOME_MADE_UP_CIPHER") is None


def test_fingerprint_host_unreachable_is_honest_not_faked() -> None:
    result = fingerprint_host("127.0.0.1", 1, use_tls=False, tcp_samples=1, timeout=0.2)
    assert result["passed"] is False
    assert result["score"] == 0.0
    assert "unreachable" in result["detail"]


def test_probe_tls_reports_error_on_non_tls_port_gracefully() -> None:
    # No TLS listener anywhere near this ephemeral high port; must not raise.
    fp = probe_tls("127.0.0.1", 1, timeout=0.2)
    assert fp.ok is False
    assert fp.error


# --- live loopback tests -----------------------------------------------------


@pytest.mark.skipif(not _LOOPBACK_OK, reason="loopback TCP bind unavailable in this sandbox")
def test_probe_tcp_stack_against_real_local_listener() -> None:
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 0))
    srv.listen(5)
    port = srv.getsockname()[1]
    stop = threading.Event()

    def _accept_loop() -> None:
        srv.settimeout(0.2)
        while not stop.is_set():
            try:
                conn, _ = srv.accept()
                conn.close()
            except OSError:
                continue

    t = threading.Thread(target=_accept_loop, daemon=True)
    t.start()
    try:
        sig = probe_tcp_stack("127.0.0.1", port, samples=3, timeout=2.0)
        assert sig.reachable is True
        assert sig.connect_errors == 0
        assert sig.median_connect_ms is not None
        assert sig.median_connect_ms >= 0.0
        assert sig.connect_jitter_ms is not None
        # On non-Linux platforms TCP_INFO must be honestly absent, not faked.
        if not sys.platform.startswith("linux"):
            assert sig.linux_tcp_info is None
            assert "Linux-only" in sig.linux_tcp_info_note

        result = fingerprint_host("127.0.0.1", port, use_tls=False, tcp_samples=2, timeout=2.0)
        assert result["passed"] is True
        assert result["score"] == 100.0
    finally:
        stop.set()
        srv.close()
        t.join(timeout=1.0)


@pytest.mark.skipif(not _LOOPBACK_OK, reason="loopback TCP bind unavailable in this sandbox")
def test_probe_tls_against_real_local_self_signed_listener() -> None:
    pytest.importorskip("cryptography")
    import datetime
    import os
    import tempfile

    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.x509.oid import NameOID

    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name(
        [x509.NameAttribute(NameOID.COMMON_NAME, "localhost")]
    )
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.now(datetime.UTC))
        .not_valid_after(datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1))
        .sign(key, hashes.SHA256())
    )

    with tempfile.TemporaryDirectory() as tmp:
        cert_path = os.path.join(tmp, "cert.pem")
        key_path = os.path.join(tmp, "key.pem")
        with open(cert_path, "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        with open(key_path, "wb") as f:
            f.write(
                key.private_bytes(
                    serialization.Encoding.PEM,
                    serialization.PrivateFormat.TraditionalOpenSSL,
                    serialization.NoEncryption(),
                )
            )

        server_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        server_ctx.load_cert_chain(cert_path, key_path)

        raw_srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        raw_srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        raw_srv.bind(("127.0.0.1", 0))
        raw_srv.listen(5)
        port = raw_srv.getsockname()[1]
        stop = threading.Event()

        def _tls_accept_loop() -> None:
            raw_srv.settimeout(0.3)
            while not stop.is_set():
                try:
                    conn, _ = raw_srv.accept()
                except OSError:
                    continue
                try:
                    tls_conn = server_ctx.wrap_socket(conn, server_side=True)
                    tls_conn.close()
                except (OSError, ssl.SSLError):
                    pass

        t = threading.Thread(target=_tls_accept_loop, daemon=True)
        t.start()
        try:
            fp = probe_tls("127.0.0.1", port, timeout=2.0)
            assert fp.ok is True
            assert fp.tls_version is not None
            assert fp.cipher_name is not None
            # Self-signed with CN=localhost -> both anomaly signals expected.
            assert fp.cert_self_signed is True
            assert any("self-signed" in a for a in fp.anomaly_flags)
        finally:
            stop.set()
            raw_srv.close()
            t.join(timeout=1.0)
