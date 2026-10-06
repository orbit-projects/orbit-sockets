# Operations

Use a TLS-terminating ingress with explicit WebSocket upgrade support, request and connection
timeouts appropriate for long-lived sessions, and a bounded per-instance connection budget. Set
limits for message size, receive queues, write buffers, connection admission, and shutdown drain
time. Deployments must verify that proxies preserve upgrade headers and honor idle-timeout settings.
The Python server defaults to loopback binding, accepts clients without an `Origin` header, and
rejects browser clients until explicit HTTP(S) origins are configured. Its default message limit is
256 KiB.

Authorize every connection and resource subscription. Validate browser origins against an explicit
allowlist; origin checks are not authentication. Do not put bearer credentials in URLs. Avoid
unbounded per-client fanout, retained session state, and unbounded broadcast queues. Drain sessions
on shutdown and let clients reconnect with application-defined backoff. The Python server waits for
handlers up to its configured shutdown timeout, then cancels remaining handler tasks.

These are deployment requirements, not a claim that this contract package provides a server or
operational control plane.
