"""Stable, provider-neutral socket capability errors."""

from __future__ import annotations


class SocketError(Exception):
    """Base for sanitized socket capability failures."""

    code = "socket.error"


class SocketClosedError(SocketError):
    """The session is already closed or is closing."""

    code = "socket.closed"


class SocketMessageTooLargeError(SocketError, ValueError):
    """A text or binary message exceeded the capability's size limit."""

    code = "socket.message_too_large"


class SocketProtocolError(SocketError, ValueError):
    """A message or close frame violated the capability contract."""

    code = "socket.protocol"
