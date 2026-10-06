"""Provider-neutral WebSocket values and async session contract."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Protocol, TypeAlias

from orbit_sockets.errors import SocketMessageTooLargeError, SocketProtocolError

MAX_MESSAGE_BYTES = 1_048_576
MAX_CLOSE_REASON_BYTES = 123
MessageData: TypeAlias = str | bytes


@dataclass(frozen=True, slots=True)
class SocketMessage:
    """One bounded text or binary WebSocket message."""

    data: MessageData = field(repr=False)

    def __post_init__(self) -> None:
        if isinstance(self.data, str):
            try:
                size = len(self.data.encode("utf-8", errors="strict"))
            except UnicodeEncodeError:
                raise SocketProtocolError("Text messages must contain valid Unicode.") from None
        elif isinstance(self.data, bytes):
            size = len(self.data)
        else:
            raise TypeError("Socket message data must be str or bytes.")
        if size > MAX_MESSAGE_BYTES:
            raise SocketMessageTooLargeError("Socket message exceeds the 1 MiB limit.")

    def __repr__(self) -> str:
        size = len(self.data.encode("utf-8") if isinstance(self.data, str) else self.data)
        kind = "text" if isinstance(self.data, str) else "binary"
        return f"SocketMessage(kind={kind!r}, size={size})"


@dataclass(frozen=True, slots=True)
class SocketClose:
    """Validated WebSocket close details suitable for a provider adapter."""

    code: int = 1000
    reason: str = ""

    def __post_init__(self) -> None:
        if (
            isinstance(self.code, bool)
            or not isinstance(self.code, int)
            or not 1000 <= self.code <= 4999
        ):
            raise SocketProtocolError("Close code must be an integer from 1000 through 4999.")
        if self.code in {1004, 1005, 1006, 1015} or 1016 <= self.code <= 2999:
            raise SocketProtocolError("Close code is reserved by the WebSocket protocol.")
        if not isinstance(self.reason, str):
            raise TypeError("Close reason must be text.")
        try:
            size = len(self.reason.encode("utf-8", errors="strict"))
        except UnicodeEncodeError:
            raise SocketProtocolError("Close reason must contain valid Unicode.") from None
        if size > MAX_CLOSE_REASON_BYTES:
            raise SocketProtocolError("Close reason exceeds the 123-byte protocol limit.")

    def __repr__(self) -> str:
        size = len(self.reason.encode("utf-8"))
        return f"SocketClose(code={self.code}, reason=<redacted:{size} bytes>)"


class SocketSession(Protocol):
    """One bidirectional WebSocket session with explicit message-level backpressure.

    Implementations must keep at most their documented bounded receive queue, propagate task
    cancellation, and make ``close`` idempotent. A successful ``send`` means the adapter accepted
    the message under its transport's flow-control rules; it is not an application-level ACK.
    """

    async def receive(self) -> SocketMessage:
        """Wait for the next complete text or binary message, or raise on peer closure."""
        ...

    async def send(self, message: SocketMessage) -> None:
        """Send one bounded message, applying transport backpressure to the caller."""
        ...

    async def close(self, close: SocketClose | None = None) -> None:
        """Begin the WebSocket close handshake and release session resources."""
        ...


SocketHandler: TypeAlias = Callable[[SocketSession], Awaitable[None]]
