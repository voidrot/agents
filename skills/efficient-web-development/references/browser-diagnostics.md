# Browser Diagnostics

Read this only when live browser tooling is available and the changed journey needs integration evidence or failure diagnosis.

1. Reproduce the exact journey and record the browser/version, viewport, relevant network condition, and user steps. Collect only artifacts permitted by the environment; redact credentials, tokens, and sensitive data.
2. Inspect console messages and network requests/responses for the affected action. Record observable accessibility semantics and focus behavior, rendered narrow/zoomed state when relevant, and a performance trace or timing only when performance is in scope.
3. Correlate timestamps and the visible outcome with server-safe logs or test artifacts. Treat a tool's output as an observation, not proof of cause: form a falsifiable hypothesis and confirm it by an independent boundary, controlled reproduction, or targeted change.
4. Classify the evidence before editing: browser/runtime, client integration, server contract or authorization, test harness, or unavailable infrastructure. Remove temporary instrumentation after diagnosis.

Use any available browser inspector or the repository's existing test tooling; do not add dependencies or require tool-specific commands.
