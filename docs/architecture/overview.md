# Architecture

`orbit-sockets` owns message bounds, close metadata, normalized capability errors, and the async
session protocol. It deliberately does not own a listener, router, ASGI server, credentials, or
provider SDK. Each implementation owns its transport, TLS configuration, listener lifecycle,
authentication integration, and provider-specific failure mapping.

`orbit-realtime` independently owns Server-Sent Events. WebTransport is a separate capability due to
its HTTP/3/QUIC session, multiplexed reliable streams, and unreliable datagrams. The WebTransport
server maturity and supported protocol revision must be documented by its own package; a shared
WebSocket session protocol is not a substitute.

The Python, Go, and Rust implementations are standalone listeners deployed behind ingress. They do
not use Core's local process-plugin gRPC boundary: that host is for trusted local plugin lifecycle
and typed capability calls, not general microservice communication. Application and deployment
configuration select one implementation explicitly.

The Python listener owns its sockets and accepted connection lifecycle. Applications own identity,
authorization, upstream resources, fanout, replay, and scaling across service instances. Its session
contract has one reader per connection and applies transport backpressure when `send` is awaited.
