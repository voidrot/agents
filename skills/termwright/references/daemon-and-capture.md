# Daemon sessions and capture

This reference covers CLI daemon sessions and `exec`; it does not document the Rust API. Source claims are verified at upstream commit [`50fd1703af2b7ebf8904e51f7bcd416785dce050`](https://github.com/fcoury/termwright/tree/50fd1703af2b7ebf8904e51f7bcd416785dce050). Confirm methods, parameters, and output using the installed `termwright info protocols` and `--help`.

## Start, readiness, interact, observe, close

Start only a session you own. Prefer a fresh socket path inside a private directory; do not reuse an existing socket path. At this revision, daemon startup removes an existing path before binding, so reusing a path could remove the existing file. The Unix socket has no authentication in the protocol and this code shows no explicit permission hardening; keep its directory private, do not share it, and do not expose sensitive apps through a daemon. Do not connect to an unrelated socket. Execute the following commands **one at a time**, checking each JSON response before sending the next request; the block is a sequence, not a script to run blindly.

```bash
SOCK=/private/task-dir/termwright.sock
termwright daemon --socket "$SOCK" --background -- ./build/my-tui
termwright exec --socket "$SOCK" --method handshake
termwright exec --socket "$SOCK" --method wait_for_text --params '{"text":"Main menu","timeout_ms":5000}'
termwright exec --socket "$SOCK" --method screen --params '{"format":"text"}'
termwright exec --socket "$SOCK" --method press --params '{"key":"Down"}'
termwright exec --socket "$SOCK" --method press --params '{"key":"Enter"}'
termwright exec --socket "$SOCK" --method screen --params '{"format":"text"}'
termwright exec --socket "$SOCK" --method close
```

Use a new, private path in place of the illustrative `SOCK`; ensure its parent directory exists. Check each response's JSON, not only the CLI exit status: in the pinned implementation `exec` prints the protocol response and can exit 0 even when it contains an `error`. Treat any `error` as failure except the expected close response with `error.code` equal to `closing`. Verify the post-input screen against the requested outcome. `close` kills the daemon's child process; call it only for a daemon you own and expect that closing response. Source: [`src/main.rs`](https://github.com/fcoury/termwright/blob/50fd1703af2b7ebf8904e51f7bcd416785dce050/src/main.rs) and [`src/daemon/server.rs`](https://github.com/fcoury/termwright/blob/50fd1703af2b7ebf8904e51f7bcd416785dce050/src/daemon/server.rs).

`termwright daemon --background -- COMMAND [ARGS...]` prints the socket path; if using its generated path, capture and reuse that exact path. Use `handshake` to confirm a protocol response, then a relevant `wait_for_text`/screen observation to establish app readiness. For errors or interrupted workflows, clean up only a session you started and verify closure; if uncertain, report it rather than closing an unknown daemon.

## Request parameters and screenshot

`--params` takes JSON; supply parameters matching the method's schema. Examples:

```bash
termwright exec --socket "$SOCK" --method type --params '{"text":"hello"}'
termwright exec --socket "$SOCK" --method wait_for_text --params '{"text":"Ready","timeout_ms":5000}'
termwright exec --socket "$SOCK" --method screen --params '{"format":"json"}'
termwright exec --socket "$SOCK" --method screenshot --params '{}'
```

At the pinned revision `screenshot` requires the object fields to deserialize, so pass `--params '{}'` rather than omitting `--params`. Its response's `result.png_base64` is base64-encoded PNG data; decode it only into an approved artifact path and do not print the image payload. Check the response has no `error` before using `result`. Protocol structs and server behavior: [`src/daemon/protocol.rs`](https://github.com/fcoury/termwright/blob/50fd1703af2b7ebf8904e51f7bcd416785dce050/src/daemon/protocol.rs), [`src/daemon/server.rs`](https://github.com/fcoury/termwright/blob/50fd1703af2b7ebf8904e51f7bcd416785dce050/src/daemon/server.rs).

## Optional operations and one-shot capture

The protocol includes `mouse_move`, `mouse_click`, and `resize`; inspect `info protocols` for exact parameters before use. `run` supports `text`, `json`, and `json-compact` output; `screenshot` writes PNG to `--output` or stdout. One-shot commands start and then kill their launched process after capture. Use their documented `--wait-for`, `--delay`, dimensions, and timeout options as appropriate; prefer a readiness condition to an arbitrary delay.

**Version-scoped quirks at the pinned revision:** daemon `screen` with `{"format":"json-compact"}` returns compact JSON as a string inside protocol `result`, rather than a JSON object. Parse the outer response first, then parse that string if needed; don't generalize this quirk to other versions/formats. The daemon's `hotkey` handler checks `ctrl` before `alt`, so setting both sends Ctrl only. The daemon key parser rejects `Insert` as an invalid multi-character key; it also lowercases before function-key parsing, so literal `f` and `F` are parsed as malformed function-key names. Treat these as this revision's implementation mismatches, not general Termwright guarantees; use `info keys` but verify any edge-case key against the installed build. Sources: [`src/daemon/server.rs`](https://github.com/fcoury/termwright/blob/50fd1703af2b7ebf8904e51f7bcd416785dce050/src/daemon/server.rs), [`src/daemon/protocol.rs`](https://github.com/fcoury/termwright/blob/50fd1703af2b7ebf8904e51f7bcd416785dce050/src/daemon/protocol.rs), and [`src/input/keys.rs`](https://github.com/fcoury/termwright/blob/50fd1703af2b7ebf8904e51f7bcd416785dce050/src/input/keys.rs).
