import pytest

from orbit_sockets import (
    MAX_MESSAGE_BYTES,
    SocketClose,
    SocketMessage,
    SocketMessageTooLargeError,
    SocketProtocolError,
)


def test_text_and_binary_messages_accept_exact_limit() -> None:
    assert len(SocketMessage("a" * MAX_MESSAGE_BYTES).data) == MAX_MESSAGE_BYTES
    assert len(SocketMessage(b"a" * MAX_MESSAGE_BYTES).data) == MAX_MESSAGE_BYTES


@pytest.mark.parametrize("data", ["a" * (MAX_MESSAGE_BYTES + 1), b"a" * (MAX_MESSAGE_BYTES + 1)])
def test_messages_reject_payload_over_limit(data: str | bytes) -> None:
    with pytest.raises(SocketMessageTooLargeError):
        SocketMessage(data)


def test_text_rejects_invalid_unicode_without_leaking_payload() -> None:
    with pytest.raises(SocketProtocolError, match="valid Unicode"):
        SocketMessage("\ud800")


@pytest.mark.parametrize("code", [True, 999, 1004, 1005, 1006, 1015, 1016, 2999, 5000, "1000"])
def test_close_code_is_validated(code: object) -> None:
    with pytest.raises(SocketProtocolError):
        SocketClose(code=code)  # type: ignore[arg-type]


def test_close_reason_uses_utf8_byte_limit() -> None:
    assert SocketClose(reason="é" * 61)
    with pytest.raises(SocketProtocolError, match="123-byte"):
        SocketClose(reason="é" * 62)


def test_sensitive_values_are_redacted_from_representations() -> None:
    message = SocketMessage("bearer-secret")
    close = SocketClose(reason="sensitive detail")
    assert "bearer-secret" not in repr(message)
    assert "sensitive detail" not in repr(close)
