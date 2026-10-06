"""Provider-neutral WebSocket capability contracts for Orbit."""

from orbit_sockets.contracts import (
    MAX_CLOSE_REASON_BYTES,
    MAX_MESSAGE_BYTES,
    MessageData,
    SocketClose,
    SocketHandler,
    SocketMessage,
    SocketSession,
)
from orbit_sockets.errors import (
    SocketClosedError,
    SocketError,
    SocketMessageTooLargeError,
    SocketProtocolError,
)
from orbit_sockets.server import WebSocketServer, WebSocketServerSettings, WebSocketSession

__all__ = [
    "MAX_CLOSE_REASON_BYTES",
    "MAX_MESSAGE_BYTES",
    "MessageData",
    "SocketClose",
    "SocketClosedError",
    "SocketError",
    "SocketHandler",
    "SocketMessage",
    "SocketMessageTooLargeError",
    "SocketProtocolError",
    "SocketSession",
    "WebSocketServer",
    "WebSocketServerSettings",
    "WebSocketSession",
]
