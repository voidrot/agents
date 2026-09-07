# Native C/C++, engines, and consoles

An exception/error event is one captured occurrence. Sentry Logs and breadcrumbs are separate signals and are not substitutes; an Issue is server-side grouping of events, and Issue triage is outside this skill.

Select the exact target; no API or capture parity is assumed.

| Target | Official source | Confirmed status |
|---|---|---|
| Sentry Native C/C++ | [Capturing Errors](https://docs.sentry.io/platforms/native/usage/) and [platform guide](https://docs.sentry.io/platforms/native/) | Manual behavior is confirmed only as shown on the usage page. Automatic crash ownership is **unconfirmed** until the selected backend/OS docs establish it. |
| Godot | [Capturing Errors](https://docs.sentry.io/platforms/godot/usage/) and [platform guide](https://docs.sentry.io/platforms/godot/) | Manual behavior is confirmed only as shown on the usage page. Automatic GDScript/C#/native behavior is **unconfirmed** until the exact export docs establish it. |
| Unreal Engine | [Capturing Errors](https://docs.sentry.io/platforms/unreal/usage/) and [platform guide](https://docs.sentry.io/platforms/unreal/) | Manual behavior is confirmed only as shown on the usage page. Automatic plugin/engine crash behavior is **unconfirmed** until the exact target docs establish it. |
| Nintendo Switch | [platform page](https://docs.sentry.io/platforms/nintendo-switch/) | No verified general `/usage/` capture guide was established during authoring; both general manual and automatic behavior are **unconfirmed**. Do not invent Native/Unreal parity. |
| PlayStation | [platform page](https://docs.sentry.io/platforms/playstation/) | No verified general `/usage/` capture guide was established during authoring; both general manual and automatic behavior are **unconfirmed**. Do not invent parity. |
| Xbox | [platform page](https://docs.sentry.io/platforms/xbox/) | No verified general `/usage/` capture guide was established during authoring; both general manual and automatic behavior are **unconfirmed**. Do not invent parity. |

## Layer and owner decisions

Map language exceptions, signals/SEH/Mach exceptions, engine-level error callbacks, managed scripting layers, platform crash reporters, and watchdog/OOM/forced termination separately. Use only a currently documented crash backend/integration for that OS, architecture, engine, and distribution target. Preserve existing signal/exception handlers and engine/platform crash flow. Do not catch, continue after, or re-raise undefined/fatal native faults merely for telemetry.

Manual handled-error capture is appropriate only when the exact SDK documents it and the application intentionally consumes an actionable error. Messages, engine logs, breadcrumbs, and console output are not exception/crash events. Do not report the same fault through engine callback, native backend, platform crash reporter, and manual call.

Keep event context fixed-size and allowlisted: subsystem, operation class, build configuration, bounded outcome. Never copy memory, minidumps, register dumps, command lines, file contents, player data, network payloads, credentials, or raw crash reports into snippets/evidence. Attachments and crash dumps may contain secrets and PII and require separate policy review.

## Lifecycle, frames, and validation

Crash handlers operate under severe allocation, lock, signal-safety, and time constraints. Use only official SDK handler/lifecycle APIs; never perform custom network I/O or arbitrary logging in a fatal handler. Crash persistence and next-launch upload are target-specific and never guaranteed.

Readable native/engine stacks require matching executable identity and debug symbols; managed scripting layers may also need mappings/source maps. These are prerequisites only—generation/upload/admin is outside scope.

Prefer one authorized handled synthetic error on the actual target build. A hard crash requires separate authorization, a disposable test environment/device, and the platform's official test procedure. Confirm one event, correct mechanism/layer, preserved crash/engine behavior, no cross-layer duplicate, safe context, and readable frames. For restricted console docs/features not publicly established, report them **unconfirmed** and stop at the platform page.
