---
name: termwright
description: "Automate, inspect, or test terminal UI applications with Termwright's CLI, step files, screenshots, or daemon sessions. Use when an agent must observe and interact with a TUI; not for browser automation or Termwright Rust library development."
---

# Termwright TUI Automation

Use Termwright's CLI to launch a TUI in a pseudo-terminal, interact with it, inspect the screen, and capture artifacts. This skill covers CLI workflows, not the Rust API. Upstream at [commit `50fd1703af2b7ebf8904e51f7bcd416785dce050`](https://github.com/fcoury/termwright/tree/50fd1703af2b7ebf8904e51f7bcd416785dce050) documents macOS and Linux support and says Windows is unsupported; screenshot rendering depends on system fonts. Treat all behavior below as version-scoped; inspect the installed CLI's `--help` and `info` output when available.

## Workflow

1. **Set a safe boundary.** Confirm the executable, arguments, working directory, and disposable/local environment. Termwright sends real keystrokes to the launched process. Do not target production, authenticated, or user-data-bearing apps without authorization; stop for approval before external effects such as saving, submitting, deleting, purchasing, or sending. Keep credentials and private data out of step files and artifacts.
2. **Check availability and syntax; do not install or reconfigure Termwright as routine setup.** Use `termwright --help` and `termwright info steps`, `info keys`, `info protocols`, and `info capabilities` as needed. If unavailable or unsuitable, report that instead of installing or substituting another tool. See upstream [`src/main.rs`](https://github.com/fcoury/termwright/blob/50fd1703af2b7ebf8904e51f7bcd416785dce050/src/main.rs).
3. **Prefer `run-steps` for repeatable workflows.** Define explicit readiness, inputs, and assertions that demonstrate the requested state transition—not just that the target text exists. For example, in an app where this screen sequence is verified, assert the destination was absent before navigating:

   ```yaml
   session:
     command: ./build/my-tui
     cwd: .
     cols: 100
     rows: 30
   steps:
     - waitForText: {text: "Main menu", timeoutMs: 5000}
     - notExpectText: {text: "Settings"}
     - press: {key: Down}
     - press: {key: Enter}
     - expectText: {text: "Settings", timeoutMs: 2000}
   artifacts:
     mode: onFailure
     dir: ./termwright-artifacts
   ```

   Before running, follow [step files and artifacts](references/steps-and-artifacts.md) for schema, assertion choices, trace/artifact behavior, and `--connect` semantics. Run `termwright run-steps ./path/to/test.yaml`; add `--trace` only when its potentially sensitive output is approved.
4. **Use one-shot commands for capture-only tasks.** `termwright run --wait-for "Ready" -- ./my-tui` captures screen text; `--format json` selects JSON output. `termwright screenshot --wait-for "Ready" -o ./artifacts/screen.png -- ./my-tui` saves a PNG. These commands kill the launched process after capture in the pinned source. Use a daemon for incremental interaction; see [daemon sessions and capture](references/daemon-and-capture.md).
5. **Verify results and clean up.** Inspect visible state and relevant artifacts; a successful CLI exit or input request alone does not prove the intended state. Protect screen text, JSON, traces, and screenshots as potentially sensitive. Report observed verification, artifact paths (not sensitive contents), cleanup, and unresolved failures.

## Failure handling

- On parse, step, or key errors, consult the installed `info steps`/`info keys`; do not blindly repeat input.
- On timeout, inspect the screen and trace, confirm the app started, and adjust timing only when justified; do not mask missing state with arbitrary delay.
- After assertion failure, re-evaluate observed state before any retry that could duplicate an external effect.
- For daemon connection or cleanup failure, verify the exact socket belongs to the session started for this task; clean up only sessions you own.

## Version caveat

Syntax and edge cases are version-sensitive. The references document source-verified behavior at the pinned upstream commit above, not every release or the installed binary. When the installed CLI differs, prefer its reported interface and verify against that build. Termwright was not installed or run while authoring this skill.
