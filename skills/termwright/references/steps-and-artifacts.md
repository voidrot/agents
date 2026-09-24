# Step files and artifacts

This reference covers `termwright run-steps` step files and output behavior verified at upstream commit [`50fd1703af2b7ebf8904e51f7bcd416785dce050`](https://github.com/fcoury/termwright/tree/50fd1703af2b7ebf8904e51f7bcd416785dce050). Check the installed `termwright info steps` and `--help` before relying on version-specific details.

## File and session

A step file is YAML or JSON with a `steps` list, optional `session`, and optional `artifacts` configuration. When starting a new process, `session` is required. `session.command` is required and may be a string with `args`, or an array whose first item is the executable and the rest are arguments (`args` is ignored in the array form). Optional fields include `cwd`, `env`, `cols`, `rows`, `noDefaultEnv`, and `noOscEmulation`; dimensions default to 80 columns by 24 rows in the pinned source. Commands are launched directly; avoid shell wrappers unless the task needs them.

When using `termwright run-steps --connect SOCKET FILE`, the existing daemon is used instead of starting a session. `session` is not needed for that path, and the connected daemon is not closed by the runner. Do not assume `session` environment or working-directory settings will apply to an already-running daemon. Source: [`src/steps.rs`](https://github.com/fcoury/termwright/blob/50fd1703af2b7ebf8904e51f7bcd416785dce050/src/steps.rs), [`src/runner.rs`](https://github.com/fcoury/termwright/blob/50fd1703af2b7ebf8904e51f7bcd416785dce050/src/runner.rs), and [`src/main.rs`](https://github.com/fcoury/termwright/blob/50fd1703af2b7ebf8904e51f7bcd416785dce050/src/main.rs).

## Steps and assertions

The pinned implementation supports `waitForText`, `waitForPattern`, `waitForIdle`, `waitForTextGone`, `waitForPatternGone`, `press`, `type`, `hotkey`, `expectText`, `expectPattern`, `notExpectText`, `notExpectPattern`, and `screenshot`. Check `termwright info steps` for installed-build detail. Readiness waits establish expected startup/async state; after consequential input, assert the resulting state. `expectText`/`expectPattern` wait for text/pattern to appear (optional `timeoutMs`); `notExpectText`/`notExpectPattern` assert non-presence in the current screen and are not a wait-for-disappearance operation. Use `waitForTextGone`/`waitForPatternGone` when disappearance is the condition.

Example: establish a known source state, then check a destination absent before navigation and present afterward. Tailor the text to screens the target app actually shows:

```yaml
steps:
  - waitForText: {text: "Main menu", timeoutMs: 5000}
  - notExpectText: {text: "Settings"}
  - press: {key: Down}
  - press: {key: Enter}
  - expectText: {text: "Settings", timeoutMs: 2000}
```

The precondition avoids passing merely because `Settings` was already visible. Stronger app-specific destination text is preferable if the label can remain on screen after navigation.

## Artifacts and trace

`artifacts.mode` accepts `onFailure` (default), `always`, or `off`; `artifacts.dir` selects the base directory (default `termwright-artifacts`). A timestamped run directory is created when artifacts are enabled or `--trace` is passed. `always` captures screen text and JSON after each successful step. `onFailure` captures screen text and JSON after a step fails. A `screenshot` step saves a PNG when a run directory exists, including on successful runs with `mode: onFailure`; it fails if no artifacts directory exists. `--trace` writes `trace.json` with step labels, elapsed time, before/after screen-text hashes, and error text (if any) after processing. At this pinned revision, `mode: off` combined with `--trace` still creates the run directory and writes the trace; a screenshot step can therefore also save a screenshot. **Artifact mode is not a privacy boundary:** `off` does not suppress trace output when `--trace` is used, and screenshots explicitly requested by a screenshot step are saved on success even with `onFailure`.

Screenshot names are joined to the run directory without path sanitization in this revision. Use only a simple basename (for example `final-screen`), never separators, `..`, absolute paths, or other path segments. Artifacts may contain sensitive app content; choose an approved task-local directory and inspect before sharing.

Sources: [`src/steps.rs`](https://github.com/fcoury/termwright/blob/50fd1703af2b7ebf8904e51f7bcd416785dce050/src/steps.rs) and [`src/runner.rs`](https://github.com/fcoury/termwright/blob/50fd1703af2b7ebf8904e51f7bcd416785dce050/src/runner.rs).
