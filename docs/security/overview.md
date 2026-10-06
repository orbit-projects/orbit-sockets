# Security

WebSocket and WebTransport sessions are long-lived, resource-consuming connections. Implementations
and applications should apply explicit origin policy, authentication, per-message authorization,
connection quotas, message and queue bounds, handshake timeouts, and graceful shutdown. Origin
validation does not replace authentication or CSRF defenses. Enforce TLS at the transport or a
trusted ingress and correctly configure forwarded client identity.

Do not log message bodies, authorization headers, URL query strings containing secrets, session
tokens, or raw provider exceptions. Keep authentication and authorization in `orbit-auth`; this
package defines transport-level values only.
