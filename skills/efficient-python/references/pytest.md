# Pytest conditions

Read this only when the repository already configures pytest as its test runner. Use the installed pytest version, declared dependencies, and local configuration; do not install pytest or plugins, upgrade the runner, or introduce runner-specific configuration for a change.

- Keep fixtures function-scoped unless sharing is both safe and needed. For every acquired file, connection, task, patched global, or other mutable state, make cleanup deterministic on success and failure. A broader scope must not leak state between tests or outlive the resource it owns.
- Parametrize cases only when each case exercises meaningfully distinct behavior, boundary, or failure contract. Keep a separate test when setup, assertions, or the behavior under test differs enough to hide its purpose in a parameter table.
- Mock at a boundary the code does not own: network, filesystem, clock, process, credentials, or third-party service. Patch the name looked up by the unit under test, and assert the observable request or result where that boundary contract matters. Do not mock internal collaborators merely to mirror implementation steps.
- For async tests, use only the repository's existing async-test support. Keep loop-bound fixtures, clients, and tasks within their owning loop and lifecycle. Await or cancel and collect created tasks before teardown; close async resources on failure and cancellation rather than relying on loop shutdown.
