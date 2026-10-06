# Roadmap

## Implemented

- Provider-neutral bounded WebSocket message, close, and async session contracts.

## Implemented

- Python standalone listener using the `websockets` asyncio server.

## In progress

- Separate Go implementation using `coder/websocket`.
- Separate Rust implementation using Tokio and `tokio-tungstenite`.

## Planned separately

- WebTransport capability and server adapter in a separate package after the selected protocol
  implementation has a clear maturity and interoperability gate.
- Shared conformance fixtures and representative load testing.
