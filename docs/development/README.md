# Development

Install development dependencies with `python -m pip install -e '.[dev]'`. Run `pytest`,
`ruff check .`, `ruff format --check .`, `mypy`, and `python -m build` before a change is proposed.

Contract changes must update the bounded Python values, language-neutral schema when present,
implementation conformance suites, compatibility documentation, and release notes together. Tests
should cover size boundaries, Unicode validation, cancellation, transport flow control, close
handshake, overload, peer disconnect, and secret-safe failures using deterministic local transports.
