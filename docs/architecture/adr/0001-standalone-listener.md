# 0001: Keep WebSocket listeners independent of the Core process host

- Status: accepted
- Date: 2026-10-06

## Context

Core's gRPC process host supervises local plugins. It is not the application's distributed RPC
system, and it has no browser-connection stream contract. Forwarding every WebSocket frame through
that boundary would add a hop and couple listener availability to the plugin host.

## Decision

The Python, Go, and Rust implementations are standalone WebSocket services behind an ingress that
supports WebSocket upgrades. Each listener enforces bounded messages and connections, validates its
configured route and browser origins, propagates cancellation, and shuts down within a deadline.
The Core application selects and deploys one implementation explicitly. This package does not
provide identity, durable delivery, fanout, or service discovery.

## Consequences

Deployments own service addressing, ingress behavior, TLS termination, and horizontal routing. The
three implementations need a shared protocol-conformance suite before they can be described as
interchangeable. Core's local process-plugin contract remains independent.
