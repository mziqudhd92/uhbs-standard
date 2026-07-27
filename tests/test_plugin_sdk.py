"""Unit tests for uhbs_core.plugin_sdk (third-party plugin-author helpers)."""

from __future__ import annotations

from conftest_uhbs_sdk import uhbs_target_mock, uhbs_tps_mock  # noqa: F401

from uhbs_core.plugin_sdk import (
    PktLineBuilder,
    sample_udp_latencies,
    tcp_transact,
    udp_transact,
)

# ---------------------------------------------------------------------------
# tcp_transact / udp_transact / sample_udp_latencies — thin wrapper behavior
# ---------------------------------------------------------------------------


def test_tcp_transact_unreachable_port_returns_error_not_raise() -> None:
    data, rtt_ms, err = tcp_transact("127.0.0.1", 1, b"", timeout=0.5)
    assert data == b""
    assert err  # some OSError message
    assert rtt_ms >= 0.0


def test_udp_transact_send_only_shape() -> None:
    data, rtt_ms, err = udp_transact("127.0.0.1", 9, b"\x00", timeout=0.2)
    # A UDP send to a closed/unlikely-listening port either times out with
    # an empty reply (no err) or errors — either way this must not raise.
    assert isinstance(data, bytes)
    assert isinstance(rtt_ms, float)
    assert isinstance(err, str)


def test_sample_udp_latencies_returns_expected_shape() -> None:
    lat, errors = sample_udp_latencies("127.0.0.1", 9, samples=3, timeout=0.2)
    assert isinstance(lat, list)
    assert isinstance(errors, int)
    assert errors >= 0


# ---------------------------------------------------------------------------
# PktLineBuilder
# ---------------------------------------------------------------------------


def test_pkt_line_encode_matches_git_hand_rolled_format() -> None:
    body = b"git-upload-pack /uhbs.git\0host=uhbs\0"
    encoded = PktLineBuilder.encode(body)
    # Length prefix counts itself (4 hex digits) + body length.
    assert encoded[:4] == f"{len(body) + 4:04x}".encode("ascii")
    assert encoded[4:] == body


def test_pkt_line_flush_is_bare_zero() -> None:
    assert PktLineBuilder.flush() == b"0000"


def test_pkt_line_decode_length_round_trips() -> None:
    body = b"abc"
    encoded = PktLineBuilder.encode(body)
    assert PktLineBuilder.decode_length(encoded) == len(body) + 4


def test_pkt_line_decode_length_handles_garbage_without_raising() -> None:
    assert PktLineBuilder.decode_length(b"") is None
    assert PktLineBuilder.decode_length(b"zzzz") is None
    assert PktLineBuilder.decode_length(b"zz") is None


# ---------------------------------------------------------------------------
# uhbs_target_mock / uhbs_tps_mock fixtures (tests/conftest_uhbs_sdk.py)
# ---------------------------------------------------------------------------


def test_uhbs_target_mock_default_is_unreachable_and_generic(uhbs_target_mock) -> None:  # noqa: F811
    target = uhbs_target_mock()
    assert target.host == "127.0.0.1"
    assert target.port == 1
    assert target.protocol == "generic"
    assert target.protocols == ["generic"]


def test_uhbs_target_mock_accepts_overrides(uhbs_target_mock) -> None:  # noqa: F811
    target = uhbs_target_mock(protocol="coap", port=5683, name="my-coap-target")
    assert target.protocol == "coap"
    assert target.port == 5683
    assert target.name == "my-coap-target"
    assert target.protocols == ["coap"]


def test_uhbs_tps_mock_defaults_to_class_only_no_gold_baseline(uhbs_tps_mock) -> None:  # noqa: F811
    tps = uhbs_tps_mock()
    assert tps.profile_class == "POSIX-Shell"
    assert tps.gold_baseline_host is None
